import fnmatch
import logging
import mimetypes
import os
import posixpath
import urllib.request
from tempfile import mkstemp
from urllib.parse import urlparse
from pathlib import Path
import hashlib

import requests

log = logging.getLogger(__name__)


def scan_dir(dirname, extension=None):
    if extension is None:
        extension = "*"
    for root, dirnames, filenames in os.walk(dirname):
        for fname in fnmatch.filter(filenames, extension):
            yield os.path.join(root, fname)


def multi_fnmatch(fname, extensions):
    for ext in extensions:
        if fnmatch.fnmatch(fname, "*." + ext):
            return True
    return False


def is_audio(fname):
    mimetype = mimetypes.guess_type(fname)[0]
    if mimetype is None:
        return False
    return mimetype.split("/")[0] == "audio"


def scan_dir_audio(dirname, extensions=("mp3", "oga", "wav", "ogg")):
    for root, dirnames, filenames in os.walk(dirname):
        for fname in filenames:
            if is_audio(fname):
                yield os.path.join(root, fname)


def shortname(path):
    name = os.path.basename(path)  # filename
    name = name.rsplit(".", 1)[0]  # no extension
    name = "".join(c for c in name if c.isalnum())  # no strange chars
    return name


def http_expected_length(url):
    resp = requests.head(url, allow_redirects=True)
    resp.raise_for_status()
    header_value = resp.headers.get('content-length')
    expected_length = int(header_value)
    return expected_length


def download_http(url, destdir=None, copy=False, prefix="httpdl"):
    if url.split(":")[0] not in ("http", "https"):
        log.warning("Not a valid URL: %s", url)
        return None
    ext = url.split(".")[-1].split("?")[0]
    if ext.lower() not in ("mp3", "ogg", "oga", "wma", "m4a"):
        log.warning('Invalid format (%s) for "%s"', ext, url)
        return None
    if not copy:
        return url
    if destdir is None:
        destdir = os.getenv('TMPDIR', '/tmp/')
    fname = posixpath.basename(urlparse(url).path)
    # sanitize
    fname = "".join(
        c for c in fname if c.isalnum() or c in list("_-")
    ).rstrip()
    url_hash = hashlib.sha1(url.encode('utf8')).hexdigest()

    final_path = Path(destdir) / ('%s-%s-%s.%s' % (prefix, fname[:20], url_hash, ext))

    # it might be already fully downloaded, let's check
    if final_path.exists():

        # this "touch" helps avoiding a race condition in which the
        # UnusedCleaner could delete  this
        final_path.touch()

        actual_size = final_path.stat().st_size
        try:
            expected_size = http_expected_length(url)
        except Exception as exc:
            log.debug("Could not determine expected length for %s: %s", url, exc)
        else:
            if expected_size == actual_size:
                log.debug("File %s already present and complete, download not needed", final_path)
                return final_path.as_uri()
            else:
                log.debug("File %s is already present, but has the wrong length: %d but expected %d", final_path, actual_size, expected_size)
    else:
        log.debug("File %s does not exist", final_path)
    tmp = mkstemp(
        suffix="." + ext, prefix="%s-%s-%s-" % (prefix, fname, url_hash), dir=destdir
    )
    os.close(tmp[0])
    log.info("downloading %s -> %s -> %s", url, tmp[1], final_path)
    fname, headers = urllib.request.urlretrieve(url, tmp[1])
    Path(fname).rename(final_path)
    return final_path.as_uri()
# "file://%s" % os.path.realpath(final_path)
