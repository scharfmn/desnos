import json
import logging
import os
import redis
from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, g, jsonify, current_app, Markup
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
k = os.environ.get('FOR_DESNOS_ONLY', 'Testkey')
app.config['SECRET_KEY'] = os.environ.get('FOR_DESNOS_ONLY', 'Testkey')
logging.info(f'Secret key:{k}')
Bootstrap(app)
CSRFProtect(app)

cache = redis.StrictRedis(charset='utf-8', decode_responses=True, host='redis', port=6379)
#cache.flushdb() # DELETE BEFORE PRODUCTION
TEXTBOX_A_KEY = 'box_a'
TEXTBOX_B_KEY = 'box_b'
QA_QUESTION_KEY = 'qa_q'
QA_ANSWER_KEY = 'qa_a'
COND_IF_KEY = 'cond_if'
COND_THEN_KEY = 'cond_then'

QA_MAP = {TEXTBOX_A_KEY: QA_QUESTION_KEY, TEXTBOX_B_KEY: QA_ANSWER_KEY} 
COND_MAP = {TEXTBOX_A_KEY: COND_IF_KEY, TEXTBOX_B_KEY: COND_THEN_KEY}

def add_to_cache_on_post(request, event_map, event_instance):
    for textbox, event_type in event_map.items():
        item = request.form.get(textbox, '').strip()
        if item:
            cache.sadd(f'{event_instance}_{event_type}', item)

@app.route('/<event_instance>/if-then', methods=['GET', 'POST'])
def cond_input(event_instance):
    success = add_to_cache_on_post(request, COND_MAP, event_instance)
    return render_template(
        'input.html', 
        action=f'/{event_instance}/if-then',
        box_a='If or When', 
        box_b='Then', 
        event='Conditional Future',
        success=success
    )

@app.route('/<event_instance>/if-then-display', methods=['GET'])
def cond_combine(event_instance):
    return render_template(
        'desnos.html', 
        desnotic=json.dumps({
            TEXTBOX_A_KEY: list(cache.smembers(f'{event_instance}_{COND_IF_KEY}')),
            TEXTBOX_B_KEY: list(cache.smembers(f'{event_instance}_{COND_THEN_KEY}')),
        })
    )

@app.route('/<event_instance>/qa', methods=['GET', 'POST'])
def qa_input(event_instance):
    success = add_to_cache_on_post(request, QA_MAP, event_instance)
    return render_template(
        'input.html', 
        action=f'/{event_instance}/qa',
        box_a='Question', 
        box_b='Answer', 
        event='q/a', 
        success=success
    )

@app.route('/<event_instance>/qa-display', methods=['GET'])
def qa_combine(event_instance):
    return render_template(
        'desnos.html', 
        desnotic=json.dumps({
            TEXTBOX_A_KEY: list(cache.smembers(f'{event_instance}_{QA_QUESTION_KEY}')),
            TEXTBOX_B_KEY: list(cache.smembers(f'{event_instance}_{QA_ANSWER_KEY}')),
        })
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0')