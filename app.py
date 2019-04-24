import json
import os
import redis
from functools import partial
from flask import Flask, render_template, flash, redirect, url_for, request, g, jsonify, current_app, Markup
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from test_data import TEST_DATA

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FOR_DESNOS_ONLY', 'Testkey')
Bootstrap(app)
CSRFProtect(app)

# redis-server /usr/local/etc/redis.conf

if os.environ.get('REDIS_URL'): # Heroku
    cache = redis.from_url(os.environ['REDIS_URL'], charset='utf-8', decode_responses=True)
elif os.environ.get('FLASK_APP'): # local
    cache = redis.StrictRedis(charset='utf-8', decode_responses=True)
else: # Docker (with redis on same server)
    cache = redis.StrictRedis(charset='utf-8', decode_responses=True, host='redis', port=6379)

#cache.flushdb() # DELETE BEFORE PRODUCTION

textbox_key = partial('box_{0}'.format)
TEXTBOXES = 'textboxes'
LABELS = 'labels'
EVENT_TITLE_TEXT = 'event_text'

EVENTS = {
    'qa': {
        TEXTBOXES: {textbox_key('a'): 'Question', textbox_key('b'): 'Answer',},
        EVENT_TITLE_TEXT: ['language event:', 'question · answer'], 
    },
    'if-then': {
        TEXTBOXES: {textbox_key('a'): 'If (or when)', textbox_key('b'): 'then',},
        EVENT_TITLE_TEXT: ['language event:', 'if · then'],
    },
    'after': {
        TEXTBOXES: {textbox_key('a'): 'After', textbox_key('b'): '(...)'},
        EVENT_TITLE_TEXT: ['language event', 'Nihaal Prasad’s “After”'],
    },
}

def add_to_cache_on_post(request, instance_id, event_id):
    success = []
    for textbox_key in EVENTS[event_id][TEXTBOXES]:
        item = request.form.get(textbox_key, '').strip()
        if item:
            cache.sadd(f'{instance_id}_{textbox_key}', item)
            success.append(item)
    return success

def retrieve_instance_data(instance_id, event_id):
    text_to_combine = { key: list(cache.smembers(f'{instance_id}_{key}')) 
            for key in EVENTS[event_id][TEXTBOXES]
    }
    if not all(text_to_combine.values()): # if missing data  - show test data
        text_to_combine = TEST_DATA # TODO: redirect to failure but show something for now
    return text_to_combine

@app.route('/<instance_id>/<event_id>/add', methods=['GET', 'POST'])
def text_input(instance_id, event_id):
    success = add_to_cache_on_post(request, instance_id, event_id)
    return render_template(
        'input.html', 
        action=f'/{instance_id}/{event_id}/add',
        textboxes=EVENTS[event_id][TEXTBOXES],
        event_text=EVENTS[event_id][EVENT_TITLE_TEXT],
        success=success
    )

@app.route('/<instance_id>/<event_id>/combine', methods=['GET'])
def combine(instance_id, event_id):
    text_to_combine = retrieve_instance_data(instance_id, event_id)
    return render_template('desnos.html', text_to_combine=json.dumps(text_to_combine))

@app.route('/<instance_id>/<event_id>/show', methods=['GET'])
def show(instance_id, event_id):
    all_texts = retrieve_instance_data(instance_id, event_id)
    text_for_display = {EVENTS[event_id][TEXTBOXES][key]: sorted(texts) for key, texts in all_texts.items() }
    return render_template(
        'show.html',
        text_for_display=text_for_display,
        event_text=EVENTS[event_id][EVENT_TITLE_TEXT], 
    )

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()