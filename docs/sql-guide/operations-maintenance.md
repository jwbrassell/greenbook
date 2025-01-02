# Database Operations and Maintenance Guide

## Table of Contents
- [Database Operations and Maintenance Guide](#database-operations-and-maintenance-guide)
  - [Monitoring Your Database](#monitoring-your-database)
    - [Key Metrics to Watch](#key-metrics-to-watch)
    - [Setting Up Monitoring Tools](#setting-up-monitoring-tools)
  - [Database Variables](#database-variables)
    - [MySQL/MariaDB Important Variables](#mysql/mariadb-important-variables)
    - [Oracle Important Parameters](#oracle-important-parameters)
  - [User Management](#user-management)
    - [Creating Users](#creating-users)
    - [Managing Permissions](#managing-permissions)
  - [Table Operations](#table-operations)
    - [Table Maintenance](#table-maintenance)
    - [Managing Indexes](#managing-indexes)
  - [Backup Procedures](#backup-procedures)
    - [MySQL Backup](#mysql-backup)
- [Full backup](#full-backup)
- [Single database backup](#single-database-backup)
- [Automated backup script](#automated-backup-script)
- [!/bin/bash](#!/bin/bash)
    - [Oracle Backup](#oracle-backup)
  - [Logging Setup](#logging-setup)
    - [MySQL Logging](#mysql-logging)
- [my.cnf configuration](#mycnf-configuration)
    - [Oracle Logging](#oracle-logging)
  - [Performance Tuning](#performance-tuning)
    - [Query Optimization](#query-optimization)
    - [System Configuration](#system-configuration)
- [MySQL configuration optimization](#mysql-configuration-optimization)
    - [Connection Pool Setup](#connection-pool-setup)
- [Python connection pooling example](#python-connection-pooling-example)
  - [Monitoring Scripts](#monitoring-scripts)
    - [Basic Health Check Script](#basic-health-check-script)
  - [Regular Maintenance Tasks](#regular-maintenance-tasks)
    - [Daily Tasks](#daily-tasks)
    - [Weekly Tasks](#weekly-tasks)
    - [Monthly Tasks](#monthly-tasks)
  - [Emergency Procedures](#emergency-procedures)
    - [Database Won't Start](#database-won't-start)
    - [Performance Issues](#performance-issues)
  - [Best Practices](#best-practices)



## Monitoring Your Database

### Key Metrics to Watch

1. **System Resources**
   ```sql
   -- MySQL: Check system variables
   SHOW GLOBAL STATUS;
   
   -- Check connected users
   SELECT user, host, db FROM information_schema.processlist;
   ```

2. **Query Performance**
   ```sql
   -- Find slow queries in MySQL
   SHOW FULL PROCESSLIST;
   
   -- Enable slow query log
   SET GLOBAL slow_query_log = 'ON';
   SET GLOBAL long_query_time = 2;
   ```

### Setting Up Monitoring Tools

1. **MySQL Enterprise Monitor**
   - Watches your database 24/7
   - Sends alerts if something's wrong
   - Shows performance graphs

2. **Prometheus + Grafana**
   ```yaml
   # prometheus.yml example
   scrape_configs:
     - job_name: 'mysql'
       static_configs:
         - targets: ['localhost:9104']
   ```

## Database Variables

### MySQL/MariaDB Important Variables
```sql
-- Show all variables
SHOW VARIABLES;

-- Common variables to tune
SET GLOBAL max_connections = 1000;
SET GLOBAL innodb_buffer_pool_size = 1073741824; -- 1GB
SET GLOBAL query_cache_size = 67108864; -- 64MB
```

### Oracle Important Parameters
```sql
-- Show parameters
SELECT name, value FROM v$parameter;

-- Common parameters
ALTER SYSTEM SET processes=300 SCOPE=SPFILE;
ALTER SYSTEM SET sga_max_size=2G SCOPE=SPFILE;
```

## User Management

### Creating Users
```sql
-- MySQL
CREATE USER 'webapp'@'localhost' IDENTIFIED BY 'password123';

-- Oracle
CREATE USER webapp IDENTIFIED BY password123;
```

### Managing Permissions
```sql
-- MySQL: Grant permissions
GRANT SELECT, INSERT ON database_name.* TO 'webapp'@'localhost';

-- Oracle: Grant permissions
GRANT CREATE SESSION TO webapp;
GRANT SELECT ON schema.table TO webapp;
```

## Table Operations

### Table Maintenance
```sql
-- MySQL: Optimize table
OPTIMIZE TABLE my_table;

-- MySQL: Analyze table
ANALYZE TABLE my_table;

-- Oracle: Gather statistics
EXEC DBMS_STATS.GATHER_TABLE_STATS('schema', 'table_name');
```

### Managing Indexes
```sql
-- Create index
CREATE INDEX idx_name ON table_name(column_name);

-- Show indexes
SHOW INDEX FROM table_name; -- MySQL
SELECT * FROM user_indexes; -- Oracle
```

## Backup Procedures

### MySQL Backup
```bash
# Full backup
mysqldump -u root -p --all-databases > backup.sql

# Single database backup
mysqldump -u root -p database_name > database_backup.sql

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
mysqldump -u root -p --all-databases > backup_$DATE.sql
gzip backup_$DATE.sql
```

### Oracle Backup
```sql
-- RMAN backup commands
BACKUP DATABASE;
BACKUP DATABASE PLUS ARCHIVELOG;
```

## Logging Setup

### MySQL Logging
```ini
# my.cnf configuration
[mysqld]
log_error = /var/log/mysql/error.log
slow_query_log = 1
slow_query_log_file = /var/log/mysql/slow.log
long_query_time = 2
```

### Oracle Logging
```sql
-- Enable archive logging
ALTER DATABASE ARCHIVELOG;

-- Set up audit logging
AUDIT SELECT TABLE BY ACCESS;
```

## Performance Tuning

### Query Optimization
```sql
-- Analyze query performance
EXPLAIN SELECT * FROM large_table WHERE id > 1000;

-- Add missing indexes
CREATE INDEX idx_column ON table(column);

-- Update statistics
ANALYZE TABLE table_name;
```

### System Configuration
```ini
# MySQL configuration optimization
innodb_buffer_pool_size = 70% of available RAM
innodb_log_file_size = 256M
innodb_flush_log_at_trx_commit = 2
```

### Connection Pool Setup
```python
# Python connection pooling example
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine('mysql://user:pass@localhost/db',
                      poolclass=QueuePool,
                      pool_size=10,
                      max_overflow=20,
                      pool_timeout=30)
```

## Monitoring Scripts

### Basic Health Check Script
```python
import mysql.connector
import smtplib

def check_database_health():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="monitor",
            password="password",
            database="mysql"
        )
        cursor = conn.cursor()
        
        # Check connections
        cursor.execute("SHOW STATUS LIKE 'Threads_connected'")
        connections = cursor.fetchone()[1]
        
        # Check slow queries
        cursor.execute("SHOW GLOBAL STATUS LIKE 'Slow_queries'")
        slow_queries = cursor.fetchone()[1]
        
        # Alert if thresholds exceeded
        if int(connections) > 100 or int(slow_queries) > 50:
            send_alert_email()
            
    except Exception as e:
        send_alert_email(str(e))
    finally:
        conn.close()
```

## Regular Maintenance Tasks

### Daily Tasks
1. Check error logs
2. Monitor disk space
3. Review slow query log
4. Verify backup completion

### Weekly Tasks
1. Analyze table statistics
2. Review user permissions
3. Check index usage
4. Clean up temporary tables

### Monthly Tasks
1. Review security patches
2. Analyze long-term performance trends
3. Update documentation
4. Test backup recovery

## Emergency Procedures

### Database Won't Start
1. Check error logs
2. Verify disk space
3. Check file permissions
4. Try recovery mode

### Performance Issues
1. Kill long-running queries
2. Clear query cache
3. Restart if necessary
4. Add emergency indexes

## Best Practices

1. **Regular Backups**
   - Daily full backups
   - Point-in-time recovery setup
   - Regular backup testing

2. **Security**
   - Regular security audits
   - Strong password policies
   - Minimal privilege assignments

3. **Monitoring**
   - Set up automated monitoring
   - Configure alerts
   - Regular performance reviews

4. **Documentation**
   - Keep change logs
   - Document configurations
   - Maintain recovery procedures
