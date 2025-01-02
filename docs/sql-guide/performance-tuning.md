# Database Performance Tuning Guide

## Table of Contents
- [Database Performance Tuning Guide](#database-performance-tuning-guide)
  - [Understanding Performance](#understanding-performance)
    - [Key Performance Indicators (KPIs)](#key-performance-indicators-kpis)
  - [Query Optimization](#query-optimization)
    - [1. EXPLAIN Command](#1-explain-command)
    - [2. Index Optimization](#2-index-optimization)
    - [3. Query Rewriting](#3-query-rewriting)
  - [System Configuration](#system-configuration)
    - [1. MySQL/MariaDB Configuration](#1-mysql/mariadb-configuration)
- [my.cnf optimizations](#mycnf-optimizations)
- [Buffer Pool Size (70-80% of available RAM)](#buffer-pool-size-70-80%-of-available-ram)
- [Read/Write Optimization](#read/write-optimization)
- [Query Cache (if using MySQL < 8.0)](#query-cache-if-using-mysql-<-80)
- [Connection Settings](#connection-settings)
    - [2. Oracle Configuration](#2-oracle-configuration)
  - [Table Optimization](#table-optimization)
    - [1. Table Structure](#1-table-structure)
    - [2. Partitioning](#2-partitioning)
  - [Monitoring and Analysis](#monitoring-and-analysis)
    - [1. Performance Monitoring](#1-performance-monitoring)
    - [2. Slow Query Analysis](#2-slow-query-analysis)
  - [Performance Testing](#performance-testing)
    - [1. Load Testing Script](#1-load-testing-script)
- [Run multiple threads](#run-multiple-threads)
    - [2. Query Performance Metrics](#2-query-performance-metrics)
  - [Memory Optimization](#memory-optimization)
    - [1. Buffer Pool Management](#1-buffer-pool-management)
    - [2. Query Cache (MySQL < 8.0)](#2-query-cache-mysql-<-80)
  - [Connection Pool Management](#connection-pool-management)
    - [1. Database Connection Pool](#1-database-connection-pool)
- [Usage](#usage)
    - [2. Connection Monitoring](#2-connection-monitoring)
  - [Regular Maintenance Tasks](#regular-maintenance-tasks)
    - [Daily Tasks](#daily-tasks)
    - [Weekly Tasks](#weekly-tasks)
    - [Monthly Tasks](#monthly-tasks)
  - [Emergency Performance Fixes](#emergency-performance-fixes)
    - [1. Immediate Actions](#1-immediate-actions)
    - [2. Quick Optimizations](#2-quick-optimizations)
  - [Performance Monitoring Tools](#performance-monitoring-tools)
    - [1. Built-in Tools](#1-built-in-tools)
    - [2. External Monitoring](#2-external-monitoring)
- [Create metrics](#create-metrics)
- [Start metrics server](#start-metrics-server)



## Understanding Performance

### Key Performance Indicators (KPIs)
1. Query response time
2. Throughput (queries per second)
3. Resource utilization
4. Wait times
5. Buffer hit ratio

## Query Optimization

### 1. EXPLAIN Command
```sql
-- MySQL/MariaDB
EXPLAIN SELECT * FROM users WHERE email = 'user@example.com';

-- Oracle
EXPLAIN PLAN FOR
SELECT * FROM users WHERE email = 'user@example.com';
SELECT * FROM TABLE(DBMS_XPLAN.DISPLAY);
```

### 2. Index Optimization
```sql
-- Create optimal indexes
CREATE INDEX idx_email ON users(email);

-- Composite indexes for multiple columns
CREATE INDEX idx_name_email ON users(last_name, first_name, email);

-- Analyze index usage
SELECT 
    index_name,
    table_name,
    stat_name,
    stat_value
FROM performance_schema.table_statistics;
```

### 3. Query Rewriting
```sql
-- Bad Query (Full table scan)
SELECT * FROM orders WHERE YEAR(order_date) = 2023;

-- Good Query (Can use index)
SELECT * FROM orders 
WHERE order_date >= '2023-01-01' 
AND order_date < '2024-01-01';

-- Bad Query (Function on column)
SELECT * FROM users WHERE LOWER(email) = 'user@example.com';

-- Good Query (No function on column)
SELECT * FROM users WHERE email = 'user@example.com';
```

## System Configuration

### 1. MySQL/MariaDB Configuration
```ini
# my.cnf optimizations

# Buffer Pool Size (70-80% of available RAM)
innodb_buffer_pool_size = 12G

# Read/Write Optimization
innodb_read_io_threads = 8
innodb_write_io_threads = 8
innodb_flush_log_at_trx_commit = 2

# Query Cache (if using MySQL < 8.0)
query_cache_type = 1
query_cache_size = 128M

# Connection Settings
max_connections = 1000
thread_cache_size = 128
```

### 2. Oracle Configuration
```sql
-- Memory Management
ALTER SYSTEM SET sga_max_size = 12G;
ALTER SYSTEM SET pga_aggregate_target = 4G;

-- Optimizer Settings
ALTER SYSTEM SET optimizer_mode = 'ALL_ROWS';
ALTER SYSTEM SET optimizer_index_cost_adj = 50;
```

## Table Optimization

### 1. Table Structure
```sql
-- Use appropriate data types
CREATE TABLE users (
    id INT UNSIGNED AUTO_INCREMENT, -- Instead of BIGINT if not needed
    email VARCHAR(255),            -- Instead of TEXT for emails
    created_at TIMESTAMP,          -- Instead of VARCHAR for dates
    PRIMARY KEY (id)
);

-- Add appropriate constraints
ALTER TABLE users
ADD CONSTRAINT unique_email UNIQUE (email),
ADD CONSTRAINT valid_email CHECK (email LIKE '%@%.%');
```

### 2. Partitioning
```sql
-- Range Partitioning
CREATE TABLE orders (
    id INT,
    order_date DATE,
    amount DECIMAL(10,2)
)
PARTITION BY RANGE (YEAR(order_date)) (
    PARTITION p2021 VALUES LESS THAN (2022),
    PARTITION p2022 VALUES LESS THAN (2023),
    PARTITION p2023 VALUES LESS THAN (2024)
);

-- List Partitioning
CREATE TABLE sales (
    id INT,
    region VARCHAR(50),
    amount DECIMAL(10,2)
)
PARTITION BY LIST (region) (
    PARTITION p_east VALUES IN ('NY', 'NJ', 'CT'),
    PARTITION p_west VALUES IN ('CA', 'OR', 'WA')
);
```

## Monitoring and Analysis

### 1. Performance Monitoring
```sql
-- MySQL/MariaDB: Show running queries
SELECT 
    id,
    user,
    host,
    db,
    command,
    time,
    state,
    info
FROM information_schema.processlist
WHERE command != 'Sleep';

-- Oracle: Active Sessions
SELECT 
    sid,
    serial#,
    username,
    program,
    sql_id,
    event,
    seconds_in_wait
FROM v$session
WHERE status = 'ACTIVE';
```

### 2. Slow Query Analysis
```sql
-- MySQL/MariaDB: Enable slow query log
SET GLOBAL slow_query_log = 1;
SET GLOBAL long_query_time = 2;

-- Find slow queries
SELECT 
    start_time,
    query_time,
    sql_text
FROM mysql.slow_log
ORDER BY query_time DESC
LIMIT 10;
```

## Performance Testing

### 1. Load Testing Script
```python
import mysql.connector
import time
import threading

def run_test_query(thread_id, iterations):
    conn = mysql.connector.connect(
        host="localhost",
        user="test_user",
        password="password",
        database="test_db"
    )
    cursor = conn.cursor()
    
    start_time = time.time()
    for i in range(iterations):
        cursor.execute("SELECT * FROM large_table WHERE id > %s", (i,))
        cursor.fetchall()
    
    duration = time.time() - start_time
    print(f"Thread {thread_id}: {iterations} queries in {duration:.2f} seconds")
    
    cursor.close()
    conn.close()

# Run multiple threads
threads = []
for i in range(10):
    t = threading.Thread(target=run_test_query, args=(i, 1000))
    threads.append(t)
    t.start()

for t in threads:
    t.join()
```

### 2. Query Performance Metrics
```python
def measure_query_performance(query, iterations=1000):
    conn = mysql.connector.connect(
        host="localhost",
        user="test_user",
        password="password",
        database="test_db"
    )
    cursor = conn.cursor()
    
    times = []
    for _ in range(iterations):
        start = time.time()
        cursor.execute(query)
        cursor.fetchall()
        times.append(time.time() - start)
    
    return {
        'min': min(times),
        'max': max(times),
        'avg': sum(times) / len(times),
        'p95': sorted(times)[int(len(times) * 0.95)]
    }
```

## Memory Optimization

### 1. Buffer Pool Management
```sql
-- MySQL/MariaDB: Monitor buffer pool
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool_%';

-- Optimize buffer pool size
SET GLOBAL innodb_buffer_pool_size = 12884901888; -- 12GB
```

### 2. Query Cache (MySQL < 8.0)
```sql
-- Enable query cache
SET GLOBAL query_cache_type = 1;
SET GLOBAL query_cache_size = 134217728; -- 128MB

-- Monitor cache effectiveness
SHOW GLOBAL STATUS LIKE 'Qcache_%';
```

## Connection Pool Management

### 1. Database Connection Pool
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

def create_connection_pool():
    return create_engine(
        'mysql://user:pass@localhost/db',
        poolclass=QueuePool,
        pool_size=20,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )

# Usage
engine = create_connection_pool()
with engine.connect() as conn:
    result = conn.execute("SELECT * FROM users")
```

### 2. Connection Monitoring
```sql
-- MySQL/MariaDB: Monitor connections
SHOW STATUS WHERE Variable_name LIKE 'Threads_%'
OR Variable_name LIKE 'Connections';

-- Kill idle connections
SELECT 
    concat('KILL ', id, ';') 
FROM information_schema.processlist 
WHERE command = 'Sleep' 
AND time > 3600;
```

## Regular Maintenance Tasks

### Daily Tasks
1. Monitor slow query log
2. Check buffer pool hit ratio
3. Review active connections
4. Analyze wait events

### Weekly Tasks
1. Update table statistics
2. Review index usage
3. Clean up temporary tables
4. Optimize buffer pool size

### Monthly Tasks
1. Full system performance review
2. Capacity planning
3. Query optimization review
4. Index maintenance

## Emergency Performance Fixes

### 1. Immediate Actions
```sql
-- Kill long-running queries
SELECT concat('KILL ', id, ';')
FROM information_schema.processlist
WHERE time > 300;

-- Clear query cache
FLUSH QUERY CACHE;
RESET QUERY CACHE;

-- Free up memory
FLUSH TABLES;
FLUSH STATUS;
```

### 2. Quick Optimizations
```sql
-- Add emergency index
CREATE INDEX CONCURRENTLY idx_emergency 
ON problem_table(problem_column);

-- Optimize table
OPTIMIZE TABLE problem_table;

-- Update statistics
ANALYZE TABLE problem_table;
```

## Performance Monitoring Tools

### 1. Built-in Tools
```sql
-- MySQL/MariaDB Performance Schema
UPDATE performance_schema.setup_instruments 
SET ENABLED = 'YES', TIMED = 'YES';

UPDATE performance_schema.setup_consumers 
SET ENABLED = 'YES';

-- Oracle AWR Reports
BEGIN
    DBMS_WORKLOAD_REPOSITORY.create_snapshot();
END;
/
```

### 2. External Monitoring
```python
import prometheus_client
from prometheus_client import start_http_server, Gauge

# Create metrics
query_time = Gauge('database_query_time_seconds', 
                  'Time taken for query execution')
connection_count = Gauge('database_connections', 
                        'Number of active connections')

def collect_metrics():
    while True:
        # Measure query time
        with query_time.time():
            execute_test_query()
            
        # Count connections
        connection_count.set(get_connection_count())
        time.sleep(60)

# Start metrics server
start_http_server(8000)
