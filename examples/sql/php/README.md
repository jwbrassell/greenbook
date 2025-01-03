# SQL Operations with PHP Examples

## Table of Contents
- [SQL Operations with PHP Examples](#sql-operations-with-php-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Operations
   - Connection management
   - CRUD operations
   - Transaction handling
   - Batch processing

2. Advanced Features
   - Complex queries
   - Stored procedures
   - Triggers and events
   - Replication management

3. Integration Features
   - ORM integration
   - Migration management
   - Backup automation
   - Monitoring integration

4. Full Applications
   - Data warehouse ETL
   - Query analyzer
   - Schema manager
   - Backup manager

## Project Structure

```
php/
├── basic/
│   ├── connection/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── config.php
│   ├── crud/
│   ├── transactions/
│   └── batch/
├── advanced/
│   ├── queries/
│   ├── procedures/
│   ├── triggers/
│   └── replication/
├── integration/
│   ├── orm/
│   ├── migrations/
│   ├── backup/
│   └── monitoring/
└── applications/
    ├── etl_manager/
    ├── query_analyzer/
    ├── schema_manager/
    └── backup_manager/
```

## Getting Started

1. Install Dependencies:
```bash
composer require doctrine/dbal
```

2. Configure Database Connection:
```php
<?php
// config.php
return [
    'mysql' => [
        'host' => 'localhost',
        'user' => 'root',
        'password' => 'your-password',
        'database' => 'test_db'
    ],
    'postgres' => [
        'host' => 'localhost',
        'user' => 'postgres',
        'password' => 'your-password',
        'database' => 'test_db',
        'port' => 5432
    ]
];
```

3. Basic Setup:
```php
<?php
require 'vendor/autoload.php';
```

## Basic Operations

### Connection Management
```php
<?php
class DatabaseManager {
    private $config;
    private $type;
    private $pdo;
    
    public function __construct($type = 'mysql') {
        $this->type = $type;
        $this->config = require 'config.php';
        $this->connect();
    }
    
    private function connect() {
        $config = $this->config[$this->type];
        
        try {
            $dsn = $this->type === 'mysql'
                ? "mysql:host={$config['host']};dbname={$config['database']};charset=utf8mb4"
                : "pgsql:host={$config['host']};port={$config['port']};dbname={$config['database']}";
            
            $this->pdo = new PDO($dsn, $config['user'], $config['password'], [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
                PDO::ATTR_EMULATE_PREPARES => false
            ]);
        } catch (PDOException $e) {
            throw new Exception("Connection failed: " . $e->getMessage());
        }
    }
    
    public function executeQuery($query, $params = []) {
        try {
            $stmt = $this->pdo->prepare($query);
            $stmt->execute($params);
            
            if (stripos($query, 'SELECT') === 0) {
                return $stmt->fetchAll();
            }
            return $stmt->rowCount();
        } catch (PDOException $e) {
            throw new Exception("Query failed: " . $e->getMessage());
        }
    }
    
    public function beginTransaction() {
        return $this->pdo->beginTransaction();
    }
    
    public function commit() {
        return $this->pdo->commit();
    }
    
    public function rollback() {
        return $this->pdo->rollBack();
    }
}
```

### CRUD Operations
```php
<?php
class CRUDManager {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function createRecord($table, array $data) {
        $columns = implode(', ', array_keys($data));
        $values = implode(', ', array_fill(0, count($data), '?'));
        
        $query = "INSERT INTO {$table} ({$columns}) VALUES ({$values})";
        return $this->db->executeQuery($query, array_values($data));
    }
    
    public function readRecords($table, array $conditions = null, array $fields = null) {
        $fields = $fields ? implode(', ', $fields) : '*';
        $query = "SELECT {$fields} FROM {$table}";
        $params = [];
        
        if ($conditions) {
            $clauses = [];
            foreach ($conditions as $key => $value) {
                $clauses[] = "{$key} = ?";
                $params[] = $value;
            }
            $query .= " WHERE " . implode(' AND ', $clauses);
        }
        
        return $this->db->executeQuery($query, $params);
    }
    
    public function updateRecord($table, array $data, array $conditions) {
        $set = implode(', ', array_map(function($key) {
            return "{$key} = ?";
        }, array_keys($data)));
        
        $where = implode(' AND ', array_map(function($key) {
            return "{$key} = ?";
        }, array_keys($conditions)));
        
        $query = "UPDATE {$table} SET {$set} WHERE {$where}";
        $params = array_merge(array_values($data), array_values($conditions));
        
        return $this->db->executeQuery($query, $params);
    }
    
    public function deleteRecord($table, array $conditions) {
        $where = implode(' AND ', array_map(function($key) {
            return "{$key} = ?";
        }, array_keys($conditions)));
        
        $query = "DELETE FROM {$table} WHERE {$where}";
        return $this->db->executeQuery($query, array_values($conditions));
    }
}
```

### Transaction Management
```php
<?php
class TransactionManager {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function executeTransaction(callable $callback) {
        try {
            $this->db->beginTransaction();
            $result = $callback($this->db);
            $this->db->commit();
            return $result;
        } catch (Exception $e) {
            $this->db->rollback();
            throw $e;
        }
    }
    
    public function transferFunds($fromAccount, $toAccount, $amount) {
        return $this->executeTransaction(function($db) use ($fromAccount, $toAccount, $amount) {
            // Debit from account
            $result = $db->executeQuery(
                "UPDATE accounts SET balance = balance - ? 
                WHERE account_id = ? AND balance >= ?",
                [$amount, $fromAccount, $amount]
            );
            
            if ($result === 0) {
                throw new Exception("Insufficient funds");
            }
            
            // Credit to account
            $db->executeQuery(
                "UPDATE accounts SET balance = balance + ? 
                WHERE account_id = ?",
                [$amount, $toAccount]
            );
            
            return true;
        });
    }
}
```

## Advanced Features

### Complex Queries
```php
<?php
class QueryManager {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function getSalesReport($startDate, $endDate) {
        $query = "
            SELECT 
                p.category,
                COUNT(s.id) as total_sales,
                SUM(s.amount) as revenue,
                AVG(s.amount) as avg_sale,
                GROUP_CONCAT(DISTINCT c.name) as customers
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN customers c ON s.customer_id = c.id
            WHERE s.sale_date BETWEEN ? AND ?
            GROUP BY p.category
            HAVING COUNT(s.id) > 5
            ORDER BY revenue DESC
        ";
        
        return $this->db->executeQuery($query, [$startDate, $endDate]);
    }
    
    public function getCustomerInsights($customerId) {
        $query = "
            WITH customer_stats AS (
                SELECT 
                    sale_date,
                    amount,
                    SUM(amount) OVER (
                        PARTITION BY MONTH(sale_date)
                    ) as monthly_total,
                    AVG(amount) OVER (
                        ORDER BY sale_date
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                    ) as moving_avg
                FROM sales
                WHERE customer_id = ?
            )
            SELECT *,
                CASE 
                    WHEN amount > monthly_total * 0.5 THEN 'High Value'
                    WHEN amount > monthly_total * 0.2 THEN 'Medium Value'
                    ELSE 'Low Value'
                END as transaction_category
            FROM customer_stats
        ";
        
        return $this->db->executeQuery($query, [$customerId]);
    }
}
```

### Stored Procedures
```php
<?php
class ProcedureManager {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function createUpdateInventoryProcedure() {
        $query = "
            CREATE PROCEDURE update_inventory(
                IN p_product_id INT,
                IN p_quantity INT,
                IN p_operation VARCHAR(10)
            )
            BEGIN
                DECLARE v_current_stock INT;
                
                SELECT stock INTO v_current_stock
                FROM inventory
                WHERE id = p_product_id;
                
                IF p_operation = 'add' THEN
                    UPDATE inventory
                    SET stock = v_current_stock + p_quantity
                    WHERE id = p_product_id;
                ELSEIF p_operation = 'remove' THEN
                    IF v_current_stock >= p_quantity THEN
                        UPDATE inventory
                        SET stock = v_current_stock - p_quantity
                        WHERE id = p_product_id;
                    ELSE
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Insufficient stock';
                    END IF;
                END IF;
            END
        ";
        
        return $this->db->executeQuery($query);
    }
    
    public function callProcedure($name, array $params) {
        $placeholders = implode(', ', array_fill(0, count($params), '?'));
        $query = "CALL {$name}({$placeholders})";
        return $this->db->executeQuery($query, $params);
    }
}
```

## Security Considerations

1. SQL Injection Prevention:
```php
<?php
class SecureQueryBuilder {
    public static function buildSelect($table, array $conditions = null, array $fields = null) {
        $fields = $fields ? implode(', ', $fields) : '*';
        $query = "SELECT {$fields} FROM {$table}";
        $params = [];
        
        if ($conditions) {
            $clauses = [];
            foreach ($conditions as $key => $value) {
                if (is_array($value)) {
                    $placeholders = implode(', ', array_fill(0, count($value), '?'));
                    $clauses[] = "{$key} IN ({$placeholders})";
                    $params = array_merge($params, $value);
                } else {
                    $clauses[] = "{$key} = ?";
                    $params[] = $value;
                }
            }
            $query .= " WHERE " . implode(' AND ', $clauses);
        }
        
        return [$query, $params];
    }
}
```

2. Access Control:
```php
<?php
class DatabaseAccessControl {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function createUser($username, $password, array $privileges) {
        $this->db->executeTransaction(function($db) use ($username, $password, $privileges) {
            // Create user
            $db->executeQuery(
                "CREATE USER ?@'localhost' IDENTIFIED BY ?",
                [$username, $password]
            );
            
            // Grant privileges
            foreach ($privileges as $table => $actions) {
                $grant = implode(', ', $actions);
                $db->executeQuery(
                    "GRANT {$grant} ON {$table} TO ?@'localhost'",
                    [$username]
                );
            }
        });
    }
    
    public function revokeAccess($username, array $privileges) {
        foreach ($privileges as $table => $actions) {
            $revoke = implode(', ', $actions);
            $this->db->executeQuery(
                "REVOKE {$revoke} ON {$table} FROM ?@'localhost'",
                [$username]
            );
        }
    }
}
```

## Performance Optimization

1. Query Optimization:
```php
<?php
class QueryOptimizer {
    private $db;
    
    public function __construct(DatabaseManager $db) {
        $this->db = $db;
    }
    
    public function analyzeQuery($query, array $params = []) {
        return $this->db->executeQuery("EXPLAIN ANALYZE {$query}", $params);
    }
    
    public function createIndexes($table, array $columns) {
        foreach ($columns as $column) {
            $indexName = "idx_{$table}_{$column}";
            $this->db->executeQuery(
                "CREATE INDEX {$indexName} ON {$table} ({$column})"
            );
        }
    }
    
    public function optimizeTable($table) {
        return $this->db->executeQuery("OPTIMIZE TABLE {$table}");
    }
}
```

2. Connection Pooling:
```php
<?php
class ConnectionPool {
    private static $instances = [];
    private static $maxInstances = 5;
    private $config;
    
    public function __construct($config) {
        $this->config = $config;
    }
    
    public function getConnection() {
        if (count(self::$instances) < self::$maxInstances) {
            $db = new DatabaseManager($this->config);
            self::$instances[] = $db;
            return $db;
        }
        
        return self::$instances[array_rand(self::$instances)];
    }
}
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class DatabaseTests extends TestCase {
    private $db;
    private $crud;
    
    protected function setUp(): void {
        $this->db = new DatabaseManager('mysql');
        $this->crud = new CRUDManager($this->db);
    }
    
    public function testCrudOperations() {
        // Create record
        $data = [
            'name' => 'Test Product',
            'price' => 99.99,
            'category' => 'Test'
        ];
        $result = $this->crud->createRecord('products', $data);
        $this->assertEquals(1, $result);
        
        // Read record
        $records = $this->crud->readRecords(
            'products',
            ['name' => 'Test Product']
        );
        $this->assertCount(1, $records);
        $this->assertEquals(99.99, $records[0]['price']);
    }
    
    public function testTransactionHandling() {
        $manager = new TransactionManager($this->db);
        
        $this->expectException(Exception::class);
        $manager->transferFunds(1, 2, 1000000);  // Should fail
    }
}
```

2. Integration Tests:
```php
<?php
class DatabaseIntegrationTests extends TestCase {
    private $db;
    private $query;
    
    protected function setUp(): void {
        $this->db = new DatabaseManager('mysql');
        $this->query = new QueryManager($this->db);
    }
    
    public function testComplexQuery() {
        // Setup test data
        $this->setupTestData();
        
        // Run complex query
        $results = $this->query->getSalesReport(
            '2023-01-01',
            '2023-12-31'
        );
        
        // Verify results
        $this->assertNotEmpty($results);
        $this->assertArrayHasKey('revenue', $results[0]);
        $this->assertArrayHasKey('avg_sale', $results[0]);
        
        // Clean up
        $this->cleanupTestData();
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
