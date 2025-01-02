"""
Flask-Session Example - Secure Session Management
Shows how to handle sessions properly compared to PHP's default session handling
"""

from flask import Flask, session, redirect, url_for, request
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import redis

app = Flask(__name__)

# Session Configuration
app.config.update(
    # Basic settings
    SECRET_KEY='your-secret-key',
    SESSION_TYPE='redis',  # Options: redis, memcached, sqlalchemy, filesystem
    
    # Redis settings
    SESSION_REDIS=redis.from_url('redis://localhost:6379'),
    
    # Security settings
    SESSION_COOKIE_SECURE=True,  # Only send over HTTPS
    SESSION_COOKIE_HTTPONLY=True,  # Prevent JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',  # CSRF protection
    PERMANENT_SESSION_LIFETIME=timedelta(days=7)
)

"""
PHP Traditional Session Handling:
```php
// Basic session usage (insecure)
session_start();
$_SESSION['user_id'] = $user['id'];
$_SESSION['username'] = $user['username'];

// Access session data
if (isset($_SESSION['user_id'])) {
    $user_id = $_SESSION['user_id'];
}

// Custom session handler (file-based)
class FileSessionHandler implements SessionHandlerInterface {
    private $savePath;

    public function open($savePath, $sessionName) {
        $this->savePath = $savePath;
        if (!is_dir($savePath)) {
            mkdir($savePath, 0777);
        }
        return true;
    }

    public function read($id) {
        return (string)@file_get_contents("$this->savePath/sess_$id");
    }

    public function write($id, $data) {
        return file_put_contents("$this->savePath/sess_$id", $data) === false ? false : true;
    }
}

session_set_save_handler(new FileSessionHandler(), true);
```
"""

Session(app)
db = SQLAlchemy(app)

# Example User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    session_id = db.Column(db.String(255))  # Track current session

# Session Management Examples

@app.route('/login', methods=['POST'])
def login():
    """
    Secure login with session management
    
    PHP Equivalent:
    ```php
    session_start();
    if ($valid_login) {
        $_SESSION['user_id'] = $user['id'];
        $_SESSION['login_time'] = time();
    }
    ```
    """
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and check_password(user, password):
        # Store minimal data in session
        session['user_id'] = user.id
        session['login_time'] = datetime.utcnow().timestamp()
        
        # Track session for security
        user.session_id = session.id
        db.session.commit()
        
        return redirect(url_for('dashboard'))
    return 'Invalid login', 401

@app.route('/logout')
def logout():
    """
    Secure logout
    
    PHP Equivalent:
    ```php
    session_start();
    session_destroy();
    setcookie(session_name(), '', time() - 3600);
    ```
    """
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        if user:
            user.session_id = None
            db.session.commit()
    
    # Clear session
    session.clear()
    return redirect(url_for('login'))

# Session Security Features

@app.before_request
def validate_session():
    """
    Session validation middleware
    
    PHP Equivalent:
    ```php
    session_start();
    if (isset($_SESSION['login_time']) && 
        time() - $_SESSION['login_time'] > 3600) {
        session_destroy();
        header('Location: /login.php');
        exit();
    }
    ```
    """
    if 'user_id' in session:
        # Check session age
        login_time = session.get('login_time', 0)
        if time.time() - login_time > 3600:  # 1 hour timeout
            session.clear()
            return redirect(url_for('login'))
            
        # Validate session ID against stored value
        user = User.query.get(session['user_id'])
        if user and user.session_id != session.id:
            session.clear()
            return redirect(url_for('login'))
        
        # Rotate session ID periodically
        if time.time() - login_time > 300:  # 5 minutes
            session.regenerate()
            if user:
                user.session_id = session.id
                db.session.commit()

# Session Data Management

def set_session_data(key, value):
    """
    Secure way to store session data
    
    PHP Equivalent:
    ```php
    $_SESSION[$key] = $value;
    ```
    """
    try:
        session[key] = value
        return True
    except Exception as e:
        app.logger.error(f"Session storage error: {e}")
        return False

def get_session_data(key, default=None):
    """
    Secure way to retrieve session data
    
    PHP Equivalent:
    ```php
    return $_SESSION[$key] ?? null;
    ```
    """
    try:
        return session.get(key, default)
    except Exception as e:
        app.logger.error(f"Session retrieval error: {e}")
        return default

# Session-based Shopping Cart Example

@app.route('/cart/add/<int:product_id>')
def add_to_cart(product_id):
    """
    Shopping cart using session storage
    
    PHP Equivalent:
    ```php
    if (!isset($_SESSION['cart'])) {
        $_SESSION['cart'] = array();
    }
    $_SESSION['cart'][] = $product_id;
    ```
    """
    cart = session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1
    session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/cart/remove/<int:product_id>')
def remove_from_cart(product_id):
    """Remove item from session-based cart"""
    cart = session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
    return redirect(url_for('cart'))

# Session-based Flash Messages

def set_flash_message(message, category='info'):
    """
    Store flash message in session
    
    PHP Equivalent:
    ```php
    $_SESSION['flash_messages'][] = [
        'message' => $message,
        'category' => $category
    ];
    ```
    """
    if 'flash_messages' not in session:
        session['flash_messages'] = []
    session['flash_messages'].append({
        'message': message,
        'category': category
    })

def get_flash_messages():
    """
    Retrieve and clear flash messages
    
    PHP Equivalent:
    ```php
    $messages = $_SESSION['flash_messages'] ?? [];
    unset($_SESSION['flash_messages']);
    return $messages;
    ```
    """
    messages = session.pop('flash_messages', [])
    return messages

# Best Practices

"""
1. Security:
   - Use secure session configuration
   - Implement session validation
   - Rotate session IDs
   - Clear sensitive data

2. Storage:
   - Use Redis/Memcached for scalability
   - Implement proper serialization
   - Handle storage errors
   - Monitor session size

3. Data Management:
   - Store minimal data
   - Use proper data structures
   - Implement timeout handling
   - Clear old sessions

4. Configuration Example:
```python
app.config.update(
    SESSION_TYPE='redis',
    SESSION_REDIS=redis.from_url('redis://localhost:6379'),
    SESSION_KEY_PREFIX='myapp:',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
```

5. Session Cleanup:
```python
def cleanup_old_sessions():
    redis_client = redis.from_url('redis://localhost:6379')
    prefix = 'session:'
    
    # Get all session keys
    keys = redis_client.keys(f'{prefix}*')
    
    for key in keys:
        ttl = redis_client.ttl(key)
        if ttl < 0:  # Expired or no TTL
            redis_client.delete(key)
```

6. Session Monitoring:
```python
def get_session_stats():
    redis_client = redis.from_url('redis://localhost:6379')
    return {
        'active_sessions': len(redis_client.keys('session:*')),
        'memory_used': redis_client.info()['used_memory_human']
    }
```

7. Error Handling:
```python
def safe_session_operation(operation):
    try:
        return operation()
    except redis.RedisError as e:
        app.logger.error(f"Redis session error: {e}")
        return None
    except Exception as e:
        app.logger.error(f"Session error: {e}")
        return None
```
"""

if __name__ == '__main__':
    app.run(debug=True)
