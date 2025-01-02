# Database Backup and Recovery Guide

## Table of Contents
- [Database Backup and Recovery Guide](#database-backup-and-recovery-guide)
  - [Types of Backups](#types-of-backups)
    - [1. Full Backups](#1-full-backups)
- [MySQL/MariaDB](#mysql/mariadb)
- [Oracle](#oracle)
- [SQLite](#sqlite)
    - [2. Incremental Backups](#2-incremental-backups)
    - [3. Differential Backups](#3-differential-backups)
  - [Automated Backup Scripts](#automated-backup-scripts)
    - [1. Daily MySQL Backup Script](#1-daily-mysql-backup-script)
- [!/bin/bash](#!/bin/bash)
- [Configuration](#configuration)
- [Create backup directory if it doesn't exist](#create-backup-directory-if-it-doesn't-exist)
- [Generate filename with timestamp](#generate-filename-with-timestamp)
- [Perform backup](#perform-backup)
- [Remove old backups](#remove-old-backups)
    - [2. Oracle Automated Backup](#2-oracle-automated-backup)
  - [Backup Verification](#backup-verification)
    - [1. Test MySQL Backup](#1-test-mysql-backup)
- [Create test database](#create-test-database)
- [Restore backup to test database](#restore-backup-to-test-database)
- [Verify data](#verify-data)
    - [2. Test Oracle Backup](#2-test-oracle-backup)
  - [Recovery Procedures](#recovery-procedures)
    - [1. Full Database Recovery](#1-full-database-recovery)
    - [2. Point-in-Time Recovery](#2-point-in-time-recovery)
    - [3. Table-Level Recovery](#3-table-level-recovery)
- [Extract table from backup](#extract-table-from-backup)
- [Restore single table](#restore-single-table)
  - [Backup Strategy Best Practices](#backup-strategy-best-practices)
    - [1. Backup Schedule](#1-backup-schedule)
    - [2. Storage Requirements](#2-storage-requirements)
    - [3. Monitoring Backup Success](#3-monitoring-backup-success)
  - [Disaster Recovery](#disaster-recovery)
    - [1. Recovery Time Objective (RTO)](#1-recovery-time-objective-rto)
    - [2. Recovery Point Objective (RPO)](#2-recovery-point-objective-rpo)
    - [3. Recovery Procedure Documentation](#3-recovery-procedure-documentation)
  - [Backup Security](#backup-security)
    - [1. Encryption](#1-encryption)
- [MySQL backup with encryption](#mysql-backup-with-encryption)
- [Decrypt for recovery](#decrypt-for-recovery)
    - [2. Access Control](#2-access-control)
  - [Cloud Backup Solutions](#cloud-backup-solutions)
    - [1. AWS S3 Backup](#1-aws-s3-backup)
    - [2. Multi-Region Backup](#2-multi-region-backup)
  - [Backup Performance Optimization](#backup-performance-optimization)
    - [1. Parallel Backup](#1-parallel-backup)
- [MySQL parallel backup](#mysql-parallel-backup)
    - [2. Compression](#2-compression)
  - [Recovery Testing Schedule](#recovery-testing-schedule)
    - [Monthly Tests](#monthly-tests)
    - [Quarterly Tests](#quarterly-tests)



## Types of Backups

### 1. Full Backups
Complete copy of your entire database

```bash
# MySQL/MariaDB
mysqldump -u root -p --all-databases > full_backup_$(date +%Y%m%d).sql

# Oracle
expdp system/password full=y directory=DATA_PUMP_DIR \
  dumpfile=full_backup_%date%.dmp logfile=full_backup_%date%.log

# SQLite
sqlite3 database.db ".backup 'backup.db'"
```

### 2. Incremental Backups
Only backup changes since last backup

```sql
-- MySQL/MariaDB with binary logs
FLUSH LOGS;
mysqldump -u root -p --all-databases --single-transaction \
  --flush-logs --master-data=2 > backup.sql

-- Oracle RMAN
BACKUP INCREMENTAL LEVEL 1 DATABASE;
```

### 3. Differential Backups
All changes since last full backup

```sql
-- Oracle RMAN
BACKUP INCREMENTAL LEVEL 0 DATABASE; -- Full backup
BACKUP INCREMENTAL LEVEL 1 CUMULATIVE DATABASE; -- Differential
```

## Automated Backup Scripts

### 1. Daily MySQL Backup Script
```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/var/backups/mysql"
MYSQL_USER="backup_user"
MYSQL_PASSWORD="your_password"
RETENTION_DAYS=7

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Generate filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.sql.gz"

# Perform backup
mysqldump -u $MYSQL_USER -p$MYSQL_PASSWORD --all-databases \
  --single-transaction --quick --lock-tables=false | gzip > $BACKUP_FILE

# Remove old backups
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete
```

### 2. Oracle Automated Backup
```sql
-- Create RMAN backup script
CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 7 DAYS;
CONFIGURE BACKUP OPTIMIZATION ON;

RUN {
  BACKUP DATABASE PLUS ARCHIVELOG;
  DELETE NOPROMPT OBSOLETE;
}
```

## Backup Verification

### 1. Test MySQL Backup
```bash
# Create test database
mysql -u root -p -e "CREATE DATABASE backup_test;"

# Restore backup to test database
gunzip < backup.sql.gz | mysql -u root -p backup_test

# Verify data
mysql -u root -p backup_test -e "SHOW TABLES;"
```

### 2. Test Oracle Backup
```sql
-- Test restore in separate environment
RESTORE DATABASE TEST_DB VALIDATE;
```

## Recovery Procedures

### 1. Full Database Recovery
```sql
-- MySQL/MariaDB
mysql -u root -p < backup.sql

-- Oracle
STARTUP MOUNT;
RESTORE DATABASE;
RECOVER DATABASE;
ALTER DATABASE OPEN;
```

### 2. Point-in-Time Recovery
```sql
-- MySQL/MariaDB
mysqlbinlog binlog.000001 binlog.000002 | \
mysql -u root -p --force

-- Oracle
RECOVER DATABASE UNTIL TIME '2023-12-31 23:59:59';
```

### 3. Table-Level Recovery
```sql
-- MySQL/MariaDB
# Extract table from backup
sed -n '/CREATE TABLE `specific_table`/,/CREATE TABLE/p' backup.sql > table_backup.sql

# Restore single table
mysql -u root -p database_name < table_backup.sql
```

## Backup Strategy Best Practices

### 1. Backup Schedule
- Full backup: Weekly
- Incremental backup: Daily
- Transaction logs: Every hour

### 2. Storage Requirements
```python
def calculate_backup_storage(db_size_gb, retention_days):
    """Calculate required backup storage"""
    daily_change_rate = 0.05  # 5% daily change
    
    full_backup = db_size_gb
    incremental_size = db_size_gb * daily_change_rate
    total_storage = full_backup + (incremental_size * retention_days)
    
    return total_storage
```

### 3. Monitoring Backup Success
```python
import smtplib
from email.message import EmailMessage

def monitor_backup(backup_path, size_threshold_mb=100):
    """Monitor backup completion and size"""
    backup_size = os.path.getsize(backup_path) / (1024 * 1024)  # Convert to MB
    
    if backup_size < size_threshold_mb:
        send_alert(f"Backup may be incomplete: {backup_size}MB")
        return False
    return True

def send_alert(message):
    """Send alert email"""
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Backup Alert'
    msg['From'] = "backup@yourdomain.com"
    msg['To'] = "dba@yourdomain.com"
    
    smtp_server = smtplib.SMTP('localhost')
    smtp_server.send_message(msg)
    smtp_server.quit()
```

## Disaster Recovery

### 1. Recovery Time Objective (RTO)
```python
def estimate_recovery_time(backup_size_gb, network_speed_mbps):
    """Estimate recovery time in hours"""
    # Convert sizes to consistent units (bits)
    backup_bits = backup_size_gb * 8 * 1024 * 1024 * 1024
    speed_bits_per_hour = network_speed_mbps * 1024 * 1024 * 3600
    
    # Add 20% for database startup and verification
    recovery_hours = (backup_bits / speed_bits_per_hour) * 1.2
    return recovery_hours
```

### 2. Recovery Point Objective (RPO)
- Transaction log shipping: 15 minutes
- Incremental backups: 24 hours
- Full backups: 7 days

### 3. Recovery Procedure Documentation
```markdown
1. Assess the Failure
   - Identify type of failure
   - Determine last good backup
   - Estimate recovery time

2. Prepare Recovery Environment
   - Verify backup files
   - Check storage space
   - Set up temporary instance if needed

3. Execute Recovery
   - Restore latest full backup
   - Apply incremental backups
   - Roll forward transaction logs
   - Verify data integrity

4. Validate Recovery
   - Check database consistency
   - Verify application connectivity
   - Test critical functionality

5. Switch Production Traffic
   - Update DNS/load balancers
   - Verify client connections
   - Monitor performance
```

## Backup Security

### 1. Encryption
```bash
# MySQL backup with encryption
mysqldump -u root -p --all-databases | \
openssl enc -aes-256-cbc -salt -out backup.sql.enc

# Decrypt for recovery
openssl enc -d -aes-256-cbc -in backup.sql.enc | \
mysql -u root -p
```

### 2. Access Control
```sql
-- MySQL/MariaDB: Create backup user
CREATE USER 'backup'@'localhost' 
IDENTIFIED BY 'strong_password';
GRANT BACKUP_ADMIN, SELECT, LOCK TABLES 
ON *.* TO 'backup'@'localhost';

-- Oracle: Create backup user
CREATE USER backup_user 
IDENTIFIED BY strong_password;
GRANT BACKUP_ADMIN TO backup_user;
```

## Cloud Backup Solutions

### 1. AWS S3 Backup
```python
import boto3

def backup_to_s3(backup_file, bucket_name):
    """Upload backup to S3"""
    s3 = boto3.client('s3')
    s3.upload_file(backup_file, bucket_name, 
                   f"backups/{os.path.basename(backup_file)}")

def list_s3_backups(bucket_name):
    """List available backups in S3"""
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(
        Bucket=bucket_name,
        Prefix="backups/"
    )
    return [obj['Key'] for obj in response['Contents']]
```

### 2. Multi-Region Backup
```python
def replicate_backup(source_bucket, dest_bucket, region):
    """Replicate backup to different region"""
    s3 = boto3.client('s3')
    
    # Configure replication
    replication = {
        'Role': 'arn:aws:iam::account:role/replication_role',
        'Rules': [{
            'Status': 'Enabled',
            'Priority': 1,
            'DeleteMarkerReplication': { 'Status': 'Enabled' },
            'Destination': {
                'Bucket': f'arn:aws:s3:::{dest_bucket}',
                'StorageClass': 'STANDARD'
            }
        }]
    }
    
    s3.put_bucket_replication(
        Bucket=source_bucket,
        ReplicationConfiguration=replication
    )
```

## Backup Performance Optimization

### 1. Parallel Backup
```bash
# MySQL parallel backup
mysqldump -u root -p --all-databases \
  --parallel=4 \
  --compress \
  > backup.sql
```

### 2. Compression
```python
def compress_backup(backup_file):
    """Compress backup file"""
    import zlib
    
    with open(backup_file, 'rb') as f_in:
        with open(f"{backup_file}.gz", 'wb') as f_out:
            compress = zlib.compressobj(level=9)
            for chunk in iter(lambda: f_in.read(4096), b''):
                f_out.write(compress.compress(chunk))
            f_out.write(compress.flush())
```

## Recovery Testing Schedule

### Monthly Tests
1. Full recovery test
2. Point-in-time recovery test
3. Table-level recovery test
4. Application integration test

### Quarterly Tests
1. Disaster recovery simulation
2. Multi-site recovery test
3. Performance benchmark
4. Security audit
