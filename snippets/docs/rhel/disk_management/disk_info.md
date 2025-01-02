# Understanding Disk Information Commands in RHEL/Rocky Linux

## Table of Contents
- [Understanding Disk Information Commands in RHEL/Rocky Linux](#understanding-disk-information-commands-in-rhel/rocky-linux)
  - [Table of Contents](#table-of-contents)
  - [Real-World Scenario: The Full Disk Crisis](#real-world-scenario:-the-full-disk-crisis)
  - [Basic Disk Space Commands](#basic-disk-space-commands)
    - [1. The df Command (Disk Free)](#1-the-df-command-disk-free)
      - [What is it?](#what-is-it?)
      - [Basic Usage](#basic-usage)
      - [Example Output and Explanation](#example-output-and-explanation)
      - [Common Scenarios for Using df](#common-scenarios-for-using-df)
    - [2. The lsblk Command (List Block Devices)](#2-the-lsblk-command-list-block-devices)
      - [What is it?](#what-is-it?)
      - [Basic Usage](#basic-usage)
      - [Example Output and Explanation](#example-output-and-explanation)
      - [Real-World Scenarios for lsblk](#real-world-scenarios-for-lsblk)
  - [Advanced Usage: Combining Commands](#advanced-usage:-combining-commands)
    - [Scenario: Investigating High Disk Usage](#scenario:-investigating-high-disk-usage)
  - [Best Practices](#best-practices)
  - [Troubleshooting Common Issues](#troubleshooting-common-issues)
    - [Problem 1: "No Space Left" Despite Available Space](#problem-1:-"no-space-left"-despite-available-space)
- [Check inode usage](#check-inode-usage)
- [Find directories with many files](#find-directories-with-many-files)
    - [Problem 2: Hidden Space Usage](#problem-2:-hidden-space-usage)
- [Check for deleted but open files](#check-for-deleted-but-open-files)
- [Check for hidden files](#check-for-hidden-files)
  - [Learning Exercises](#learning-exercises)
  - [Additional Tips](#additional-tips)



This guide will help you understand how to check disk space and manage storage on your Linux system. We'll explore the commands used to view disk information and understand what the output means.

## Real-World Scenario: The Full Disk Crisis

Imagine you're managing a company's web server, and suddenly the website stops working. The error logs show "No space left on device." This is a common scenario where disk information commands become your best friends to quickly identify and solve the problem.

## Basic Disk Space Commands

### 1. The `df` Command (Disk Free)

#### What is it?
Think of `df` as your storage space dashboard. Just like checking your phone's storage status, `df` shows you how much space is used and available on all your disks.

#### Basic Usage
```bash
df -h
```
The `-h` means "human-readable" - it shows sizes in GB and MB instead of just bytes (like saying "2 GB" instead of "2,147,483,648 bytes").

#### Example Output and Explanation
```
Filesystem      Size  Used  Avail Use% Mounted on
/dev/sda1       50G   32G    18G  64% /
/dev/sdb1      500G  125G   375G  25% /data
```

Let's break this down:
- `Filesystem`: The disk or partition name (like labeling different drawers in a filing cabinet)
- `Size`: Total storage space (like the size of your filing cabinet)
- `Used`: How much space is taken up (how many files are in the cabinet)
- `Avail`: Free space remaining (empty space in the cabinet)
- `Use%`: Percentage of space used (how full the cabinet is)
- `Mounted on`: Where you can access this storage (like the room where the cabinet is located)

#### Common Scenarios for Using df
1. **System Health Check**
   ```bash
   # Check all mounted filesystems
   df -h
   
   # Check a specific directory
   df -h /var
   ```
   Use this during your daily system checks to spot potential space issues before they become problems.

2. **Inode Check**
   ```bash
   # Check inode usage
   df -i
   ```
   Sometimes a disk appears to have space but can't create new files. This command helps you check if you've run out of inodes (think of them as file tracking labels).

### 2. The `lsblk` Command (List Block Devices)

#### What is it?
`lsblk` is like an X-ray of your computer's storage devices. It shows all storage devices connected to your system, including hard drives, SSDs, and USB drives.

#### Basic Usage
```bash
lsblk
```

#### Example Output and Explanation
```
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
sda      8:0    0  500G  0 disk 
├─sda1   8:1    0  100G  0 part /
├─sda2   8:2    0   8G  0 part [SWAP]
└─sda3   8:3    0  392G  0 part /home
sdb      8:16   1   32G  0 disk 
└─sdb1   8:17   1   32G  0 part /media/usb
```

Think of this like a family tree of your storage:
- `NAME`: Device name (like people's names in a family tree)
- `SIZE`: Storage capacity
- `TYPE`: Whether it's a disk or partition
- `MOUNTPOINT`: Where you can access it in your system

#### Real-World Scenarios for lsblk

1. **Adding a New Hard Drive**
   ```bash
   # Before plugging in the new drive
   lsblk
   
   # After plugging in the new drive
   lsblk
   # Compare to see the new drive
   ```

2. **USB Drive Investigation**
   ```bash
   # List with serial numbers
   lsblk -o NAME,SIZE,TYPE,SERIAL
   ```
   Useful when you need to identify specific drives, like finding which USB drive belongs to which department.

## Advanced Usage: Combining Commands

### Scenario: Investigating High Disk Usage

Let's say your monitoring system alerts you that a disk is 90% full. Here's a step-by-step investigation:

1. **Check Overall Disk Usage**
   ```bash
   df -h
   ```
   This shows which filesystem is running out of space.

2. **Check Specific Directory Usage**
   ```bash
   # If /var is the problem
   du -sh /var/*
   ```
   This helps pinpoint which subdirectory is using the most space.

3. **Monitor Real-Time Changes**
   ```bash
   watch -n 1 'df -h'
   ```
   This updates the disk usage display every second, helpful when tracking rapid changes.

## Best Practices

1. **Regular Monitoring**
   - Check disk space daily (morning routine)
   - Set up alerts for when usage exceeds 80%
   - Keep track of growth patterns

2. **Documentation**
   - Keep a log of normal disk usage patterns
   - Document any large changes in disk usage
   - Note seasonal patterns (like log file growth)

3. **Preventive Actions**
   - Clean up old logs regularly
   - Archive unused files
   - Plan for storage expansion before it's urgent

## Troubleshooting Common Issues

### Problem 1: "No Space Left" Despite Available Space
```bash
# Check inode usage
df -i

# Find directories with many files
find / -xdev -type f | cut -d "/" -f 2 | sort | uniq -c | sort -n
```

### Problem 2: Hidden Space Usage
```bash
# Check for deleted but open files
lsof | grep deleted

# Check for hidden files
ls -la
```

## Learning Exercises

1. **Disk Space Monitor**
   Create a simple monitoring routine:
   ```bash
   # Morning check routine
   df -h > disk_usage_$(date +%Y%m%d).log
   ```

2. **Practice Scenario**
   - Create some large files
   - Monitor space changes
   - Clean up and verify space recovery

## Additional Tips

1. **Color Output**
   ```bash
   # Add color to df output
   df -h | grep -E --color "^|[0-9]{2}%"
   ```

2. **Quick Space Check**
   ```bash
   # One-liner for critical filesystems
   df -h / /home /var | grep -v tmpfs
   ```

Remember: Regular monitoring and early intervention prevent emergency situations. These commands are your tools for maintaining healthy storage systems.
