import json
import os
from collections import defaultdict
from datetime import datetime
from flask import Flask, render_template, flash, redirect, url_for, request, g, jsonify, current_app, Markup
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ.get('FOR_DESNOS_ONLY')
Bootstrap(app)
CSRFProtect(app)


conditional_cache = defaultdict(lambda: defaultdict(list))
qa_cache = defaultdict(lambda: defaultdict(list))

def add_to_cache_on_post(request, cache, event_instance):
    cache, items = qa_cache if cache == 'qa' else conditional_cache, []
    for item_type in ('box_a', 'box_b'):
        item = request.form.get(item_type, '').strip()
        if item:
            cache[event_instance][item_type].append(item)
            items.append(item)
    return True if items else False

@app.route('/<event_instance>/if-then', methods=['GET', 'POST'])
def cond_input(event_instance):
    success = add_to_cache_on_post(request, 'conditional', event_instance)
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
        desnotic=json.dumps(dict(conditional_cache[event_instance]))
    )

@app.route('/<event_instance>/qa', methods=['GET', 'POST'])
def qa_input(event_instance):
    success = add_to_cache_on_post(request, 'qa', event_instance)
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
        desnotic=json.dumps(dict(qa_cache[event_instance]))
    )

if __name__ == "__main__":
    app.run(debuf=True)