"""
Flask-SocketIO Example - Real-time Communication
Shows how to implement real-time features compared to PHP's request-response cycle
"""

from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
socketio = SocketIO(app)
db = SQLAlchemy(app)

"""
PHP Traditional Approach (Polling):
```php
// check_messages.php
<?php
$last_check = $_GET['last_check'];
$messages = [];

// Read from file/database
$query = "SELECT * FROM messages WHERE timestamp > '$last_check'";
$result = mysql_query($query);

while ($row = mysql_fetch_assoc($result)) {
    $messages[] = $row;
}

echo json_encode($messages);
?>

// JavaScript polling
<script>
setInterval(function() {
    $.get('check_messages.php?last_check=' + lastCheck, function(data) {
        // Update UI with new messages
    });
}, 5000);  // Poll every 5 seconds
</script>
```
"""

# Models
class ChatRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    messages = db.relationship('Message', backref='room', lazy=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.Column(db.String(80), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('chat_room.id'), nullable=False)

# Routes
@app.route('/')
def index():
    """Render chat interface"""
    rooms = ChatRoom.query.all()
    return render_template('chat.html', rooms=rooms)

# SocketIO Event Handlers

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    """
    Handle room joining
    
    Instead of PHP's session-based room management:
    ```php
    $_SESSION['current_room'] = $_POST['room_id'];
    ```
    """
    room = data.get('room')
    join_room(room)
    emit('status', {
        'message': f'Joined room {room}'
    }, room=room)

@socketio.on('leave')
def handle_leave(data):
    """Handle room leaving"""
    room = data.get('room')
    leave_room(room)
    emit('status', {
        'message': f'Left room {room}'
    }, room=room)

@socketio.on('message')
def handle_message(data):
    """
    Handle new messages
    
    Instead of PHP's file/database write:
    ```php
    $message = [
        'user' => $_SESSION['username'],
        'content' => $_POST['message'],
        'timestamp' => time()
    ];
    file_put_contents('messages.json', json_encode($message));
    ```
    """
    room = data.get('room')
    content = data.get('message')
    user = data.get('user')
    
    # Save to database
    message = Message(
        content=content,
        user=user,
        room_id=room
    )
    db.session.add(message)
    db.session.commit()
    
    # Emit to all clients in room
    emit('message', {
        'user': user,
        'content': content,
        'timestamp': message.timestamp.isoformat()
    }, room=room)

@socketio.on('typing')
def handle_typing(data):
    """
    Handle typing status
    Not possible with traditional PHP!
    """
    room = data.get('room')
    user = data.get('user')
    emit('typing', {
        'user': user
    }, room=room, include_self=False)

# Example templates

"""
chat.html:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Flask-SocketIO Chat</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script>
        const socket = io();
        let currentRoom = null;
        
        // Connection handling
        socket.on('connect', () => {
            console.log('Connected to server');
        });
        
        socket.on('disconnect', () => {
            console.log('Disconnected from server');
        });
        
        // Message handling
        socket.on('message', (data) => {
            const messagesDiv = document.getElementById('messages');
            messagesDiv.innerHTML += `
                <div class="message">
                    <span class="user">${data.user}</span>
                    <span class="content">${data.content}</span>
                    <span class="time">${new Date(data.timestamp).toLocaleTimeString()}</span>
                </div>
            `;
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        });
        
        // Typing indicator
        socket.on('typing', (data) => {
            const typingDiv = document.getElementById('typing');
            typingDiv.textContent = `${data.user} is typing...`;
            setTimeout(() => {
                typingDiv.textContent = '';
            }, 2000);
        });
        
        // Room management
        function joinRoom(roomId) {
            if (currentRoom) {
                socket.emit('leave', {room: currentRoom});
            }
            currentRoom = roomId;
            socket.emit('join', {room: roomId});
            document.getElementById('messages').innerHTML = '';
        }
        
        // Send message
        function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (message && currentRoom) {
                socket.emit('message', {
                    room: currentRoom,
                    message: message,
                    user: 'User'  // Should come from authentication
                });
                input.value = '';
            }
        }
        
        // Typing indicator
        let typingTimeout;
        function handleTyping() {
            if (currentRoom) {
                clearTimeout(typingTimeout);
                socket.emit('typing', {
                    room: currentRoom,
                    user: 'User'  // Should come from authentication
                });
                typingTimeout = setTimeout(() => {}, 1000);
            }
        }
    </script>
    <style>
        #messages {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            margin-bottom: 10px;
        }
        .message {
            margin-bottom: 5px;
        }
        .user {
            font-weight: bold;
            margin-right: 10px;
        }
        .time {
            color: #666;
            font-size: 0.8em;
            margin-left: 10px;
        }
        #typing {
            height: 20px;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div id="rooms">
        {% for room in rooms %}
            <button onclick="joinRoom({{ room.id }})">{{ room.name }}</button>
        {% endfor %}
    </div>
    
    <div id="messages"></div>
    <div id="typing"></div>
    
    <input type="text" id="message-input" onkeyup="handleTyping()" placeholder="Type a message...">
    <button onclick="sendMessage()">Send</button>
</body>
</html>
```
"""

# Best Practices

"""
1. Connection Management:
   - Handle disconnections gracefully
   - Implement reconnection logic
   - Clean up resources on disconnect

2. Room Management:
   - Track active users in rooms
   - Handle room capacity limits
   - Clean up empty rooms

3. Message Handling:
   - Validate messages server-side
   - Rate limit messages
   - Store messages in database
   - Implement message history

4. Performance:
   - Use rooms for targeted broadcasting
   - Implement pagination for message history
   - Consider Redis for session storage
   - Monitor connection counts

5. Security:
   - Authenticate socket connections
   - Validate room access
   - Sanitize message content
   - Implement rate limiting

Example of authenticated connections:
```python
from flask_login import current_user

@socketio.on('connect')
def authenticated_connect():
    if not current_user.is_authenticated:
        return False  # Reject connection
    join_room(f'user_{current_user.id}')
    return True
```

6. Error Handling:
```python
@socketio.on_error()
def error_handler(e):
    print(f'SocketIO error: {e}')
    # Log error, notify user, etc.
```

7. Production Deployment:
   - Use multiple workers (gunicorn)
   - Configure proper proxy settings
   - Monitor connection counts
   - Implement proper logging
"""

if __name__ == '__main__':
    socketio.run(app, debug=True)
