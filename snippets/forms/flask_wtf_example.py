"""
Flask-WTF Example - Secure Form Handling
Shows how to handle forms securely compared to PHP's direct $_POST access
"""

from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
db = SQLAlchemy(app)

"""
PHP Form Processing (Insecure):
```php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'];  // No validation
    $email = $_POST['email'];        // No sanitization
    $password = $_POST['password'];  // Plain text
    
    // Direct SQL (vulnerable to injection)
    $query = "INSERT INTO users (username, email, password) 
              VALUES ('$username', '$email', '$password')";
    mysql_query($query);
}
```
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Custom Validator Example
def username_exists(form, field):
    """Custom validator to check if username is taken"""
    if User.query.filter_by(username=field.data).first():
        raise ValidationError('Username already exists')

class RegistrationForm(FlaskForm):
    """
    Registration form with validation
    
    Benefits over PHP:
    1. Automatic CSRF protection
    2. Built-in validation
    3. Secure field processing
    4. Error handling
    """
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=80),
        username_exists
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address')
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])

class ProfileForm(FlaskForm):
    """
    Profile update form showing different field types
    """
    bio = TextAreaField('Bio', validators=[Length(max=500)])
    country = SelectField('Country', choices=[
        ('us', 'United States'),
        ('uk', 'United Kingdom'),
        ('ca', 'Canada')
    ])
    newsletter = BooleanField('Subscribe to newsletter')
    
    def validate_bio(self, field):
        """Custom field-level validation"""
        if 'http' in field.data:
            raise ValidationError('URLs not allowed in bio')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Secure registration with form validation
    
    PHP Equivalent (Insecure):
    ```php
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // No CSRF protection
        // No automatic validation
        $errors = [];
        
        if (empty($_POST['username'])) {
            $errors[] = 'Username required';
        }
        if (empty($_POST['email'])) {
            $errors[] = 'Email required';
        }
        if (empty($_POST['password'])) {
            $errors[] = 'Password required';
        }
        
        if (empty($errors)) {
            // Process form...
        }
    }
    ```
    """
    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data  # Should hash this!
            )
            db.session.add(user)
            db.session.commit()
            flash('Registration successful!')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed')
            
    return render_template('register.html', form=form)

@app.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """Example of pre-populating form and handling updates"""
    user = User.query.get_or_404(1)  # Get current user
    form = ProfileForm(obj=user)  # Pre-populate form
    
    if form.validate_on_submit():
        try:
            form.populate_obj(user)  # Update user with form data
            db.session.commit()
            flash('Profile updated!')
            return redirect(url_for('profile'))
        except Exception as e:
            db.session.rollback()
            flash('Update failed')
            
    return render_template('edit_profile.html', form=form)

# Example templates showing proper form rendering

"""
register.html:
```html
<form method="POST">
    {{ form.csrf_token }}  <!-- CSRF protection -->
    
    <div>
        {{ form.username.label }}
        {{ form.username }}
        {% if form.username.errors %}
            {% for error in form.username.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <div>
        {{ form.email.label }}
        {{ form.email }}
        {% if form.email.errors %}
            {% for error in form.email.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <div>
        {{ form.password.label }}
        {{ form.password }}
        {% if form.password.errors %}
            {% for error in form.password.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <div>
        {{ form.confirm_password.label }}
        {{ form.confirm_password }}
        {% if form.confirm_password.errors %}
            {% for error in form.confirm_password.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <button type="submit">Register</button>
</form>
```

edit_profile.html:
```html
<form method="POST">
    {{ form.csrf_token }}
    
    <div>
        {{ form.bio.label }}
        {{ form.bio }}
        {% if form.bio.errors %}
            {% for error in form.bio.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <div>
        {{ form.country.label }}
        {{ form.country }}
        {% if form.country.errors %}
            {% for error in form.country.errors %}
                <span class="error">{{ error }}</span>
            {% endfor %}
        {% endif %}
    </div>
    
    <div>
        {{ form.newsletter }}
        {{ form.newsletter.label }}
    </div>
    
    <button type="submit">Update Profile</button>
</form>
```
"""

# Form Handling Best Practices

"""
1. Security:
   - Always use CSRF protection (enabled by default in Flask-WTF)
   - Validate and sanitize all input
   - Use proper field types (e.g., EmailField for emails)
   - Implement rate limiting for form submissions

2. Validation:
   - Use built-in validators when possible
   - Create custom validators for specific needs
   - Validate at both client and server side
   - Handle validation errors gracefully

3. User Experience:
   - Pre-populate forms when editing
   - Preserve form data on validation failure
   - Show clear error messages
   - Use appropriate HTML5 input types

4. File Uploads:
   ```python
   from flask_wtf.file import FileField, FileRequired, FileAllowed
   
   class UploadForm(FlaskForm):
       photo = FileField('Photo', validators=[
           FileRequired(),
           FileAllowed(['jpg', 'png'], 'Images only!')
       ])
   ```

5. AJAX Forms:
   ```python
   @app.route('/api/check-username')
   def check_username():
       username = request.args.get('username')
       exists = User.query.filter_by(username=username).first() is not None
       return jsonify({'exists': exists})
   ```

6. Complex Validation:
   ```python
   class AdvancedForm(FlaskForm):
       def validate(self):
           if not super().validate():
               return False
               
           # Custom form-level validation
           if self.end_date.data < self.start_date.data:
               self.end_date.errors.append('End date must be after start date')
               return False
               
           return True
   ```
"""
