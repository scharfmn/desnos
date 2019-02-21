import json
import os
import redis
from flask import Flask, render_template, flash, redirect, url_for, request, g, jsonify, current_app, Markup
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
#from test_data import TEST_DATA

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
TEXTBOX_A_KEY = 'box_a'
TEXTBOX_B_KEY = 'box_b'
QA_QUESTION_KEY = 'qa_q'
QA_ANSWER_KEY = 'qa_a'
COND_IF_KEY = 'cond_if'
COND_THEN_KEY = 'cond_then'

MAPS = {
    'qa': {
        'textbox_map': {TEXTBOX_A_KEY: QA_QUESTION_KEY, TEXTBOX_B_KEY: QA_ANSWER_KEY},
        'box_a': 'Question', 
        'box_b': 'Answer', 
        'event': ['Language event 1', 'question · answer'], 
    },
    'if-then': {
        'textbox_map': {TEXTBOX_A_KEY: COND_IF_KEY, TEXTBOX_B_KEY: COND_THEN_KEY},
        'box_a': 'If (or when)', 
        'box_b': '(then)', 
        'event': ['Language event 2', 'if · then'],
    },
}

EVENT_NAMES = ['qa', 'if-then']

#def retrieve(instance, key):
#    return list(cache.smembers(f'{instance}_{textbox_map[key]}'))

def add_to_cache_on_post(request, event_instance, event_name):
    items = []
    for textbox, event_type in MAPS[event_name]['textbox_map'].items():
        item = request.form.get(textbox, '').strip()
        if item:
            # if event_name == 'if-then':
            #     if textbox == TEXTBOX_A_KEY:
            #         if not item.lower().startswith('if'):
            #             item = "If " + item
            #     if textbox == TEXTBOX_B_KEY:
            #         if not item.lower().startswith('then'):
            #             item = "then " + item
            items.append(item)
            cache.sadd(f'{event_instance}_{event_type}', item)
    return items

@app.route('/<event_instance>/<event_name>/add', methods=['GET', 'POST'])
def text_input(event_instance, event_name):
    success = add_to_cache_on_post(request, event_instance, event_name)
    return render_template(
        'input.html', 
        action=f'/{event_instance}/{event_name}/add',
        box_a=MAPS[event_name]['box_a'],
        box_b=MAPS[event_name]['box_b'],
        event=MAPS[event_name]['event'], 
        success=success
    )

@app.route('/<event_instance>/<event_name>/combine', methods=['GET'])
def combine(event_instance, event_name):
    #textbox_map = MAPS[event_name]['textbox_map']
    return render_template(
        'desnos.html', 
        desnotic=json.dumps({
            TEXTBOX_A_KEY: list(cache.smembers(f'{event_instance}_{textbox_map[TEXTBOX_A_KEY]}')),
            TEXTBOX_B_KEY: list(cache.smembers(f'{event_instance}_{textbox_map[TEXTBOX_B_KEY]}')),
        })
        #desnotic=json.dumps(TEST_DATA)
    )

@app.route('/<event_instance>/<event_name>/show', methods=['GET'])
def show(event_instance, event_name):
    textbox_map = MAPS[event_name]['textbox_map']
    return render_template(
        'show.html', 
        all_a = list(cache.smembers(f'{event_instance}_{textbox_map[TEXTBOX_A_KEY]}')),
        all_b = list(cache.smembers(f'{event_instance}_{textbox_map[TEXTBOX_B_KEY]}')),
        box_a=MAPS[event_name]['box_a'],
        box_b=MAPS[event_name]['box_b'],
        event=MAPS[event_name]['event'], 
    )

if __name__ == "__main__":
    #app.run(host='0.0.0.0')
    app.run()