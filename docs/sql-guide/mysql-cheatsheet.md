# MySQL Cheatsheet

## Table of Contents
- [MySQL Cheatsheet](#mysql-cheatsheet)
  - [Command Line Basics](#command-line-basics)
- [Connect to MySQL](#connect-to-mysql)
- [Import/Export](#import/export)
- [Common Options](#common-options)
  - [Server Administration](#server-administration)
    - [User Management](#user-management)
    - [Database Operations](#database-operations)
  - [Table Operations](#table-operations)
    - [Create Table](#create-table)
    - [Alter Table](#alter-table)
    - [Table Information](#table-information)
  - [Data Manipulation](#data-manipulation)
    - [Insert Data](#insert-data)
    - [Update Data](#update-data)
    - [Delete Data](#delete-data)
  - [Querying Data](#querying-data)
    - [Basic Queries](#basic-queries)
    - [Joins](#joins)
    - [Advanced Queries](#advanced-queries)
  - [Transactions](#transactions)
  - [Performance Optimization](#performance-optimization)
    - [Explain and Analyze](#explain-and-analyze)
    - [Indexing](#indexing)
    - [Query Cache](#query-cache)
  - [Server Status and Variables](#server-status-and-variables)
  - [Backup and Recovery](#backup-and-recovery)
    - [Backup](#backup)
- [Full backup](#full-backup)
- [Single database backup](#single-database-backup)
- [Table backup](#table-backup)
- [Backup with options](#backup-with-options)
    - [Recovery](#recovery)
- [Restore full backup](#restore-full-backup)
- [Restore single database](#restore-single-database)
- [Point-in-time recovery](#point-in-time-recovery)
  - [Python Integration](#python-integration)
- [Connection](#connection)
- [Basic connection](#basic-connection)
- [Connection pool](#connection-pool)
- [Using the pool](#using-the-pool)
- [Transactions](#transactions)
  - [Maintenance and Monitoring](#maintenance-and-monitoring)
    - [Table Maintenance](#table-maintenance)
    - [Monitoring Queries](#monitoring-queries)
    - [Storage Engine Status](#storage-engine-status)



## Command Line Basics

```bash
# Connect to MySQL
mysql -u username -p
mysql -h hostname -u username -p database_name
mysql -u username -p -e "SELECT * FROM table"  # Execute command directly

# Import/Export
mysqldump -u username -p database_name > backup.sql
mysql -u username -p database_name < backup.sql

# Common Options
--host=hostname      # Specify host
--port=port_number   # Specify port
--default-character-set=utf8mb4  # Set character set
```

## Server Administration

### User Management
```sql
-- Create user
CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
CREATE USER 'username'@'%' IDENTIFIED BY 'password';  -- Allow remote connections

-- Grant privileges
GRANT ALL PRIVILEGES ON database_name.* TO 'username'@'localhost';
GRANT SELECT, INSERT ON database_name.* TO 'username'@'localhost';
GRANT SELECT ON database_name.table_name TO 'username'@'localhost';

-- Show grants
SHOW GRANTS FOR 'username'@'localhost';

-- Revoke privileges
REVOKE ALL PRIVILEGES ON database_name.* FROM 'username'@'localhost';

-- Delete user
DROP USER 'username'@'localhost';

-- Reload privileges
FLUSH PRIVILEGES;
```

### Database Operations
```sql
-- Create database
CREATE DATABASE database_name
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Show databases
SHOW DATABASES;

-- Select database
USE database_name;

-- Show current database
SELECT DATABASE();

-- Drop database
DROP DATABASE database_name;

-- Show character set
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';
```

## Table Operations

### Create Table
```sql
-- Basic table creation
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive') DEFAULT 'active',
    INDEX idx_email (email),
    FULLTEXT INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table with foreign key
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- Temporary table
CREATE TEMPORARY TABLE temp_users AS
SELECT * FROM users WHERE status = 'active';
```

### Alter Table
```sql
-- Add column
ALTER TABLE users
ADD COLUMN age INT AFTER username,
ADD COLUMN phone VARCHAR(20) AFTER email;

-- Modify column
ALTER TABLE users
MODIFY COLUMN username VARCHAR(100) NOT NULL;

-- Change column (rename and modify)
ALTER TABLE users
CHANGE COLUMN username user_name VARCHAR(100) NOT NULL;

-- Drop column
ALTER TABLE users
DROP COLUMN age;

-- Add index
ALTER TABLE users
ADD INDEX idx_username_email (username, email);

-- Add foreign key
ALTER TABLE orders
ADD CONSTRAINT fk_user
FOREIGN KEY (user_id) REFERENCES users(id);

-- Modify table engine
ALTER TABLE users ENGINE = MyISAM;
```

### Table Information
```sql
-- Show tables
SHOW TABLES;

-- Describe table
DESCRIBE users;
SHOW COLUMNS FROM users;
SHOW CREATE TABLE users;

-- Show indexes
SHOW INDEX FROM users;

-- Table status
SHOW TABLE STATUS LIKE 'users';
```

## Data Manipulation

### Insert Data
```sql
-- Single row insert
INSERT INTO users (username, email)
VALUES ('john_doe', 'john@example.com');

-- Multiple row insert
INSERT INTO users (username, email) VALUES 
    ('jane_doe', 'jane@example.com'),
    ('bob_smith', 'bob@example.com');

-- Insert ignore (skip duplicates)
INSERT IGNORE INTO users (username, email) VALUES 
    ('john_doe', 'john@example.com');

-- Insert with on duplicate key update
INSERT INTO users (username, email, login_count) 
VALUES ('john_doe', 'john@example.com', 1)
ON DUPLICATE KEY UPDATE login_count = login_count + 1;

-- Insert from select
INSERT INTO users_backup
SELECT * FROM users WHERE status = 'active';
```

### Update Data
```sql
-- Basic update
UPDATE users 
SET status = 'inactive' 
WHERE last_login < DATE_SUB(NOW(), INTERVAL 1 YEAR);

-- Update with join
UPDATE users u
JOIN orders o ON u.id = o.user_id
SET u.total_spent = (
    SELECT SUM(amount) 
    FROM orders 
    WHERE user_id = u.id
);

-- Update multiple tables
UPDATE users u, orders o
SET u.order_count = u.order_count + 1,
    o.status = 'processed'
WHERE u.id = o.user_id
AND o.id = 123;
```

### Delete Data
```sql
-- Delete rows
DELETE FROM users WHERE status = 'inactive';

-- Delete with join
DELETE u, o 
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE u.status = 'inactive';

-- Delete all rows
TRUNCATE TABLE users;
```

## Querying Data

### Basic Queries
```sql
-- Select with various clauses
SELECT 
    u.id,
    u.username,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id
HAVING total_spent > 1000
ORDER BY total_spent DESC
LIMIT 10 OFFSET 20;

-- Select into variables
SELECT COUNT(*) INTO @user_count FROM users;

-- Select into outfile
SELECT * 
INTO OUTFILE '/tmp/users.csv'
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM users;
```

### Joins
```sql
-- Inner join
SELECT u.username, o.amount
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Left join with multiple conditions
SELECT u.username, o.amount
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
    AND o.status = 'completed'
WHERE u.status = 'active';

-- Multiple joins
SELECT u.username, o.amount, p.name
FROM users u
JOIN orders o ON u.id = o.user_id
JOIN products p ON o.product_id = p.id;

-- Self join
SELECT e1.name as employee, e2.name as manager
FROM employees e1
LEFT JOIN employees e2 ON e1.manager_id = e2.id;
```

### Advanced Queries

```sql
-- Common Table Expressions (CTE)
WITH RECURSIVE subordinates AS (
    -- anchor member
    SELECT id, manager_id, name, 1 as level
    FROM employees
    WHERE id = 1
    UNION ALL
    -- recursive member
    SELECT e.id, e.manager_id, e.name, s.level + 1
    FROM employees e
    INNER JOIN subordinates s ON e.manager_id = s.id
)
SELECT * FROM subordinates;

-- Window Functions
SELECT 
    username,
    amount,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount DESC) as purchase_rank,
    AVG(amount) OVER (PARTITION BY user_id) as avg_purchase
FROM orders;

-- Full Text Search
SELECT *
FROM articles
WHERE MATCH(title, content) AGAINST('search terms' IN BOOLEAN MODE);
```

## Transactions

```sql
-- Start transaction
START TRANSACTION;

-- Set save point
SAVEPOINT my_savepoint;

-- Rollback to save point
ROLLBACK TO SAVEPOINT my_savepoint;

-- Commit transaction
COMMIT;

-- Transaction isolation levels
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET SESSION TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET SESSION TRANSACTION ISOLATION LEVEL SERIALIZABLE;
```

## Performance Optimization

### Explain and Analyze
```sql
-- Explain query plan
EXPLAIN SELECT * FROM users WHERE email = 'john@example.com';

-- Explain with extended information
EXPLAIN FORMAT=JSON SELECT * FROM users WHERE email = 'john@example.com';

-- Analyze table
ANALYZE TABLE users;
```

### Indexing
```sql
-- Create indexes
CREATE INDEX idx_email ON users(email);
CREATE UNIQUE INDEX idx_username ON users(username);
CREATE FULLTEXT INDEX idx_search ON articles(title, content);

-- Show index usage
SHOW INDEX FROM users;

-- Find unused indexes
SELECT * 
FROM performance_schema.table_io_waits_summary_by_index_usage 
WHERE index_name IS NOT NULL 
AND count_star = 0;
```

### Query Cache
```sql
-- Check query cache status
SHOW VARIABLES LIKE 'query_cache%';
SHOW STATUS LIKE 'Qcache%';

-- Use query cache
SELECT SQL_CACHE * FROM users;
SELECT SQL_NO_CACHE * FROM users;
```

## Server Status and Variables

```sql
-- Show status
SHOW GLOBAL STATUS;
SHOW SESSION STATUS;

-- Show variables
SHOW VARIABLES;
SHOW VARIABLES LIKE 'max_connections';

-- Set variables
SET GLOBAL max_connections = 1000;
SET SESSION sort_buffer_size = 1048576;

-- Process list
SHOW PROCESSLIST;
SHOW FULL PROCESSLIST;
```

## Backup and Recovery

### Backup
```bash
# Full backup
mysqldump -u root -p --all-databases > backup.sql

# Single database backup
mysqldump -u root -p database_name > database_backup.sql

# Table backup
mysqldump -u root -p database_name table_name > table_backup.sql

# Backup with options
mysqldump -u root -p \
    --single-transaction \
    --routines \
    --triggers \
    --events \
    database_name > backup.sql
```

### Recovery
```bash
# Restore full backup
mysql -u root -p < backup.sql

# Restore single database
mysql -u root -p database_name < database_backup.sql

# Point-in-time recovery
mysqlbinlog --start-datetime="2023-01-01 00:00:00" \
            --stop-datetime="2023-01-01 01:00:00" \
            /var/log/mysql/mysql-bin.000001 | mysql -u root -p
```

## Python Integration

```python
import mysql.connector
from mysql.connector import pooling

# Connection
config = {
    'user': 'username',
    'password': 'password',
    'host': 'localhost',
    'database': 'database_name',
    'raise_on_warnings': True
}

# Basic connection
conn = mysql.connector.connect(**config)
cursor = conn.cursor(dictionary=True)

# Connection pool
pool_config = {
    'pool_name': 'mypool',
    'pool_size': 5,
    **config
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**pool_config)

# Using the pool
connection = connection_pool.get_connection()
try:
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
finally:
    cursor.close()
    connection.close()

# Transactions
try:
    conn.start_transaction()
    cursor.execute("INSERT INTO users (username) VALUES (%s)", ("john",))
    cursor.execute("UPDATE users SET status = %s WHERE id = %s", ("active", 1))
    conn.commit()
except:
    conn.rollback()
    raise
finally:
    cursor.close()
    conn.close()
```

## Maintenance and Monitoring

### Table Maintenance
```sql
-- Check tables
CHECK TABLE users;

-- Repair tables
REPAIR TABLE users;

-- Optimize tables
OPTIMIZE TABLE users;

-- Analyze tables
ANALYZE TABLE users;
```

### Monitoring Queries
```sql
-- Show running queries
SELECT * FROM information_schema.PROCESSLIST
WHERE command != 'Sleep';

-- Kill query
KILL QUERY thread_id;
KILL CONNECTION thread_id;

-- Slow query log
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 2;
```

### Storage Engine Status
```sql
-- Show engine status
SHOW ENGINE INNODB STATUS;

-- Table sizes
SELECT 
    table_name,
    table_rows,
    data_length/1024/1024 as data_size_mb,
    index_length/1024/1024 as index_size_mb
FROM information_schema.TABLES
WHERE table_schema = 'database_name';
