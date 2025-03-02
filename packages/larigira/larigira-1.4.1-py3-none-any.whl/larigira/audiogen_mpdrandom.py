import logging
import random

from mpd import MPDClient

from .config import get_conf

log = logging.getLogger(__name__)


def generate_by_artist(spec):
    """Choose HOWMANY random artists, and for each one choose a random song."""
    spec.setdefault("howmany", 1)
    prefix = spec.get("prefix", "").rstrip("/")
    log.info("generating")
    conf = get_conf()
    c = MPDClient(use_unicode=True)
    c.connect(conf["MPD_HOST"], conf["MPD_PORT"])

    if prefix:
        # TODO: listallinfo is discouraged.
        #       how else could we achieve the same result?
        artists = list(
            {r["artist"] for r in c.listallinfo(prefix) if "artist" in r}
        )
    else:
        artists = c.list("artist")
    if not artists:
        raise ValueError("no artists in your mpd database")
    for _ in range(spec["howmany"]):
        artist = random.choice(artists)  # pick one artist
        if type(artist) is not str:
            # different mpd library versions have different behavior
            artist = artist['artist']
        # pick one song from that artist
        artist_songs = (res["file"] for res in c.find("artist", artist))
        if prefix:
            artist_songs = [
                fname
                for fname in artist_songs
                if fname.startswith(prefix + "/")
            ]
        yield random.choice(list(artist_songs))
