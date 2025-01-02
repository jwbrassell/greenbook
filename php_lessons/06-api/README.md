# PHP API Development

## Table of Contents
- [PHP API Development](#php-api-development)
  - [Basic API Structure](#basic-api-structure)
    - [Directory Structure](#directory-structure)
    - [Router Setup](#router-setup)
  - [Controller Example](#controller-example)
    - [User Controller](#user-controller)
  - [Authentication](#authentication)
    - [JWT Authentication Middleware](#jwt-authentication-middleware)
  - [Rate Limiting](#rate-limiting)
    - [Rate Limit Middleware](#rate-limit-middleware)
  - [API Documentation](#api-documentation)
    - [Using OpenAPI/Swagger](#using-openapi/swagger)
  - [Response Formatting](#response-formatting)
    - [Response Utility Class](#response-utility-class)
  - [API Versioning](#api-versioning)
    - [URL-based Versioning](#url-based-versioning)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)



This guide covers building RESTful APIs with PHP, including authentication, rate limiting, and documentation.

## Basic API Structure

### Directory Structure
```
api/
├── config/
│   ├── database.php
│   └── config.php
├── controllers/
│   └── UserController.php
├── models/
│   └── User.php
├── middleware/
│   ├── Auth.php
│   └── RateLimit.php
├── utils/
│   └── Response.php
└── index.php
```

### Router Setup
```php
<?php
// index.php

require_once 'config/config.php';

// Parse URI and method
$uri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$method = $_SERVER['REQUEST_METHOD'];

// Define routes
$routes = [
    'GET' => [
        '/api/users' => 'UserController@index',
        '/api/users/(\d+)' => 'UserController@show'
    ],
    'POST' => [
        '/api/users' => 'UserController@store'
    ],
    'PUT' => [
        '/api/users/(\d+)' => 'UserController@update'
    ],
    'DELETE' => [
        '/api/users/(\d+)' => 'UserController@delete'
    ]
];

// Route handling
foreach ($routes[$method] as $pattern => $handler) {
    if (preg_match("#^$pattern$#", $uri, $matches)) {
        // Parse handler
        list($controller, $action) = explode('@', $handler);
        
        // Load controller
        require_once "controllers/$controller.php";
        $controller = new $controller();
        
        // Remove full match from matches array
        array_shift($matches);
        
        // Call handler with parameters
        $response = call_user_func_array([$controller, $action], $matches);
        
        // Send response
        header('Content-Type: application/json');
        echo json_encode($response);
        exit;
    }
}

// No route found
header("HTTP/1.0 404 Not Found");
echo json_encode(['error' => 'Not Found']);
?>
```

## Controller Example

### User Controller
```php
<?php
class UserController {
    private $db;
    
    public function __construct() {
        $this->db = require_once 'config/database.php';
    }
    
    public function index() {
        try {
            $stmt = $this->db->query("SELECT * FROM users");
            return [
                'status' => 'success',
                'data' => $stmt->fetchAll(PDO::FETCH_ASSOC)
            ];
        } catch (PDOException $e) {
            return $this->error($e->getMessage());
        }
    }
    
    public function show($id) {
        try {
            $stmt = $this->db->prepare("SELECT * FROM users WHERE id = ?");
            $stmt->execute([$id]);
            $user = $stmt->fetch(PDO::FETCH_ASSOC);
            
            if (!$user) {
                return $this->error('User not found', 404);
            }
            
            return [
                'status' => 'success',
                'data' => $user
            ];
        } catch (PDOException $e) {
            return $this->error($e->getMessage());
        }
    }
    
    public function store() {
        try {
            $data = json_decode(file_get_contents('php://input'), true);
            
            // Validate input
            if (!isset($data['name']) || !isset($data['email'])) {
                return $this->error('Missing required fields', 400);
            }
            
            $stmt = $this->db->prepare("INSERT INTO users (name, email) VALUES (?, ?)");
            $stmt->execute([$data['name'], $data['email']]);
            
            return [
                'status' => 'success',
                'message' => 'User created successfully',
                'id' => $this->db->lastInsertId()
            ];
        } catch (PDOException $e) {
            return $this->error($e->getMessage());
        }
    }
    
    private function error($message, $code = 500) {
        http_response_code($code);
        return [
            'status' => 'error',
            'message' => $message
        ];
    }
}
?>
```

## Authentication

### JWT Authentication Middleware
```php
<?php
require_once 'vendor/autoload.php';
use \Firebase\JWT\JWT;

class Auth {
    private $secret_key = "your_secret_key";
    
    public function generateToken($user) {
        $payload = [
            'iss' => 'your_app_name',
            'aud' => 'your_app_client',
            'iat' => time(),
            'exp' => time() + (60 * 60), // 1 hour
            'user_id' => $user['id']
        ];
        
        return JWT::encode($payload, $this->secret_key, 'HS256');
    }
    
    public function validateToken() {
        $headers = getallheaders();
        
        if (!isset($headers['Authorization'])) {
            throw new Exception('No token provided');
        }
        
        $token = str_replace('Bearer ', '', $headers['Authorization']);
        
        try {
            $decoded = JWT::decode($token, $this->secret_key, ['HS256']);
            return $decoded;
        } catch (Exception $e) {
            throw new Exception('Invalid token');
        }
    }
}

// Usage in router
$auth = new Auth();
try {
    $auth->validateToken();
    // Continue with protected route
} catch (Exception $e) {
    header('HTTP/1.0 401 Unauthorized');
    echo json_encode(['error' => $e->getMessage()]);
    exit;
}
?>
```

## Rate Limiting

### Rate Limit Middleware
```php
<?php
class RateLimit {
    private $redis;
    private $max_requests = 100; // per window
    private $window = 3600; // 1 hour in seconds
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379);
    }
    
    public function check($ip) {
        $key = "rate_limit:$ip";
        $current = $this->redis->get($key);
        
        if (!$current) {
            $this->redis->setex($key, $this->window, 1);
            return true;
        }
        
        if ($current >= $this->max_requests) {
            return false;
        }
        
        $this->redis->incr($key);
        return true;
    }
}

// Usage in router
$rateLimit = new RateLimit();
if (!$rateLimit->check($_SERVER['REMOTE_ADDR'])) {
    header('HTTP/1.0 429 Too Many Requests');
    echo json_encode(['error' => 'Rate limit exceeded']);
    exit;
}
?>
```

## API Documentation

### Using OpenAPI/Swagger
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /api/users:
    get:
      summary: Get all users
      responses:
        '200':
          description: List of users
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create a new user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserInput'
      responses:
        '201':
          description: User created

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        email:
          type: string
```

## Response Formatting

### Response Utility Class
```php
<?php
class Response {
    public static function json($data, $status = 200) {
        header('Content-Type: application/json');
        http_response_code($status);
        echo json_encode([
            'status' => $status < 400 ? 'success' : 'error',
            'data' => $data
        ]);
        exit;
    }
    
    public static function error($message, $status = 400) {
        self::json(['message' => $message], $status);
    }
}

// Usage
Response::json(['users' => $users]);
Response::error('Invalid input', 400);
?>
```

## API Versioning

### URL-based Versioning
```php
<?php
// index.php

$version = 'v1'; // Default version
if (preg_match('/^\/api\/(v[0-9]+)\//', $uri, $matches)) {
    $version = $matches[1];
    // Remove version from URI for routing
    $uri = preg_replace('/^\/api\/v[0-9]+/', '/api', $uri);
}

// Load version-specific controller
require_once "controllers/$version/UserController.php";
?>
```

## Best Practices

1. **Security**
   - Always validate input
   - Use HTTPS
   - Implement proper authentication
   - Rate limit requests
   - Sanitize output

2. **Performance**
   - Cache responses
   - Paginate results
   - Optimize queries
   - Use appropriate indexes

3. **Documentation**
   - Use OpenAPI/Swagger
   - Document all endpoints
   - Include examples
   - Keep docs updated

4. **Error Handling**
   - Use appropriate HTTP status codes
   - Return meaningful error messages
   - Log errors properly
   - Handle all edge cases

## Next Steps
- Implement caching
- Add request validation
- Set up API monitoring
- Create API documentation
