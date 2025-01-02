"""
Real-time Chat Application Example
This example demonstrates WebSocket integration using Flask-SocketIO.
It shows how to implement real-time features that would be difficult with PHP.
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Store messages in memory (use a database in production)
messages = []

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

@socketio.on('connect')
def handle_connect():
    # Send existing messages to new clients
    emit('message_history', messages)

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    message = {
        'type': 'system',
        'username': 'System',
        'content': f'{username} has joined the room.',
        'room': room,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(message)
    emit('message', message, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    message = {
        'type': 'system',
        'username': 'System',
        'content': f'{username} has left the room.',
        'room': room,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(message)
    emit('message', message, room=room)

@socketio.on('message')
def handle_message(data):
    message = {
        'type': 'user',
        'username': data['username'],
        'content': data['message'],
        'room': data['room'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    messages.append(message)
    emit('message', message, room=data['room'])

@socketio.on('typing')
def handle_typing(data):
    emit('typing', {
        'username': data['username'],
        'isTyping': data['isTyping']
    }, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True)
