# Database Layer Troubleshooting

## Table of Contents
- [Database Layer Troubleshooting](#database-layer-troubleshooting)
  - [Table of Contents](#table-of-contents)
  - [Common Database Issues](#common-database-issues)
    - [Connection Problems](#connection-problems)
- [Check database service status](#check-database-service-status)
- [Check connections](#check-connections)
- [Check max connections](#check-max-connections)
- [Check service status](#check-service-status)
- [Check connections](#check-connections)
- [Connection settings](#connection-settings)
    - [Performance Issues](#performance-issues)
- [Show slow queries](#show-slow-queries)
- [Query performance](#query-performance)
- [Table statistics](#table-statistics)
- [Query analysis](#query-analysis)
- [Table statistics](#table-statistics)
- [Index usage](#index-usage)
    - [Backup and Recovery](#backup-and-recovery)
- [Create backup](#create-backup)
- [Compressed backup](#compressed-backup)
- [Restore from backup](#restore-from-backup)
- [Create backup](#create-backup)
- [Custom format backup](#custom-format-backup)
- [Restore from backup](#restore-from-backup)
  - [Database Maintenance](#database-maintenance)
    - [Index Management](#index-management)
- [Show indexes](#show-indexes)
- [Add index](#add-index)
- [Analyze index usage](#analyze-index-usage)
- [Show indexes](#show-indexes)
- [Index maintenance](#index-maintenance)
- [Find unused indexes](#find-unused-indexes)
    - [Storage Management](#storage-management)
- [Check table sizes](#check-table-sizes)
- [Optimize tables](#optimize-tables)
- [Database size](#database-size)
- [Table sizes](#table-sizes)
  - [Common Problems and Solutions](#common-problems-and-solutions)
    - [High CPU Usage](#high-cpu-usage)
    - [Memory Issues](#memory-issues)
- [MySQL (/etc/mysql/my.cnf)](#mysql-/etc/mysql/mycnf)
- [PostgreSQL (postgresql.conf)](#postgresql-postgresqlconf)
    - [Disk I/O Problems](#disk-i/o-problems)
- [Check I/O stats](#check-i/o-stats)
- [MySQL specific](#mysql-specific)
- [MySQL](#mysql)
- [PostgreSQL](#postgresql)
  - [Monitoring and Prevention](#monitoring-and-prevention)
    - [Setting Up Monitoring](#setting-up-monitoring)
- [Install monitoring tools](#install-monitoring-tools)
- [Database specific exporters](#database-specific-exporters)
    - [Best Practices](#best-practices)
- [Schedule regular backups](#schedule-regular-backups)
- [Monitor log files](#monitor-log-files)
  - [Recovery Procedures](#recovery-procedures)
    - [Data Corruption](#data-corruption)
- [Stop database](#stop-database)
- [Check logs for errors](#check-logs-for-errors)
- [Restore from backup if needed](#restore-from-backup-if-needed)
    - [Transaction Recovery](#transaction-recovery)
  - [Documentation](#documentation)



## Common Database Issues

### Connection Problems

**Symptoms:**
- Connection timeout
- Connection refused
- Authentication failure
- Too many connections

**MySQL/MariaDB Commands:**
```bash
# Check database service status
systemctl status mysql
journalctl -u mysql

# Check connections
mysqladmin -u root -p processlist
SHOW PROCESSLIST;

# Check max connections
SHOW VARIABLES LIKE 'max_connections';
SHOW STATUS LIKE '%onn%';
```

**PostgreSQL Commands:**
```bash
# Check service status
systemctl status postgresql

# Check connections
SELECT * FROM pg_stat_activity;

# Connection settings
SHOW max_connections;
SHOW superuser_reserved_connections;
```

### Performance Issues

**Symptoms:**
- Slow queries
- High CPU usage
- Memory pressure
- Disk I/O bottlenecks

**MySQL Performance Analysis:**
```bash
# Show slow queries
SHOW GLOBAL VARIABLES LIKE '%slow%';
SHOW GLOBAL STATUS LIKE '%slow%';

# Query performance
EXPLAIN SELECT * FROM table WHERE condition;
SHOW PROFILE FOR QUERY query_id;

# Table statistics
SHOW TABLE STATUS;
ANALYZE TABLE table_name;
```

**PostgreSQL Performance Analysis:**
```bash
# Query analysis
EXPLAIN ANALYZE SELECT * FROM table WHERE condition;

# Table statistics
ANALYZE table_name;
SELECT * FROM pg_stat_user_tables;

# Index usage
SELECT * FROM pg_stat_user_indexes;
```

### Backup and Recovery

**MySQL Backup Commands:**
```bash
# Create backup
mysqldump -u root -p database_name > backup.sql
mysqldump -u root -p --all-databases > full_backup.sql

# Compressed backup
mysqldump -u root -p database_name | gzip > backup.sql.gz

# Restore from backup
mysql -u root -p database_name < backup.sql
zcat backup.sql.gz | mysql -u root -p database_name
```

**PostgreSQL Backup Commands:**
```bash
# Create backup
pg_dump dbname > backup.sql
pg_dumpall > full_backup.sql

# Custom format backup
pg_dump -Fc dbname > backup.dump

# Restore from backup
psql dbname < backup.sql
pg_restore -d dbname backup.dump
```

## Database Maintenance

### Index Management

**MySQL Index Operations:**
```bash
# Show indexes
SHOW INDEX FROM table_name;

# Add index
CREATE INDEX idx_name ON table_name (column_name);

# Analyze index usage
SELECT * FROM sys.schema_unused_indexes;
SELECT * FROM sys.schema_redundant_indexes;
```

**PostgreSQL Index Operations:**
```bash
# Show indexes
\d table_name

# Index maintenance
REINDEX TABLE table_name;
VACUUM ANALYZE table_name;

# Find unused indexes
SELECT * FROM pg_stat_user_indexes WHERE idx_scan = 0;
```

### Storage Management

**MySQL Storage Issues:**
```bash
# Check table sizes
SELECT 
    table_name,
    round(((data_length + index_length) / 1024 / 1024), 2) AS "Size (MB)"
FROM information_schema.TABLES
ORDER BY (data_length + index_length) DESC;

# Optimize tables
OPTIMIZE TABLE table_name;
```

**PostgreSQL Storage Issues:**
```bash
# Database size
SELECT pg_size_pretty(pg_database_size('dbname'));

# Table sizes
SELECT
    relname as table_name,
    pg_size_pretty(pg_total_relation_size(relid)) as total_size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

## Common Problems and Solutions

### High CPU Usage

1. **Identify Resource-Intensive Queries:**
```sql
-- MySQL
SELECT * FROM information_schema.PROCESSLIST
WHERE command != 'Sleep'
ORDER BY time DESC;

-- PostgreSQL
SELECT pid, query, state
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start DESC;
```

2. **Optimize Queries:**
```sql
-- Add appropriate indexes
CREATE INDEX idx_name ON table (column);

-- Update statistics
ANALYZE table_name;

-- Review and optimize query plans
EXPLAIN ANALYZE SELECT ...;
```

### Memory Issues

1. **Check Buffer Usage:**
```sql
-- MySQL
SHOW GLOBAL VARIABLES LIKE 'innodb_buffer_pool%';
SHOW GLOBAL STATUS LIKE 'Innodb_buffer_pool%';

-- PostgreSQL
SHOW shared_buffers;
SELECT * FROM pg_stat_bgwriter;
```

2. **Adjust Memory Settings:**
```bash
# MySQL (/etc/mysql/my.cnf)
innodb_buffer_pool_size = 4G
innodb_buffer_pool_instances = 4

# PostgreSQL (postgresql.conf)
shared_buffers = 2GB
work_mem = 16MB
```

### Disk I/O Problems

1. **Monitor I/O Usage:**
```bash
# Check I/O stats
iostat -x 1
iotop

# MySQL specific
SHOW GLOBAL STATUS LIKE '%innodb_data_read%';
```

2. **Optimize I/O Settings:**
```bash
# MySQL
innodb_io_capacity = 2000
innodb_write_io_threads = 8
innodb_read_io_threads = 8

# PostgreSQL
effective_io_concurrency = 200
random_page_cost = 1.1
```

## Monitoring and Prevention

### Setting Up Monitoring

1. **System Monitoring:**
```bash
# Install monitoring tools
apt-get install prometheus node_exporter
apt-get install grafana

# Database specific exporters
apt-get install prometheus-mysqld-exporter
apt-get install prometheus-postgres-exporter
```

2. **Key Metrics to Monitor:**
- Connection counts
- Query response times
- Buffer pool usage
- Disk I/O rates
- Cache hit ratios
- Transaction rates

### Best Practices

1. **Regular Maintenance:**
```bash
# Schedule regular backups
0 2 * * * /usr/local/bin/backup-database.sh

# Monitor log files
tail -f /var/log/mysql/error.log
tail -f /var/log/postgresql/postgresql-main.log
```

2. **Performance Tuning:**
- Regular ANALYZE/OPTIMIZE operations
- Index maintenance
- Query optimization
- Configuration tuning

3. **Security Measures:**
```sql
-- Regular user audit
SELECT user, host FROM mysql.user;

-- Review permissions
SHOW GRANTS FOR 'user'@'host';

-- Update passwords regularly
ALTER USER 'user'@'host' IDENTIFIED BY 'new_password';
```

## Recovery Procedures

### Data Corruption

1. **Check Data Integrity:**
```sql
-- MySQL
CHECK TABLE table_name;
REPAIR TABLE table_name;

-- PostgreSQL
SELECT * FROM pg_stat_database_conflicts;
```

2. **Recovery Steps:**
```bash
# Stop database
systemctl stop mysql
systemctl stop postgresql

# Check logs for errors
tail -f /var/log/mysql/error.log

# Restore from backup if needed
mysql -u root -p < backup.sql
```

### Transaction Recovery

1. **Check Transaction Status:**
```sql
-- MySQL
SHOW ENGINE INNODB STATUS;

-- PostgreSQL
SELECT * FROM pg_prepared_xacts;
```

2. **Handle Dead Locks:**
```sql
-- Identify blocked queries
SELECT * FROM information_schema.INNODB_TRX;

-- Kill blocking sessions if necessary
KILL connection_id;
```

## Documentation

1. **Maintain Documentation:**
- Database schema diagrams
- Backup procedures
- Recovery plans
- Performance baselines

2. **Change Management:**
- Track configuration changes
- Document optimization efforts
- Keep upgrade history
- Monitor performance trends
