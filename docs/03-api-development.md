# Module 3: API Development

## Table of Contents
- [Module 3: API Development](#module-3:-api-development)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [RESTful API Design](#restful-api-design)
    - [PHP File-based Approach vs Flask API](#php-file-based-approach-vs-flask-api)
    - [Flask RESTful Approach](#flask-restful-approach)
- [GET endpoint](#get-endpoint)
- [POST endpoint](#post-endpoint)
  - [API Structure](#api-structure)
    - [Basic REST Endpoints](#basic-rest-endpoints)
- [models.py](#modelspy)
- [routes.py](#routespy)
  - [Error Handling](#error-handling)
  - [Request Validation](#request-validation)
  - [Authentication](#authentication)
  - [Rate Limiting](#rate-limiting)
  - [API Documentation with Swagger/OpenAPI](#api-documentation-with-swagger/openapi)
  - [Consuming APIs](#consuming-apis)
    - [Making API Requests](#making-api-requests)
- [GET request](#get-request)
- [POST request](#post-request)
- [PUT request](#put-request)
- [DELETE request](#delete-request)
  - [Best Practices](#best-practices)
  - [Exercise: Converting File-based System to API](#exercise:-converting-file-based-system-to-api)
  - [Common Pitfalls](#common-pitfalls)
  - [Next Steps](#next-steps)
  - [Additional Resources](#additional-resources)



## Introduction

This module covers building and consuming APIs with Flask, focusing on RESTful design principles and best practices. We'll explore how to create robust APIs that can replace traditional file-based data sharing methods.

## RESTful API Design

### PHP File-based Approach vs Flask API
```php
// PHP (old way)
<?php
// save-data.php
$data = $_POST;
file_put_contents('data.json', json_encode($data));

// get-data.php
echo json_encode(json_decode(file_get_contents('data.json')));
?>
```

### Flask RESTful Approach
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

# GET endpoint
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

# POST endpoint
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

## API Structure

### Basic REST Endpoints
```python
# models.py
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }

# routes.py
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    for key, value in data.items():
        setattr(user, key, value)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
```

## Error Handling

```python
from flask import jsonify
from werkzeug.exceptions import HTTPException

@app.errorhandler(HTTPException)
def handle_exception(e):
    response = {
        "error": {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    }
    return jsonify(response), e.code

class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    response = {
        "error": {
            "code": error.status_code,
            "message": error.message
        }
    }
    return jsonify(response), error.status_code
```

## Request Validation

```python
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

@app.route('/api/users', methods=['POST'])
def create_user():
    form = UserForm(data=request.get_json())
    if not form.validate():
        return jsonify({"errors": form.errors}), 400
    
    user = User(
        username=form.username.data,
        email=form.email.data
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201
```

## Authentication

```python
from functools import wraps
from flask import request, jsonify
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])
        except:
            return jsonify({'message': 'Token is invalid'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/api/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    return jsonify({'message': f'Hello {current_user.username}'})
```

## Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/users', methods=['GET'])
@limiter.limit("1 per second")
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
```

## API Documentation with Swagger/OpenAPI

```python
from flask_restx import Api, Resource, fields

api = Api(app, version='1.0', title='User API', description='A simple user API')
ns = api.namespace('users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readonly=True),
    'username': fields.String(required=True),
    'email': fields.String(required=True)
})

@ns.route('/')
class UserList(Resource):
    @ns.doc('list_users')
    @ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        return User.query.all()

    @ns.doc('create_user')
    @ns.expect(user_model)
    @ns.marshal_with(user_model, code=201)
    def post(self):
        """Create a new user"""
        data = api.payload
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user, 201
```

## Consuming APIs

### Making API Requests
```python
import requests

# GET request
response = requests.get('http://api.example.com/users')
users = response.json()

# POST request
data = {'username': 'john_doe', 'email': 'john@example.com'}
response = requests.post('http://api.example.com/users', json=data)
new_user = response.json()

# PUT request
user_id = 1
data = {'username': 'jane_doe'}
response = requests.put(f'http://api.example.com/users/{user_id}', json=data)
updated_user = response.json()

# DELETE request
user_id = 1
response = requests.delete(f'http://api.example.com/users/{user_id}')
```

## Best Practices

1. **Use Proper HTTP Methods**
   - GET: Retrieve data
   - POST: Create new resources
   - PUT/PATCH: Update existing resources
   - DELETE: Remove resources

2. **Return Appropriate Status Codes**
   - 200: Success
   - 201: Created
   - 400: Bad Request
   - 401: Unauthorized
   - 403: Forbidden
   - 404: Not Found
   - 500: Server Error

3. **Version Your API**
```python
@app.route('/api/v1/users')
def get_users_v1():
    # Version 1 implementation
    pass

@app.route('/api/v2/users')
def get_users_v2():
    # Version 2 implementation
    pass
```

4. **Implement Pagination**
```python
@app.route('/api/users')
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    pagination = User.query.paginate(page=page, per_page=per_page)
    users = pagination.items
    
    return jsonify({
        'users': [user.to_dict() for user in users],
        'meta': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    })
```

## Exercise: Converting File-based System to API

1. Start with this PHP file:
```php
// data.php
<?php
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $data = $_POST;
    file_put_contents('data.json', json_encode($data));
    echo json_encode(['status' => 'success']);
} else {
    echo file_get_contents('data.json');
}
?>
```

2. Convert to Flask API:
```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.JSON)

@app.route('/api/data', methods=['GET', 'POST'])
def handle_data():
    if request.method == 'POST':
        data_entry = Data(content=request.get_json())
        db.session.add(data_entry)
        db.session.commit()
        return jsonify({'status': 'success'})
    else:
        data = Data.query.order_by(Data.id.desc()).first()
        return jsonify(data.content if data else {})
```

## Common Pitfalls

1. **Not Validating Input**
   - Always validate request data
   - Use form validation or schema validation

2. **Poor Error Handling**
   - Implement proper error handlers
   - Return meaningful error messages

3. **Security Issues**
   - Implement authentication
   - Use HTTPS
   - Validate input
   - Implement rate limiting

4. **Performance**
   - Implement caching
   - Use pagination
   - Optimize database queries

## Next Steps

1. Complete the exercise above
2. Implement authentication in your API
3. Add documentation using Swagger/OpenAPI
4. Implement rate limiting
5. Move on to Module 4: Authentication & Security

## Additional Resources

- [Flask-RESTX Documentation](https://flask-restx.readthedocs.io/)
- [Flask-Limiter Documentation](https://flask-limiter.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [REST API Best Practices](https://restfulapi.net/)
