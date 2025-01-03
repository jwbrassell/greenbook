# Chapter 1: Flask Fundamentals

## Introduction

Think about a restaurant kitchen - you need a system to take orders, organize cooking, and serve meals efficiently. A web framework like Flask serves a similar purpose for web applications. It provides the structure and tools to handle web requests, process data, and serve responses. In this chapter, we'll learn how to build web applications with Flask.

## 1. Web Framework Basics

### The Restaurant Kitchen Metaphor

Think of Flask like a restaurant kitchen system:
- Routes are like the order counter
- Views are like the chefs
- Templates are like plating guidelines
- Static files are like pre-prepared ingredients
- Configuration is like kitchen rules

### Setting Up Flask

```bash
# Create virtual environment
python -m venv venv

# Activate environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# Install Flask
pip install flask

# Create requirements.txt
pip freeze > requirements.txt
```

### Basic Flask Application

```python
# app.py
from flask import Flask

# Create Flask application (like setting up kitchen)
app = Flask(__name__)

# Define route (like creating order counter)
@app.route('/')
def home():
    return 'Welcome to our restaurant!'

# Run application (like opening for business)
if __name__ == '__main__':
    app.run(debug=True)
```

### Hands-On Exercise: First Flask App

Create a simple menu application:
```python
# menu_app.py
from flask import Flask

app = Flask(__name__)

# Menu data (like inventory)
menu = {
    'appetizers': [
        {'name': 'Salad', 'price': 8.99},
        {'name': 'Soup', 'price': 6.99}
    ],
    'main_courses': [
        {'name': 'Steak', 'price': 25.99},
        {'name': 'Fish', 'price': 21.99}
    ],
    'desserts': [
        {'name': 'Cake', 'price': 7.99},
        {'name': 'Ice Cream', 'price': 5.99}
    ]
}

@app.route('/')
def home():
    return '''
        <h1>Welcome to Our Restaurant</h1>
        <nav>
            <a href="/menu">View Menu</a>
            <a href="/about">About Us</a>
            <a href="/contact">Contact</a>
        </nav>
    '''

@app.route('/menu')
def view_menu():
    menu_html = '<h1>Our Menu</h1>'
    
    for category, items in menu.items():
        menu_html += f'<h2>{category.title()}</h2><ul>'
        for item in items:
            menu_html += f'<li>{item["name"]} - ${item["price"]:.2f}</li>'
        menu_html += '</ul>'
    
    return menu_html

@app.route('/about')
def about():
    return '''
        <h1>About Us</h1>
        <p>We serve delicious food with love!</p>
    '''

@app.route('/contact')
def contact():
    return '''
        <h1>Contact Us</h1>
        <p>Phone: (555) 123-4567</p>
        <p>Email: info@restaurant.com</p>
    '''

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. Routes and Views

### The Mail Sorting Metaphor

Think of routing like sorting mail:
- URLs are like addresses
- Routes are like sorting rules
- Views are like mail handlers
- Parameters are like package details
- Responses are like return mail

### Basic Routing

```python
# Different route types
@app.route('/')
def home():
    return 'Home Page'

@app.route('/about')
def about():
    return 'About Us'

# Dynamic routes (like addressing to different apartments)
@app.route('/user/<username>')
def user_profile(username):
    return f'Profile of {username}'

# Multiple methods (like different delivery types)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Processing login'
    return 'Please log in'
```

### URL Building

```python
from flask import url_for

@app.route('/')
def home():
    # Generate URLs (like writing addresses)
    profile_url = url_for('user_profile', username='john')
    login_url = url_for('login')
    
    return f'''
        <a href="{profile_url}">John's Profile</a>
        <a href="{login_url}">Login</a>
    '''
```

### Hands-On Exercise: Route Practice

Create a blog-like application:
```python
# blog_app.py
from flask import Flask, url_for, abort
from datetime import datetime

app = Flask(__name__)

# Blog posts (like articles in filing cabinet)
posts = [
    {
        'id': 1,
        'title': 'First Post',
        'content': 'This is my first blog post!',
        'date': datetime(2024, 1, 1)
    },
    {
        'id': 2,
        'title': 'Flask Tutorial',
        'content': 'Learn Flask step by step...',
        'date': datetime(2024, 1, 15)
    }
]

@app.route('/')
def home():
    # Generate post links
    post_links = ''
    for post in posts:
        url = url_for('view_post', post_id=post['id'])
        post_links += f'<li><a href="{url}">{post["title"]}</a></li>'
    
    return f'''
        <h1>My Blog</h1>
        <ul>{post_links}</ul>
        <p><a href="{url_for('archive')}">Archive</a></p>
    '''

@app.route('/post/<int:post_id>')
def view_post(post_id):
    # Find post by id
    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        abort(404)
    
    return f'''
        <article>
            <h1>{post['title']}</h1>
            <time>{post['date'].strftime('%B %d, %Y')}</time>
            <p>{post['content']}</p>
        </article>
        <p><a href="{url_for('home')}">Back to Home</a></p>
    '''

@app.route('/archive')
def archive():
    # Sort posts by date
    sorted_posts = sorted(posts, key=lambda x: x['date'], reverse=True)
    
    archive_html = '<h1>Archive</h1><ul>'
    for post in sorted_posts:
        url = url_for('view_post', post_id=post['id'])
        date = post['date'].strftime('%Y-%m-%d')
        archive_html += f'<li>{date}: <a href="{url}">{post["title"]}</a></li>'
    archive_html += '</ul>'
    
    return archive_html

@app.errorhandler(404)
def page_not_found(error):
    return '''
        <h1>Page Not Found</h1>
        <p>Sorry, the requested page doesn't exist.</p>
        <p><a href="/">Back to Home</a></p>
    ''', 404

if __name__ == '__main__':
    app.run(debug=True)
```

## 3. Templates

### The Document Templates Metaphor

Think of templates like document templates:
- Base template like letterhead
- Blocks like fill-in sections
- Variables like mail merge
- Inheritance like document types
- Filters like text formatting

### Basic Templates

```python
# app.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html', title='Welcome')
```

```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - My Site</title>
</head>
<body>
    <header>
        <nav>
            <a href="{{ url_for('home') }}">Home</a>
            <a href="{{ url_for('about') }}">About</a>
            <a href="{{ url_for('contact') }}">Contact</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 My Site</p>
    </footer>
</body>
</html>

<!-- templates/home.html -->
{% extends "base.html" %}

{% block content %}
    <h1>{{ title }}</h1>
    <p>Welcome to our website!</p>
{% endblock %}
```

### Template Logic

```html
<!-- Conditions -->
{% if user %}
    <h1>Welcome, {{ user.name }}!</h1>
{% else %}
    <h1>Welcome, Guest!</h1>
{% endif %}

<!-- Loops -->
<ul>
{% for item in items %}
    <li>{{ item.name }} - ${{ item.price }}</li>
{% endfor %}
</ul>

<!-- Filters -->
{{ name|title }}
{{ date|strftime('%B %d, %Y') }}
{{ description|truncate(100) }}
```

### Hands-On Exercise: Template System

Create a restaurant menu system:
```python
# restaurant_app.py
from flask import Flask, render_template

app = Flask(__name__)

# Menu data
menu_items = {
    'Appetizers': [
        {'name': 'Salad', 'price': 8.99, 'description': 'Fresh garden salad'},
        {'name': 'Soup', 'price': 6.99, 'description': 'Soup of the day'}
    ],
    'Main Courses': [
        {'name': 'Steak', 'price': 25.99, 'description': 'Grilled ribeye'},
        {'name': 'Fish', 'price': 21.99, 'description': 'Fresh catch'}
    ],
    'Desserts': [
        {'name': 'Cake', 'price': 7.99, 'description': 'Chocolate cake'},
        {'name': 'Ice Cream', 'price': 5.99, 'description': 'Vanilla bean'}
    ]
}

@app.route('/')
def home():
    return render_template('restaurant/home.html', 
                         title='Welcome',
                         menu_items=menu_items)

@app.route('/menu')
def menu():
    return render_template('restaurant/menu.html',
                         title='Our Menu',
                         menu_items=menu_items)

@app.route('/about')
def about():
    return render_template('restaurant/about.html',
                         title='About Us')

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/restaurant/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - Our Restaurant</title>
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

        .menu-section {
            margin-bottom: 30px;
        }

        .menu-item {
            border-bottom: 1px solid #ddd;
            padding: 10px 0;
        }

        .price {
            color: #666;
            font-weight: bold;
        }

        footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            text-align: center;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('menu') }}">Menu</a>
        <a href="{{ url_for('about') }}">About</a>
    </nav>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2024 Our Restaurant. All rights reserved.</p>
    </footer>
</body>
</html>

<!-- templates/restaurant/home.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>Welcome to Our Restaurant</h1>
    
    <p>Experience the finest dining in town!</p>
    
    <h2>Today's Specials</h2>
    {% for category, items in menu_items.items() %}
        {% for item in items[:1] %}
            <div class="menu-item">
                <h3>{{ item.name }}</h3>
                <p>{{ item.description }}</p>
                <p class="price">${{ "%.2f"|format(item.price) }}</p>
            </div>
        {% endfor %}
    {% endfor %}
{% endblock %}

<!-- templates/restaurant/menu.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>Our Menu</h1>

    {% for category, items in menu_items.items() %}
        <section class="menu-section">
            <h2>{{ category }}</h2>
            {% for item in items %}
                <div class="menu-item">
                    <h3>{{ item.name }}</h3>
                    <p>{{ item.description }}</p>
                    <p class="price">${{ "%.2f"|format(item.price) }}</p>
                </div>
            {% endfor %}
        </section>
    {% endfor %}
{% endblock %}

<!-- templates/restaurant/about.html -->
{% extends "restaurant/base.html" %}

{% block content %}
    <h1>About Our Restaurant</h1>
    
    <p>We've been serving delicious meals since 2010.</p>
    
    <h2>Our Philosophy</h2>
    <p>We believe in using fresh, local ingredients to create memorable dining experiences.</p>
    
    <h2>Location</h2>
    <p>123 Main Street<br>Anytown, ST 12345</p>
    
    <h2>Hours</h2>
    <ul>
        <li>Monday - Friday: 11:00 AM - 10:00 PM</li>
        <li>Saturday: 10:00 AM - 11:00 PM</li>
        <li>Sunday: 10:00 AM - 9:00 PM</li>
    </ul>
{% endblock %}
```

## Practical Exercises

### 1. Portfolio Site
Build personal portfolio:
1. Home page
2. Projects page
3. Contact page
4. Dynamic routing
5. Template inheritance

### 2. Blog System
Create simple blog:
1. Post listing
2. Individual posts
3. Categories
4. Archives
5. Author pages

### 3. Product Catalog
Develop catalog system:
1. Category listing
2. Product details
3. Search function
4. Filtering
5. Sorting options

## Review Questions

1. **Flask Basics**
   - What is Flask?
   - How handle requests?
   - When use debug mode?

2. **Routing**
   - How define routes?
   - When use dynamic routes?
   - Best practices for URLs?

3. **Templates**
   - Why use templates?
   - How inheritance works?
   - When use filters?

## Additional Resources

### Online Tools
- Flask debugger
- Route testers
- Template validators

### Further Reading
- Flask documentation
- Jinja2 templates
- Web frameworks

### Video Resources
- Flask tutorials
- Template guides
- Routing examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Build Flask applications
2. Create dynamic routes
3. Design template systems

Remember: Flask's simplicity makes it perfect for learning web development!

## Common Questions and Answers

Q: When should I use Flask vs other frameworks?
A: Flask is great for learning and small to medium projects. Use larger frameworks for complex applications.

Q: How do I organize a growing Flask application?
A: Use blueprints and packages to organize code as your application grows.

Q: Should I use templates for everything?
A: Yes, templates help separate logic from presentation and make maintenance easier.

## Glossary

- **Flask**: Web framework
- **Route**: URL pattern
- **View**: Function handling request
- **Template**: HTML with placeholders
- **Blueprint**: Code organization
- **Decorator**: Route definition
- **Context**: Template variables
- **Filter**: Value formatter
- **Extension**: Added functionality
- **Debug**: Development mode

Remember: Start simple and add complexity as needed - Flask grows with your application!
