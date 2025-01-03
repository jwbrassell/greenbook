# Chapter 3: Database Integration

## Introduction

Think about organizing a library - you need a system to catalog books, track borrowers, and manage inventory. Similarly, web applications need databases to store and organize data persistently. In this chapter, we'll learn how to integrate databases with Flask applications using SQLAlchemy.

## 1. Database Setup

### The Library Catalog Metaphor

Think of databases like a library catalog system:
- Tables are like different sections (Books, Members, Loans)
- Rows are like individual items
- Columns are like item properties
- Relationships are like cross-references
- Queries are like search requests

### Setting Up SQLAlchemy

```python
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define models (like catalog cards)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    published_date = db.Column(db.Date)
    loans = db.relationship('Loan', backref='book', lazy=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    loans = db.relationship('Loan', backref='member', lazy=True)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)

# Create tables
with app.app_context():
    db.create_all()
```

### Database Migrations

```python
# migrations.py
from flask_migrate import Migrate

migrate = Migrate(app, db)

# Terminal commands:
# flask db init    # Initialize migrations
# flask db migrate # Create migration
# flask db upgrade # Apply migration
```

### Hands-On Exercise: Library System

Create a library management system:
```python
# library_app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key'

db = SQLAlchemy(app)

# Models
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True)
    quantity = db.Column(db.Integer, default=1)
    available = db.Column(db.Integer)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.available = self.quantity

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('member.id'), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    returned_date = db.Column(db.DateTime)
    
    book = db.relationship('Book', backref=db.backref('loans', lazy=True))
    member = db.relationship('Member', backref=db.backref('loans', lazy=True))

# Routes
@app.route('/')
def home():
    books = Book.query.all()
    return render_template('library/home.html', books=books)

@app.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('library/books.html', books=books)

@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = Book(
            title=request.form['title'],
            author=request.form['author'],
            isbn=request.form['isbn'],
            quantity=int(request.form['quantity'])
        )
        
        try:
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully!')
            return redirect(url_for('list_books'))
        except:
            db.session.rollback()
            flash('Error adding book.')
            
    return render_template('library/add_book.html')

@app.route('/members')
def list_members():
    members = Member.query.all()
    return render_template('library/members.html', members=members)

@app.route('/members/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        member = Member(
            name=request.form['name'],
            email=request.form['email']
        )
        
        try:
            db.session.add(member)
            db.session.commit()
            flash('Member added successfully!')
            return redirect(url_for('list_members'))
        except:
            db.session.rollback()
            flash('Error adding member.')
            
    return render_template('library/add_member.html')

@app.route('/loans')
def list_loans():
    loans = Loan.query.filter_by(returned_date=None).all()
    return render_template('library/loans.html', loans=loans)

@app.route('/loan/new', methods=['GET', 'POST'])
def new_loan():
    if request.method == 'POST':
        book_id = int(request.form['book_id'])
        member_id = int(request.form['member_id'])
        
        # Check if book is available
        book = Book.query.get(book_id)
        if not book or book.available <= 0:
            flash('Book not available.')
            return redirect(url_for('new_loan'))
        
        # Create loan
        loan = Loan(
            book_id=book_id,
            member_id=member_id,
            due_date=datetime.utcnow() + timedelta(days=14)
        )
        
        # Update book availability
        book.available -= 1
        
        try:
            db.session.add(loan)
            db.session.commit()
            flash('Loan created successfully!')
            return redirect(url_for('list_loans'))
        except:
            db.session.rollback()
            flash('Error creating loan.')
    
    books = Book.query.filter(Book.available > 0).all()
    members = Member.query.all()
    return render_template('library/new_loan.html', 
                         books=books, 
                         members=members)

@app.route('/loan/return/<int:loan_id>')
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    if not loan.returned_date:
        loan.returned_date = datetime.utcnow()
        loan.book.available += 1
        
        try:
            db.session.commit()
            flash('Book returned successfully!')
        except:
            db.session.rollback()
            flash('Error returning book.')
    
    return redirect(url_for('list_loans'))

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
```

```html
<!-- templates/library/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Library Management System</title>
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

        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }

        th, td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }

        th {
            background-color: #f5f5f5;
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

        input, select {
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

        .book-count {
            color: #666;
        }

        .overdue {
            color: #a94442;
        }
    </style>
</head>
<body>
    <nav>
        <a href="{{ url_for('home') }}">Home</a>
        <a href="{{ url_for('list_books') }}">Books</a>
        <a href="{{ url_for('list_members') }}">Members</a>
        <a href="{{ url_for('list_loans') }}">Loans</a>
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

<!-- templates/library/home.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Library Management System</h1>
    
    <h2>Quick Actions</h2>
    <p>
        <a href="{{ url_for('add_book') }}">Add New Book</a> |
        <a href="{{ url_for('add_member') }}">Add New Member</a> |
        <a href="{{ url_for('new_loan') }}">Create New Loan</a>
    </p>
    
    <h2>Available Books</h2>
    <table>
        <tr>
            <th>Title</th>
            <th>Author</th>
            <th>Available</th>
        </tr>
        {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td class="book-count">{{ book.available }}/{{ book.quantity }}</td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}

<!-- templates/library/books.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Books</h1>
    
    <p><a href="{{ url_for('add_book') }}">Add New Book</a></p>
    
    <table>
        <tr>
            <th>Title</th>
            <th>Author</th>
            <th>ISBN</th>
            <th>Available</th>
        </tr>
        {% for book in books %}
            <tr>
                <td>{{ book.title }}</td>
                <td>{{ book.author }}</td>
                <td>{{ book.isbn }}</td>
                <td class="book-count">{{ book.available }}/{{ book.quantity }}</td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}

<!-- templates/library/add_book.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Add New Book</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" required>
        </div>
        
        <div class="form-group">
            <label for="author">Author:</label>
            <input type="text" id="author" name="author" required>
        </div>
        
        <div class="form-group">
            <label for="isbn">ISBN:</label>
            <input type="text" id="isbn" name="isbn" required>
        </div>
        
        <div class="form-group">
            <label for="quantity">Quantity:</label>
            <input type="number" id="quantity" name="quantity" value="1" min="1" required>
        </div>
        
        <button type="submit">Add Book</button>
    </form>
{% endblock %}

<!-- templates/library/members.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Members</h1>
    
    <p><a href="{{ url_for('add_member') }}">Add New Member</a></p>
    
    <table>
        <tr>
            <th>Name</th>
            <th>Email</th>
            <th>Join Date</th>
        </tr>
        {% for member in members %}
            <tr>
                <td>{{ member.name }}</td>
                <td>{{ member.email }}</td>
                <td>{{ member.join_date.strftime('%Y-%m-%d') }}</td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}

<!-- templates/library/add_member.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Add New Member</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <button type="submit">Add Member</button>
    </form>
{% endblock %}

<!-- templates/library/loans.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Active Loans</h1>
    
    <p><a href="{{ url_for('new_loan') }}">Create New Loan</a></p>
    
    <table>
        <tr>
            <th>Book</th>
            <th>Member</th>
            <th>Loan Date</th>
            <th>Due Date</th>
            <th>Action</th>
        </tr>
        {% for loan in loans %}
            <tr>
                <td>{{ loan.book.title }}</td>
                <td>{{ loan.member.name }}</td>
                <td>{{ loan.loan_date.strftime('%Y-%m-%d') }}</td>
                <td class="{{ 'overdue' if loan.due_date < now }}">
                    {{ loan.due_date.strftime('%Y-%m-%d') }}
                </td>
                <td>
                    <a href="{{ url_for('return_book', loan_id=loan.id) }}">Return</a>
                </td>
            </tr>
        {% endfor %}
    </table>
{% endblock %}

<!-- templates/library/new_loan.html -->
{% extends "library/base.html" %}

{% block content %}
    <h1>Create New Loan</h1>
    
    <form method="POST">
        <div class="form-group">
            <label for="book_id">Book:</label>
            <select id="book_id" name="book_id" required>
                <option value="">Select a book...</option>
                {% for book in books %}
                    <option value="{{ book.id }}">
                        {{ book.title }} ({{ book.available }} available)
                    </option>
                {% endfor %}
            </select>
        </div>
        
        <div class="form-group">
            <label for="member_id">Member:</label>
            <select id="member_id" name="member_id" required>
                <option value="">Select a member...</option>
                {% for member in members %}
                    <option value="{{ member.id }}">{{ member.name }}</option>
                {% endfor %}
            </select>
        </div>
        
        <button type="submit">Create Loan</button>
    </form>
{% endblock %}
```

## 2. CRUD Operations

### The Inventory Management Metaphor

Think of CRUD operations like managing inventory:
- Create like adding new items
- Read like checking stock
- Update like modifying details
- Delete like removing items
- Queries like inventory checks

### Basic Operations

```python
# Create
new_book = Book(title='Python 101', author='John Doe')
db.session.add(new_book)
db.session.commit()

# Read
book = Book.query.get(1)  # Get by ID
books = Book.query.all()  # Get all
python_books = Book.query.filter_by(author='John Doe').all()

# Update
book = Book.query.get(1)
book.title = 'Python 102'
db.session.commit()

# Delete
book = Book.query.get(1)
db.session.delete(book)
db.session.commit()
```

### Querying

```python
# Filter operations
Book.query.filter_by(author='John Doe')
Book.query.filter(Book.price < 20)

# Ordering
Book.query.order_by(Book.title)
Book.query.order_by(Book.price.desc())

# Limiting
Book.query.limit(10)
Book.query.offset(20).limit(10)

# Joins
db.session.query(Book, Author).join(Author)
```

### Relationships

```python
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    books = db.relationship('Book', backref='author', lazy=True)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

# Using relationships
author = Author.query.get(1)
author.books  # Get all books by author

book = Book.query.get(1)
book.author  # Get book's author
```

## 3. Advanced Database Concepts

### The Library System Metaphor

Think of advanced concepts like library systems:
- Transactions like batch processing
- Migrations like renovations
- Backups like archive copies
- Indexing like catalog cards
- Optimization like efficient shelving

### Transactions

```python
# Basic transaction
try:
    db.session.add(new_book)
    db.session.add(new_author)
    db.session.commit()
except:
    db.session.rollback()
    raise

# Context manager
from contextlib import contextmanager

@contextmanager
def db_transaction():
    try:
        yield
        db.session.commit()
    except:
        db.session.rollback()
        raise
```

### Database Migrations

```python
# migrations/env.py
from alembic import context
from flask import current_app

config.set_main_option(
    'sqlalchemy.url',
    current_app.config.get('SQLALCHEMY_DATABASE_URI')
)

target_metadata = current_app.extensions['migrate'].db.metadata

# Create migration
"""add user table
Revision ID: abc123
"""
def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('user')
```

### Performance Optimization

```python
# Eager loading
books = Book.query.options(
    joinedload(Book.author)
).all()

# Pagination
page = Book.query.paginate(
    page=2, 
    per_page=20,
    error_out=False
)

# Indexing
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), index=True)
    isbn = db.Column(db.String(13), unique=True, index=True)
```

## Practical Exercises

### 1. Blog System
Build blog with:
1. Posts and comments
2. Categories and tags
3. User management
4. Search functionality
5. Admin interface

### 2. Inventory System
Create inventory with:
1. Product management
2. Stock tracking
3. Order processing
4. Supplier management
5. Reports generation

### 3. School Database
Develop system for:
1. Student records
2. Course management
3. Grade tracking
4. Attendance records
5. Report cards

## Review Questions

1. **Database Setup**
   - When use different databases?
   - How handle migrations?
   - Best practices for models?

2. **CRUD Operations**
   - How optimize queries?
   - When use relationships?
   - Best transaction practices?

3. **Advanced Concepts**
   - When use indexing?
   - How handle large datasets?
   - Best backup strategies?

## Additional Resources

### Online Tools
- Database designers
- Query optimizers
- Migration tools

### Further Reading
- SQLAlchemy documentation
- Database patterns
- Performance guides

### Video Resources
- Database tutorials
- SQLAlchemy guides
- Optimization tips

## Next Steps

After mastering these concepts, you'll be ready to:
1. Design database schemas
2. Build efficient queries
3. Manage complex data

Remember: Good database design is crucial for application performance!

## Common Questions and Answers

Q: When should I use SQLAlchemy vs raw SQL?
A: Use SQLAlchemy for most cases - it provides ORM benefits while still allowing raw SQL when needed.

Q: How do I handle database migrations?
A: Use Flask-Migrate (Alembic) to manage schema changes safely.

Q: Should I use lazy loading or eager loading?
A: Use eager loading when you know you'll need related data, lazy loading for occasional access.

## Glossary

- **ORM**: Object-Relational Mapping
- **Migration**: Schema change
- **Transaction**: Atomic operation
- **Index**: Search optimization
- **Relationship**: Table connection
- **Query**: Data request
- **Session**: Database connection
- **Model**: Data structure
- **Schema**: Database design
- **Backref**: Reverse reference

Remember: A well-designed database makes application development easier!
