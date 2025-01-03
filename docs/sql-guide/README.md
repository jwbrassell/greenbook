# SQL and Database Guide

## Table of Contents
- [SQL and Database Guide](#sql-and-database-guide)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Basic Concepts](#basic-concepts)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing Strategies](#testing-strategies)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
This comprehensive guide covers SQL databases, from basic concepts to advanced operations. Learn how to effectively use and manage different database systems, including MySQL, PostgreSQL, Oracle, and SQLite.

## Prerequisites
- Basic understanding of:
  - Data structures
  - Programming concepts
  - Command line interface
  - Network basics
- Required software:
  - Database client tools
  - SQL IDE (optional)
  - Python (for examples)

## Installation and Setup
1. MySQL Installation:
```bash
# Install MySQL Server
sudo apt install mysql-server  # Debian/Ubuntu
sudo dnf install mysql-server  # RHEL/Fedora

# Secure installation
sudo mysql_secure_installation

# Create database and user
mysql -u root -p << EOF
CREATE DATABASE myapp;
CREATE USER 'myapp_user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON myapp.* TO 'myapp_user'@'localhost';
FLUSH PRIVILEGES;
EOF
```

2. Database Configuration:
```sql
-- Configure MySQL settings
SET GLOBAL max_connections = 200;
SET GLOBAL innodb_buffer_pool_size = 1073741824;  -- 1GB

-- Create initial schema
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Basic Concepts
1. Table Operations:
```sql
-- Create table with constraints
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'completed', 'cancelled'),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert data
INSERT INTO orders (user_id, total, status)
VALUES (1, 99.99, 'pending');
```

2. Querying Data:
```sql
-- Basic SELECT with JOIN
SELECT 
    o.id,
    u.username,
    o.total,
    o.status
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.status = 'pending'
ORDER BY o.total DESC;
```

## Advanced Features
1. Stored Procedures:
```sql
DELIMITER //
CREATE PROCEDURE process_order(
    IN order_id INT,
    IN new_status VARCHAR(20)
)
BEGIN
    DECLARE current_total DECIMAL(10,2);
    
    -- Get order total
    SELECT total INTO current_total
    FROM orders WHERE id = order_id;
    
    -- Update status
    UPDATE orders 
    SET status = new_status,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = order_id;
    
    -- Log change
    INSERT INTO order_history (order_id, status, total)
    VALUES (order_id, new_status, current_total);
END //
DELIMITER ;
```

2. Triggers:
```sql
CREATE TRIGGER after_order_update
AFTER UPDATE ON orders
FOR EACH ROW
BEGIN
    IF NEW.status = 'completed' THEN
        INSERT INTO notifications (user_id, message)
        VALUES (NEW.user_id, CONCAT('Order #', NEW.id, ' completed'));
    END IF;
END;
```

## Security Considerations
1. Access Control:
```sql
-- Create role-based access
CREATE ROLE 'app_read', 'app_write';

GRANT SELECT ON myapp.* TO 'app_read';
GRANT SELECT, INSERT, UPDATE ON myapp.* TO 'app_write';

-- Assign roles to users
GRANT 'app_read' TO 'reporting_user'@'localhost';
GRANT 'app_write' TO 'application_user'@'localhost';
```

2. Data Protection:
```sql
-- Enable encryption
ALTER TABLE users
MODIFY COLUMN password_hash VARBINARY(256);

-- Create encrypted backup
mysqldump --single-transaction \
          --routines \
          --triggers \
          --add-drop-table \
          --databases myapp \
          | openssl enc -aes-256-cbc -salt > backup.sql.enc
```

## Performance Optimization
1. Indexing:
```sql
-- Create indexes
CREATE INDEX idx_user_email ON users(email);
CREATE INDEX idx_order_status ON orders(status);

-- Analyze query performance
EXPLAIN ANALYZE
SELECT u.username, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

2. Query Optimization:
```sql
-- Use subqueries efficiently
SELECT username
FROM users
WHERE id IN (
    SELECT user_id
    FROM orders
    GROUP BY user_id
    HAVING COUNT(*) > 10
);

-- Optimize JOIN operations
SELECT /*+ HASH_JOIN(u o) */
    u.username,
    o.total
FROM users u
JOIN orders o ON u.id = o.user_id;
```

## Testing Strategies
1. Data Validation:
```sql
-- Test constraints
INSERT INTO users (username, email) VALUES
    ('test_user', 'invalid_email')  -- Should fail
;

-- Test foreign keys
INSERT INTO orders (user_id, total)
VALUES (999999, 100)  -- Should fail
;
```

2. Performance Testing:
```sql
-- Generate test data
DELIMITER //
CREATE PROCEDURE generate_test_data(IN count INT)
BEGIN
    DECLARE i INT DEFAULT 0;
    WHILE i < count DO
        INSERT INTO users (username, email)
        VALUES (
            CONCAT('user', i),
            CONCAT('user', i, '@example.com')
        );
        SET i = i + 1;
    END WHILE;
END //
DELIMITER ;
```

## Troubleshooting
1. Common Issues:
```sql
-- Check table status
CHECK TABLE users, orders;

-- Analyze table statistics
ANALYZE TABLE users, orders;

-- Show process list
SHOW FULL PROCESSLIST;
```

2. Monitoring:
```sql
-- Monitor slow queries
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 2;

-- Check system variables
SHOW VARIABLES LIKE 'max_connections';
SHOW STATUS LIKE 'Threads_connected';
```

## Best Practices
1. Database Design:
```sql
-- Use appropriate data types
CREATE TABLE products (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Implement soft deletes
ALTER TABLE users
ADD COLUMN deleted_at TIMESTAMP NULL DEFAULT NULL;
```

2. Error Handling:
```sql
DELIMITER //
CREATE PROCEDURE safe_delete_user(
    IN user_id INT,
    OUT result VARCHAR(100)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET result = 'Error occurred';
        ROLLBACK;
    END;
    
    START TRANSACTION;
        UPDATE users SET deleted_at = NOW()
        WHERE id = user_id;
        SET result = 'Success';
    COMMIT;
END //
DELIMITER ;
```

## Integration Points
1. Application Integration:
```python
import mysql.connector
from contextlib import contextmanager

@contextmanager
def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="app_user",
        password="password",
        database="myapp"
    )
    try:
        yield conn
    finally:
        conn.close()
```

2. External Systems:
```sql
-- Create federated table
CREATE TABLE remote_orders (
    id INT,
    total DECIMAL(10,2)
)
ENGINE=FEDERATED
CONNECTION='mysql://remote_user@remote_host:3306/remote_db/orders';
```

## Next Steps
1. Advanced Topics
   - Replication and clustering
   - Database sharding
   - Advanced query optimization
   - High availability setup

2. Further Learning
   - [MySQL Documentation](https://dev.mysql.com/doc/)
   - [PostgreSQL Documentation](https://www.postgresql.org/docs/)
   - [SQL Performance Tuning](https://use-the-index-luke.com/)
   - Community resources

## Related Documentation
- [Backup and Recovery](backup-recovery.md)
- [Operations and Maintenance](operations-maintenance.md)
- [MySQL Cheatsheet](mysql-cheatsheet.md)
- [Oracle/CX Cheatsheet](cx-oracle-cheatsheet.md)

## Contributing
Feel free to contribute to this documentation by submitting pull requests or opening issues for improvements. Please ensure your contributions include practical examples and follow SQL best practices.
