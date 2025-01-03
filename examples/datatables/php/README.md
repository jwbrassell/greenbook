# DataTables with PHP Examples

## Table of Contents
- [DataTables with PHP Examples](#datatables-with-php-examples)
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
   - PDO database integration
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
php/
├── basic/
│   ├── client_side/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── templates/
│   │       └── table.php
│   └── server_side/
│       ├── index.php
│       ├── composer.json
│       └── templates/
│           └── table.php
├── advanced/
│   ├── row_selection/
│   ├── inline_editing/
│   ├── custom_filtering/
│   └── export/
├── integration/
│   ├── database/
│   ├── api/
│   ├── realtime/
│   └── import_export/
└── applications/
    ├── admin_dashboard/
    ├── data_management/
    ├── reporting/
    └── analytics/
```

## Getting Started

1. Install Dependencies:
```bash
composer install
```

2. Configure Web Server:
```apache
# Apache configuration
<VirtualHost *:80>
    DocumentRoot "/path/to/examples/datatables/php"
    <Directory "/path/to/examples/datatables/php">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

3. Run Example:
```bash
php -S localhost:8000 -t basic/server_side
```

## Basic Examples

### Server-side Processing
```php
<?php
// index.php
require 'vendor/autoload.php';

class DataTableController {
    private $pdo;
    
    public function __construct() {
        $this->pdo = new PDO(
            'mysql:host=localhost;dbname=test',
            'user',
            'password',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
    }
    
    public function getData() {
        // Get DataTables parameters
        $draw = $_GET['draw'] ?? 1;
        $start = $_GET['start'] ?? 0;
        $length = $_GET['length'] ?? 10;
        $search = $_GET['search']['value'] ?? '';
        
        // Base query
        $query = "SELECT SQL_CALC_FOUND_ROWS * FROM users";
        $params = [];
        
        // Apply search
        if ($search) {
            $query .= " WHERE name LIKE ? OR email LIKE ? OR role LIKE ?";
            $params = array_fill(0, 3, "%$search%");
        }
        
        // Apply pagination
        $query .= " LIMIT ?, ?";
        $params[] = (int)$start;
        $params[] = (int)$length;
        
        // Execute query
        $stmt = $this->pdo->prepare($query);
        $stmt->execute($params);
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        // Get total records
        $total = $this->pdo->query("SELECT FOUND_ROWS()")->fetchColumn();
        
        // Format data for DataTables
        $formatted = array_map(function($row) {
            return [
                'id' => $row['id'],
                'name' => $row['name'],
                'email' => $row['email'],
                'role' => $row['role'],
                'actions' => sprintf(
                    '<button onclick="editUser(%d)">Edit</button>',
                    $row['id']
                )
            ];
        }, $data);
        
        return [
            'draw' => (int)$draw,
            'recordsTotal' => $total,
            'recordsFiltered' => $total,
            'data' => $formatted
        ];
    }
}

// Handle AJAX request
if (isset($_GET['action']) && $_GET['action'] === 'getData') {
    $controller = new DataTableController();
    header('Content-Type: application/json');
    echo json_encode($controller->getData());
    exit;
}
?>

<!-- Template -->
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
                ajax: 'index.php?action=getData',
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
```php
<?php
class UserController {
    private $pdo;
    
    public function updateUser($id) {
        $data = json_decode(file_get_contents('php://input'), true);
        
        $stmt = $this->pdo->prepare(
            "UPDATE users SET name = ?, email = ?, role = ? WHERE id = ?"
        );
        
        $stmt->execute([
            $data['name'],
            $data['email'],
            $data['role'],
            $id
        ]);
        
        return ['status' => 'success'];
    }
}

// Handle PUT request
if ($_SERVER['REQUEST_METHOD'] === 'PUT') {
    $controller = new UserController();
    header('Content-Type: application/json');
    echo json_encode($controller->updateUser($_GET['id']));
    exit;
}
?>
```

### Custom Filtering
```php
<?php
class DataFilter {
    private $pdo;
    
    public function getFilteredData() {
        $role = $_GET['role'] ?? null;
        $dateFrom = $_GET['date_from'] ?? null;
        $dateTo = $_GET['date_to'] ?? null;
        
        $query = "SELECT * FROM users WHERE 1=1";
        $params = [];
        
        if ($role) {
            $query .= " AND role = ?";
            $params[] = $role;
        }
        
        if ($dateFrom && $dateTo) {
            $query .= " AND created_at BETWEEN ? AND ?";
            $params[] = $dateFrom;
            $params[] = $dateTo;
        }
        
        // ... rest of the processing
    }
}
?>
```

## Security Considerations

1. Input Validation:
```php
<?php
class Validator {
    public static function validateUser($data) {
        $errors = [];
        
        if (empty($data['name']) || strlen($data['name']) > 100) {
            $errors['name'] = 'Invalid name';
        }
        
        if (!filter_var($data['email'], FILTER_VALIDATE_EMAIL)) {
            $errors['email'] = 'Invalid email';
        }
        
        if (!in_array($data['role'], ['admin', 'user', 'guest'])) {
            $errors['role'] = 'Invalid role';
        }
        
        return $errors;
    }
}

// Usage
$errors = Validator::validateUser($_POST);
if (!empty($errors)) {
    http_response_code(400);
    echo json_encode(['errors' => $errors]);
    exit;
}
?>
```

2. CSRF Protection:
```php
<?php
session_start();

function generateToken() {
    return bin2hex(random_bytes(32));
}

function validateToken($token) {
    return hash_equals($_SESSION['csrf_token'], $token);
}

// Generate token
$_SESSION['csrf_token'] = generateToken();
?>

<!-- In template -->
<meta name="csrf-token" content="<?= $_SESSION['csrf_token'] ?>">

<!-- In JavaScript -->
$.ajaxSetup({
    headers: {
        'X-CSRF-TOKEN': $('meta[name="csrf-token"]').attr('content')
    }
});
```

## Performance Optimization

1. Query Optimization:
```php
<?php
class QueryOptimizer {
    private $pdo;
    
    public function getOptimizedData() {
        // Use indexes
        $this->createIndexIfNotExists('users', 'email');
        
        // Use prepared statements
        $stmt = $this->pdo->prepare("
            SELECT u.*, COUNT(o.id) as order_count
            FROM users u
            LEFT JOIN orders o ON u.id = o.user_id
            GROUP BY u.id
        ");
        
        // Use pagination
        $page = $_GET['page'] ?? 1;
        $perPage = $_GET['per_page'] ?? 10;
        $offset = ($page - 1) * $perPage;
        
        $stmt->bindValue(':limit', $perPage, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>
```

2. Caching:
```php
<?php
class DataCache {
    private $redis;
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379);
    }
    
    public function getData($key) {
        if ($data = $this->redis->get($key)) {
            return json_decode($data, true);
        }
        return null;
    }
    
    public function setData($key, $data, $ttl = 300) {
        $this->redis->setex($key, $ttl, json_encode($data));
    }
}
?>
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class DataTablesTest extends TestCase {
    private $controller;
    
    protected function setUp(): void {
        $this->controller = new DataTableController();
    }
    
    public function testApiResponse() {
        $_GET['draw'] = 1;
        $_GET['start'] = 0;
        $_GET['length'] = 10;
        
        $response = $this->controller->getData();
        
        $this->assertArrayHasKey('data', $response);
        $this->assertArrayHasKey('recordsTotal', $response);
    }
}
?>
```

2. Integration Tests:
```php
<?php
class DatabaseTest extends TestCase {
    protected function setUp(): void {
        $this->pdo = new PDO('sqlite::memory:');
        // Set up test database
    }
    
    public function testDataWorkflow() {
        // Create test user
        $controller = new UserController($this->pdo);
        $userId = $controller->createUser([
            'name' => 'Test User',
            'email' => 'test@example.com',
            'role' => 'user'
        ]);
        
        // Verify in DataTables response
        $dtController = new DataTableController($this->pdo);
        $response = $dtController->getData();
        
        $found = false;
        foreach ($response['data'] as $row) {
            if ($row['email'] === 'test@example.com') {
                $found = true;
                break;
            }
        }
        
        $this->assertTrue($found);
    }
}
?>
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
