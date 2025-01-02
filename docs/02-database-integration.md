# Module 2: Database Integration

## Table of Contents
- [Module 2: Database Integration](#module-2:-database-integration)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [File-based Storage vs Database Comparison](#file-based-storage-vs-database-comparison)
    - [PHP File-based Approach](#php-file-based-approach)
    - [Flask SQLAlchemy Approach](#flask-sqlalchemy-approach)
- [Creating a user](#creating-a-user)
- [Reading users](#reading-users)
  - [Setting Up Database Integration](#setting-up-database-integration)
    - [1. Install Required Packages](#1-install-required-packages)
    - [2. Configure Database](#2-configure-database)
- [config.py](#configpy)
- [app.py](#apppy)
    - [3. Create Models](#3-create-models)
- [models.py](#modelspy)
  - [Database Operations](#database-operations)
    - [Creating Records](#creating-records)
- [PHP Way (File-based)](#php-way-file-based)
- [Flask SQLAlchemy Way](#flask-sqlalchemy-way)
    - [Reading Records](#reading-records)
- [Basic Queries](#basic-queries)
- [Advanced Queries](#advanced-queries)
- [Users with posts](#users-with-posts)
- [Users with specific conditions](#users-with-specific-conditions)
    - [Updating Records](#updating-records)
    - [Deleting Records](#deleting-records)
  - [Database Migrations with Alembic](#database-migrations-with-alembic)
    - [Initialize Migrations](#initialize-migrations)
    - [Create a Migration](#create-a-migration)
    - [Apply Migration](#apply-migration)
    - [Rollback Migration](#rollback-migration)
  - [Connection Pooling](#connection-pooling)
  - [Best Practices](#best-practices)
- [config.py](#configpy)
- [Add repr for debugging](#add-repr-for-debugging)
- [Add helper methods](#add-helper-methods)
  - [Exercise: Converting File-based Storage to Database](#exercise:-converting-file-based-storage-to-database)
- [models.py](#modelspy)
- [migration script](#migration-script)
  - [Common Pitfalls](#common-pitfalls)
  - [Next Steps](#next-steps)
  - [Additional Resources](#additional-resources)



## Introduction

This module covers the transition from file-based storage (common in PHP environments) to proper database management using SQLAlchemy ORM in Flask. We'll explore how to structure data models and perform database operations efficiently.

## File-based Storage vs Database Comparison

### PHP File-based Approach
```php
// PHP file-based storage
$data = [
    'id' => 1,
    'name' => 'John Doe',
    'email' => 'john@example.com'
];
file_put_contents('users.json', json_encode($data));

// Reading data
$users = json_decode(file_get_contents('users.json'), true);
```

### Flask SQLAlchemy Approach
```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Creating a user
new_user = User(name='John Doe', email='john@example.com')
db.session.add(new_user)
db.session.commit()

# Reading users
users = User.query.all()
```

## Setting Up Database Integration

### 1. Install Required Packages
```bash
pip install flask-sqlalchemy flask-migrate
```

### 2. Configure Database
```python
# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/dbname'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

### 3. Create Models
```python
# models.py
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
```

## Database Operations

### Creating Records
```python
# PHP Way (File-based)
$user = [
    'username' => 'john_doe',
    'email' => 'john@example.com'
];
$users = json_decode(file_get_contents('users.json'), true);
$users[] = $user;
file_put_contents('users.json', json_encode($users));

# Flask SQLAlchemy Way
@app.route('/create_user', methods=['POST'])
def create_user():
    user = User(
        username=request.form['username'],
        email=request.form['email']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})
```

### Reading Records
```python
# Basic Queries
users = User.query.all()  # Get all users
user = User.query.get(1)  # Get by primary key
user = User.query.filter_by(username='john_doe').first()  # Get by condition

# Advanced Queries
# Users with posts
users = User.query.join(Post).all()

# Users with specific conditions
users = User.query.filter(
    User.email.endswith('@example.com')
).order_by(User.username).all()
```

### Updating Records
```python
user = User.query.get(1)
user.username = 'new_username'
db.session.commit()
```

### Deleting Records
```python
user = User.query.get(1)
db.session.delete(user)
db.session.commit()
```

## Database Migrations with Alembic

### Initialize Migrations
```bash
flask db init
```

### Create a Migration
```bash
flask db migrate -m "Create users table"
```

### Apply Migration
```bash
flask db upgrade
```

### Rollback Migration
```bash
flask db downgrade
```

## Connection Pooling

SQLAlchemy handles connection pooling automatically. Configure pool settings in your database URI:

```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/dbname?pool_size=10&pool_recycle=3600'
```

## Best Practices

1. **Use Environment Variables**
```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

2. **Implement Models Properly**
```python
class User(db.Model):
    __tablename__ = 'users'  # Explicitly name your tables
    
    # Add repr for debugging
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Add helper methods
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
```

3. **Use Context Managers for Sessions**
```python
def create_user(username, email):
    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e
```

## Exercise: Converting File-based Storage to Database

1. Start with this PHP-style data storage:
```php
// users.json
{
    "users": [
        {
            "id": 1,
            "username": "john_doe",
            "email": "john@example.com"
        }
    ]
}
```

2. Convert to Flask-SQLAlchemy:
```python
# models.py
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

# migration script
def migrate_from_json():
    with open('users.json') as f:
        data = json.load(f)
        for user_data in data['users']:
            user = User(**user_data)
            db.session.add(user)
        db.session.commit()
```

## Common Pitfalls

1. **Not Handling Sessions Properly**
   - Always commit or rollback sessions
   - Use try/except blocks for database operations

2. **N+1 Query Problem**
   - Use `joinedload()` for related data
   - Implement proper relationships

3. **Connection Management**
   - Don't create new connections for each request
   - Use connection pooling
   - Configure pool recycling

4. **Security**
   - Never store passwords in plain text
   - Use parameterized queries (SQLAlchemy handles this)
   - Sanitize input data

## Next Steps

1. Complete the exercise above
2. Experiment with different relationship types
3. Try implementing complex queries
4. Practice database migrations
5. Move on to Module 3: API Development

## Additional Resources

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Database Design Patterns](https://docs.sqlalchemy.org/en/14/orm/patterns.html)
