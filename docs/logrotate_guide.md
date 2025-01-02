# Log Rotation and Lsync Setup Guide

## Table of Contents
- [Log Rotation and Lsync Setup Guide](#log-rotation-and-lsync-setup-guide)
  - [Table of Contents](#table-of-contents)
  - [Understanding Log Rotation](#understanding-log-rotation)
    - [Key Benefits](#key-benefits)
  - [Logrotate Configuration](#logrotate-configuration)
    - [Basic Configuration Structure](#basic-configuration-structure)
    - [Common Options](#common-options)
  - [Lsync Overview](#lsync-overview)
    - [Key Features](#key-features)
    - [Common Use Cases](#common-use-cases)
  - [Setup Scripts](#setup-scripts)
    - [Using the Setup Scripts](#using-the-setup-scripts)



## Table of Contents
1. [Understanding Log Rotation](#understanding-log-rotation)
2. [Logrotate Configuration](#logrotate-configuration)
3. [Lsync Overview](#lsync-overview)
4. [Setup Scripts](#setup-scripts)

## Understanding Log Rotation

Log rotation is a critical system administration task that helps manage log files by:
- Preventing logs from consuming excessive disk space
- Maintaining organized log archives
- Enabling efficient log management and cleanup

### Key Benefits
- Prevents disk space exhaustion
- Maintains system performance
- Simplifies log archival and retrieval
- Enables compliance with retention policies

## Logrotate Configuration

Logrotate is typically configured through files in `/etc/logrotate.d/`. Each file defines rotation rules for specific log files or directories.

### Basic Configuration Structure
```conf
/var/log/program/*.log {
    daily                   # Rotate daily
    missingok              # Don't error if log file is missing
    rotate 7               # Keep 7 rotated logs
    compress              # Compress rotated logs
    delaycompress         # Don't compress most recent rotated log
    notifempty           # Don't rotate empty files
    create 0640 user group  # Create new log with these permissions
    postrotate           # Script to run after rotation
        /usr/bin/killall -HUP program
    endscript
}
```

### Common Options
- `daily`, `weekly`, `monthly`: Rotation frequency
- `rotate N`: Number of rotated logs to keep
- `size N`: Rotate when log reaches size (e.g., 100M)
- `compress`: Compress rotated logs
- `missingok`: Don't error if log is missing
- `notifempty`: Don't rotate empty files
- `create MODE USER GROUP`: Create new log file with specified permissions
- `dateext`: Add date extension to rotated logs

## Lsync Overview

Lsync (Live Syncing) is a file synchronization tool that combines the benefits of rsync with real-time filesystem monitoring.

### Key Features
- Real-time synchronization
- Efficient delta transfers
- Support for complex sync scenarios
- Low system overhead

### Common Use Cases
1. Real-time backup
2. Log file synchronization
3. Directory mirroring
4. Disaster recovery setup

## Setup Scripts

This guide includes two helper scripts:
1. `logrotate_setup.sh`: Shell script for configuring logrotate
2. `lsync_config.py`: Python script for setting up lsync

### Using the Setup Scripts

1. Make the scripts executable:
```bash
chmod +x logrotate_setup.sh
chmod +x lsync_config.py
```

2. Run the logrotate setup:
```bash
./logrotate_setup.sh /path/to/logs
```

3. Configure lsync:
```bash
python3 lsync_config.py /path/to/source
```

For detailed script usage, see the individual script documentation below.
