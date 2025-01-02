# Module 4: Authentication & Security

## Table of Contents
- [Module 4: Authentication & Security](#module-4:-authentication-&-security)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Basic Concepts](#basic-concepts)
    - [PHP Session Auth vs Flask Auth](#php-session-auth-vs-flask-auth)
    - [Flask Modern Auth](#flask-modern-auth)
  - [Session Management](#session-management)
    - [Flask Session Configuration](#flask-session-configuration)
    - [Custom Session Handler](#custom-session-handler)
  - [Password Security](#password-security)
    - [Password Hashing](#password-hashing)
    - [Password Reset Flow](#password-reset-flow)
  - [CSRF Protection](#csrf-protection)
    - [Setup CSRF Protection](#setup-csrf-protection)
- [In forms](#in-forms)
- [In templates](#in-templates)
    - [AJAX Requests with CSRF](#ajax-requests-with-csrf)
  - [Role-based Access Control](#role-based-access-control)
    - [Role Implementation](#role-implementation)
  - [Security Headers](#security-headers)
    - [Implementing Security Headers](#implementing-security-headers)
  - [Two-Factor Authentication](#two-factor-authentication)
    - [Implementing 2FA](#implementing-2fa)
  - [Rate Limiting](#rate-limiting)
    - [Implementing Rate Limiting](#implementing-rate-limiting)
  - [Exercise: Secure Authentication System](#exercise:-secure-authentication-system)
  - [Common Pitfalls](#common-pitfalls)
  - [Next Steps](#next-steps)
  - [Additional Resources](#additional-resources)



## Introduction

This module covers implementing secure authentication and authorization in Flask applications. We'll explore how to move from basic PHP session-based auth to more robust solutions using Flask-Login and proper security practices.

## Basic Concepts

### PHP Session Auth vs Flask Auth
```php
// PHP Session Auth
<?php
session_start();
if ($_POST['username'] === 'admin' && $_POST['password'] === 'password') {
    $_SESSION['user_id'] = 1;
    $_SESSION['logged_in'] = true;
}
?>
```

### Flask Modern Auth
```python
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'})
    return jsonify({'message': 'Invalid credentials'}), 401
```

## Session Management

### Flask Session Configuration
```python
from flask_session import Session
from datetime import timedelta

app.config.update(
    SESSION_TYPE='filesystem',
    PERMANENT_SESSION_LIFETIME=timedelta(days=7),
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
Session(app)
```

### Custom Session Handler
```python
from flask import session
from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/protected')
@login_required
def protected():
    return f"Hello, {session['username']}"
```

## Password Security

### Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### Password Reset Flow
```python
from itsdangerous import URLSafeTimedSerializer

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=expiration
        )
        return email
    except:
        return None

@app.route('/reset-password', methods=['POST'])
def reset_password():
    email = request.form.get('email')
    token = generate_reset_token(email)
    # Send email with reset link
    return jsonify({'message': 'Reset email sent'})

@app.route('/reset-password/<token>', methods=['POST'])
def reset_password_confirm(token):
    email = verify_reset_token(token)
    if not email:
        return jsonify({'message': 'Invalid or expired token'}), 400
    
    user = User.query.filter_by(email=email).first()
    user.set_password(request.form.get('password'))
    db.session.commit()
    return jsonify({'message': 'Password updated'})
```

## CSRF Protection

### Setup CSRF Protection
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# In forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

# In templates
<form method="post">
    {{ form.csrf_token }}
    {{ form.username }}
    {{ form.password }}
    <input type="submit" value="Login">
</form>
```

### AJAX Requests with CSRF
```javascript
// JavaScript
const csrfToken = document.querySelector('meta[name="csrf-token"]').content;

fetch('/api/data', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRF-Token': csrfToken
    },
    body: JSON.stringify(data)
});
```

## Role-based Access Control

### Role Implementation
```python
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for('login'))
            if current_user.role.name != role_name:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin')
@role_required('admin')
def admin_panel():
    return 'Admin Panel'
```

## Security Headers

### Implementing Security Headers
```python
from flask_talisman import Talisman

Talisman(app, 
    content_security_policy={
        'default-src': "'self'",
        'script-src': "'self' 'unsafe-inline' 'unsafe-eval'",
        'style-src': "'self' 'unsafe-inline'"
    },
    force_https=True
)
```

## Two-Factor Authentication

### Implementing 2FA
```python
import pyotp

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    otp_secret = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.otp_secret is None:
            self.otp_secret = pyotp.random_base32()

    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            self.username,
            issuer_name='Your App Name'
        )

    def verify_totp(self, token):
        totp = pyotp.TOTP(self.otp_secret)
        return totp.verify(token)

@app.route('/login/2fa', methods=['POST'])
def login_2fa():
    token = request.form.get('token')
    if current_user.verify_totp(token):
        session['2fa_verified'] = True
        return redirect(url_for('index'))
    return 'Invalid token', 401
```

## Rate Limiting

### Implementing Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic here
    pass
```

## Exercise: Secure Authentication System

1. Start with this basic PHP auth:
```php
<?php
session_start();
if ($_POST) {
    if ($_POST['username'] === 'admin' && $_POST['password'] === 'password') {
        $_SESSION['logged_in'] = true;
        header('Location: dashboard.php');
    }
}
?>
```

2. Convert to secure Flask auth:
```python
from flask import Flask, request, session, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
login_manager = LoginManager(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html')
```

## Common Pitfalls

1. **Weak Password Storage**
   - Never store plain text passwords
   - Use strong hashing algorithms (bcrypt, Argon2)
   - Implement password complexity requirements

2. **Session Vulnerabilities**
   - Set secure session cookies
   - Implement proper session timeouts
   - Use secure session storage

3. **CSRF Vulnerabilities**
   - Always use CSRF protection
   - Implement proper token validation
   - Include tokens in forms and AJAX requests

4. **Missing Access Controls**
   - Implement proper role-based access
   - Validate permissions on every request
   - Don't rely on client-side security

## Next Steps

1. Complete the exercise above
2. Implement 2FA in your application
3. Add role-based access control
4. Implement password reset functionality
5. Move on to Module 5: Advanced Topics

## Additional Resources

- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Flask-Security Documentation](https://flask-security.readthedocs.io/)
- [OWASP Security Guidelines](https://owasp.org/www-project-web-security-testing-guide/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)
