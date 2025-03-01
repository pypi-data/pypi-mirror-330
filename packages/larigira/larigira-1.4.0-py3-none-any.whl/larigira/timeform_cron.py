import logging

from .timeform_base import BaseForm

from wtforms import StringField, validators, SubmitField, ValidationError
from croniter import croniter

log = logging.getLogger(__name__)


class CronAlarmForm(BaseForm):
    nick = StringField(
        "Alarm nick",
        validators=[validators.required()],
        description="A simple name to recognize this alarm",
    )
    cron_format = StringField(
        "cron-like format",
        validators=[validators.required()],
        description="the frequency specification, as in the <tt>cron</tt> command; "
        'see <a href="https://crontab.guru/">crontab.guru</a> for a hepl with cron format',
    )
    exclude = BaseForm.field_exclude()
    submit = SubmitField("Submit")

    def populate_from_timespec(self, timespec):
        super().populate_from_timespec(timespec)
        if "cron_format" in timespec:
            self.cron_format.data = timespec["cron_format"]

    def validate_cron_format(self, field):
        if not croniter.is_valid(field.data):
            raise ValidationError("formato di cron non valido")

    @classmethod
    def get_kind(cls):
        return "cron"

    @classmethod
    def form_receive(cls, form) -> dict:
        data = super().form_receive(form)
        data.update({
                "cron_format": form.cron_format.data,
                })
        return data
