                                                                                                                                                                  # SQLite3 Cheatsheet

## Command Line Basics

```bash
# Start SQLite3 with a database (creates if doesn't exist)

## Table of Contents
  - [Command Line Basics](#command-line-basics)
- [Start SQLite3 with a database (creates if doesn't exist)](#start-sqlite3-with-a-database-creates-if-doesn't-exist)
- [Common command line options](#common-command-line-options)
  - [Meta Commands (in SQLite shell)](#meta-commands-in-sqlite-shell)
  - [Database Operations](#database-operations)
    - [Create & Connect](#create-&-connect)
- [Python connection](#python-connection)
- [Memory-only database](#memory-only-database)
    - [Attach & Detach Databases](#attach-&-detach-databases)
  - [Table Operations](#table-operations)
    - [Create Table](#create-table)
    - [Alter Table](#alter-table)
    - [Drop Table](#drop-table)
  - [Data Manipulation](#data-manipulation)
    - [Insert Data](#insert-data)
    - [Update Data](#update-data)
    - [Delete Data](#delete-data)
  - [Querying Data](#querying-data)
    - [Basic Queries](#basic-queries)
    - [Joins](#joins)
    - [Aggregation](#aggregation)
    - [Subqueries](#subqueries)
  - [Indexes](#indexes)
    - [Create Indexes](#create-indexes)
    - [Manage Indexes](#manage-indexes)
  - [Transactions](#transactions)
    - [Basic Transaction](#basic-transaction)
    - [Python Transaction Example](#python-transaction-example)
  - [Views](#views)
    - [Create Views](#create-views)
    - [Manage Views](#manage-views)
  - [Common Functions](#common-functions)
    - [Text Functions](#text-functions)
    - [Date/Time Functions](#date/time-functions)
    - [Aggregate Functions](#aggregate-functions)
  - [Performance Tips](#performance-tips)
    - [Optimization](#optimization)
    - [Maintenance](#maintenance)
  - [Python Integration](#python-integration)
    - [Basic Operations](#basic-operations)
- [Connect to database](#connect-to-database)
- [Execute query](#execute-query)
- [Insert with parameters](#insert-with-parameters)
- [Commit and close](#commit-and-close)
    - [Advanced Usage](#advanced-usage)
- [Context manager](#context-manager)
- [Row factory for dictionary results](#row-factory-for-dictionary-results)
- [Custom aggregation](#custom-aggregation)
  - [Backup and Restore](#backup-and-restore)
    - [Command Line](#command-line)
- [Backup](#backup)
- [Restore](#restore)
- [Online backup](#online-backup)
    - [Python Backup](#python-backup)


sqlite3 database.db

# Common command line options
sqlite3 database.db -column -header  # Display results in columns with headers
sqlite3 database.db -csv             # Output in CSV format
sqlite3 database.db -init init.sql   # Execute commands from init.sql at startup
```

## Meta Commands (in SQLite shell)

```sql
.help           -- Show help message
.tables         -- List all tables
.schema         -- Show schema of all tables
.schema TABLE   -- Show schema of specific table
.indexes        -- List all indexes
.quit          -- Exit SQLite prompt
.mode column   -- Set output mode to column
.headers on    -- Turn headers on
.separator ROW -- Change separator for CSV output
.dump         -- Dump database in SQL format
.backup FILE  -- Backup database to FILE
.read FILE    -- Execute SQL from FILE
.databases    -- List all attached databases
```

## Database Operations

### Create & Connect
```python
# Python connection
import sqlite3
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Memory-only database
conn = sqlite3.connect(':memory:')
```

### Attach & Detach Databases
```sql
-- Attach another database
ATTACH DATABASE 'other.db' AS other;

-- Detach database
DETACH DATABASE other;
```

## Table Operations

### Create Table
```sql
-- Basic table creation
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table with foreign key
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    amount DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create table from SELECT
CREATE TABLE users_backup AS 
SELECT * FROM users;
```

### Alter Table
```sql
-- Add column
ALTER TABLE users ADD COLUMN age INTEGER;

-- Rename table
ALTER TABLE users RENAME TO customers;

-- Rename column (SQLite 3.25+)
ALTER TABLE users RENAME COLUMN name TO full_name;
```

### Drop Table
```sql
-- Drop table
DROP TABLE IF EXISTS users;

-- Drop all tables (using schema)
SELECT 'DROP TABLE IF EXISTS ' || name || ';'
FROM sqlite_master
WHERE type = 'table';
```

## Data Manipulation

### Insert Data
```sql
-- Single row insert
INSERT INTO users (name, email) 
VALUES ('John Doe', 'john@example.com');

-- Multiple row insert
INSERT INTO users (name, email) VALUES 
    ('Jane Doe', 'jane@example.com'),
    ('Bob Smith', 'bob@example.com');

-- Insert from select
INSERT INTO users_backup 
SELECT * FROM users;
```

### Update Data
```sql
-- Basic update
UPDATE users 
SET name = 'John Smith' 
WHERE id = 1;

-- Update with case
UPDATE users 
SET status = CASE 
    WHEN age >= 18 THEN 'adult'
    ELSE 'minor'
END;

-- Update from another table
UPDATE orders 
SET amount = amount * 1.1
WHERE user_id IN (SELECT id FROM users WHERE country = 'US');
```

### Delete Data
```sql
-- Delete specific rows
DELETE FROM users WHERE id = 1;

-- Delete all rows
DELETE FROM users;

-- Delete with subquery
DELETE FROM orders 
WHERE user_id IN (SELECT id FROM users WHERE status = 'inactive');
```

## Querying Data

### Basic Queries
```sql
-- Select all columns
SELECT * FROM users;

-- Select specific columns
SELECT name, email FROM users;

-- Select with conditions
SELECT * FROM users 
WHERE age >= 18 AND country = 'US';

-- Select distinct values
SELECT DISTINCT country FROM users;
```

### Joins
```sql
-- Inner join
SELECT u.name, o.amount 
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- Left join
SELECT u.name, o.amount 
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;

-- Cross join
SELECT u.name, p.name 
FROM users u
CROSS JOIN products p;
```

### Aggregation
```sql
-- Basic aggregation
SELECT 
    COUNT(*) as total_users,
    AVG(age) as avg_age,
    MAX(created_at) as latest_user
FROM users;

-- Group by
SELECT 
    country,
    COUNT(*) as user_count,
    AVG(age) as avg_age
FROM users
GROUP BY country
HAVING COUNT(*) > 10;
```

### Subqueries
```sql
-- Subquery in SELECT
SELECT name,
    (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count
FROM users;

-- Subquery in WHERE
SELECT * FROM users 
WHERE id IN (SELECT user_id FROM orders WHERE amount > 1000);

-- Subquery in FROM
SELECT avg_amount, country
FROM (
    SELECT AVG(amount) as avg_amount, country
    FROM orders o
    JOIN users u ON o.user_id = u.id
    GROUP BY country
) t;
```

## Indexes

### Create Indexes
```sql
-- Single column index
CREATE INDEX idx_users_email ON users(email);

-- Unique index
CREATE UNIQUE INDEX idx_users_email ON users(email);

-- Multi-column index
CREATE INDEX idx_users_name_email ON users(name, email);

-- Partial index
CREATE INDEX idx_active_users ON users(name) 
WHERE status = 'active';
```

### Manage Indexes
```sql
-- List indexes
SELECT name FROM sqlite_master 
WHERE type = 'index';

-- Drop index
DROP INDEX IF EXISTS idx_users_email;
```

## Transactions

### Basic Transaction
```sql
-- Start transaction
BEGIN TRANSACTION;

-- Commit changes
COMMIT;

-- Rollback changes
ROLLBACK;
```

### Python Transaction Example
```python
conn = sqlite3.connect('database.db')
try:
    conn.execute('BEGIN')
    conn.execute('INSERT INTO users (name) VALUES (?)', ('John',))
    conn.execute('INSERT INTO orders (user_id) VALUES (?)', (1,))
    conn.commit()
except:
    conn.rollback()
    raise
finally:
    conn.close()
```

## Views

### Create Views
```sql
-- Simple view
CREATE VIEW active_users AS
SELECT * FROM users WHERE status = 'active';

-- Complex view
CREATE VIEW user_stats AS
SELECT 
    u.name,
    COUNT(o.id) as order_count,
    SUM(o.amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;
```

### Manage Views
```sql
-- List views
SELECT name FROM sqlite_master 
WHERE type = 'view';

-- Drop view
DROP VIEW IF EXISTS active_users;
```

## Common Functions

### Text Functions
```sql
-- String manipulation
SELECT 
    LOWER(name),
    UPPER(name),
    LENGTH(name),
    SUBSTR(name, 1, 3),
    REPLACE(name, ' ', '_'),
    TRIM(name)
FROM users;
```

### Date/Time Functions
```sql
-- Date/time operations
SELECT 
    DATE('now'),
    DATETIME('now', 'localtime'),
    STRFTIME('%Y-%m-%d', created_at),
    STRFTIME('%Y-%m-%d', 'now', '-1 day')
FROM users;
```

### Aggregate Functions
```sql
SELECT
    COUNT(*),
    SUM(amount),
    AVG(amount),
    MIN(amount),
    MAX(amount),
    GROUP_CONCAT(name, ', ')
FROM orders;
```

## Performance Tips

### Optimization
```sql
-- Add EXPLAIN to analyze query
EXPLAIN QUERY PLAN
SELECT * FROM users WHERE email = 'john@example.com';

-- Use prepared statements
-- Python example
cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))

-- Use transactions for bulk operations
BEGIN TRANSACTION;
INSERT INTO users ...;
INSERT INTO users ...;
COMMIT;
```

### Maintenance
```sql
-- Rebuild database to reclaim space
VACUUM;

-- Analyze tables for query optimization
ANALYZE;

-- Reindex for better performance
REINDEX;
```

## Python Integration

### Basic Operations
```python
import sqlite3

# Connect to database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Execute query
cursor.execute('SELECT * FROM users WHERE age > ?', (18,))
results = cursor.fetchall()

# Insert with parameters
cursor.execute('''
    INSERT INTO users (name, email, age) 
    VALUES (?, ?, ?)
''', ('John', 'john@example.com', 25))

# Commit and close
conn.commit()
conn.close()
```

### Advanced Usage
```python
# Context manager
with sqlite3.connect('database.db') as conn:
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    
# Row factory for dictionary results
def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

conn.row_factory = dict_factory

# Custom aggregation
class Median:
    def __init__(self):
        self.values = []
    
    def step(self, value):
        self.values.append(value)
    
    def finalize(self):
        size = len(self.values)
        if size == 0:
            return None
        self.values.sort()
        if size % 2 == 0:
            return (self.values[size//2-1] + self.values[size//2]) / 2
        return self.values[size//2]

conn.create_aggregate("median", 1, Median)
```

## Backup and Restore

### Command Line
```bash
# Backup
sqlite3 database.db .dump > backup.sql

# Restore
sqlite3 database.db < backup.sql

# Online backup
sqlite3 database.db ".backup 'backup.db'"
```

### Python Backup
```python
import sqlite3
import shutil
from datetime import datetime

def backup_database(db_path):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f'backup_{timestamp}.db'
    
    # Connection to source database
    conn = sqlite3.connect(db_path)
    
    # Create backup
    backup = sqlite3.connect(backup_path)
    conn.backup(backup)
    
    # Close connections
    backup.close()
    conn.close()
