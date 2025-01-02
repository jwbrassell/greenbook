# CRUD Operations in PHP

## Table of Contents
- [CRUD Operations in PHP](#crud-operations-in-php)
  - [Database Connection](#database-connection)
  - [Create Operation](#create-operation)
    - [Basic Insert](#basic-insert)
    - [Batch Insert](#batch-insert)
  - [Read Operation](#read-operation)
    - [Single Record](#single-record)
    - [Multiple Records](#multiple-records)
  - [Update Operation](#update-operation)
    - [Single Update](#single-update)
  - [Delete Operation](#delete-operation)
    - [Single Delete](#single-delete)
    - [Batch Delete](#batch-delete)
  - [Best Practices](#best-practices)
  - [Example Database Schema](#example-database-schema)
  - [Complete Example](#complete-example)
  - [Next Steps](#next-steps)



This guide covers the fundamentals of Create, Read, Update, and Delete (CRUD) operations in PHP with MySQL.

## Database Connection

```php
<?php
$host = 'localhost';
$dbname = 'test_db';
$username = 'root';
$password = 'your_password';

try {
    $pdo = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    echo "Connected successfully";
} catch(PDOException $e) {
    echo "Connection failed: " . $e->getMessage();
}
?>
```

## Create Operation

### Basic Insert
```php
<?php
function createUser($pdo, $name, $email) {
    try {
        $sql = "INSERT INTO users (name, email) VALUES (:name, :email)";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([
            ':name' => $name,
            ':email' => $email
        ]);
        return $pdo->lastInsertId();
    } catch(PDOException $e) {
        error_log("Error creating user: " . $e->getMessage());
        throw $e;
    }
}

// Usage
$userId = createUser($pdo, "John Doe", "john@example.com");
?>
```

### Batch Insert
```php
<?php
function batchCreateUsers($pdo, $users) {
    try {
        $pdo->beginTransaction();
        
        $sql = "INSERT INTO users (name, email) VALUES (:name, :email)";
        $stmt = $pdo->prepare($sql);
        
        foreach ($users as $user) {
            $stmt->execute([
                ':name' => $user['name'],
                ':email' => $user['email']
            ]);
        }
        
        $pdo->commit();
        return true;
    } catch(PDOException $e) {
        $pdo->rollBack();
        error_log("Error in batch create: " . $e->getMessage());
        throw $e;
    }
}
?>
```

## Read Operation

### Single Record
```php
<?php
function getUser($pdo, $id) {
    try {
        $sql = "SELECT * FROM users WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':id' => $id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    } catch(PDOException $e) {
        error_log("Error fetching user: " . $e->getMessage());
        throw $e;
    }
}
?>
```

### Multiple Records
```php
<?php
function getUsers($pdo, $limit = 10, $offset = 0) {
    try {
        $sql = "SELECT * FROM users LIMIT :limit OFFSET :offset";
        $stmt = $pdo->prepare($sql);
        $stmt->bindValue(':limit', $limit, PDO::PARAM_INT);
        $stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
        $stmt->execute();
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    } catch(PDOException $e) {
        error_log("Error fetching users: " . $e->getMessage());
        throw $e;
    }
}
?>
```

## Update Operation

### Single Update
```php
<?php
function updateUser($pdo, $id, $data) {
    try {
        $fields = array_map(function($key) {
            return "$key = :$key";
        }, array_keys($data));
        
        $sql = "UPDATE users SET " . implode(', ', $fields) . " WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        
        $data['id'] = $id;
        $stmt->execute($data);
        
        return $stmt->rowCount();
    } catch(PDOException $e) {
        error_log("Error updating user: " . $e->getMessage());
        throw $e;
    }
}

// Usage
$data = [
    'name' => 'Updated Name',
    'email' => 'updated@example.com'
];
$rowsAffected = updateUser($pdo, 1, $data);
?>
```

## Delete Operation

### Single Delete
```php
<?php
function deleteUser($pdo, $id) {
    try {
        $sql = "DELETE FROM users WHERE id = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->execute([':id' => $id]);
        return $stmt->rowCount();
    } catch(PDOException $e) {
        error_log("Error deleting user: " . $e->getMessage());
        throw $e;
    }
}
?>
```

### Batch Delete
```php
<?php
function batchDeleteUsers($pdo, $ids) {
    try {
        $pdo->beginTransaction();
        
        $placeholders = str_repeat('?,', count($ids) - 1) . '?';
        $sql = "DELETE FROM users WHERE id IN ($placeholders)";
        
        $stmt = $pdo->prepare($sql);
        $stmt->execute($ids);
        
        $pdo->commit();
        return $stmt->rowCount();
    } catch(PDOException $e) {
        $pdo->rollBack();
        error_log("Error in batch delete: " . $e->getMessage());
        throw $e;
    }
}
?>
```

## Best Practices

1. **Always Use Prepared Statements**
   - Prevents SQL injection
   - Better performance with repeated execution

2. **Transaction Management**
   - Use transactions for multiple operations
   - Ensures data integrity
   - Proper error handling with rollback

3. **Error Handling**
   - Catch and log exceptions
   - Return meaningful error messages
   - Use proper error logging

4. **Input Validation**
   - Validate all input data
   - Sanitize data before storage
   - Use proper data types

5. **Security**
   - Use PDO for database operations
   - Implement proper access control
   - Secure sensitive data

## Example Database Schema
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Complete Example
```php
<?php
// config.php
class Database {
    private static $instance = null;
    private $conn;
    
    private function __construct() {
        $host = 'localhost';
        $dbname = 'test_db';
        $username = 'root';
        $password = 'your_password';
        
        try {
            $this->conn = new PDO("mysql:host=$host;dbname=$dbname", $username, $password);
            $this->conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch(PDOException $e) {
            die("Connection failed: " . $e->getMessage());
        }
    }
    
    public static function getInstance() {
        if (self::$instance == null) {
            self::$instance = new Database();
        }
        return self::$instance;
    }
    
    public function getConnection() {
        return $this->conn;
    }
}

// Usage
$db = Database::getInstance();
$pdo = $db->getConnection();

// Now you can use any of the CRUD functions defined above
?>
```

## Next Steps
- Learn about form handling and data validation
- Implement user authentication
- Study security best practices
- Explore API development
