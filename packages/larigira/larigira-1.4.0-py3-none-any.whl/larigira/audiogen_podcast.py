import datetime
import logging
import os
import random
import sys
from subprocess import CalledProcessError, check_output

import dateutil.parser
import requests
from lxml import html
from pytimeparse.timeparse import timeparse

from larigira.fsutils import download_http


def delta_humanreadable(tdelta):
    if tdelta is None:
        return ""
    days = tdelta.days
    hours = (tdelta - datetime.timedelta(days=days)).seconds // 3600
    if days:
        return "{}d{}h".format(days, hours)
    return "{}h".format(hours)


def get_duration(url):
    try:
        lineout = check_output(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-i",
                url,
            ]
        ).split(b"\n")
    except CalledProcessError as exc:
        raise ValueError("error probing `%s`" % url) from exc
    duration = next(l for l in lineout if l.startswith(b"duration="))
    value = duration.split(b"=")[1]
    return int(float(value))


class Audio(object):
    def __init__(self, url, duration=None, date=None):
        self.url = url
        self._duration = duration
        self.date = date
        self.end_date = datetime.datetime(
            9999, 12, 31, tzinfo=datetime.timezone.utc
        )

    def __str__(self):
        return self.url

    def __repr__(self):
        return "<Audio {} ({} {})>".format(
            self.url, self._duration, delta_humanreadable(self.age)
        )

    @property
    def duration(self):
        """lazy-calculation"""
        if self._duration is None:
            try:
                self._duration = get_duration(self.url.encode("utf-8"))
            except:
                logging.exception(
                    "Error while computing duration of %s; set it to 0",
                    self.url,
                )
                self._duration = 0
        return self._duration

    @property
    def urls(self):
        return [self.url]

    @property
    def age(self):
        if self.date is None:
            return None
        now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)

        return now - self.date

    @property
    def valid(self):
        return self.end_date >= datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc
        )


def get_tree(feed_url):
    if feed_url.startswith("http:") or feed_url.startswith("https:"):
        tree = html.fromstring(requests.get(feed_url).content)
    else:
        if not os.path.exists(feed_url):
            raise ValueError("file not found: {}".format(feed_url))
        tree = html.parse(open(feed_url))
    return tree


def get_item_date(el):
    el_date = el.find("pubdate")
    if el_date is None:
        return None
    for time_format in ("%Y-%m-%dT%H:%M:%S%z", "%a, %d %b %Y %H:%M:%S %z"):
        try:
            return datetime.datetime.strptime(el_date.text, time_format)
        except:
            continue
    return dateutil.parser.parse(el_date.text)


def get_audio_from_item(item):
    encl = item.find("enclosure")
    if encl is not None:
        url = encl.get("url")
    else:
        return None
    audio_args = {}
    if item.find("duration") is not None:
        duration_parts = item.findtext("duration").split(":")
        total_seconds = 0
        for i, num in enumerate(reversed(duration_parts)):
            total_seconds += int(float(num)) * (60 ** i)
        if total_seconds:
            audio_args["duration"] = total_seconds
    else:
        contents = item.xpath("group/content")
        if not contents:
            contents = item.xpath("content")
        for child in contents:
            if child.get("url") == url and child.get("duration") is not None:
                audio_args["duration"] = int(float(child.get("duration")))
                break
    return Audio(url, **audio_args)


def get_urls(tree):
    items = tree.xpath("//item")
    for i, it in enumerate(items):
        try:
            audio = get_audio_from_item(it)
        except Exception:
            logging.error("Could not parse item #%d, skipping", i)
            continue
        if audio is None:
            continue
        if audio.date is None:
            try:
                audio.date = get_item_date(it)
            except Exception:
                logging.warn("Could not find date for item #%d", i)
        yield audio

def parse_duration(arg):
    if arg.isdecimal():
        secs = int(arg)
    else:
        secs = timeparse(arg)
        if secs is None:
            raise ValueError("%r is not a valid duration" % arg)
    return secs


def generate(spec):
    if "url" not in spec:
        raise ValueError("Malformed audiospec: missing 'url'")
    audios = list(get_urls(get_tree(spec["url"])))
    if spec.get("min_len", False):
        audios = [
            a for a in audios if a.duration >= parse_duration(spec["min_len"])
        ]
    if spec.get("max_len", False):
        audios = [
            a for a in audios if a.duration <= parse_duration(spec["max_len"])
        ]

    # sort
    sort_by = spec.get("sort_by", "none")
    if sort_by == "random":
        random.shuffle(audios)
    elif sort_by == "date":
        audios.sort(key=lambda x: x.age)
    elif sort_by == "duration":
        audios.sort(key=lambda x: x.duration)

    if spec.get("reverse", False):
        audios.reverse()

    # slice
    audios = audios[int(spec.get("start", 0)) :]
    audios = audios[: int(spec.get("howmany", 1))]

    # copy local
    local_audios = [
        download_http(a.url, copy=spec.get("copy", True), prefix="podcast")
        for a in audios
    ]
    return local_audios


# TODO: testing
# TODO: lxml should maybe be optional?
# TODO: ui


if __name__ == "__main__":
    # less than proper testing
    logging.basicConfig(level=logging.DEBUG)
    for u in get_urls(get_tree(sys.argv[1])):
        print(" -", repr(u))
