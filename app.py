import json
import os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from cache import get_cache
from config import (
    TEXTBOXES,
    EVENTS,
    EVENT_TITLE_TEXT,
    TEST_DATA
)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("FOR_DESNOS_ONLY", "Testkey")
Bootstrap(app)
CSRFProtect(app)
cache = get_cache()

def add_to_cache_on_post(request, instance_id, event_id):
    success = []
    for textbox_key in EVENTS[event_id][TEXTBOXES]:
        item = request.form.get(textbox_key, "").strip()
        if item:
            cache.sadd(f"{instance_id}_{textbox_key}", item)
            success.append(item)
    return success


def retrieve_instance_data(instance_id, event_id):
    text_to_combine = {
        key: list(cache.smembers(f"{instance_id}_{key}"))
        for key in EVENTS[event_id][TEXTBOXES]
    }
    if not all(text_to_combine.values()):  # if missing data  - show test data
        text_to_combine = (
            TEST_DATA  # TODO: redirect to failure but show something for now
        )
    return text_to_combine


@app.route("/<instance_id>/<event_id>/add", methods=["GET", "POST"])
def text_input(instance_id, event_id):
    success = add_to_cache_on_post(request, instance_id, event_id)
    return render_template(
        "input.html",
        action=f"/{instance_id}/{event_id}/add",
        textboxes=EVENTS[event_id][TEXTBOXES],
        event_text=EVENTS[event_id][EVENT_TITLE_TEXT],
        success=success,
    )


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/", methods=["GET"])
@app.route("/htb", methods=["GET"])
def htb():
    return render_template("htb.html")


@app.route("/tables", methods=["GET"])
def tables():
    return render_template("tables.html")

@app.route("/ingirum.html", methods=["GET"])
@app.route("/ingirum", methods=["GET"])
def ingirum():
    return render_template("ingirum.html")

@app.route("/posted.html", methods=["GET"])
@app.route("/posted", methods=["GET"])
def posted():
    return render_template("posted.html")


@app.route("/<instance_id>/<event_id>/combine", methods=["GET"])
def combine(instance_id, event_id):
    text_to_combine = retrieve_instance_data(instance_id, event_id)
    return render_template("desnos.html", text_to_combine=json.dumps(text_to_combine))


@app.route("/<instance_id>/<event_id>/show", methods=["GET"])
def show(instance_id, event_id):
    all_texts = retrieve_instance_data(instance_id, event_id)
    text_for_display = {
        EVENTS[event_id][TEXTBOXES][key]: sorted(texts)
        for key, texts in all_texts.items()
    }
    return render_template(
        "show.html",
        text_for_display=text_for_display,
        event_text=EVENTS[event_id][EVENT_TITLE_TEXT],
    )


if __name__ == "__main__":
    app.run()
