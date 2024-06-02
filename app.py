from flask import Flask, render_template, Response, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import random
import configparser
import psutil
import json
import time
import re
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cpu_percentage')
def cpu_percentage():
    # Mock CPU usage data for demonstration
    while True:
        cpu_percent = random.randint(0, 100)
        data = {'cpu_percent': cpu_percent}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

#@app.route('/cpu_percentage')
#def cpu_percentage():
    while True:
        cpu_percent = psutil.cpu_percent(interval=1)
        data = {'cpu_percent': cpu_percent}
        yield f"data: {json.dumps(data)}\n\n"
        time.sleep(1)

@app.route('/stream')
def stream():
    return Response(cpu_percentage(), content_type='text/event-stream')


@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form.get('password')
    message = None

    if not password:
        message = 'No password provided'
    elif len(password) < 8:
        message = 'Password should be at least 8 characters long'
    elif not re.search('[a-z]', password) or not re.search('[A-Z]', password):
        message = 'Password should contain both uppercase and lowercase letters'
    elif not re.search('\d', password):
        message = 'Password should contain at least one digit'
    elif not re.search('[@$!%*?&]', password):
        message = 'Password should contain at least one special character'
    else:
        message = 'Password is strong'

    return render_template('index.html', message=message)


@app.route('/upload_config', methods=['POST'])
def upload_config():
    config_file = request.files.get('config')
    if not config_file:
        return {'message': 'No config file provided'}, 400

    filename = secure_filename(config_file.filename)
    folder_path = os.path.join(os.getcwd(), 'uploadable')
    os.makedirs(folder_path, exist_ok=True)
    filepath = os.path.join(folder_path, filename)
    config_file.save(filepath)

    config = configparser.ConfigParser()
    try:
        config.read(filepath)
    except configparser.Error as e:
        return {'message': str(e)}, 400

    config_dict = {s: dict(config.items(s)) for s in config.sections()}
    json_data = json.dumps(config_dict)

    private_folder = os.path.join(os.getcwd(), 'private')
    os.makedirs(private_folder, exist_ok=True)
    json_file = os.path.join(private_folder, 'saved.json')
    with open(json_file, 'w') as f:  
        f.write(json_data + '\n')

    return jsonify(config_dict)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')