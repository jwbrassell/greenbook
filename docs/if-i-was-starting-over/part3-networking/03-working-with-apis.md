# Chapter 3: Working with APIs

## Introduction

Think about using a vending machine: you insert money (authentication), press specific buttons (make a request), and receive your item (get a response). APIs work similarly - they're interfaces that let you interact with services in standardized ways. In this chapter, we'll explore how to work with APIs, using familiar real-world examples to understand these interactions.

## 1. API Fundamentals

### The Restaurant Menu Metaphor

Think of APIs like restaurant menus:
- Menu lists available items (API documentation)
- Each item has a description (endpoint documentation)
- Prices are listed (rate limits/costs)
- Ordering instructions provided (authentication requirements)
- Modifications allowed (parameters)

### REST API Concepts

```
REST Principles:
1. Resources (Nouns)
   Like menu categories:
   /users
   /products
   /orders

2. Methods (Verbs)
   Like ordering actions:
   GET: Read menu
   POST: Place order
   PUT: Modify order
   DELETE: Cancel order

3. Representations
   Like order formats:
   JSON, XML, etc.
```

### API Endpoints

```
Endpoint Structure:
Base URL: https://api.restaurant.com
└── Version: /v1
    └── Resource: /menu
        └── Identifier: /items/123
            └── Action: /prepare

Common Patterns:
GET /menu                 # List all items
GET /menu/123            # Get specific item
POST /orders             # Create order
PUT /orders/456          # Update order
DELETE /orders/456       # Cancel order
```

### Hands-On Exercise: API Explorer

Create simple API client:
```python
import requests

# Basic API interaction
def get_menu():
    response = requests.get(
        'https://api.example.com/v1/menu',
        headers={'Accept': 'application/json'}
    )
    return response.json()

# Test different methods
def test_api():
    # GET request
    items = get_menu()
    print("Menu items:", items)
    
    # POST request
    order = requests.post(
        'https://api.example.com/v1/orders',
        json={'item_id': 123, 'quantity': 1}
    )
    print("Order status:", order.status_code)
```

## 2. Authentication Methods

### The VIP Access Metaphor

Think of API authentication like different types of access cards:
- API Key: Like a simple access card
- OAuth: Like a temporary guest pass
- JWT: Like a smart card with embedded info
- Basic Auth: Like showing ID at door

### Authentication Types

```
1. API Keys
Simple token in header/query:
Authorization: Bearer abc123

Like membership card:
- Simple to use
- Limited security
- No user context

2. OAuth 2.0
Multi-step authorization:
1. Request permission
2. User approves
3. Get access token
4. Use token

Like guest pass system:
- More secure
- User controlled
- Temporary access

3. JWT (JSON Web Tokens)
Self-contained tokens:
header.payload.signature

Like smart ID card:
- Contains user info
- Can't be tampered
- Verified locally
```

### Implementing Authentication

```python
# API Key Example
headers = {
    'Authorization': 'Bearer your_api_key_here'
}
response = requests.get(url, headers=headers)

# OAuth Example
from requests_oauthlib import OAuth2Session

client_id = 'your_client_id'
client_secret = 'your_client_secret'

oauth = OAuth2Session(client_id)
token = oauth.fetch_token(
    'https://api.example.com/oauth/token',
    client_secret=client_secret
)

# JWT Example
import jwt

token = jwt.encode(
    {'user_id': 123, 'exp': 1600000000},
    'secret_key',
    algorithm='HS256'
)
```

### Hands-On Exercise: Auth Tester

Create authentication tester:
```python
def test_auth_methods():
    # Test API Key
    api_key = "your_key_here"
    response = requests.get(
        'https://api.example.com/data',
        headers={'Authorization': f'Bearer {api_key}'}
    )
    print("API Key Auth:", response.status_code)
    
    # Test Basic Auth
    response = requests.get(
        'https://api.example.com/data',
        auth=('username', 'password')
    )
    print("Basic Auth:", response.status_code)
```

## 3. Data Formats

### The Recipe Format Metaphor

Think of data formats like recipe writing styles:
- JSON: Like modern recipe cards
- XML: Like traditional cookbook format
- Query Parameters: Like recipe modifications
- Headers: Like cooking instructions

### JSON Format

```json
{
    "menu": {
        "items": [
            {
                "id": 1,
                "name": "Pizza",
                "price": 12.99,
                "toppings": ["cheese", "tomato"]
            }
        ]
    }
}

Like recipe card:
- Clear structure
- Easy to read
- Nested information
```

### XML Format

```xml
<menu>
    <items>
        <item>
            <id>1</id>
            <name>Pizza</name>
            <price>12.99</price>
            <toppings>
                <topping>cheese</topping>
                <topping>tomato</topping>
            </toppings>
        </item>
    </items>
</menu>

Like cookbook format:
- More verbose
- Strict structure
- Clear hierarchy
```

### Working with Data

```python
# JSON Example
import json

# Parse JSON
data = json.loads(response.text)
print(data['menu']['items'])

# Create JSON
order = {
    'item_id': 1,
    'quantity': 2,
    'notes': 'Extra cheese'
}
json_data = json.dumps(order)

# XML Example
import xml.etree.ElementTree as ET

# Parse XML
root = ET.fromstring(response.text)
items = root.findall('./items/item')

# Create XML
order = ET.Element('order')
item_id = ET.SubElement(order, 'item_id')
item_id.text = '1'
```

### Hands-On Exercise: Format Converter

Create format conversion tool:
```python
def convert_formats():
    # JSON to dict
    json_str = '{"name": "Pizza", "price": 12.99}'
    json_data = json.loads(json_str)
    
    # Dict to XML
    root = ET.Element('item')
    for key, value in json_data.items():
        child = ET.SubElement(root, key)
        child.text = str(value)
    
    # XML to string
    xml_str = ET.tostring(root, encoding='unicode')
    print("XML:", xml_str)
```

## Practical Exercises

### 1. Weather API Client
Build weather app that:
1. Gets API key
2. Makes requests
3. Handles responses
4. Formats data
5. Handles errors

### 2. GitHub API Explorer
Create tool to:
1. Authenticate with GitHub
2. List repositories
3. Get commit history
4. Create issues
5. Handle pagination

### 3. Currency Converter
Develop converter that:
1. Connects to exchange API
2. Gets current rates
3. Converts amounts
4. Caches results
5. Handles errors

## Review Questions

1. **API Basics**
   - What are REST principles?
   - How endpoints work?
   - When use different methods?

2. **Authentication**
   - Different auth types?
   - When use OAuth?
   - How JWTs work?

3. **Data Formats**
   - JSON vs XML?
   - How to parse responses?
   - Best practices for data handling?

## Additional Resources

### Online Tools
- API testers
- JWT debuggers
- JSON/XML validators

### Further Reading
- REST API design
- Authentication flows
- Data format specs

### Video Resources
- API tutorials
- Auth implementation
- Data handling guides

## Next Steps

After mastering these concepts, you'll be ready to:
1. Build API integrations
2. Implement authentication
3. Handle different data formats

Remember: APIs are your gateway to external services - master them well!

## Common Questions and Answers

Q: When should I use different authentication methods?
A: Choose based on security needs: API keys for simple access, OAuth for user data, JWT for stateless auth.

Q: Why prefer JSON over XML?
A: JSON is typically more concise and easier to work with in modern applications, but some APIs still use XML.

Q: How do I handle API errors?
A: Always check status codes and implement proper error handling with meaningful user feedback.

## Glossary

- **API**: Application Programming Interface
- **REST**: Representational State Transfer
- **Endpoint**: Specific API URL
- **Authentication**: Identity verification
- **Authorization**: Access permission
- **OAuth**: Open Authorization
- **JWT**: JSON Web Token
- **JSON**: JavaScript Object Notation
- **XML**: Extensible Markup Language
- **Rate Limit**: Request restrictions

Remember: Good API integration requires attention to authentication, data handling, and error management!
