"""
This module contains a flask blueprint for db administration stuff

Templates are self-contained in this directory
"""

import mimetypes
import os
from collections import defaultdict
from datetime import datetime, time, timedelta

from flask import (Blueprint, Response, abort, current_app, flash, jsonify,
                   redirect, render_template, request, url_for)

from larigira import forms
from larigira.audiogen import get_audiogenerator
from larigira.config import get_conf
from larigira.entrypoints_utils import get_avail_entrypoints
from larigira.timegen import get_timegenerator, timegenerate

from .suggestions import get_suggestions

db = Blueprint(
    "db",
    __name__,
    url_prefix=get_conf()["ROUTE_PREFIX"] + "/db",
    template_folder="templates",
)


def request_wants_json():
    best = request.accept_mimetypes.best_match(
        ["application/json", "text/html"]
    )
    return (
        best == "application/json"
        and request.accept_mimetypes[best]
        > request.accept_mimetypes["text/html"]
    )


def get_model():
    return current_app.larigira.controller.monitor.model


@db.route("/")
def home():
    return render_template("dbadmin_base.html")


@db.route("/list")
def events_list():
    model = current_app.larigira.controller.monitor.model
    alarms = tuple(model.get_all_alarms())
    events = [(alarm, model.get_actions_by_alarm(alarm)) for alarm in alarms]
    return render_template("list.html", events=events)


@db.route("/calendar")
def events_calendar():
    model = current_app.larigira.controller.monitor.model
    today = datetime.now().date()
    max_days = 30
    max_occurrences = get_conf()["UI_CALENDAR_OCCURRENCIES_THRESHOLD"]
    # {date: {datetime: [(alarm1,actions1), (alarm2,actions2)]}}
    days = defaultdict(lambda: defaultdict(list))
    show_all = request.args.get("all", "0") == "1"
    for alarm in model.get_all_alarms():
        actions = tuple(model.get_actions_by_alarm(alarm))
        if not actions:
            continue
        today_dt = datetime.fromtimestamp(int(today.strftime("%s")))
        max_dt = datetime.combine(today_dt + timedelta(days=max_days), time())
        occurrences = []
        for t in timegenerate(
            alarm, now=today_dt, howmany=max_occurrences + 1
        ):
            if t is None:
                break
            if t > max_dt:
                break
            occurrences.append(t)
        if not occurrences:
            continue
        if not show_all and len(occurrences) > max_occurrences:
            continue
        for t in occurrences:
            days[t.date()][t].append((alarm, actions))

    # { weeknum: [day1, day2, day3] }
    weeks = defaultdict(list)
    for d in sorted(days.keys()):
        weeks[d.isocalendar()[:2]].append(d)

    return render_template(
        "calendar.html", days=days, weeks=weeks, show_all=show_all
    )


@db.route("/add/time")
def addtime():
    kinds = get_avail_entrypoints("larigira.timeform_create")

    def gen_info(gen):
        return dict(description=getattr(gen, "description", ""))

    info = {kind: gen_info(get_timegenerator(kind)) for kind in kinds}
    return render_template("add_time.html", kinds=kinds, info=info)


@db.route("/edit/time/<alarmid>", methods=["GET", "POST"])
def edit_time(alarmid):
    model = get_model()
    timespec = model.get_alarm_by_id(alarmid)
    kind = timespec["kind"]
    Form, receiver = tuple(forms.get_timeform(kind))
    form = Form()
    if request.method == "GET":
        form.populate_from_timespec(timespec)
    if request.method == "POST" and form.validate():
        data = receiver(form)
        model.update_alarm(alarmid, data)
        model.reload()
        return redirect(
            url_for("db.events_calendar", highlight=model.canonicalize(alarmid))
        )
    return render_template(
        "add_time_kind.html",
        form=form,
        kind=kind,
        mode="edit",
        alarmid=alarmid,
    )


def is_xhr():
    return request.headers.get("x-requested-with") is not None


@db.route("/add/time/<kind>", methods=["GET", "POST"])
def addtime_kind(kind):
    Form, receiver = tuple(forms.get_timeform(kind))
    form = Form(csrf_enabled=(not is_xhr()))
    if request.method == "POST":
        if form.validate():
            data = receiver(form)
            eid = get_model().add_alarm(data)
            if not is_xhr():
                return redirect(url_for("db.edit_event", alarmid=eid))
            else:
                resp = jsonify(alarmid=eid)
                resp.status_code = 201
                return resp
        elif is_xhr():
            resp = jsonify(errors=form.errors)
            resp.status_code = 400
            return resp

    return render_template(
        "add_time_kind.html", form=form, kind=kind, mode="add"
    )


@db.route("/add/audio")
def addaudio():
    kinds = get_avail_entrypoints("larigira.audioform_create")

    def gen_info(gen):
        return dict(description=getattr(gen, "description", ""))

    info = {kind: gen_info(get_audiogenerator(kind)) for kind in kinds}
    return render_template("add_audio.html", kinds=kinds, info=info)


@db.route("/add/audio/<kind>", methods=["GET", "POST"])
def addaudio_kind(kind):
    Form, receiver = tuple(forms.get_audioform(kind))
    form = Form(csrf_enabled=(not is_xhr()))
    if request.method == "POST":
        if form.validate():
            data = receiver(form)
            model = current_app.larigira.controller.monitor.model
            eid = model.add_action(data)
            return jsonify(dict(inserted=eid, data=data))
        else:
            resp = jsonify(errors=form.errors)
            resp.status_code = 400
            return resp

    return render_template(
        "add_audio_kind.html",
        form=form,
        kind=kind,
        suggestions=get_suggestions(),
    )


@db.route("/edit/audio/<actionid>", methods=["GET", "POST"])
def edit_audio(actionid):
    model = get_model()
    audiospec = model.get_action_by_id(actionid)
    kind = audiospec["kind"]
    Form, receiver = tuple(forms.get_audioform(kind))
    form = Form()
    if request.method == "GET":
        form.populate_from_audiospec(audiospec)
    if request.method == "POST" and form.validate():
        data = receiver(form)
        model.update_action(actionid, data)
        model.reload()
        return redirect(url_for("db.events_list"))
    return render_template(
        "add_audio_kind.html",
        form=form,
        kind=kind,
        mode="edit",
        suggestions=get_suggestions(),
    )


@db.route("/edit/event/<alarmid>")
def edit_event(alarmid):
    model = current_app.larigira.controller.monitor.model
    alarm = model.get_alarm_by_id(alarmid)
    if alarm is None:
        abort(404)
    allactions = model.get_all_actions()
    allactions.sort(key=lambda a: a.eid, reverse=True)
    actions = tuple(model.get_actions_by_alarm(alarm))
    return render_template(
        "edit_event.html",
        alarm=alarm,
        all_actions=allactions,
        actions=actions,
        routeprefix=get_conf()["ROUTE_PREFIX"],
    )


@db.route("/api/alarm/<alarmid>/actions", methods=["POST"])
def change_actions(alarmid):
    new_actions = request.form.getlist("actions[]")
    if new_actions is None:
        new_actions = []
    model = current_app.larigira.controller.monitor.model
    ret = model.update_alarm(
        alarmid, new_fields={"actions": [a for a in new_actions]}
    )
    return jsonify(dict(updated=alarmid, ret=ret))


@db.route("/api/alarm/<alarmid>/delete", methods=["POST"])
def delete_alarm(alarmid):
    model = current_app.larigira.controller.monitor.model
    try:
        alarm = model.get_alarm_by_id(alarmid)
        print(alarm["nick"])
        model.delete_alarm(alarmid)
    except KeyError:
        abort(404)
    if request_wants_json():
        return jsonify(dict(deleted=alarmid))
    flash("Evento %d `%s` cancellato" % (alarmid, alarm["nick"]))
    return redirect(url_for("db.events_list"))


@db.route("/extra/<path:relpath>")
def static_custom(relpath):
    basepath = get_conf()["EXTRA_STATIC_PATH"]
    if not basepath:
        abort(405)
    fpath = os.path.join(basepath, relpath)
    print(basepath, fpath)
    if not os.path.isfile(fpath):
        abort(404, "File non trovato")
    mime, _encoding = mimetypes.guess_type(fpath)
    return Response(open(fpath, "rb").read(), mimetype=mime)
