# DataTables with Python/Flask Examples

## Table of Contents
- [DataTables with Python/Flask Examples](#datatables-with-pythonflask-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Examples](#basic-examples)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Tables
   - Client-side processing
   - Server-side processing
   - AJAX data loading
   - Custom column rendering

2. Advanced Features
   - Row selection
   - Inline editing
   - Custom filtering
   - Export functionality

3. Data Integration
   - SQLAlchemy integration
   - REST API endpoints
   - Real-time updates
   - CSV/Excel import/export

4. Full Applications
   - Admin dashboard
   - Data management system
   - Reporting interface
   - Analytics platform

## Project Structure

```
python/
├── basic/
│   ├── client_side/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── templates/
│   │       └── index.html
│   └── server_side/
│       ├── app.py
│       ├── requirements.txt
│       └── templates/
│           └── index.html
├── advanced/
│   ├── row_selection/
│   ├── inline_editing/
│   ├── custom_filtering/
│   └── export/
├── integration/
│   ├── sqlalchemy/
│   ├── rest_api/
│   ├── realtime/
│   └── import_export/
└── applications/
    ├── admin_dashboard/
    ├── data_management/
    ├── reporting/
    └── analytics/
```

## Getting Started

1. Setup Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Run Example:
```bash
cd basic/server_side
python app.py
```

## Basic Examples

### Server-side Processing
```python
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    role = db.Column(db.String(50))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # Get DataTables parameters
    draw = request.args.get('draw', type=int)
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    search_value = request.args.get('search[value]')
    
    # Base query
    query = User.query
    
    # Apply search
    if search_value:
        query = query.filter(or_(
            User.name.like(f'%{search_value}%'),
            User.email.like(f'%{search_value}%'),
            User.role.like(f'%{search_value}%')
        ))
    
    # Get total records
    total_records = query.count()
    
    # Apply pagination
    query = query.offset(start).limit(length)
    
    # Format data for DataTables
    data = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'actions': f'<button onclick="editUser({user.id})">Edit</button>'
    } for user in query.all()]
    
    return jsonify({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True)
```

### Template with DataTables
```html
<!-- templates/index.html -->
<!DOCTYPE html>
<html>
<head>
    <title>DataTables Example</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/buttons/2.2.2/css/buttons.dataTables.min.css">
</head>
<body>
    <table id="dataTable" class="display">
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Actions</th>
            </tr>
        </thead>
    </table>

    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script type="text/javascript" src="https://cdn.datatables.net/buttons/2.2.2/js/dataTables.buttons.min.js"></script>
    
    <script>
        $(document).ready(function() {
            $('#dataTable').DataTable({
                processing: true,
                serverSide: true,
                ajax: '/api/data',
                columns: [
                    { data: 'id' },
                    { data: 'name' },
                    { data: 'email' },
                    { data: 'role' },
                    { 
                        data: 'actions',
                        orderable: false,
                        searchable: false
                    }
                ]
            });
        });
    </script>
</body>
</html>
```

## Advanced Features

### Inline Editing
```python
@app.route('/api/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    
    db.session.commit()
    return jsonify({'status': 'success'})
```

### Custom Filtering
```python
@app.route('/api/data')
def get_filtered_data():
    role_filter = request.args.get('role')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    
    query = User.query
    
    if role_filter:
        query = query.filter(User.role == role_filter)
    
    if date_from and date_to:
        query = query.filter(User.created_at.between(date_from, date_to))
    
    # ... rest of the processing
```

## Security Considerations

1. Input Validation:
```python
from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    role = fields.Str(validate=validate.OneOf(['admin', 'user', 'guest']))

@app.route('/api/user', methods=['POST'])
def create_user():
    schema = UserSchema()
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400
    
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 'success'})
```

2. CSRF Protection:
```python
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'your-secret-key'

# In template
<meta name="csrf-token" content="{{ csrf_token() }}">

# In JavaScript
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

## Performance Optimization

1. Query Optimization:
```python
from sqlalchemy import func

def get_optimized_data():
    # Use select_from for complex joins
    query = db.session.query(
        User,
        func.count(Order.id).label('order_count')
    ).select_from(User).outerjoin(Order)
    
    # Add indexes
    if not has_index('users', 'email'):
        db.engine.execute('CREATE INDEX idx_users_email ON users(email)')
    
    # Use pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    return query.paginate(page=page, per_page=per_page)
```

2. Caching:
```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/stats')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_stats():
    return compute_expensive_stats()
```

## Testing

1. Unit Tests:
```python
import unittest
from app import app, db

class DataTablesTest(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        db.create_all()
    
    def test_api_response(self):
        response = self.client.get('/api/data?draw=1&start=0&length=10')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', data)
        self.assertIn('recordsTotal', data)
```

2. Integration Tests:
```python
def test_data_workflow():
    # Create test user
    response = self.client.post('/api/user', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'user'
    })
    self.assertEqual(response.status_code, 200)
    
    # Verify in DataTables response
    response = self.client.get('/api/data')
    data = response.get_json()
    self.assertTrue(any(
        d['email'] == 'test@example.com' 
        for d in data['data']
    ))
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
