import re
import datetime
from typing import Optional

from croniter import croniter


class BaseExclusion:
    PATTERN = None

    @classmethod
    def is_valid(cls, line: str):
        return cls.PATTERN.match(line) is not None


class CronExclusion:
    @classmethod
    def is_valid(cls, line: str):
        return croniter.is_valid(line)

    def __init__(self, line: str):
        self.line = line

    def matches(self, dt: datetime.datetime):
        base = dt - datetime.timedelta(seconds=1)
        nt = croniter(self.line, base).get_next(datetime.datetime)
        return nt == dt


class DateExclusion(BaseExclusion):
    PATTERN = re.compile(r"""^\d\d\d\d-\d\d-\d\d$""")

    def __init__(self, line: str):
        (
            year,
            month,
            day,
        ) = [int(x, base=10) for x in line.strip().split("-")]
        self.date = datetime.date(year=year, month=month, day=day)

    def matches(self, dt: datetime.datetime):
        return dt.date() == self.date


class DateTimeExclusion(BaseExclusion):
    PATTERN = re.compile(r"""^\d\d\d\d-\d\d-\d\dT\d\d:\d\d:\d\d$""")
    NUMBER = re.compile(r"""\d+""")

    def __init__(self, line: str):
        params = [int(num, base=10) for num in self.NUMBER.findall(line)]
        self.dt = datetime.datetime(*params)

    def matches(self, dt: datetime.datetime):
        return dt == self.dt


def multi_exclusion(
    line: str, exclusions=[DateTimeExclusion, DateExclusion, CronExclusion]
) -> Optional[BaseExclusion]:
    for cls in exclusions:
        if cls.is_valid(line):
            return cls(line)
