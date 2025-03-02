import logging
from datetime import datetime

from croniter import croniter

from .timegen_every import AlarmWithExclusions

log = logging.getLogger("time-cron")



class CronAlarm(AlarmWithExclusions):

    description = "Frequency specified by cron-like format. nerds preferred"

    def __init__(self, obj):
        super().__init__(obj)

        self.cron_format = obj["cron_format"]
        if not croniter.is_valid(self.cron_format):
            raise ValueError("Invalid cron_format: `%s`" % self.cron_format)

    def do_next_rings(self, current_time):
        # cron granularity is to the minute
        # thus, doing 2000 attemps guarantees at least 32hours.
        # if your event is no more frequent than 10minutes, this is 13days
        for _ in range(2000):
            nt = croniter(self.cron_format, current_time).get_next(datetime)
            yield nt
            current_time = nt
