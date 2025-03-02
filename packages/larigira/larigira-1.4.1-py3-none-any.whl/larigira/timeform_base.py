import logging
from datetime import datetime

from pytimeparse.timeparse import timeparse

from flask_wtf import FlaskForm
from larigira.formutils import EasyDateTimeField
from wtforms import (SelectMultipleField, StringField, SubmitField,
                     TextAreaField, ValidationError, validators)

from .timegen_exclusions import multi_exclusion

log = logging.getLogger(__name__)

class BaseForm(FlaskForm):
    def validate_exclude(self, field):
        for line in field.data.split("\n"):
            if line.strip() and multi_exclusion(line) is None:
                raise ValidationError("formato di exclude non valido: %s" % line)

    def populate_from_timespec(self, timespec):
        if "nick" in timespec:
            self.nick.data = timespec["nick"]
        if hasattr(self, 'exclude') and "exclude" in timespec:
            if type(timespec["exclude"]) is str:
                self.exclude.data = timespec["exclude"]
            else:
                self.exclude.data = "\n".join(timespec["exclude"])

    @classmethod
    def get_kind(cls) -> str:
        # This is a simple euristics, but please override it
        return cls.__name__.removesuffix('AlarmForm').lower()

    @classmethod
    def form_receive(cls, form) -> dict:
        data = {
                "kind": cls.get_kind(),
                "nick": form.nick.data,
                }
        if hasattr(form , "exclude"):
            data["exclude"] = [
                    line.strip() for line in form.exclude.data.split("\n") if line.strip()
                    ]
        return data

    @classmethod
    def field_exclude(cls):
        return TextAreaField(
                "Any matching time will be excluded",
                description="Supported formats: YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS or cron-like format"
                )



class SingleAlarmForm(BaseForm):
    nick = StringField(
        "Alarm nick",
        validators=[validators.required()],
        description="A simple name to recognize this alarm",
    )
    dt = EasyDateTimeField(
        "Date and time",
        validators=[validators.required()],
        description="Date to ring on, expressed as " "2000-12-31T13:42:00",
    )
    submit = SubmitField("Submit")

    def populate_from_timespec(self, timespec):
        super().populate_from_timespec(timespec)
        if "nick" in timespec:
            self.nick.data = timespec["nick"]
        if "timestamp" in timespec:
            self.dt.data = datetime.fromtimestamp(timespec["timestamp"])

    @classmethod
    def get_kind(cls) -> str:
        # This is a simple euristics, but please override it
        return "single"

    @classmethod
    def form_receive(form) -> dict:
        data = super().form_receive(form)
        data["timestamp"] = int(form.dt.data.strftime("%s")),
        return data


class FrequencyAlarmForm(BaseForm):
    nick = StringField(
        "Alarm nick",
        validators=[validators.required()],
        description="A simple name to recognize this alarm",
    )
    interval = StringField(
        "Frequency",
        validators=[validators.required()],
        description="in seconds, or human-readable " "(like 9w3d12h)",
    )
    start = EasyDateTimeField(
        "Start date and time",
        validators=[validators.optional()],
        description="Before this, no alarm will ring. "
        "Expressed as YYYY-MM-DDTHH:MM:SS. If omitted, "
        "the alarm will always ring",
    )
    end = EasyDateTimeField(
        "End date and time",
        validators=[validators.optional()],
        description="After this, no alarm will ring. "
        "Expressed as YYYY-MM-DDTHH:MM:SS. If omitted, "
        "the alarm will always ring",
    )
    weekdays = SelectMultipleField(
        "Days on which the alarm should be played",
        choices=[
            ("1", "Monday"),
            ("2", "Tuesday"),
            ("3", "Wednesday"),
            ("4", "Thursday"),
            ("5", "Friday"),
            ("6", "Saturday"),
            ("7", "Sunday"),
        ],
        default=list("1234567"),
        validators=[validators.required()],
        description="The alarm will ring only on " "selected weekdays",
    )
    exclude = BaseForm.field_exclude()
    submit = SubmitField("Submit")

    def populate_from_timespec(self, timespec):
        super().populate_from_timespec(timespec)
        if timespec.get("start"):
            self.start.data = datetime.fromtimestamp(timespec["start"])
        if timespec.get("end"):
            self.end.data = datetime.fromtimestamp(timespec["end"])
        if "weekdays" in timespec:
            self.weekdays.data = timespec["weekdays"]
        else:
            self.weekdays.data = list("1234567")
        self.interval.data = timespec["interval"]

    def validate_interval(self, field):
        try:
            int(field.data)
        except ValueError:
            if timeparse(field.data) is None:
                raise ValidationError(
                    "interval must either be a number "
                    "(in seconds) or a human-readable "
                    "string like '1h2m'  or '1d12h'"
                )

    @classmethod
    def get_kind(cls):
        return "frequency"

    @staticmethod
    def form_receive(form) -> dict:
        data = super().form_receive(form)
        data.update({
            "interval": form.interval.data,
            "weekdays": form.weekdays.data,
        })
        if form.start.data:
            data["start"] = int(form.start.data.strftime("%s"))
        else:
            data["start"] = 0

        data["end"] = int(form.end.data.strftime("%s")) if form.end.data else None
        return data
