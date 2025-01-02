# RESTful APIs and HTTP Clients: A Comprehensive Guide

## Table of Contents
- [RESTful APIs and HTTP Clients: A Comprehensive Guide](#restful-apis-and-http-clients:-a-comprehensive-guide)
  - [Table of Contents](#table-of-contents)
  - [Introduction to REST](#introduction-to-rest)
  - [HTTP Methods](#http-methods)
    - [GET](#get)
    - [POST](#post)
    - [PUT](#put)
    - [PATCH](#patch)
    - [DELETE](#delete)
  - [HTTP Status Codes](#http-status-codes)
  - [Authentication Methods](#authentication-methods)
    - [Basic Authentication](#basic-authentication)
- [Using curl](#using-curl)
- [Using wget](#using-wget)
    - [API Key Authentication](#api-key-authentication)
- [In header](#in-header)
- [In query parameter](#in-query-parameter)
    - [OAuth 2.0](#oauth-20)
- [Bearer token](#bearer-token)
- [Refresh token](#refresh-token)
    - [JWT (JSON Web Tokens)](#jwt-json-web-tokens)
    - [Success Codes (2xx)](#success-codes-2xx)
    - [Client Error Codes (4xx)](#client-error-codes-4xx)
    - [Server Error Codes (5xx)](#server-error-codes-5xx)
  - [Command Line Tools](#command-line-tools)
    - [curl Examples](#curl-examples)
    - [wget Examples](#wget-examples)
  - [Language-Specific Examples](#language-specific-examples)
    - [Python (using requests)](#python-using-requests)
- [GET Request](#get-request)
- [POST Request](#post-request)
- [PUT Request](#put-request)
- [DELETE Request](#delete-request)
    - [JavaScript (using fetch)](#javascript-using-fetch)
    - [PHP (using cURL)](#php-using-curl)
    - [Shell Script Examples](#shell-script-examples)
- [!/bin/bash](#!/bin/bash)
- [Function to make GET request](#function-to-make-get-request)
- [Function to create user (POST)](#function-to-create-user-post)
- [Function to update user (PUT)](#function-to-update-user-put)
- [Function to delete user](#function-to-delete-user)
- [Example usage:](#example-usage:)
- [get_user 123](#get_user-123)
- [create_user "John Doe" "john@example.com"](#create_user-"john-doe"-"john@examplecom")
- [update_user 123 "John Updated" "john@example.com"](#update_user-123-"john-updated"-"john@examplecom")
- [delete_user 123](#delete_user-123)
  - [Best Practices](#best-practices)
  - [Response Formats](#response-formats)
    - [JSON Response](#json-response)
    - [XML Response](#xml-response)
  - [Error Handling](#error-handling)
    - [Python Error Handling](#python-error-handling)
    - [JavaScript Error Handling](#javascript-error-handling)
  - [Real-World Examples](#real-world-examples)
    - [GitHub API](#github-api)
- [List repositories for a user](#list-repositories-for-a-user)
- [Create an issue](#create-an-issue)
    - [Weather API (OpenWeatherMap)](#weather-api-openweathermap)
- [Get current weather](#get-current-weather)
- [Get 5-day forecast](#get-5-day-forecast)
  - [Exercise Ideas](#exercise-ideas)



## Table of Contents
1. [Introduction to REST](#introduction)
2. [HTTP Methods](#http-methods)
3. [HTTP Status Codes](#status-codes)
4. [Authentication Methods](#authentication)
5. [Command Line Tools](#cli-tools)
6. [Language-Specific Examples](#code-examples)
7. [Response Formats](#response-formats)
8. [Error Handling](#error-handling)
9. [Real-World Examples](#real-world-examples)

## Introduction to REST <a name="introduction"></a>

REST (Representational State Transfer) is an architectural style for designing networked applications. RESTful APIs use HTTP requests to perform CRUD operations:

- Create (POST)
- Read (GET)
- Update (PUT/PATCH)
- Delete (DELETE)

## HTTP Methods <a name="http-methods"></a>

### GET
- Retrieves resources
- Should be idempotent (same result regardless of how many times called)
- Data is sent in URL parameters
- Example URL: `https://api.example.com/users?id=123`

### POST
- Creates new resources
- Not idempotent (each call creates new resource)
- Data is sent in request body
- Example URL: `https://api.example.com/users`

### PUT
- Updates entire resource
- Idempotent
- Requires complete resource data
- Example URL: `https://api.example.com/users/123`

### PATCH
- Partially updates resource
- Sends only changed fields
- Example URL: `https://api.example.com/users/123`

### DELETE
- Removes resource
- Example URL: `https://api.example.com/users/123`

## HTTP Status Codes <a name="status-codes"></a>

## Authentication Methods <a name="authentication"></a>

### Basic Authentication
```bash
# Using curl
curl -u username:password https://api.example.com/users

# Using wget
wget --user=username --password=password https://api.example.com/users
```

### API Key Authentication
```bash
# In header
curl -H "X-API-Key: your_api_key" https://api.example.com/users

# In query parameter
curl https://api.example.com/users?api_key=your_api_key
```

### OAuth 2.0
```bash
# Bearer token
curl -H "Authorization: Bearer your_access_token" https://api.example.com/users

# Refresh token
curl -X POST https://api.example.com/oauth/token \
     -d "grant_type=refresh_token" \
     -d "refresh_token=your_refresh_token" \
     -d "client_id=your_client_id" \
     -d "client_secret=your_client_secret"
```

### JWT (JSON Web Tokens)
```bash
curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \
     https://api.example.com/users
```

### Success Codes (2xx)
- 200: OK
- 201: Created
- 204: No Content

### Client Error Codes (4xx)
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 429: Too Many Requests

### Server Error Codes (5xx)
- 500: Internal Server Error
- 502: Bad Gateway
- 503: Service Unavailable

## Command Line Tools <a name="cli-tools"></a>

### curl Examples

1. GET Request:
```bash
curl https://api.example.com/users
```

2. GET with Headers:
```bash
curl -H "Authorization: Bearer token123" https://api.example.com/users
```

3. POST Request:
```bash
curl -X POST -H "Content-Type: application/json" \
     -d '{"name": "John", "email": "john@example.com"}' \
     https://api.example.com/users
```

4. PUT Request:
```bash
curl -X PUT -H "Content-Type: application/json" \
     -d '{"id": 123, "name": "John Updated", "email": "john@example.com"}' \
     https://api.example.com/users/123
```

5. DELETE Request:
```bash
curl -X DELETE https://api.example.com/users/123
```

### wget Examples

1. GET Request:
```bash
wget https://api.example.com/users
```

2. POST Request with Data:
```bash
wget --header="Content-Type: application/json" \
     --post-data='{"name": "John", "email": "john@example.com"}' \
     https://api.example.com/users
```

## Language-Specific Examples <a name="code-examples"></a>

### Python (using requests)

```python
import requests

# GET Request
def get_user(user_id):
    response = requests.get(f'https://api.example.com/users/{user_id}')
    return response.json()

# POST Request
def create_user(user_data):
    response = requests.post(
        'https://api.example.com/users',
        json=user_data,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# PUT Request
def update_user(user_id, user_data):
    response = requests.put(
        f'https://api.example.com/users/{user_id}',
        json=user_data,
        headers={'Content-Type': 'application/json'}
    )
    return response.json()

# DELETE Request
def delete_user(user_id):
    response = requests.delete(f'https://api.example.com/users/{user_id}')
    return response.status_code == 204
```

### JavaScript (using fetch)

```javascript
// GET Request
async function getUser(userId) {
    const response = await fetch(`https://api.example.com/users/${userId}`);
    return await response.json();
}

// POST Request
async function createUser(userData) {
    const response = await fetch('https://api.example.com/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

// PUT Request
async function updateUser(userId, userData) {
    const response = await fetch(`https://api.example.com/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData)
    });
    return await response.json();
}

// DELETE Request
async function deleteUser(userId) {
    const response = await fetch(`https://api.example.com/users/${userId}`, {
        method: 'DELETE'
    });
    return response.ok;
}
```

### PHP (using cURL)

```php
<?php

// GET Request
function getUser($userId) {
    $ch = curl_init("https://api.example.com/users/$userId");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

// POST Request
function createUser($userData) {
    $ch = curl_init("https://api.example.com/users");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($userData));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

// PUT Request
function updateUser($userId, $userData) {
    $ch = curl_init("https://api.example.com/users/$userId");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($userData));
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        'Content-Type: application/json'
    ]);
    $response = curl_exec($ch);
    curl_close($ch);
    return json_decode($response, true);
}

// DELETE Request
function deleteUser($userId) {
    $ch = curl_init("https://api.example.com/users/$userId");
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "DELETE");
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    return $httpCode === 204;
}
```

### Shell Script Examples

```bash
#!/bin/bash

# Function to make GET request
get_user() {
    local user_id=$1
    curl -s "https://api.example.com/users/$user_id"
}

# Function to create user (POST)
create_user() {
    local name=$1
    local email=$2
    curl -s -X POST \
         -H "Content-Type: application/json" \
         -d "{\"name\": \"$name\", \"email\": \"$email\"}" \
         "https://api.example.com/users"
}

# Function to update user (PUT)
update_user() {
    local user_id=$1
    local name=$2
    local email=$3
    curl -s -X PUT \
         -H "Content-Type: application/json" \
         -d "{\"name\": \"$name\", \"email\": \"$email\"}" \
         "https://api.example.com/users/$user_id"
}

# Function to delete user
delete_user() {
    local user_id=$1
    curl -s -X DELETE "https://api.example.com/users/$user_id"
}

# Example usage:
# get_user 123
# create_user "John Doe" "john@example.com"
# update_user 123 "John Updated" "john@example.com"
# delete_user 123
```

## Best Practices

1. Always handle errors appropriately
2. Use proper HTTP status codes
3. Include appropriate headers (Content-Type, Authorization)
4. Validate input data
5. Use HTTPS for secure communication
6. Implement rate limiting
7. Document your API endpoints
8. Use proper versioning
9. Keep endpoints RESTful and consistent
10. Implement proper authentication/authorization

## Response Formats <a name="response-formats"></a>

### JSON Response
```python
import requests

response = requests.get('https://api.example.com/users')
json_data = response.json()
print(json_data['users'][0]['name'])
```

### XML Response
```python
import requests
import xml.etree.ElementTree as ET

response = requests.get('https://api.example.com/users')
root = ET.fromstring(response.content)
users = root.findall('.//user')
for user in users:
    print(user.find('name').text)
```

## Error Handling <a name="error-handling"></a>

### Python Error Handling
```python
import requests
from requests.exceptions import RequestException

def safe_api_call(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except requests.exceptions.ConnectionError as conn_err:
        print(f'Error connecting: {conn_err}')
    except requests.exceptions.Timeout as timeout_err:
        print(f'Timeout error: {timeout_err}')
    except requests.exceptions.RequestException as err:
        print(f'Error occurred: {err}')
    return None
```

### JavaScript Error Handling
```javascript
async function safeApiFetch(url) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        if (error instanceof TypeError) {
            console.error('Network error:', error);
        } else {
            console.error('Other error:', error);
        }
        return null;
    }
}
```

## Real-World Examples <a name="real-world-examples"></a>

### GitHub API
```bash
# List repositories for a user
curl -H "Authorization: token YOUR_TOKEN" \
     https://api.github.com/users/octocat/repos

# Create an issue
curl -X POST \
     -H "Authorization: token YOUR_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"Found a bug","body":"Details about the bug"}' \
     https://api.github.com/repos/owner/repo/issues
```

### Weather API (OpenWeatherMap)
```bash
# Get current weather
curl "https://api.openweathermap.org/data/2.5/weather?q=London&appid=YOUR_API_KEY"

# Get 5-day forecast
curl "https://api.openweathermap.org/data/2.5/forecast?q=London&appid=YOUR_API_KEY"
```

## Exercise Ideas

1. Create a simple REST API server
2. Implement CRUD operations using different tools
3. Practice error handling with different scenarios:
   - Network failures
   - Invalid authentication
   - Rate limiting
   - Malformed requests
4. Add different types of authentication:
   - API keys
   - OAuth 2.0
   - JWT
5. Test API endpoints using different methods
6. Document API using OpenAPI/Swagger
7. Create a simple client that handles multiple response formats
8. Implement retry logic for failed requests
9. Build a rate limiter for API requests
10. Create a caching layer for API responses
