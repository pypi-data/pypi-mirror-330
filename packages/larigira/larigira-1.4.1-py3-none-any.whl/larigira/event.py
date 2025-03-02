
import logging
from datetime import datetime, timedelta

import gevent
from gevent import monkey
from gevent.queue import Queue

from .audiogen import audiogenerate
from .db import EventModel
from .eventutils import ParentedLet, Timer
from .timegen import timegenerate

monkey.patch_all(subprocess=True)


logging.getLogger("mpd").setLevel(logging.WARNING)


class Monitor(ParentedLet):
    """
    Manages timegenerators and audiogenerators for DB events
    
    The mechanism is partially based on ticks, partially on scheduled actions.
    Ticks are emitted periodically; at every tick, :func:`on_tick
    <larigira.event.Monitor.on_tick>` checks if any event is "near enough". If
    an event is near enough, it is ":func:`scheduled
    <larigira.event.Monitor.schedule>`": a greenlet is run which will wait for
    the right time, then generate the audio, then submit to Controller.

    The tick mechanism allows for events to be changed on disk: if everything
    was scheduled immediately, no further changes would be possible.
    The scheduling mechanism allows for more precision, catching exactly the
    right time. Being accurate only with ticks would have required very
    frequent ticks, which is cpu-intensive.
    """

    def __init__(self, parent_queue, conf):
        ParentedLet.__init__(self, parent_queue)
        self.log = logging.getLogger(self.__class__.__name__)
        self.running = {}
        self.conf = conf
        self.q = Queue()
        self.model = EventModel(self.conf["DB_URI"], self.conf['DB_ADDITIONAL_DIR'])
        self.ticker = Timer(int(self.conf["EVENT_TICK_SECS"]) * 1000, self.q)

    def _alarm_missing_time(self, timespec):
        now = datetime.now() + timedelta(seconds=self.conf["CACHING_TIME"])
        try:
            when = next(timegenerate(timespec, now=now))
        except:
            logging.exception(
                "Could not generate " "an alarm from timespec %s", timespec
            )
            return None
        if when is None:
            # expired
            return None
        delta = (when - now).total_seconds()
        assert delta > 0
        return delta

    def on_tick(self):
        """
        this is called every EVENT_TICK_SECS.
        Checks every event in the DB (which might be slightly CPU-intensive, so
        it is advisable to run it in its own greenlet); if the event is "near
        enough", schedule it; if it is too far, or already expired, ignore it.
        """
        self.model.reload()
        for alarm in self.model.get_all_alarms():
            actions = list(self.model.get_actions_by_alarm(alarm))
            if alarm.eid in self.running:
                continue
            delta = self._alarm_missing_time(alarm)
            # why this 2*EVENT_TICK_SECS? EVENT_TICK_SECS would be enough,
            # but it is "tricky"; any small delay would cause the event to be
            # missed
            if delta is None:
                # this is way too much logging! we need more levels!
                # self.log.debug(
                #    "Skipping event %s: will never ring", alarm.get("nick", alarm.eid)
                # )
                pass
            elif delta <= 2 * self.conf["EVENT_TICK_SECS"]:
                self.log.debug(
                    "Scheduling event %s (%ds) => %s",
                    alarm.get("nick", alarm.eid),
                    delta,
                    [a.get("nick", a.eid) for a in actions],
                )
                self.schedule(alarm, actions, delta)
            else:
                self.log.debugv(
                    "Skipping event %s too far (%ds)",
                    alarm.get("nick", alarm.eid),
                    delta,
                )

    def schedule(self, timespec, audiospecs, delta=None):
        """
        prepare an event to be run at a specified time with the specified
        actions; the DB won't be read anymore after this call.

        This means that this call should not be done too early, or any update
        to the DB will be ignored.
        """
        if delta is None:
            delta = self._alarm_missing_time(timespec)

        audiogen = gevent.spawn_later(
            delta, self.process_action, timespec, audiospecs
        )
        audiogen.parent_greenlet = self
        audiogen.doc = 'Will wait {} seconds, then generate audio "{}"'.format(
            delta, ",".join(aspec.get("nick", "") for aspec in audiospecs)
        )
        self.running[timespec.eid] = {
            "greenlet": audiogen,
            "running_time": datetime.now() + timedelta(seconds=delta),
            "timespec": timespec,
            "audiospecs": audiospecs,
        }

    def process_action(self, timespec, audiospecs):
        """Generate audio and submit it to Controller"""
        if timespec.eid in self.running:
            del self.running[timespec.eid]
        else:
            self.log.warning(
                "Timespec %s completed but not in running "
                "registry; this is most likely a bug",
                timespec.get("nick", timespec.eid),
            )
        uris = []
        for audiospec in audiospecs:
            try:
                uris.extend(audiogenerate(audiospec))
            except Exception as exc:
                self.log.error(
                    "audiogenerate for <%s> failed; reason: %s",
                    str(audiospec),
                    str(exc),
                )
        self.send_to_parent(
            "uris_enqueue",
            dict(
                uris=uris,
                timespec=timespec,
                audiospecs=audiospecs,
                aids=[a.eid for a in audiospecs],
            ),
        )

    def _run(self):
        self.ticker.start()
        gevent.spawn(self.on_tick)
        while True:
            value = self.q.get()
            kind = value["kind"]
            if kind in ("forcetick", "timer"):
                gevent.spawn(self.on_tick)
            else:
                self.log.warning("Unknown message: %s", str(value))
