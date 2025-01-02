# Python Commands and Examples Reference

###### tags: `python`, `flask`, `sqlalchemy`, `database`, `web`, `api`, `orm`, `authentication`, `forms`, `caching`, `sessions`, `security`, `aws`, `boto3`, `socketio`, `realtime`

## Table of Contents
- [Python Commands and Examples Reference](#python-commands-and-examples-reference)
          - [tags: python, flask, sqlalchemy, database, web, api, orm, authentication, forms, caching, sessions, security, aws, boto3, socketio, realtime](#tags:-python,-flask,-sqlalchemy,-database,-web,-api,-orm,-authentication,-forms,-caching,-sessions,-security,-aws,-boto3,-socketio,-realtime)
  - [Table of Contents](#table-of-contents)
  - [Virtual Environment](#virtual-environment)
          - [tags: venv, virtualenv, pip, environment](#tags:-venv,-virtualenv,-pip,-environment)
- [Create virtual environment](#create-virtual-environment)
- [Activate virtual environment](#activate-virtual-environment)
- [Windows](#windows)
- [Unix/MacOS](#unix/macos)
- [Deactivate virtual environment](#deactivate-virtual-environment)
- [Install requirements](#install-requirements)
- [Generate requirements](#generate-requirements)
  - [Flask Commands](#flask-commands)
          - [tags: flask, web, server, routes, development](#tags:-flask,-web,-server,-routes,-development)
- [Run Flask development server](#run-flask-development-server)
- [Enable debug mode](#enable-debug-mode)
- [Show routes](#show-routes)
- [Create app instance](#create-app-instance)
- [Basic route](#basic-route)
- [Route with parameters](#route-with-parameters)
- [HTTP methods](#http-methods)
  - [Database Operations](#database-operations)
          - [tags: database, sqlalchemy, orm, migrations, alembic, crud](#tags:-database,-sqlalchemy,-orm,-migrations,-alembic,-crud)
- [Initialize database](#initialize-database)
- [Define model](#define-model)
- [Create tables](#create-tables)
- [Database migrations](#database-migrations)
- [Basic CRUD operations](#basic-crud-operations)
- [Create](#create)
- [Read](#read)
- [Update](#update)
- [Delete](#delete)
- [Complex queries](#complex-queries)
  - [File Operations](#file-operations)
          - [tags: files, io, read, write, json, csv, excel](#tags:-files,-io,-read,-write,-json,-csv,-excel)
- [Read file](#read-file)
- [Write file](#write-file)
- [JSON operations](#json-operations)
- [Read JSON](#read-json)
- [Write JSON](#write-json)
- [CSV operations](#csv-operations)
- [Read CSV](#read-csv)
- [Write CSV](#write-csv)
  - [AWS Operations](#aws-operations)
          - [tags: aws, boto3, s3, sqs, sns, cloud](#tags:-aws,-boto3,-s3,-sqs,-sns,-cloud)
- [S3 operations](#s3-operations)
- [Upload file](#upload-file)
- [Download file](#download-file)
- [List buckets](#list-buckets)
- [SQS operations](#sqs-operations)
- [Send message](#send-message)
- [Receive messages](#receive-messages)
  - [Security Operations](#security-operations)
          - [tags: security, authentication, encryption, hashing, csrf](#tags:-security,-authentication,-encryption,-hashing,-csrf)
- [Password hashing](#password-hashing)
- [Flask-Login](#flask-login)
- [CSRF protection](#csrf-protection)
- [Generate token](#generate-token)
  - [Testing Commands](#testing-commands)
          - [tags: testing, pytest, unittest, coverage](#tags:-testing,-pytest,-unittest,-coverage)
- [Run tests](#run-tests)
- [Coverage](#coverage)
- [Unittest](#unittest)
- [Flask testing](#flask-testing)
  - [Package Management](#package-management)
          - [tags: pip, packages, dependencies, requirements](#tags:-pip,-packages,-dependencies,-requirements)
- [Install package](#install-package)
- [Uninstall package](#uninstall-package)
- [List packages](#list-packages)
- [Update package](#update-package)
- [Install development packages](#install-development-packages)
  - [Common Patterns](#common-patterns)
          - [tags: patterns, decorators, context-managers, generators](#tags:-patterns,-decorators,-context-managers,-generators)
- [Decorator](#decorator)
- [Context manager](#context-manager)
- [Generator](#generator)
  - [Error Handling](#error-handling)
          - [tags: errors, exceptions, try-except, debugging](#tags:-errors,-exceptions,-try-except,-debugging)
- [Basic try-except](#basic-try-except)
- [Multiple exceptions](#multiple-exceptions)
- [Custom exception](#custom-exception)
- [Context manager with error handling](#context-manager-with-error-handling)
  - [Debugging](#debugging)
          - [tags: debug, pdb, logging, troubleshooting](#tags:-debug,-pdb,-logging,-troubleshooting)
- [PDB debugger](#pdb-debugger)
- [Logging](#logging)
- [Print debugging](#print-debugging)

## Virtual Environment
###### tags: `venv`, `virtualenv`, `pip`, `environment`

```python
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install requirements
pip install -r requirements.txt

# Generate requirements
pip freeze > requirements.txt
```

## Flask Commands
###### tags: `flask`, `web`, `server`, `routes`, `development`

```python
# Run Flask development server
flask run
flask run --host=0.0.0.0 --port=5000

# Enable debug mode
export FLASK_DEBUG=1
flask run

# Show routes
flask routes

# Create app instance
from flask import Flask
app = Flask(__name__)

# Basic route
@app.route('/')
def index():
    return 'Hello World'

# Route with parameters
@app.route('/user/<username>')
def user_profile(username):
    return f'Profile: {username}'

# HTTP methods
@app.route('/post', methods=['GET', 'POST'])
def handle_post():
    if request.method == 'POST':
        return 'Handle POST'
    return 'Handle GET'
```

## Database Operations
###### tags: `database`, `sqlalchemy`, `orm`, `migrations`, `alembic`, `crud`

```python
# Initialize database
db = SQLAlchemy(app)

# Define model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)

# Create tables
db.create_all()

# Database migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask db downgrade

# Basic CRUD operations
# Create
user = User(username='john')
db.session.add(user)
db.session.commit()

# Read
user = User.query.get(1)
users = User.query.all()
user = User.query.filter_by(username='john').first()

# Update
user.username = 'john_doe'
db.session.commit()

# Delete
db.session.delete(user)
db.session.commit()

# Complex queries
users = User.query.filter(User.age > 18).order_by(User.username).all()
users = db.session.query(User).join(Post).filter(Post.published == True).all()
```

## File Operations
###### tags: `files`, `io`, `read`, `write`, `json`, `csv`, `excel`

```python
# Read file
with open('file.txt', 'r') as f:
    content = f.read()

# Write file
with open('file.txt', 'w') as f:
    f.write('content')

# JSON operations
import json

# Read JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Write JSON
with open('data.json', 'w') as f:
    json.dump(data, f, indent=4)

# CSV operations
import csv

# Read CSV
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)

# Write CSV
with open('data.csv', 'w') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerow({'name': 'John', 'age': 30})
```

## AWS Operations
###### tags: `aws`, `boto3`, `s3`, `sqs`, `sns`, `cloud`

```python
# S3 operations
import boto3

# Upload file
s3 = boto3.client('s3')
s3.upload_file('file.txt', 'bucket-name', 'file.txt')

# Download file
s3.download_file('bucket-name', 'file.txt', 'downloaded.txt')

# List buckets
response = s3.list_buckets()
buckets = [bucket['Name'] for bucket in response['Buckets']]

# SQS operations
sqs = boto3.client('sqs')

# Send message
response = sqs.send_message(
    QueueUrl='queue-url',
    MessageBody='message'
)

# Receive messages
response = sqs.receive_message(
    QueueUrl='queue-url',
    MaxNumberOfMessages=10
)
```

## Security Operations
###### tags: `security`, `authentication`, `encryption`, `hashing`, `csrf`

```python
# Password hashing
from werkzeug.security import generate_password_hash, check_password_hash

password_hash = generate_password_hash('password123')
is_valid = check_password_hash(password_hash, 'password123')

# Flask-Login
from flask_login import LoginManager, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# CSRF protection
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Generate token
from secrets import token_urlsafe
token = token_urlsafe(32)
```

## Testing Commands
###### tags: `testing`, `pytest`, `unittest`, `coverage`

```python
# Run tests
pytest
pytest test_file.py
pytest -v  # verbose
pytest -k "test_name"  # run specific test

# Coverage
coverage run -m pytest
coverage report
coverage html

# Unittest
python -m unittest
python -m unittest test_file.py
python -m unittest discover

# Flask testing
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
```

## Package Management
###### tags: `pip`, `packages`, `dependencies`, `requirements`

```python
# Install package
pip install package_name
pip install package_name==1.0.0

# Uninstall package
pip uninstall package_name

# List packages
pip list
pip freeze

# Update package
pip install --upgrade package_name

# Install development packages
pip install -e .
```

## Common Patterns
###### tags: `patterns`, `decorators`, `context-managers`, `generators`

```python
# Decorator
def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        print(f"Time: {time.time() - start}")
        return result
    return wrapper

# Context manager
class FileManager:
    def __init__(self, filename):
        self.filename = filename
        
    def __enter__(self):
        self.file = open(self.filename, 'r')
        return self.file
        
    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()

# Generator
def number_generator(n):
    for i in range(n):
        yield i
```

## Error Handling
###### tags: `errors`, `exceptions`, `try-except`, `debugging`

```python
# Basic try-except
try:
    result = 1 / 0
except ZeroDivisionError as e:
    print(f"Error: {e}")

# Multiple exceptions
try:
    # code
except (TypeError, ValueError) as e:
    print(f"Error: {e}")
finally:
    # cleanup code

# Custom exception
class CustomError(Exception):
    pass

# Context manager with error handling
from contextlib import contextmanager

@contextmanager
def managed_resource():
    try:
        yield resource
    finally:
        resource.cleanup()
```

## Debugging
###### tags: `debug`, `pdb`, `logging`, `troubleshooting`

```python
# PDB debugger
import pdb; pdb.set_trace()

# Logging
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")

# Print debugging
print(f"Variable: {var}")
print("Debug:", var)
