# Chapter 4: Authentication and Security

## Introduction

Think about securing a building - you need ID cards for entry, security cameras for monitoring, and different access levels for different areas. Similarly, web applications need authentication to identify users, security measures to protect data, and authorization to control access. In this chapter, we'll learn how to implement security in Flask applications.

## 1. User Authentication

### The Building Security Metaphor

Think of authentication like building security:
- Login is like checking ID cards
- Passwords are like security codes
- Sessions are like temporary badges
- Logout is like returning badges
- Password reset is like replacing lost cards

### Basic User Model

```python
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
```

### Authentication System

```python
from flask import Flask, request, session, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this!

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
            
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
```

### Hands-On Exercise: Authentication System

Create a complete authentication system:
```python
# auth_app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('auth/home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']
        
        # Validation
        if password != confirm:
            flash('Passwords do not match')
            return redirect(url_for('register'))
            
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('register'))
            
        if User.query.filter_by(email=email).first():
            flash('Email already registered')
            return redirect(url_for('register'))
        
        # Create user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except:
            db.session.rollback()
            flash('Error during registration')
            
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = 'remember' in request.form
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
            
        flash('Invalid username or password')
        
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('auth/dashboard.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('auth/profile.html')

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/auth/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Authentication System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }

        nav {
            background-color: #f0f0f0;
            padding: 10px;
            margin-bottom: 20px;
        }

        nav a {
            margin-right: 10px;
            text-decoration: none;
            color: #333;
        }

        .flash-messages {
            margin-bottom: 20px;
        }

        .flash-message {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
            background-color: #f0f0f0;
        }

        .flash-message.error {
            background-color: #f2dede;
            color: #a94442;
        }

        .flash-message.success {
            background-color: #dff0d8;
            color: #3c763d;
        }

        form {
            max-width: 400px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('profile') }}">Profile</a>
            <a href="{{ url_for('logout') }}">Logout</a>
        {% else %}
            <a href="{{ url_for('login') }}">Login</a>
            <a href="{{ url_for('register') }}">Register</a>
        {% endif %}
    </nav>

    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <div class="flash-messages">
                {% for message in messages %}
                    <div class="flash-message">{{ message }}</div>
                {% endfor %}
            </div>
        {% endif %}
    {% endwith %}

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

<!-- templates/auth/home.html -->
{% extends "auth/base.html" %}

{% block content %}
    <h1>Welcome to Our Site</h1>
    
    {% if current_user.is_authenticated %}
        <p>Hello, {{ current_user.username }}!</p>
        <p><a href="{{ url_for('dashboard') }}">Go to Dashboard</a></p>
    {% else %}
        <p>Please <a href="{{ url_for('login') }}">login</a> or <a href="{{ url_for('register') }}">register</a>.</p>
    {% endif %}
{% endblock %}

<!-- templates/auth/register.html -->
{% extends "auth/base.html" %}

{% block content %}
    <h1>Register</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div class="form-group">
            <label for="confirm">Confirm Password:</label>
            <input type="password" id="confirm" name="confirm" required>
        </div>
        
        <button type="submit">Register</button>
    </form>
    
    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a></p>
{% endblock %}

<!-- templates/auth/login.html -->
{% extends "auth/base.html" %}

{% block content %}
    <h1>Login</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
        </div>
        
        <div class="form-group">
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div class="form-group">
            <label>
                <input type="checkbox" name="remember"> Remember me
            </label>
        </div>
        
        <button type="submit">Login</button>
    </form>
    
    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a></p>
{% endblock %}

<!-- templates/auth/dashboard.html -->
{% extends "auth/base.html" %}

{% block content %}
    <h1>Dashboard</h1>
    
    <p>Welcome back, {{ current_user.username }}!</p>
    
    <div class="user-info">
        <h2>Your Information</h2>
        <p><strong>Email:</strong> {{ current_user.email }}</p>
        <p><strong>Member since:</strong> {{ current_user.created_at.strftime('%Y-%m-%d') }}</p>
    </div>
{% endblock %}

<!-- templates/auth/profile.html -->
{% extends "auth/base.html" %}

{% block content %}
    <h1>Profile</h1>
    
    <div class="profile-info">
        <h2>{{ current_user.username }}</h2>
        <p><strong>Email:</strong> {{ current_user.email }}</p>
        <p><strong>Member since:</strong> {{ current_user.created_at.strftime('%Y-%m-%d') }}</p>
    </div>
{% endblock %}
```

## 2. Security Best Practices

### The Home Security Metaphor

Think of web security like home security:
- HTTPS like secure doors
- CSRF protection like window locks
- XSS prevention like security cameras
- SQL injection protection like alarm systems
- Input validation like checking visitors

### HTTPS and Security Headers

```python
from flask_talisman import Talisman

# Enable HTTPS
Talisman(app, force_https=True)

# Security headers
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

### CSRF Protection

```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# In forms
<form method="POST">
    {{ form.csrf_token }}
    ...
</form>

# In AJAX requests
const token = document.querySelector('meta[name="csrf-token"]').content;
fetch('/api/data', {
    method: 'POST',
    headers: {
        'X-CSRF-Token': token
    }
})
```

### Input Validation

```python
from werkzeug.utils import secure_filename
import re

def validate_username(username):
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValueError('Invalid username')
    return username

def validate_email(email):
    if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        raise ValueError('Invalid email')
    return email

def validate_file(filename):
    return secure_filename(filename)
```

## 3. Access Control

### The Office Access Metaphor

Think of access control like office access:
- Roles like job titles
- Permissions like access cards
- Decorators like security checkpoints
- Groups like departments
- Hierarchies like org charts

### Role-Based Access Control

```python
from functools import wraps
from flask_login import current_user

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    permissions = db.Column(db.Integer)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    
    def has_permission(self, permission):
        return self.role and (self.role.permissions & permission)

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/admin')
@login_required
@permission_required(ADMIN)
def admin():
    return 'Admin page'
```

### Hands-On Exercise: Role System

Create a role-based access system:
```python
# roles_app.py
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_required
from flask_login import current_user
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roles.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

# Permissions
class Permission:
    VIEW = 0x01
    EDIT = 0x02
    ADMIN = 0x04

# Models
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    permissions = db.Column(db.Integer)
    
    @staticmethod
    def insert_roles():
        roles = {
            'User': Permission.VIEW,
            'Editor': Permission.VIEW | Permission.EDIT,
            'Admin': Permission.VIEW | Permission.EDIT | Permission.ADMIN
        }
        
        for name, permissions in roles.items():
            role = Role.query.filter_by(name=name).first()
            if role is None:
                role = Role(name=name, permissions=permissions)
                db.session.add(role)
        db.session.commit()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', backref='users')
    
    def has_permission(self, permission):
        return self.role and (self.role.permissions & permission)
    
    def is_administrator(self):
        return self.has_permission(Permission.ADMIN)

# Decorators
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.has_permission(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)

# Routes
@app.route('/')
def home():
    return render_template('roles/home.html')

@app.route('/profile')
@login_required
def profile():
    return render_template('roles/profile.html')

@app.route('/edit')
@login_required
@permission_required(Permission.EDIT)
def edit():
    return render_template('roles/edit.html')

@app.route('/admin')
@login_required
@admin_required
def admin():
    return render_template('roles/admin.html')

# Template context processor
@app.context_processor
def inject_permissions():
    return dict(Permission=Permission)

# Error handlers
@app.errorhandler(403)
def forbidden(e):
    return render_template('roles/403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('roles/404.html'), 404

# Create tables
with app.app_context():
    db.create_all()
    Role.insert_roles()
```

```html
<!-- templates/roles/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Role System</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }

        nav {
            background-color: #f0f0f0;
            padding: 10px;
            margin-bottom: 20px;
        }

        nav a {
            margin-right: 10px;
            text-decoration: none;
            color: #333;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .error-page {
            text-align: center;
            padding: 50px;
        }

        .error-code {
            font-size: 72px;
            color: #666;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        {% if current_user.is_authenticated %}
            <a href="{{ url_for('profile') }}">Profile</a>
            {% if current_user.has_permission(Permission.EDIT) %}
                <a href="{{ url_for('edit') }}">Edit</a>
            {% endif %}
            {% if current_user.is_administrator() %}
                <a href="{{ url_for('admin') }}">Admin</a>
            {% endif %}
        {% endif %}
    </nav>

    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>

<!-- templates/roles/home.html -->
{% extends "roles/base.html" %}

{% block content %}
    <h1>Welcome</h1>
    
    {% if current_user.is_authenticated %}
        <p>Hello, {{ current_user.username }}!</p>
        <p>Your role: {{ current_user.role.name }}</p>
    {% else %}
        <p>Please log in to access features.</p>
    {% endif %}
{% endblock %}

<!-- templates/roles/profile.html -->
{% extends "roles/base.html" %}

{% block content %}
    <h1>Profile</h1>
    
    <div class="profile-info">
        <p><strong>Username:</strong> {{ current_user.username }}</p>
        <p><strong>Role:</strong> {{ current_user.role.name }}</p>
        
        <h2>Permissions:</h2>
        <ul>
            {% if current_user.has_permission(Permission.VIEW) %}
                <li>View content</li>
            {% endif %}
            {% if current_user.has_permission(Permission.EDIT) %}
                <li>Edit content</li>
            {% endif %}
            {% if current_user.has_permission(Permission.ADMIN) %}
                <li>Administrative access</li>
            {% endif %}
        </ul>
    </div>
{% endblock %}

<!-- templates/roles/edit.html -->
{% extends "roles/base.html" %}

{% block content %}
    <h1>Edit Content</h1>
    
    <p>This page is only accessible to users with edit permissions.</p>
{% endblock %}

<!-- templates/roles/admin.html -->
{% extends "roles/base.html" %}

{% block content %}
    <h1>Admin Panel</h1>
    
    <p>This page is only accessible to administrators.</p>
{% endblock %}

<!-- templates/roles/403.html -->
{% extends "roles/base.html" %}

{% block content %}
    <div class="error-page">
        <div class="error-code">403</div>
        <h1>Access Denied</h1>
        <p>You don't have permission to access this page.</p>
        <p><a href="{{ url_for('home') }}">Return to Home</a></p>
    </div>
{% endblock %}

<!-- templates/roles/404.html -->
{% extends "roles/base.html" %}

{% block content %}
    <div class="error-page">
        <div class="error-code">404</div>
        <h1>Page Not Found</h1>
        <p>The requested page does not exist.</p>
        <p><a href="{{ url_for('home') }}">Return to Home</a></p>
    </div>
{% endblock %}
```

## Practical Exercises

### 1. User Management
Build system with:
1. Registration/login
2. Password reset
3. Email verification
4. Profile management
5. Session handling

### 2. Permission System
Create system with:
1. Role hierarchy
2. Permission checks
3. Access control
4. Audit logging
5. Admin interface

### 3. Security Audit
Implement checks for:
1. HTTPS setup
2. CSRF protection
3. XSS prevention
4. Input validation
5. Error handling

## Review Questions

1. **Authentication**
   - How handle passwords?
   - When use sessions?
   - Best practices for login?

2. **Security**
   - How prevent CSRF?
   - When use HTTPS?
   - Best practices for input?

3. **Access Control**
   - How implement roles?
   - When check permissions?
   - Best practices for admin?

## Additional Resources

### Online Tools
- Security checkers
- Password hashers
- HTTPS testers

### Further Reading
- Security patterns
- Authentication flows
- Access control models

### Video Resources
- Security tutorials
- Authentication guides
- Permission examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Build secure applications
2. Implement authentication
3. Manage user access

Remember: Security should be a top priority in web development!

## Common Questions and Answers

Q: When should I hash passwords?
A: Always hash passwords before storing, using strong algorithms like bcrypt.

Q: How do I handle forgotten passwords?
A: Implement a secure reset flow with time-limited tokens sent via email.

Q: Should I implement my own authentication?
A: For learning yes, but consider using proven libraries like Flask-Login for production.

## Glossary

- **Authentication**: User verification
- **Authorization**: Access control
- **Hash**: One-way encryption
- **Session**: User state
- **Token**: Temporary credential
- **Role**: User category
- **Permission**: Access right
- **CSRF**: Cross-site request forgery
- **XSS**: Cross-site scripting
- **HTTPS**: Secure HTTP

Remember: Security is an ongoing process, not a one-time task!
