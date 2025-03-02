from wtforms import StringField, validators, SubmitField

from .audioform_base import BaseForm

class AudioForm(BaseForm):
    nick = StringField(
        "Audio nick",
        validators=[validators.required()],
        description="A simple name to recognize this audio",
    )
    urls = StringField(
        "URLs",
        validators=[validators.required()],
        description="URL of the file to download",
    )
    submit = SubmitField("Submit")

    def populate_from_audiospec(self, audiospec):
        if "nick" in audiospec:
            self.nick.data = audiospec["nick"]
        if "urls" in audiospec:
            self.urls.data = ";".join(audiospec["urls"])


def audio_receive(form):
    return {"kind": "http", "nick": form.nick.data, "urls": form.urls.data.split(";")}
