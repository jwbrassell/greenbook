"""
Flask-Login Example - Secure Authentication
Shows how to implement user authentication properly compared to PHP sessions
"""

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for sessions
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    """
    User model with secure password handling
    
    PHP Equivalent:
    ```php
    // INSECURE - storing plain passwords
    $user = [
        'username' => $_POST['username'],
        'password' => $_POST['password']  // Plain text!
    ];
    file_put_contents('users.json', json_encode($user));
    
    // Login check
    $users = json_decode(file_get_contents('users.json'), true);
    if ($users['password'] === $_POST['password']) {  // Unsafe comparison
        $_SESSION['user_id'] = $users['id'];
    }
    ```
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        """Securely hash the password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    """Required for Flask-Login"""
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Secure user registration
    
    PHP Equivalent:
    ```php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $user = [
            'username' => $_POST['username'],
            'password' => $_POST['password']  // Unsafe!
        ];
        file_put_contents('users.json', json_encode($user));
        $_SESSION['user_id'] = $user['id'];
    }
    ```
    """
    if request.method == 'POST':
        if User.query.filter_by(username=request.form['username']).first():
            flash('Username already exists')
            return redirect(url_for('register'))
        
        user = User(
            username=request.form['username'],
            email=request.form['email']
        )
        user.set_password(request.form['password'])
        
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed')
            return redirect(url_for('register'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Secure login with password hashing
    
    PHP Equivalent:
    ```php
    $users = json_decode(file_get_contents('users.json'), true);
    if ($users['password'] === $_POST['password']) {  // Unsafe comparison
        $_SESSION['user_id'] = $users['id'];
        header('Location: /dashboard.php');
    }
    ```
    """
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            # Get the page they were trying to access
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """
    Secure logout
    
    PHP Equivalent:
    ```php
    session_destroy();
    header('Location: /login.php');
    ```
    """
    logout_user()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required  # Requires authentication
def dashboard():
    """
    Protected route example
    
    PHP Equivalent:
    ```php
    if (!isset($_SESSION['user_id'])) {
        header('Location: /login.php');
        exit();
    }
    ```
    """
    return render_template('dashboard.html')

@app.route('/profile')
@login_required
def profile():
    """
    Access current user data
    
    PHP Equivalent:
    ```php
    if (!isset($_SESSION['user_id'])) {
        header('Location: /login.php');
        exit();
    }
    $users = json_decode(file_get_contents('users.json'), true);
    $current_user = array_filter($users, function($u) {
        return $u['id'] == $_SESSION['user_id'];
    })[0];
    ```
    """
    return render_template('profile.html', user=current_user)

# Example templates (save these in templates/)

"""
login.html:
```html
<form method="POST" action="{{ url_for('login') }}">
    <input type="text" name="username" required>
    <input type="password" name="password" required>
    <button type="submit">Login</button>
</form>
```

register.html:
```html
<form method="POST" action="{{ url_for('register') }}">
    <input type="text" name="username" required>
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    <button type="submit">Register</button>
</form>
```

dashboard.html:
```html
{% if current_user.is_authenticated %}
    <h1>Welcome {{ current_user.username }}</h1>
    <a href="{{ url_for('logout') }}">Logout</a>
{% endif %}
```
"""

# Security Best Practices

"""
1. Password Security:
   - Always hash passwords (never store plain text)
   - Use strong hashing algorithms (like bcrypt)
   - Implement password complexity requirements

2. Session Security:
   - Use secure session configuration
   - Implement CSRF protection
   - Set secure cookie flags

3. Access Control:
   - Use @login_required decorator
   - Implement role-based access control
   - Validate user permissions

4. Error Handling:
   - Don't expose sensitive information in errors
   - Log security events
   - Implement rate limiting

5. Additional Security Measures:
   - Enable HTTPS
   - Implement password reset functionality
   - Add two-factor authentication
"""
