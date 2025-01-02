"""
Flask-WTF CSRF Protection Example
Shows how to implement proper CSRF protection compared to PHP's manual token handling
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for CSRF
csrf = CSRFProtect(app)  # Enable CSRF protection globally

"""
PHP Traditional CSRF Protection (Manual):
```php
// Start session for CSRF token
session_start();

// Generate token
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['csrf_token'])) {
        die('CSRF token missing');
    }
    
    if ($_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die('CSRF token invalid');
    }
    
    // Process form...
}

// In form:
<form method="POST">
    <input type="hidden" name="csrf_token" 
           value="<?php echo $_SESSION['csrf_token']; ?>">
    <!-- Form fields -->
</form>
```
"""

# Basic Form with CSRF Protection
class ContactForm(FlaskForm):
    """
    Form with automatic CSRF protection
    
    Benefits over PHP:
    1. Automatic token generation
    2. Secure token validation
    3. Token rotation
    4. XSS protection
    """
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Form is valid and CSRF token is correct
        send_message(form.name.data, form.email.data, form.message.data)
        flash('Message sent successfully!')
        return redirect(url_for('contact'))
        
    return render_template('contact.html', form=form)

# AJAX Forms with CSRF Protection
"""
contact.html with AJAX:
```html
<form id="contact-form" method="POST">
    {{ form.csrf_token }}
    {{ form.name.label }} {{ form.name }}
    {{ form.email.label }} {{ form.email }}
    {{ form.message.label }} {{ form.message }}
    <button type="submit">Send</button>
</form>

<script>
document.getElementById('contact-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    
    try {
        const response = await fetch('/contact', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': form.querySelector('input[name=csrf_token]').value
            }
        });
        
        if (response.ok) {
            alert('Message sent!');
        } else {
            alert('Error sending message');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
</script>
```
"""

# File Upload with CSRF Protection
class UploadForm(FlaskForm):
    """
    File upload form with CSRF protection
    
    PHP Equivalent (Insecure):
    ```php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $file = $_FILES['file'];
        move_uploaded_file(
            $file['tmp_name'], 
            'uploads/' . $file['name']
        );
    }
    ```
    """
    file = FileField('File', validators=[DataRequired()])
    description = StringField('Description')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File uploaded successfully!')
            return redirect(url_for('upload_file'))
            
    return render_template('upload.html', form=form)

# API Endpoints with CSRF Protection
@app.route('/api/data', methods=['POST'])
@csrf.exempt  # Disable CSRF for API endpoints using tokens
def api_endpoint():
    """
    API endpoint with token authentication instead of CSRF
    Include token in Authorization header
    """
    token = request.headers.get('Authorization')
    if not token or not validate_token(token):
        return {'error': 'Invalid token'}, 401
        
    return {'message': 'Success'}, 200

# Custom CSRF Error Handler
@csrf.error_handler
def csrf_error(reason):
    """Custom error handler for CSRF errors"""
    return render_template('csrf_error.html', reason=reason), 400

# Example Templates

"""
base.html:
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    {% with messages = get_flashed_messages() %}
        {% if messages %}
            <ul class="messages">
                {% for message in messages %}
                    <li>{{ message }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    
    {% block content %}{% endblock %}
</body>
</html>
```

contact.html:
```html
{% extends "base.html" %}

{% block title %}Contact Us{% endblock %}

{% block content %}
<form method="POST">
    {{ form.csrf_token }}
    
    <div>
        {{ form.name.label }}
        {{ form.name }}
        {% if form.name.errors %}
            <ul class="errors">
                {% for error in form.name.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <div>
        {{ form.email.label }}
        {{ form.email }}
        {% if form.email.errors %}
            <ul class="errors">
                {% for error in form.email.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <div>
        {{ form.message.label }}
        {{ form.message }}
        {% if form.message.errors %}
            <ul class="errors">
                {% for error in form.message.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <button type="submit">Send Message</button>
</form>
{% endblock %}
```

upload.html:
```html
{% extends "base.html" %}

{% block title %}Upload File{% endblock %}

{% block content %}
<form method="POST" enctype="multipart/form-data">
    {{ form.csrf_token }}
    
    <div>
        {{ form.file.label }}
        {{ form.file }}
        {% if form.file.errors %}
            <ul class="errors">
                {% for error in form.file.errors %}
                    <li>{{ error }}</li>
                {% endfor %}
            </ul>
        {% endif %}
    </div>
    
    <div>
        {{ form.description.label }}
        {{ form.description }}
    </div>
    
    <button type="submit">Upload</button>
</form>
{% endblock %}
```

csrf_error.html:
```html
{% extends "base.html" %}

{% block title %}CSRF Error{% endblock %}

{% block content %}
<h1>CSRF Validation Failed</h1>
<p>{{ reason }}</p>
<p>Please try again or contact support if the problem persists.</p>
{% endblock %}
```
"""

# Best Practices

"""
1. CSRF Protection:
   - Enable CSRF protection globally
   - Use proper token storage
   - Implement proper error handling
   - Consider token rotation

2. Form Security:
   - Validate all input
   - Sanitize output
   - Use proper field types
   - Implement rate limiting

3. File Uploads:
   - Validate file types
   - Use secure filenames
   - Limit file sizes
   - Scan for malware

4. API Security:
   - Use token authentication
   - Implement rate limiting
   - Validate content types
   - Handle errors properly

5. Example Security Headers:
```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```

6. Rate Limiting:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
def login():
    # Login logic here
    pass
```

7. Secure File Upload:
```python
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def secure_file_upload(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Check file size
        file.seek(0, os.SEEK_END)
        size = file.tell()
        if size > app.config['MAX_CONTENT_LENGTH']:
            raise ValueError('File too large')
            
        # Save file
        file.seek(0)
        file.save(file_path)
        
        return filename
    raise ValueError('Invalid file')
```
"""

if __name__ == '__main__':
    app.run(debug=True)
