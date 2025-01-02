# Backup and Recovery Scripts

## Table of Contents
- [Backup and Recovery Scripts](#backup-and-recovery-scripts)
  - [Table of Contents](#table-of-contents)
          - [tags: backup, recovery, archive, restore, sync, cloud](#tags:-backup,-recovery,-archive,-restore,-sync,-cloud)
  - [Incremental Backups](#incremental-backups)
          - [tags: incremental, rsync, hardlinks](#tags:-incremental,-rsync,-hardlinks)
- [Incremental Backup System](#incremental-backup-system)
- [!/bin/bash](#!/bin/bash)
- [Create incremental backup using hard links](#create-incremental-backup-using-hard-links)
- [Rotate old backups](#rotate-old-backups)
- [Verify backup integrity](#verify-backup-integrity)
  - [Database Backups](#database-backups)
          - [tags: database, mysql, postgresql, mongodb](#tags:-database,-mysql,-postgresql,-mongodb)
- [MySQL Database Backup](#mysql-database-backup)
- [!/bin/bash](#!/bin/bash)
- [PostgreSQL Database Backup](#postgresql-database-backup)
- [!/bin/bash](#!/bin/bash)
- [MongoDB Database Backup](#mongodb-database-backup)
- [!/bin/bash](#!/bin/bash)
- [Database Restore Functions](#database-restore-functions)
  - [Remote Syncing](#remote-syncing)
          - [tags: remote, sync, rsync, ssh](#tags:-remote,-sync,-rsync,-ssh)
- [Remote Backup System](#remote-backup-system)
- [!/bin/bash](#!/bin/bash)
- [Bandwidth-limited sync](#bandwidth-limited-sync)
  - [Encrypted Backups](#encrypted-backups)
          - [tags: encryption, gpg, security](#tags:-encryption,-gpg,-security)
- [Encrypted Backup System](#encrypted-backup-system)
- [!/bin/bash](#!/bin/bash)
- [Decrypt and restore](#decrypt-and-restore)
  - [Cloud Backups](#cloud-backups)
          - [tags: cloud, aws, s3, azure](#tags:-cloud,-aws,-s3,-azure)
- [AWS S3 Backup System](#aws-s3-backup-system)
- [!/bin/bash](#!/bin/bash)
- [Rotate S3 backups](#rotate-s3-backups)
- [Azure Blob Storage Backup](#azure-blob-storage-backup)
  - [See Also](#see-also)



###### tags: `backup`, `recovery`, `archive`, `restore`, `sync`, `cloud`

## Incremental Backups
###### tags: `incremental`, `rsync`, `hardlinks`

```bash
# Incremental Backup System
#!/bin/bash
source_dir="/path/to/source"
backup_dir="/path/to/backup"
date_format=$(date +%Y%m%d)
latest_link="$backup_dir/latest"
log_file="/var/log/backup.log"

# Create incremental backup using hard links
backup_incremental() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting incremental backup..." >> "$log_file"
    
    # Create new backup directory
    backup_path="$backup_dir/$date_format"
    mkdir -p "$backup_path"
    
    # Create hard-link copy of latest backup if it exists
    if [ -L "$latest_link" ]; then
        cp -al "$latest_link/" "$backup_path"
    fi
    
    # Sync changes
    rsync -av --delete \
        --exclude='.git/' \
        --exclude='*.tmp' \
        --exclude='*.log' \
        "$source_dir/" \
        "$backup_path/" >> "$log_file" 2>&1
    
    # Update latest link
    rm -f "$latest_link"
    ln -s "$backup_path" "$latest_link"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup completed" >> "$log_file"
}

# Rotate old backups
rotate_backups() {
    # Keep daily backups for 7 days
    find "$backup_dir" -maxdepth 1 -type d -mtime +7 -exec rm -rf {} \;
    
    # Keep weekly backups for 4 weeks
    find "$backup_dir" -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;
}

# Verify backup integrity
verify_backup() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verifying backup..." >> "$log_file"
    
    rsync -avn --delete \
        "$source_dir/" \
        "$latest_link/" >> "$log_file" 2>&1
    
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup verification successful" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup verification failed" >> "$log_file"
        send_alert "Backup verification failed"
    fi
}
```

## Database Backups
###### tags: `database`, `mysql`, `postgresql`, `mongodb`

```bash
# MySQL Database Backup
#!/bin/bash
db_user="user"
db_pass="password"
backup_dir="/path/to/backup/mysql"
date_format=$(date +%Y%m%d)
log_file="/var/log/db_backup.log"

backup_mysql() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting MySQL backup..." >> "$log_file"
    
    # Create backup directory
    mkdir -p "$backup_dir"
    
    # Backup all databases
    mysqldump -u "$db_user" -p"$db_pass" \
        --all-databases \
        --single-transaction \
        --quick \
        --lock-tables=false \
        | gzip > "$backup_dir/mysql_$date_format.sql.gz"
    
    # Verify backup
    if gzip -t "$backup_dir/mysql_$date_format.sql.gz"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] MySQL backup successful" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] MySQL backup failed" >> "$log_file"
        send_alert "MySQL backup failed"
    fi
}

# PostgreSQL Database Backup
#!/bin/bash
backup_postgresql() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting PostgreSQL backup..." >> "$log_file"
    
    # Backup all databases
    databases=$(psql -l -t | cut -d'|' -f1 | sed -e 's/ //g' -e '/^$/d')
    
    for db in $databases; do
        if [ "$db" != "template0" ] && [ "$db" != "template1" ]; then
            pg_dump -Fc "$db" > "$backup_dir/postgresql_${db}_$date_format.dump"
        fi
    done
}

# MongoDB Database Backup
#!/bin/bash
backup_mongodb() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting MongoDB backup..." >> "$log_file"
    
    mongodump \
        --out "$backup_dir/mongodb_$date_format" \
        --gzip
    
    # Create archive
    tar czf "$backup_dir/mongodb_$date_format.tar.gz" \
        "$backup_dir/mongodb_$date_format"
    
    # Clean up dump directory
    rm -rf "$backup_dir/mongodb_$date_format"
}

# Database Restore Functions
restore_mysql() {
    local backup_file="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring MySQL backup..." >> "$log_file"
    
    gunzip < "$backup_file" | mysql -u "$db_user" -p"$db_pass"
}

restore_postgresql() {
    local backup_file="$1"
    local db_name="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring PostgreSQL backup..." >> "$log_file"
    
    pg_restore -d "$db_name" "$backup_file"
}

restore_mongodb() {
    local backup_file="$1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring MongoDB backup..." >> "$log_file"
    
    tar xzf "$backup_file"
    mongorestore --gzip "${backup_file%.tar.gz}"
}
```

## Remote Syncing
###### tags: `remote`, `sync`, `rsync`, `ssh`

```bash
# Remote Backup System
#!/bin/bash
source_dir="/path/to/source"
remote_user="user"
remote_host="host"
remote_dir="/path/to/backup"
exclude_file="/path/to/exclude.txt"
log_file="/var/log/remote_backup.log"

sync_to_remote() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting remote sync..." >> "$log_file"
    
    # Test SSH connection
    if ! ssh -q "$remote_user@$remote_host" exit; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] SSH connection failed" >> "$log_file"
        send_alert "Remote backup failed: SSH connection error"
        return 1
    fi
    
    # Sync files
    rsync -avz --delete \
        --exclude-from="$exclude_file" \
        -e "ssh -p 22" \
        "$source_dir/" \
        "$remote_user@$remote_host:$remote_dir/" >> "$log_file" 2>&1
    
    # Verify sync
    if [ $? -eq 0 ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Remote sync completed successfully" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Remote sync failed" >> "$log_file"
        send_alert "Remote backup failed: rsync error"
    fi
}

# Bandwidth-limited sync
sync_with_limit() {
    rsync -avz --delete \
        --bwlimit=1000 \
        --exclude-from="$exclude_file" \
        -e "ssh -p 22" \
        "$source_dir/" \
        "$remote_user@$remote_host:$remote_dir/"
}
```

## Encrypted Backups
###### tags: `encryption`, `gpg`, `security`

```bash
# Encrypted Backup System
#!/bin/bash
source_dir="/path/to/source"
backup_dir="/path/to/backup"
gpg_recipient="user@example.com"
date_format=$(date +%Y%m%d)
log_file="/var/log/encrypted_backup.log"

create_encrypted_backup() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting encrypted backup..." >> "$log_file"
    
    # Create archive and encrypt
    tar czf - "$source_dir" | \
        gpg --encrypt \
            --recipient "$gpg_recipient" \
            --trust-model always \
            --output "$backup_dir/backup_$date_format.tar.gz.gpg"
    
    # Verify encryption
    if gpg --list-packets "$backup_dir/backup_$date_format.tar.gz.gpg" >/dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Encryption successful" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Encryption failed" >> "$log_file"
        send_alert "Encrypted backup failed"
    fi
}

# Decrypt and restore
restore_encrypted_backup() {
    local backup_file="$1"
    local restore_dir="$2"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Restoring encrypted backup..." >> "$log_file"
    
    gpg --decrypt "$backup_file" | \
        tar xzf - -C "$restore_dir"
}
```

## Cloud Backups
###### tags: `cloud`, `aws`, `s3`, `azure`

```bash
# AWS S3 Backup System
#!/bin/bash
source_dir="/path/to/source"
bucket="s3://my-bucket"
date_format=$(date +%Y%m%d)
log_file="/var/log/cloud_backup.log"

backup_to_s3() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting S3 backup..." >> "$log_file"
    
    # Create local archive
    tar czf "/tmp/backup_$date_format.tar.gz" "$source_dir"
    
    # Upload to S3
    aws s3 cp \
        "/tmp/backup_$date_format.tar.gz" \
        "$bucket/backups/backup_$date_format.tar.gz" >> "$log_file" 2>&1
    
    # Clean up
    rm "/tmp/backup_$date_format.tar.gz"
    
    # Verify upload
    if aws s3 ls "$bucket/backups/backup_$date_format.tar.gz" >/dev/null 2>&1; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] S3 backup successful" >> "$log_file"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] S3 backup failed" >> "$log_file"
        send_alert "S3 backup failed"
    fi
}

# Rotate S3 backups
rotate_s3_backups() {
    # List backups older than 30 days
    aws s3 ls "$bucket/backups/" | \
        awk '{print $4}' | \
        grep -E '^backup_[0-9]{8}\.tar\.gz$' | \
        while read -r file; do
            date=${file:7:8}
            if [ $(( ( $(date +%s) - $(date -d "$date" +%s) ) / 86400 )) -gt 30 ]; then
                aws s3 rm "$bucket/backups/$file"
            fi
        done
}

# Azure Blob Storage Backup
backup_to_azure() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Azure backup..." >> "$log_file"
    
    # Create local archive
    tar czf "/tmp/backup_$date_format.tar.gz" "$source_dir"
    
    # Upload to Azure Blob Storage
    az storage blob upload \
        --container-name backups \
        --file "/tmp/backup_$date_format.tar.gz" \
        --name "backup_$date_format.tar.gz" >> "$log_file" 2>&1
    
    # Clean up
    rm "/tmp/backup_$date_format.tar.gz"
}
```

## See Also
- [Basic Operations](basics.md)
- [Advanced Script Patterns](advanced_patterns.md)
- [System Monitoring](monitoring.md)
