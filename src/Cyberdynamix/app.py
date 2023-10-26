import re
import json
from os.path import join, abspath, dirname
import importlib
from flask import Flask, request, jsonify, render_template, send_from_directory
from Cyberdynamix.plugin import Plugin, create_plugin

DIR = dirname(abspath(__file__))

with open(join(DIR, 'static', 'responses.json'), 'r', encoding='utf-8') as f:
    responses = json.load(f)

app = Flask(__name__)

def process(text):
    return next(
        (value for key, value in responses.items() if key in text),
        '抱歉，我不明白您的意思',
    )

def load_plugin(plugin_name, **kwargs):
    module_name = f'plugins.{plugin_name.lower()}'
    plugin_module = importlib.import_module(module_name)
    plugin_cls = getattr(plugin_module, plugin_name)
    plugin = create_plugin(plugin_cls, **kwargs)
    return plugin.run()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

@app.route('/chat', methods=['POST'])
def reply():
    data = request.get_json()

    message = data['message']

    reply = None
    for pattern, definition in responses.items():
        if match := re.match(pattern, message):
            if definition['type'] == 'text':
                reply = definition['data']
            elif definition['type'] == 'plugin':
                plugin_name = definition['name']
                calling_args = match.groupdict()
                reply = load_plugin(plugin_name, **calling_args)
            break

    if not reply:
        reply = process(message)

    response = {'message': reply}
    return jsonify(response)

app.run(debug=True)
