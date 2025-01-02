# Module 5: Advanced Topics

## Table of Contents
- [Module 5: Advanced Topics](#module-5:-advanced-topics)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Caching](#caching)
    - [Basic Caching with Flask-Caching](#basic-caching-with-flask-caching)
- [Cache view response](#cache-view-response)
- [Cache function results](#cache-function-results)
- [Manually cache data](#manually-cache-data)
    - [Redis Caching](#redis-caching)
- [config.py](#configpy)
- [Usage](#usage)
  - [WebSocket Integration](#websocket-integration)
    - [Basic WebSocket Setup](#basic-websocket-setup)
- [Run the app](#run-the-app)
    - [Real-time Chat Example](#real-time-chat-example)
- [Server](#server)
- [Client (JavaScript)](#client-javascript)
  - [Background Tasks](#background-tasks)
    - [Using Celery](#using-celery)
- [In your Flask route](#in-your-flask-route)
  - [File Uploads](#file-uploads)
    - [Basic File Upload](#basic-file-upload)
    - [S3 Upload](#s3-upload)
  - [Logging & Monitoring](#logging-&-monitoring)
    - [Advanced Logging](#advanced-logging)
- [Setup logging](#setup-logging)
- [Usage](#usage)
  - [Exercise: Real-time Dashboard](#exercise:-real-time-dashboard)
  - [Common Pitfalls](#common-pitfalls)
  - [Next Steps](#next-steps)
  - [Additional Resources](#additional-resources)



## Introduction

This module covers advanced Flask features and integrations that enhance application functionality and performance. We'll explore caching, real-time communication with WebSockets, background tasks, and more.

## Caching

### Basic Caching with Flask-Caching
```python
from flask_caching import Cache

cache = Cache(app, config={
    'CACHE_TYPE': 'simple',  # Use redis in production
    'CACHE_DEFAULT_TIMEOUT': 300
})

# Cache view response
@app.route('/expensive-operation')
@cache.cached(timeout=300)  # 5 minutes
def expensive_operation():
    # Expensive computation here
    return result

# Cache function results
@cache.memoize(timeout=300)
def get_user_data(user_id):
    return User.query.get(user_id)

# Manually cache data
def update_stats():
    stats = compute_statistics()
    cache.set('site_stats', stats, timeout=3600)
```

### Redis Caching
```python
# config.py
CACHE_TYPE = 'redis'
CACHE_REDIS_HOST = 'localhost'
CACHE_REDIS_PORT = 6379
CACHE_REDIS_DB = 0
CACHE_REDIS_URL = 'redis://localhost:6379/0'

# Usage
@cache.cached(timeout=300, key_prefix='all_users')
def get_all_users():
    return User.query.all()
```

## WebSocket Integration

### Basic WebSocket Setup
```python
from flask_socketio import SocketIO, emit

socketio = SocketIO(app)

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('message')
def handle_message(message):
    print('Received message:', message)
    emit('response', {'data': 'Message received!'})

@socketio.on('custom_event')
def handle_custom_event(json):
    print('Received JSON:', json)
    emit('response', json, broadcast=True)

# Run the app
if __name__ == '__main__':
    socketio.run(app, debug=True)
```

### Real-time Chat Example
```python
# Server
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{username} has joined the room.'}, room=room)

@socketio.on('message')
def on_message(data):
    username = data['username']
    room = data['room']
    message = data['message']
    emit('message', {
        'username': username,
        'message': message
    }, room=room)

# Client (JavaScript)
const socket = io();

socket.emit('join', {
    username: 'John',
    room: 'general'
});

socket.on('message', function(data) {
    console.log('Message:', data);
});
```

## Background Tasks

### Using Celery
```python
from celery import Celery

celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def long_running_task(param1, param2):
    # Time-consuming operation here
    result = complex_operation(param1, param2)
    return result

# In your Flask route
@app.route('/process')
def process():
    task = long_running_task.delay(param1, param2)
    return jsonify({'task_id': task.id})

@app.route('/status/<task_id>')
def task_status(task_id):
    task = long_running_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state == 'SUCCESS':
        response = {
            'state': task.state,
            'result': task.result
        }
    return jsonify(response)
```

## File Uploads

### Basic File Upload
```python
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'
```

### S3 Upload
```python
import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client('s3')

def upload_to_s3(file, bucket_name, object_name=None):
    if object_name is None:
        object_name = secure_filename(file.filename)

    try:
        s3_client.upload_fileobj(file, bucket_name, object_name)
    except ClientError as e:
        print(e)
        return False
    return True

@app.route('/upload-to-s3', methods=['POST'])
def upload_file_to_s3():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400
    
    if file and allowed_file(file.filename):
        if upload_to_s3(file, 'your-bucket-name'):
            return 'File uploaded to S3 successfully'
    return 'Upload failed', 400
```

## Logging & Monitoring

### Advanced Logging
```python
import logging
from logging.handlers import RotatingFileHandler

# Setup logging
if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Application startup')

# Usage
@app.route('/api/action')
def some_action():
    try:
        result = perform_action()
        app.logger.info(f'Action performed successfully: {result}')
        return jsonify(result)
    except Exception as e:
        app.logger.error(f'Failed to perform action: {str(e)}')
        return 'Error occurred', 500
```

## Exercise: Real-time Dashboard

Create a real-time dashboard that displays system metrics using WebSocket:

1. Backend Setup:
```python
from flask import Flask, render_template
from flask_socketio import SocketIO
import psutil
import time
from threading import Thread

app = Flask(__name__)
socketio = SocketIO(app)

def background_task():
    while True:
        cpu = psutil.cpu_percent()
        memory = psutil.virtual_memory().percent
        socketio.emit('system_metrics', {
            'cpu': cpu,
            'memory': memory
        })
        time.sleep(1)

@app.route('/')
def index():
    return render_template('dashboard.html')

if __name__ == '__main__':
    Thread(target=background_task, daemon=True).start()
    socketio.run(app, debug=True)
```

2. Frontend Setup:
```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html>
<head>
    <title>System Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="cpu-gauge"></div>
    <div id="memory-gauge"></div>
    <script>
        const socket = io();
        
        socket.on('system_metrics', function(data) {
            Plotly.update('cpu-gauge', {
                value: [data.cpu]
            });
            Plotly.update('memory-gauge', {
                value: [data.memory]
            });
        });

        // Initialize gauges
        Plotly.newPlot('cpu-gauge', [{
            type: 'indicator',
            mode: 'gauge+number',
            value: 0,
            title: { text: 'CPU Usage' },
            gauge: { axis: { range: [0, 100] } }
        }]);

        Plotly.newPlot('memory-gauge', [{
            type: 'indicator',
            mode: 'gauge+number',
            value: 0,
            title: { text: 'Memory Usage' },
            gauge: { axis: { range: [0, 100] } }
        }]);
    </script>
</body>
</html>
```

## Common Pitfalls

1. **Cache Invalidation**
   - Implement proper cache invalidation strategies
   - Use appropriate cache timeouts
   - Handle race conditions

2. **WebSocket Management**
   - Handle disconnections gracefully
   - Implement reconnection logic
   - Consider scaling implications

3. **Background Tasks**
   - Monitor task queues
   - Handle task failures
   - Implement proper error reporting

4. **Resource Management**
   - Monitor memory usage
   - Implement proper cleanup
   - Handle file uploads securely

## Next Steps

1. Complete the real-time dashboard exercise
2. Implement caching in your application
3. Add WebSocket functionality
4. Set up background tasks
5. Move on to Module 6: Deployment & DevOps

## Additional Resources

- [Flask-Caching Documentation](https://flask-caching.readthedocs.io/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [AWS S3 Python Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html)
