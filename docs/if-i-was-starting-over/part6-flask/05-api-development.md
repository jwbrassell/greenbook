# Chapter 5: API Development

## Introduction

Think about a restaurant's ordering system - you have a menu (API documentation), waiters taking orders (endpoints), kitchen processing requests (business logic), and serving food (responses). Similarly, web APIs provide a structured way for different systems to communicate. In this chapter, we'll learn how to build RESTful APIs with Flask.

## 1. REST APIs

### The Restaurant Menu Metaphor

Think of REST APIs like a restaurant system:
- Endpoints are like menu items
- HTTP methods are like order types
- Parameters are like special requests
- Responses are like served dishes
- Status codes are like order status

### Basic API Structure

```python
from flask import Flask, jsonify, request

app = Flask(__name__)

# GET request (like viewing menu)
@app.route('/api/items', methods=['GET'])
def get_items():
    items = [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]
    return jsonify(items)

# POST request (like placing order)
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    # Process data
    return jsonify({'message': 'Item created'}), 201

# Error handling (like order problems)
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404
```

### HTTP Methods

```python
# GET - Read data
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)

# POST - Create data
@app.route('/api/items', methods=['POST'])
def create_item():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    data = request.get_json()
    # Validate data
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    # Create item
    return jsonify({'message': 'Created'}), 201

# PUT - Update data
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json()
    # Update item
    return jsonify({'message': 'Updated'})

# DELETE - Remove data
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = find_item(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    # Delete item
    return '', 204
```

### Hands-On Exercise: Restaurant API

Create a restaurant ordering API:
```python
# restaurant_api.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurant.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Models
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    available = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'category': self.category,
            'available': self.available
        }

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    table_number = db.Column(db.Integer)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'customer_name': self.customer_name,
            'table_number': self.table_number,
            'status': self.status,
            'created_at': self.created_at.isoformat(),
            'items': [item.to_dict() for item in self.items],
            'total': sum(item.quantity * item.menu_item.price 
                        for item in self.items)
        }

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), 
                            nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    special_instructions = db.Column(db.Text)
    menu_item = db.relationship('MenuItem')
    
    def to_dict(self):
        return {
            'id': self.id,
            'menu_item': self.menu_item.to_dict(),
            'quantity': self.quantity,
            'special_instructions': self.special_instructions
        }

# Create tables
with app.app_context():
    db.create_all()

# Menu Routes
@app.route('/api/menu', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    if category:
        items = MenuItem.query.filter_by(category=category, available=True).all()
    else:
        items = MenuItem.query.filter_by(available=True).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/menu/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@app.route('/api/menu', methods=['POST'])
def create_menu_item():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    # Validate required fields
    required = ['name', 'price']
    if not all(field in data for field in required):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create item
    item = MenuItem(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category=data.get('category'),
        available=data.get('available', True)
    )
    
    try:
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'Error creating item'}), 500

@app.route('/api/menu/<int:item_id>', methods=['PUT'])
def update_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    # Update fields
    if 'name' in data:
        item.name = data['name']
    if 'description' in data:
        item.description = data['description']
    if 'price' in data:
        item.price = data['price']
    if 'category' in data:
        item.category = data['category']
    if 'available' in data:
        item.available = data['available']
    
    try:
        db.session.commit()
        return jsonify(item.to_dict())
    except:
        db.session.rollback()
        return jsonify({'error': 'Error updating item'}), 500

@app.route('/api/menu/<int:item_id>', methods=['DELETE'])
def delete_menu_item(item_id):
    item = MenuItem.query.get_or_404(item_id)
    
    try:
        db.session.delete(item)
        db.session.commit()
        return '', 204
    except:
        db.session.rollback()
        return jsonify({'error': 'Error deleting item'}), 500

# Order Routes
@app.route('/api/orders', methods=['GET'])
def get_orders():
    status = request.args.get('status')
    if status:
        orders = Order.query.filter_by(status=status).all()
    else:
        orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@app.route('/api/orders', methods=['POST'])
def create_order():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    # Validate required fields
    if 'customer_name' not in data or 'items' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Create order
    order = Order(
        customer_name=data['customer_name'],
        table_number=data.get('table_number')
    )
    
    # Add items
    for item_data in data['items']:
        if 'menu_item_id' not in item_data or 'quantity' not in item_data:
            return jsonify({'error': 'Invalid item data'}), 400
            
        menu_item = MenuItem.query.get(item_data['menu_item_id'])
        if not menu_item or not menu_item.available:
            return jsonify({'error': f'Item {item_data["menu_item_id"]} not available'}), 400
            
        order_item = OrderItem(
            menu_item=menu_item,
            quantity=item_data['quantity'],
            special_instructions=item_data.get('special_instructions')
        )
        order.items.append(order_item)
    
    try:
        db.session.add(order)
        db.session.commit()
        return jsonify(order.to_dict()), 201
    except:
        db.session.rollback()
        return jsonify({'error': 'Error creating order'}), 500

@app.route('/api/orders/<int:order_id>', methods=['PUT'])
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
        
    data = request.get_json()
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
        
    valid_statuses = ['pending', 'preparing', 'ready', 'delivered', 'cancelled']
    if data['status'] not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    order.status = data['status']
    
    try:
        db.session.commit()
        return jsonify(order.to_dict())
    except:
        db.session.rollback()
        return jsonify({'error': 'Error updating order'}), 500

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## 2. Request Handling

### The Order Processing Metaphor

Think of request handling like processing orders:
- Validation like checking order details
- Processing like preparing food
- Response like serving dishes
- Errors like order problems
- Status codes like order status

### Request Data

```python
# Query parameters
@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    limit = request.args.get('limit', 10, type=int)
    return jsonify({'results': search_items(query, limit)})

# JSON data
@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    return jsonify({'id': create_item(name, price)})

# Form data
@app.route('/api/upload', methods=['POST'])
def upload():
    file = request.files['file']
    description = request.form.get('description')
    return jsonify({'message': 'Uploaded'})

# Headers
@app.route('/api/secure')
def secure():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token'}), 401
```

### Response Formatting

```python
# Basic response
@app.route('/api/item/<int:id>')
def get_item(id):
    return jsonify({
        'id': id,
        'name': 'Item name',
        'price': 9.99
    })

# Status codes
@app.route('/api/create', methods=['POST'])
def create():
    return jsonify({'message': 'Created'}), 201

# Headers
@app.route('/api/download')
def download():
    response = jsonify({'data': 'content'})
    response.headers['Content-Type'] = 'application/json'
    return response

# Errors
@app.route('/api/error')
def error():
    return jsonify({
        'error': 'Not found',
        'message': 'Item does not exist'
    }), 404
```

### Hands-On Exercise: API Wrapper

Create an API wrapper for external service:
```python
# api_wrapper.py
from flask import Flask, jsonify, request
import requests
from functools import wraps

app = Flask(__name__)

# Configuration
WEATHER_API_KEY = 'your-api-key'
WEATHER_API_URL = 'https://api.weatherapi.com/v1'

# Decorator for API key validation
def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({'error': 'API key required'}), 401
        if not validate_api_key(api_key):
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated

# Utility functions
def validate_api_key(key):
    # In real app, check against database
    return True

def format_weather(data):
    return {
        'location': {
            'city': data['location']['name'],
            'country': data['location']['country']
        },
        'temperature': {
            'celsius': data['current']['temp_c'],
            'fahrenheit': data['current']['temp_f']
        },
        'condition': {
            'text': data['current']['condition']['text'],
            'icon': data['current']['condition']['icon']
        },
        'wind': {
            'speed': data['current']['wind_kph'],
            'direction': data['current']['wind_dir']
        },
        'humidity': data['current']['humidity'],
        'updated': data['current']['last_updated']
    }

# Routes
@app.route('/api/weather/current')
@require_api_key
def get_current_weather():
    # Get parameters
    city = request.args.get('city')
    if not city:
        return jsonify({'error': 'City parameter required'}), 400
    
    try:
        # Make API request
        response = requests.get(
            f'{WEATHER_API_URL}/current.json',
            params={
                'key': WEATHER_API_KEY,
                'q': city
            }
        )
        
        # Check response
        response.raise_for_status()
        data = response.json()
        
        # Format and return data
        return jsonify(format_weather(data))
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Weather service error'}), 503

@app.route('/api/weather/forecast')
@require_api_key
def get_weather_forecast():
    # Get parameters
    city = request.args.get('city')
    days = request.args.get('days', 3, type=int)
    
    if not city:
        return jsonify({'error': 'City parameter required'}), 400
    
    if not 1 <= days <= 7:
        return jsonify({'error': 'Days must be between 1 and 7'}), 400
    
    try:
        # Make API request
        response = requests.get(
            f'{WEATHER_API_URL}/forecast.json',
            params={
                'key': WEATHER_API_KEY,
                'q': city,
                'days': days
            }
        )
        
        # Check response
        response.raise_for_status()
        data = response.json()
        
        # Format forecast data
        forecast = []
        for day in data['forecast']['forecastday']:
            forecast.append({
                'date': day['date'],
                'temperature': {
                    'max': day['day']['maxtemp_c'],
                    'min': day['day']['mintemp_c']
                },
                'condition': {
                    'text': day['day']['condition']['text'],
                    'icon': day['day']['condition']['icon']
                },
                'chance_of_rain': day['day']['daily_chance_of_rain'],
                'humidity': day['day']['avghumidity']
            })
        
        return jsonify({
            'location': {
                'city': data['location']['name'],
                'country': data['location']['country']
            },
            'forecast': forecast
        })
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Weather service error'}), 503

@app.route('/api/weather/search')
@require_api_key
def search_locations():
    # Get parameters
    query = request.args.get('q')
    if not query:
        return jsonify({'error': 'Query parameter required'}), 400
    
    try:
        # Make API request
        response = requests.get(
            f'{WEATHER_API_URL}/search.json',
            params={
                'key': WEATHER_API_KEY,
                'q': query
            }
        )
        
        # Check response
        response.raise_for_status()
        data = response.json()
        
        # Format locations
        locations = [{
            'name': location['name'],
            'region': location['region'],
            'country': location['country'],
            'lat': location['lat'],
            'lon': location['lon']
        } for location in data]
        
        return jsonify(locations)
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': 'Weather service error'}), 503

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

## 3. API Documentation

### The Menu Design Metaphor

Think of API documentation like designing a menu:
- Endpoints like menu sections
- Parameters like dish options
- Examples like food photos
- Responses like dish descriptions
- Errors like allergen warnings

### Swagger/OpenAPI

```python
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'

swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Sample API"
    }
)

app.register_blueprint(swagger_blueprint, url_prefix=SWAGGER_URL)
```

```json
// static/swagger.json
{
  "openapi": "3.0.0",
  "info": {
    "title": "Sample API",
    "version": "1.0.0"
  },
  "paths": {
    "/api/items": {
      "get": {
        "summary": "Get all items",
        "responses": {
          "200": {
            "description": "List of items",
            "content": {
              "application/json": {
                "schema": {
                  "type": "array",
                  "items": {
                    "$ref": "#/components/schemas/Item"
                  }
                }
              }
            }
          }
        }
      }
    }
  },
  "components": {
    "schemas": {
      "Item": {
        "type": "object",
        "properties": {
          "id": {
            "type": "integer"
          },
          "name": {
            "type": "string"
          }
        }
      }
    }
  }
}
```

### API Documentation Example

Create documented API:
```python
# documented_api.py
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/api/items', methods=['GET'])
@swag_from({
    'tags': ['Items'],
    'summary': 'Get all items',
    'parameters': [
        {
            'name': 'category',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Filter by category'
        }
    ],
    'responses': {
        200: {
            'description': 'List of items',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'category': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def get_items():
    """
    Get all items
    This endpoint returns a list of all items, optionally filtered by category
    """
    category = request.args.get('category')
    items = [
        {'id': 1, 'name': 'Item 1', 'category': 'A'},
        {'id': 2, 'name': 'Item 2', 'category': 'B'}
    ]
    if category:
        items = [item for item in items if item['category'] == category]
    return jsonify(items)

@app.route('/api/items/<int:item_id>', methods=['GET'])
@swag_from({
    'tags': ['Items'],
    'summary': 'Get item by ID',
    'parameters': [
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID of item to get'
        }
    ],
    'responses': {
        200: {
            'description': 'Item details',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'category': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Item not found'
        }
    }
})
def get_item(item_id):
    """
    Get item by ID
    This endpoint returns the details of a specific item
    """
    items = {
        1: {'id': 1, 'name': 'Item 1', 'category': 'A'},
        2: {'id': 2, 'name': 'Item 2', 'category': 'B'}
    }
    item = items.get(item_id)
    if item is None:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)

@app.route('/api/items', methods=['POST'])
@swag_from({
    'tags': ['Items'],
    'summary': 'Create new item',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'category': {'type': 'string'}
                },
                'required': ['name']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Item created',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'category': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid input'
        }
    }
})
def create_item():
    """
    Create new item
    This endpoint creates a new item with the provided details
    """
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400
    
    data = request.get_json()
    if 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    new_item = {
        'id': 3,  # In real app, generate new ID
        'name': data['name'],
        'category': data.get('category', 'default')
    }
    
    return jsonify(new_item), 201

if __name__ == '__main__':
    app.run(debug=True)
```

## Practical Exercises

### 1. Blog API
Build API with:
1. Post management
2. User authentication
3. Comments system
4. Category filtering
5. Search functionality

### 2. File API
Create API for:
1. File upload
2. Download handling
3. Format conversion
4. Metadata extraction
5. Access control

### 3. Analytics API
Develop API with:
1. Data collection
2. Aggregation
3. Filtering
4. Export options
5. Visualization data

## Review Questions

1. **REST Basics**
   - When use different methods?
   - How handle resources?
   - Best practices for URLs?

2. **Request Handling**
   - How validate input?
   - When use status codes?
   - Best practices for responses?

3. **Documentation**
   - How document endpoints?
   - When use examples?
   - Best practices for specs?

## Additional Resources

### Online Tools
- API testers
- Documentation generators
- Schema validators

### Further Reading
- REST principles
- API design patterns
- Documentation standards

### Video Resources
- API tutorials
- REST guides
- Documentation examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Design RESTful APIs
2. Handle complex requests
3. Document effectively

Remember: Good APIs are easy to understand and use!

## Common Questions and Answers

Q: When should I version my API?
A: Version from the start using URL prefixes or headers.

Q: How do I handle pagination?
A: Use limit/offset or page/size parameters with metadata.

Q: Should I use authentication?
A: Yes, for any non-public API endpoints.

## Glossary

- **REST**: Representational State Transfer
- **Endpoint**: API URL
- **Resource**: Data entity
- **Method**: HTTP verb
- **Parameter**: Input data
- **Response**: Output data
- **Status**: HTTP code
- **Header**: Meta information
- **Payload**: Request/response body
- **Documentation**: API specification

Remember: APIs should be consistent, predictable, and well-documented!
