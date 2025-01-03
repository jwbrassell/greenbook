# Chapter 2: Working with Data

## Introduction

Think about processing orders at a restaurant - you need to take customer orders, validate them, keep track of tables, and ensure everything is correct before sending to the kitchen. Similarly, web applications need to handle form submissions, validate input, and manage user sessions. In this chapter, we'll learn how to work with data in Flask applications.

## 1. Form Processing

### The Order Taking Metaphor

Think of form processing like taking restaurant orders:
- Forms are like order slips
- Validation is like checking availability
- Processing is like preparing orders
- Response is like serving food
- Errors are like order problems

### Basic Form Handling

```python
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Get form data (like reading order slip)
        item = request.form.get('item')
        quantity = request.form.get('quantity')
        
        # Process order (like sending to kitchen)
        return f'Ordered {quantity} {item}(s)'
    
    # Show form (like giving menu)
    return render_template('order_form.html')
```

```html
<!-- templates/order_form.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Place Order</title>
</head>
<body>
    <h1>Place Your Order</h1>
    <form method="POST">
        <div>
            <label for="item">Item:</label>
            <input type="text" id="item" name="item" required>
        </div>
        <div>
            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" name="quantity" required min="1">
        </div>
        <button type="submit">Place Order</button>
    </form>
</body>
</html>
```

### Form Data Types

```python
# Different input types
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Text input
        username = request.form.get('username')
        
        # Checkbox (returns 'on' if checked, None if not)
        newsletter = request.form.get('newsletter')
        
        # Multiple select
        interests = request.form.getlist('interests')
        
        # File upload
        if 'photo' in request.files:
            photo = request.files['photo']
            if photo.filename != '':
                photo.save('uploads/' + photo.filename)
```

### Hands-On Exercise: Order System

Create a restaurant order system:
```python
# order_app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Required for flashing messages

# Menu items with prices
menu = {
    'burger': {'name': 'Burger', 'price': 9.99},
    'pizza': {'name': 'Pizza', 'price': 12.99},
    'salad': {'name': 'Salad', 'price': 7.99},
    'pasta': {'name': 'Pasta', 'price': 11.99}
}

# Store orders in memory (in real app, use database)
orders = []

@app.route('/')
def home():
    return render_template('restaurant/home.html', menu=menu)

@app.route('/order', methods=['GET', 'POST'])
def place_order():
    if request.method == 'POST':
        # Get order details
        customer_name = request.form.get('name')
        item_id = request.form.get('item')
        quantity = request.form.get('quantity', type=int)
        special_instructions = request.form.get('instructions')
        
        # Validate input
        if not all([customer_name, item_id, quantity]):
            flash('Please fill all required fields')
            return redirect(url_for('place_order'))
            
        if item_id not in menu:
            flash('Invalid menu item')
            return redirect(url_for('place_order'))
            
        if quantity < 1:
            flash('Quantity must be at least 1')
            return redirect(url_for('place_order'))
        
        # Calculate total
        item = menu[item_id]
        total = item['price'] * quantity
        
        # Create order
        order = {
            'id': len(orders) + 1,
            'customer': customer_name,
            'item': item['name'],
            'quantity': quantity,
            'instructions': special_instructions,
            'total': total,
            'time': datetime.now(),
            'status': 'pending'
        }
        
        # Save order
        orders.append(order)
        
        flash('Order placed successfully!')
        return redirect(url_for('view_order', order_id=order['id']))
    
    return render_template('restaurant/order_form.html', menu=menu)

@app.route('/order/<int:order_id>')
def view_order(order_id):
    # Find order
    order = next((o for o in orders if o['id'] == order_id), None)
    if order is None:
        flash('Order not found')
        return redirect(url_for('home'))
    
    return render_template('restaurant/order_details.html', order=order)

@app.route('/orders')
def list_orders():
    return render_template('restaurant/orders.html', orders=orders)
```

```html
<!-- templates/restaurant/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Order System</title>
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

        .flash-message.success {
            background-color: #dff0d8;
            color: #3c763d;
        }

        .flash-message.error {
            background-color: #f2dede;
            color: #a94442;
        }

        form {
            max-width: 500px;
            margin: 0 auto;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input, select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
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

        .order {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 4px;
        }

        .price {
            font-weight: bold;
            color: #666;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('place_order') }}">Place Order</a>
        <a href="{{ url_for('list_orders') }}">View Orders</a>
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

    {% block content %}{% endblock %}
</body>
</html>

<!-- templates/restaurant/home.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>Welcome to Our Restaurant</h1>
    
    <h2>Our Menu</h2>
    <div class="menu">
        {% for id, item in menu.items() %}
            <div class="menu-item">
                <h3>{{ item.name }}</h3>
                <p class="price">${{ "%.2f"|format(item.price) }}</p>
            </div>
        {% endfor %}
    </div>

    <p><a href="{{ url_for('place_order') }}">Place an Order</a></p>
{% endblock %}

<!-- templates/restaurant/order_form.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>Place Your Order</h1>

    <form method="POST">
        <div class="form-group">
            <label for="name">Your Name:</label>
            <input type="text" id="name" name="name" required>
        </div>

        <div class="form-group">
            <label for="item">Select Item:</label>
            <select id="item" name="item" required>
                <option value="">Choose an item...</option>
                {% for id, item in menu.items() %}
                    <option value="{{ id }}">{{ item.name }} - ${{ "%.2f"|format(item.price) }}</option>
                {% endfor %}
            </select>
        </div>

        <div class="form-group">
            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" name="quantity" required min="1" value="1">
        </div>

        <div class="form-group">
            <label for="instructions">Special Instructions:</label>
            <textarea id="instructions" name="instructions" rows="3"></textarea>
        </div>

        <button type="submit">Place Order</button>
    </form>
{% endblock %}

<!-- templates/restaurant/order_details.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>Order #{{ order.id }}</h1>

    <div class="order">
        <p><strong>Customer:</strong> {{ order.customer }}</p>
        <p><strong>Item:</strong> {{ order.item }}</p>
        <p><strong>Quantity:</strong> {{ order.quantity }}</p>
        <p><strong>Total:</strong> ${{ "%.2f"|format(order.total) }}</p>
        <p><strong>Time:</strong> {{ order.time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
        <p><strong>Status:</strong> {{ order.status }}</p>
        
        {% if order.instructions %}
            <p><strong>Special Instructions:</strong> {{ order.instructions }}</p>
        {% endif %}
    </div>

    <p><a href="{{ url_for('list_orders') }}">View All Orders</a></p>
{% endblock %}

<!-- templates/restaurant/orders.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>All Orders</h1>

    {% if orders %}
        {% for order in orders|sort(attribute='time', reverse=true) %}
            <div class="order">
                <h3>Order #{{ order.id }}</h3>
                <p><strong>Customer:</strong> {{ order.customer }}</p>
                <p><strong>Item:</strong> {{ order.item }}</p>
                <p><strong>Quantity:</strong> {{ order.quantity }}</p>
                <p><strong>Total:</strong> ${{ "%.2f"|format(order.total) }}</p>
                <p><strong>Time:</strong> {{ order.time.strftime('%Y-%m-%d %H:%M:%S') }}</p>
                <p><strong>Status:</strong> {{ order.status }}</p>
                
                {% if order.instructions %}
                    <p><strong>Special Instructions:</strong> {{ order.instructions }}</p>
                {% endif %}
                
                <a href="{{ url_for('view_order', order_id=order.id) }}">View Details</a>
            </div>
        {% endfor %}
    {% else %}
        <p>No orders yet.</p>
    {% endif %}
{% endblock %}
```

## 2. Sessions and Cookies

### The Loyalty Card Metaphor

Think of sessions and cookies like restaurant loyalty cards:
- Sessions are like temporary cards
- Cookies are like permanent cards
- Session data like visit history
- Cookie data like preferences
- Expiration like card validity

### Working with Sessions

```python
from flask import session

# Set session data
@app.route('/login')
def login():
    session['user_id'] = 123
    session['username'] = 'john'
    return 'Logged in'

# Get session data
@app.route('/profile')
def profile():
    if 'user_id' in session:
        return f'Hello, {session["username"]}'
    return 'Please log in'

# Clear session
@app.route('/logout')
def logout():
    session.clear()
    return 'Logged out'
```

### Cookie Management

```python
from flask import make_response

# Set cookie
@app.route('/set-preference')
def set_preference():
    resp = make_response('Preference set')
    resp.set_cookie('theme', 'dark', max_age=31536000)  # 1 year
    return resp

# Get cookie
@app.route('/get-preference')
def get_preference():
    theme = request.cookies.get('theme', 'light')
    return f'Theme: {theme}'

# Delete cookie
@app.route('/clear-preference')
def clear_preference():
    resp = make_response('Preference cleared')
    resp.delete_cookie('theme')
    return resp
```

### Hands-On Exercise: Shopping Cart

Create a shopping cart system:
```python
# cart_app.py
from flask import Flask, session, render_template, request, redirect, url_for, flash
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key'

# Product catalog
products = {
    1: {'name': 'T-Shirt', 'price': 19.99},
    2: {'name': 'Jeans', 'price': 49.99},
    3: {'name': 'Shoes', 'price': 79.99},
    4: {'name': 'Hat', 'price': 24.99}
}

@app.route('/')
def home():
    return render_template('shop/home.html', products=products)

@app.route('/cart')
def view_cart():
    # Get cart from session
    cart = session.get('cart', {})
    
    # Calculate total
    total = sum(
        products[int(product_id)]['price'] * quantity
        for product_id, quantity in cart.items()
    )
    
    return render_template('shop/cart.html', 
                         cart=cart, 
                         products=products, 
                         total=total)

@app.route('/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    if str(product_id) not in products:
        flash('Invalid product')
        return redirect(url_for('home'))
    
    # Get quantity
    quantity = int(request.form.get('quantity', 1))
    if quantity < 1:
        flash('Invalid quantity')
        return redirect(url_for('home'))
    
    # Initialize cart if needed
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add to cart
    cart = session['cart']
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    # Save cart
    session['cart'] = cart
    
    flash('Added to cart!')
    return redirect(url_for('view_cart'))

@app.route('/update/<int:product_id>', methods=['POST'])
def update_cart(product_id):
    if str(product_id) not in products:
        flash('Invalid product')
        return redirect(url_for('view_cart'))
    
    # Get quantity
    quantity = int(request.form.get('quantity', 0))
    
    # Update cart
    cart = session.get('cart', {})
    if quantity > 0:
        cart[str(product_id)] = quantity
    else:
        cart.pop(str(product_id), None)
    
    # Save cart
    session['cart'] = cart
    
    flash('Cart updated!')
    return redirect(url_for('view_cart'))

@app.route('/clear')
def clear_cart():
    session.pop('cart', None)
    flash('Cart cleared!')
    return redirect(url_for('view_cart'))
```

```html
<!-- templates/shop/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Online Shop</title>
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
            background-color: #dff0d8;
            color: #3c763d;
        }

        .product-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
        }

        .product {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 4px;
        }

        .cart-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #ddd;
        }

        .price {
            color: #666;
            font-weight: bold;
        }

        .total {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #ddd;
            text-align: right;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 8px 16px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        input[type="number"] {
            width: 60px;
            padding: 4px;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Shop</a>
        <a href="{{ url_for('view_cart') }}">Cart</a>
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

    {% block content %}{% endblock %}
</body>
</html>

<!-- templates/shop/home.html -->
{% extends "shop/base.html" %}

{% block content %}
    <h1>Our Products</h1>

    <div class="product-grid">
        {% for id, product in products.items() %}
            <div class="product">
                <h3>{{ product.name }}</h3>
                <p class="price">${{ "%.2f"|format(product.price) }}</p>
                <form action="{{ url_for('add_to_cart', product_id=id) }}" method="POST">
                    <input type="number" name="quantity" value="1" min="1">
                    <button type="submit">Add to Cart</button>
                </form>
            </div>
        {% endfor %}
    </div>
{% endblock %}

<!-- templates/shop/cart.html -->
{% extends "shop/base.html" %}

{% block content %}
    <h1>Shopping Cart</h1>

    {% if cart %}
        {% for product_id, quantity in cart.items() %}
            {% set product = products[product_id|int] %}
            <div class="cart-item">
                <div>
                    <h3>{{ product.name }}</h3>
                    <p class="price">${{ "%.2f"|format(product.price) }} each</p>
                </div>
                <form action="{{ url_for('update_cart', product_id=product_id) }}" method="POST">
                    <input type="number" name="quantity" value="{{ quantity }}" min="0">
                    <button type="submit">Update</button>
                </form>
            </div>
        {% endfor %}

        <div class="total">
            <h3>Total: ${{ "%.2f"|format(total) }}</h3>
            <a href="{{ url_for('clear_cart') }}">Clear Cart</a>
        </div>
    {% else %}
        <p>Your cart is empty.</p>
    {% endif %}
{% endblock %}
```

## 3. Data Validation

### The Quality Control Metaphor

Think of validation like food quality control:
- Input checking like ingredient inspection
- Sanitization like cleaning produce
- Error handling like fixing problems
- Feedback like customer communication
- Rules like cooking standards

### Basic Validation

```python
from flask import Flask, request, flash

@app.route('/register', methods=['POST'])
def register():
    # Get data
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    password = request.form.get('password', '')
    
    # Validate data
    errors = []
    
    if not username:
        errors.append('Username is required')
    elif len(username) < 3:
        errors.append('Username must be at least 3 characters')
    
    if not email:
        errors.append('Email is required')
    elif '@' not in email:
        errors.append('Invalid email format')
    
    if not password:
        errors.append('Password is required')
    elif len(password) < 8:
        errors.append('Password must be at least 8 characters')
    
    # Handle errors
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('register_form'))
    
    # Process valid data
    return 'Registration successful'
```

### Form Validation with WTForms

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Email, Length

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
        validators=[
            DataRequired(),
            Length(min=3, max=20)
        ])
    email = EmailField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    password = PasswordField('Password',
        validators=[
            DataRequired(),
            Length(min=8)
        ])

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        # Process valid form
        return 'Registration successful'
    
    return render_template('register.html', form=form)
```

### Hands-On Exercise: Contact Form

Create a validated contact form:
```python
# contact_app.py
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, EmailField, SelectField
from wtforms.validators import DataRequired, Email, Length
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50)
    ])
    
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    
    subject = SelectField('Subject', choices=[
        ('general', 'General Inquiry'),
        ('support', 'Technical Support'),
        ('feedback', 'Feedback'),
        ('other', 'Other')
    ])
    
    message = TextAreaField('Message', validators=[
        DataRequired(),
        Length(min=10, max=1000)
    ])
    
    phone = StringField('Phone (optional)', validators=[
        Length(max=20)
    ])

    def validate_phone(form, field):
        if field.data:
            # Remove non-digits
            phone = re.sub(r'\D', '', field.data)
            # Check if valid
            if len(phone) < 10:
                raise ValidationError('Invalid phone number')
            # Format number
            if len(phone) == 10:
                field.data = f"({phone[:3]}) {phone[3:6]}-{phone[6:]}"

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Process form (in real app, send email/save to database)
        flash('Thank you for your message! We will respond shortly.')
        return redirect(url_for('contact'))
    
    return render_template('contact/form.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/contact/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
        }

        .flash-messages {
            margin-bottom: 20px;
        }

        .flash-message {
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 4px;
            background-color: #dff0d8;
            color: #3c763d;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }

        input, select, textarea {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        textarea {
            height: 150px;
        }

        .error {
            color: #a94442;
            font-size: 0.9em;
            margin-top: 5px;
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
    </style>
</head>
<body>
    <div class="container">
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="flash-messages">
                    {% for message in messages %}
                        <div class="flash-message">{{ message }}</div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </div>
</body>
</html>

<!-- templates/contact/form.html -->
{% extends "contact/base.html" %}

{% block content %}
    <h1>Contact Us</h1>
    
    <form method="POST">
        {{ form.csrf_token }}
        
        <div class="form-group">
            {{ form.name.label }}
            {{ form.name }}
            {% if form.name.errors %}
                {% for error in form.name.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.email.label }}
            {{ form.email }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.phone.label }}
            {{ form.phone }}
            {% if form.phone.errors %}
                {% for error in form.phone.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.subject.label }}
            {{ form.subject }}
            {% if form.subject.errors %}
                {% for error in form.subject.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            {% endif %}
        </div>

        <div class="form-group">
            {{ form.message.label }}
            {{ form.message }}
            {% if form.message.errors %}
                {% for error in form.message.errors %}
                    <div class="error">{{ error }}</div>
                {% endfor %}
            {% endif %}
        </div>

        <button type="submit">Send Message</button>
    </form>
{% endblock %}
```

## Practical Exercises

### 1. Registration System
Build user registration:
1. Form validation
2. Password strength
3. Email verification
4. Profile updates
5. Error handling

### 2. Survey System
Create survey application:
1. Multiple question types
2. Required fields
3. Data validation
4. Progress saving
5. Results summary

### 3. File Upload
Develop upload system:
1. File validation
2. Size limits
3. Type checking
4. Progress tracking
5. Error handling

## Review Questions

1. **Form Processing**
   - How handle different methods?
   - When use different fields?
   - Best practices for validation?

2. **Sessions/Cookies**
   - When use each type?
   - How manage expiration?
   - Security considerations?

3. **Validation**
   - What to validate?
   - How handle errors?
   - When use custom validation?

## Additional Resources

### Online Tools
- Form builders
- Validation libraries
