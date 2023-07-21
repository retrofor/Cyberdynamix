import re
import json
import importlib
from flask import Flask, request, jsonify, render_template, send_from_directory
from .plugin import Plugin, create_plugin

with open('static/responses.json', 'r', encoding='utf-8') as f:
    responses = json.load(f)

app = Flask(__name__)

def process(text):
    return next(
        (value for key, value in responses.items() if key in text),
        '抱歉，我不明白您的意思',
    )

def load_plugin(plugin_name, **kwargs):
    module_name = f'plugins.{plugin_name.lower()}_plugin'
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

    # 获取请求中的输入语句
    message = data['message']

    # 在 responses 变量中查找匹配该输入语句的回复
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

    # 如果没有找到匹配的回复，则返回 process 函数的返回值
    if not reply:
        reply = process(message)

    # 将回复转换为 JSON 格式并返回响应
    response = {'message': reply}
    return jsonify(response)

app.run(debug=True)
