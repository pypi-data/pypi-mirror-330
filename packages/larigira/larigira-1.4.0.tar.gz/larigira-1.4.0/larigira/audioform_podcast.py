from wtforms import (BooleanField, IntegerField, SelectField, StringField,
                     SubmitField, validators)
from wtforms.fields.html5 import URLField
from larigira.audioform_base import BaseForm


class AudioForm(BaseForm):
    nick = StringField(
        "Audio nick",
        validators=[validators.required()],
        description="A simple name to recognize this audio",
    )
    url = URLField(
        "URL",
        validators=[validators.required()],
        description="URL of the podcast; it must be valid xml",
    )

    # TODO: group by filters/sort/select
    min_len = StringField(
        "Accetta solo audio lunghi almeno:",
        description="Leaving this empty will disable this filter",
    )
    max_len = StringField(
        "Accetta solo audio lunghi al massimo:",
        description="Leaving this empty will disable this filter",
    )
    sort_by = SelectField(
        "Sort episodes",
        choices=[
            ("none", "Don't sort"),
            ("random", "Random"),
            ("duration", "Duration"),
            ("date", "date"),
        ],
    )
    start = IntegerField(
        "Play from episode number",
        description="Episodes count from 0; 0 is a sane default",
    )
    reverse = BooleanField("Reverse sort (descending)")
    submit = SubmitField("Submit")

    def populate_from_audiospec(self, audiospec):
        for key in ("nick", "url", "sort_by", "reverse", "min_len", "max_len"):
            if key in audiospec:
                getattr(self, key).data = audiospec[key]
        self.start.data = int(audiospec.get("start", 0))


def audio_receive(form):
    d = {"kind": "podcast"}
    for key in (
        "nick",
        "url",
        "sort_by",
        "reverse",
        "min_len",
        "max_len",
        "start",
    ):
        d[key] = getattr(form, key).data
    return d
