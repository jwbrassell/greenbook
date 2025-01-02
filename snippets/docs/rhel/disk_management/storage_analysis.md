# Storage Analysis in RHEL/Rocky Linux

## Table of Contents
- [Storage Analysis in RHEL/Rocky Linux](#storage-analysis-in-rhel/rocky-linux)
  - [Table of Contents](#table-of-contents)
  - [Why Storage Analysis Matters?](#why-storage-analysis-matters?)
  - [Real-World Scenario: The Mysterious Full Disk](#real-world-scenario:-the-mysterious-full-disk)
  - [Finding Large Files](#finding-large-files)
    - [Basic Commands for Finding Big Files](#basic-commands-for-finding-big-files)
      - [Using find](#using-find)
- [Find files larger than 100MB](#find-files-larger-than-100mb)
- [Find and sort by size (largest first)](#find-and-sort-by-size-largest-first)
      - [Using du (Disk Usage)](#using-du-disk-usage)
- [Show directory sizes, sorted](#show-directory-sizes,-sorted)
- [Show only directories over 1GB](#show-only-directories-over-1gb)
  - [Real-World Example: Investigating High Disk Usage](#real-world-example:-investigating-high-disk-usage)
    - [Scenario: Log Files Growing Too Large](#scenario:-log-files-growing-too-large)
  - [Advanced Analysis Tools](#advanced-analysis-tools)
    - [1. ncdu (NCurses Disk Usage)](#1-ncdu-ncurses-disk-usage)
- [Install ncdu](#install-ncdu)
- [Analyze a directory](#analyze-a-directory)
    - [2. baobab (GNOME Disk Usage Analyzer)](#2-baobab-gnome-disk-usage-analyzer)
- [Install baobab](#install-baobab)
- [Launch the application](#launch-the-application)
  - [Common Storage Problems and Solutions](#common-storage-problems-and-solutions)
    - [Problem 1: Growing Log Files](#problem-1:-growing-log-files)
      - [Identify the Issue](#identify-the-issue)
- [Find large log files](#find-large-log-files)
      - [Solution](#solution)
- [Check log rotation settings](#check-log-rotation-settings)
- [Manually rotate a log file](#manually-rotate-a-log-file)
    - [Problem 2: Hidden Space Users](#problem-2:-hidden-space-users)
      - [Find Hidden Space](#find-hidden-space)
- [Show hidden files/directories](#show-hidden-files/directories)
- [Find dot directories larger than 1GB](#find-dot-directories-larger-than-1gb)
      - [Common Culprits](#common-culprits)
  - [Practical Exercises](#practical-exercises)
    - [Exercise 1: System Space Audit](#exercise-1:-system-space-audit)
    - [Exercise 2: Finding Space Hogs](#exercise-2:-finding-space-hogs)
  - [Best Practices](#best-practices)
  - [Quick Reference Commands](#quick-reference-commands)
    - [Space Overview](#space-overview)
- [Quick system overview](#quick-system-overview)
- [Directory sizes](#directory-sizes)
- [Specific directory analysis](#specific-directory-analysis)
    - [Finding Large Files](#finding-large-files)
- [Files over 100MB](#files-over-100mb)
- [Files modified recently](#files-modified-recently)
- [Largest files in current directory](#largest-files-in-current-directory)
    - [Cleanup Commands](#cleanup-commands)
- [Clean package manager cache](#clean-package-manager-cache)
- [Remove old log files](#remove-old-log-files)
- [Clear temporary files](#clear-temporary-files)



This guide will help you understand how to analyze and manage storage space on your Linux system. We'll cover finding large files, analyzing directory sizes, and managing disk space effectively.

## Why Storage Analysis Matters?

Imagine your computer's storage like a closet. Over time, it fills up with stuff, and sometimes you need to:
- Find what's taking up the most space
- Clean out things you don't need
- Organize things better
- Make room for new stuff

## Real-World Scenario: The Mysterious Full Disk

Imagine you're a system administrator, and you get an alert: "Server running out of space!" Your mission is to:
1. Find out what's eating up the space
2. Determine if it's normal or a problem
3. Fix the issue before the disk fills up completely

Let's learn the tools that make this job easier!

## Finding Large Files

### Basic Commands for Finding Big Files

#### Using `find`
```bash
# Find files larger than 100MB
find /path -type f -size +100M

# Find and sort by size (largest first)
find /path -type f -exec du -h {} \; | sort -rh | head -n 20
```

Think of this like:
- Going through your closet
- Picking out all items bigger than a certain size
- Arranging them from biggest to smallest

#### Using `du` (Disk Usage)
```bash
# Show directory sizes, sorted
du -h --max-depth=1 /path | sort -rh

# Show only directories over 1GB
du -h --max-depth=1 /path | sort -rh | grep "G"
```

This is like:
- Checking each shelf in your closet
- Seeing how much stuff is on each shelf
- Listing the fullest shelves first

## Real-World Example: Investigating High Disk Usage

### Scenario: Log Files Growing Too Large

1. **Check Overall Space**
   ```bash
   df -h
   ```
   Output might show:
   ```
   Filesystem      Size  Used  Avail Use%  Mounted on
   /dev/sda1       100G   95G     5G  95%  /
   ```

2. **Find Big Directories**
   ```bash
   sudo du -h --max-depth=1 / | sort -rh
   ```
   Might reveal:
   ```
   50G  /var
   20G  /home
   15G  /usr
   ```

3. **Drill Down into Problem Directory**
   ```bash
   sudo du -h --max-depth=1 /var | sort -rh
   ```
   Could show:
   ```
   45G  /var/log
   3G   /var/cache
   2G   /var/lib
   ```

4. **Find Specific Large Files**
   ```bash
   sudo find /var/log -type f -size +100M -exec ls -lh {} \;
   ```

## Advanced Analysis Tools

### 1. ncdu (NCurses Disk Usage)
```bash
# Install ncdu
sudo dnf install ncdu

# Analyze a directory
ncdu /path
```

Benefits:
- Interactive interface
- Easy navigation
- Visual representation of space usage

### 2. baobab (GNOME Disk Usage Analyzer)
```bash
# Install baobab
sudo dnf install baobab

# Launch the application
baobab
```

Think of this like:
- A map of your storage
- Shows size of folders visually
- Easy to spot space hogs

## Common Storage Problems and Solutions

### Problem 1: Growing Log Files

#### Identify the Issue
```bash
# Find large log files
sudo find /var/log -type f -size +100M
```

#### Solution
```bash
# Check log rotation settings
cat /etc/logrotate.conf

# Manually rotate a log file
sudo logrotate -f /etc/logrotate.d/specific-log
```

### Problem 2: Hidden Space Users

#### Find Hidden Space
```bash
# Show hidden files/directories
ls -la

# Find dot directories larger than 1GB
du -h .[!.]* | grep "G"
```

#### Common Culprits
1. Browser caches
2. Application logs
3. Package manager caches
4. Old backups

## Practical Exercises

### Exercise 1: System Space Audit

Scenario: Monthly storage check-up

1. **Overall Status**
   ```bash
   # Check filesystem usage
   df -h
   
   # Check inode usage
   df -i
   ```

2. **User Space Analysis**
   ```bash
   # Check home directory sizes
   sudo du -h --max-depth=1 /home | sort -rh
   ```

3. **Temporary Files Check**
   ```bash
   # Check /tmp size
   du -sh /tmp
   
   # Find old temporary files
   find /tmp -type f -atime +30
   ```

### Exercise 2: Finding Space Hogs

Scenario: Quick space recovery needed

1. **Find Large Files**
   ```bash
   # Files over 1GB
   sudo find / -type f -size +1G -exec ls -lh {} \;
   
   # Files modified in last 24 hours
   sudo find / -type f -mtime -1 -size +100M
   ```

2. **Check Common Space Hogs**
   ```bash
   # Package manager cache
   du -sh /var/cache/dnf
   
   # Old log files
   sudo find /var/log -type f -size +50M
   ```

## Best Practices

1. **Regular Monitoring**
   - Set up daily space monitoring
   - Keep track of growth trends
   - Set alerts for threshold breaches

2. **Proactive Management**
   - Regular cleanup of temporary files
   - Log rotation configuration
   - Archive old, unused files

3. **Documentation**
   - Keep notes on normal space usage
   - Document cleanup procedures
   - Track seasonal patterns

4. **Automation**
   Create a simple daily check script:
   ```bash
   #!/bin/bash
   # Save as /usr/local/bin/space-check.sh
   
   echo "=== Disk Space Report ==="
   date
   echo "========================"
   df -h
   echo "========================"
   echo "Largest Directories:"
   du -h --max-depth=1 / | sort -rh | head -n 10
   ```

## Quick Reference Commands

### Space Overview
```bash
# Quick system overview
df -h

# Directory sizes
du -sh *

# Specific directory analysis
du -h --max-depth=1 /var | sort -rh
```

### Finding Large Files
```bash
# Files over 100MB
find / -type f -size +100M

# Files modified recently
find / -type f -mtime -1 -size +50M

# Largest files in current directory
ls -lSh
```

### Cleanup Commands
```bash
# Clean package manager cache
sudo dnf clean all

# Remove old log files
sudo find /var/log -type f -name "*.gz" -delete

# Clear temporary files
sudo rm -rf /tmp/*
```

Remember: Always verify what you're deleting and have backups of important data before major cleanup operations.
