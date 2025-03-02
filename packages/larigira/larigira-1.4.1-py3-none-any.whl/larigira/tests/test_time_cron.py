import datetime

import pytest

from larigira.timegen_cron import CronAlarm


@pytest.fixture
def a_time():
    # 6th of august 2019 at 10:42
    return datetime.datetime(2019, 8, 6, 10, 42, 0)


@pytest.fixture(params=("* * * * *", "* * * * * *"))
def valid_cron(request):
    return request.param


def CA(fmt, exclude=""):
    return CronAlarm(dict(cron_format=fmt, exclude=exclude))


def test_valid_cron_format():
    CA("* * * * *")


def test_valid_cron_format_six():
    CA("* * * * * *")


def test_valid_cron_format_spaces_left(valid_cron):
    """if a  format is valid, a format with left spaces is also valid"""
    CA(" " + valid_cron)


def test_valid_cron_format_spaces_right(valid_cron):
    """if a  format is valid, a format with right spaces is also valid"""
    CA(valid_cron + " ")


def test_invalid_cron_format_four():
    with pytest.raises(ValueError):
        CA("* * * *")


def test_never_equal(a_time):
    c = CA("* * * * *")
    nt = c.next_ring(a_time)
    assert nt.minute != a_time.minute


def test_exclude_single(valid_cron):
    CA(valid_cron, valid_cron)


def test_exclude_multi_newline(valid_cron):
    CA(valid_cron, valid_cron + "\n" + valid_cron)


def test_exclude_multi_list(valid_cron):
    CA(valid_cron, [valid_cron, valid_cron])


def test_exclude_cron_works(a_time):
    c = CA("* * * * *")
    nt = c.next_ring(a_time)
    assert nt.day == 6
    c = CA("* * * * *", "* * 6 * *")
    nt = c.next_ring(a_time)
    assert nt is not None
    assert nt.day == 7


def test_exclude_fails(a_time):
    """exclude fails if every specification in cron_format is excluded"""
    c = CA("* * * * *", "* * * * *")
    assert c.has_ring(a_time) is False
    assert c.next_ring(a_time) is None

def test_exclude_date(a_time):
    """Exclude can exclude a whole date"""
    c = CA("* * * * *", "2019-08-06")
    assert c.has_ring(a_time)
    nt = c.next_ring(a_time)
    assert nt.day == 7

def test_exclude_more_dates(a_time):
    """Exclude can exclude a whole date"""
    c = CA("0 * * * *", "2019-08-06\n2019-08-07")
    print(c.next_ring(a_time))
    assert c.has_ring(a_time)
    nt = c.next_ring(a_time)
    assert nt.day == 8

def test_exclude_datetime(a_time):
    """Exclude can exclude a specific datetime"""
    c = CA("0 * * * *", "2019-08-06\n2019-08-07T00:00:00")
    assert c.has_ring(a_time)
    nt = c.next_ring(a_time)
    print(nt)
    assert nt.year == 2019
    assert nt.month == 8
    assert nt.day == 7
    assert nt.hour == 1
    assert nt.minute == 0
