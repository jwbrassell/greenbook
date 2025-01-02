# Understanding Disk Partitions in RHEL/Rocky Linux

## Table of Contents
- [Understanding Disk Partitions in RHEL/Rocky Linux](#understanding-disk-partitions-in-rhel/rocky-linux)
  - [Table of Contents](#table-of-contents)
  - [What is a Partition?](#what-is-a-partition?)
    - [Why Do We Partition Disks?](#why-do-we-partition-disks?)
  - [Real-World Scenario: Setting Up a Web Server](#real-world-scenario:-setting-up-a-web-server)
  - [Working with Partitions](#working-with-partitions)
    - [Viewing Current Partitions](#viewing-current-partitions)
      - [The fdisk -l Command](#the-fdisk--l-command)
    - [Creating a New Partition](#creating-a-new-partition)
      - [Scenario: Adding Storage for Database Files](#scenario:-adding-storage-for-database-files)
    - [Formatting a Partition](#formatting-a-partition)
- [For general use (like storing files)](#for-general-use-like-storing-files)
- [For special uses (like swap space)](#for-special-uses-like-swap-space)
  - [Common Partition Layouts](#common-partition-layouts)
    - [1. Basic Desktop Setup](#1-basic-desktop-setup)
    - [2. Server Setup](#2-server-setup)
  - [Practical Exercises](#practical-exercises)
    - [Exercise 1: Create a New Data Partition](#exercise-1:-create-a-new-data-partition)
    - [Exercise 2: Resize a Partition](#exercise-2:-resize-a-partition)
  - [Troubleshooting Common Issues](#troubleshooting-common-issues)
    - [Problem 1: "Partition Table in Use"](#problem-1:-"partition-table-in-use")
- [List processes using the partition](#list-processes-using-the-partition)
- [Safely stop processes](#safely-stop-processes)
    - [Problem 2: "Unable to Mount Partition"](#problem-2:-"unable-to-mount-partition")
- [Check filesystem](#check-filesystem)
- [Check mount points](#check-mount-points)
  - [Best Practices](#best-practices)
  - [Safety Tips](#safety-tips)



This guide will help you understand disk partitions - what they are, how to work with them, and when to use them. We'll use real-world examples to make these concepts easy to understand.

## What is a Partition?

Think of a hard drive like a big pizza. Partitioning is like cutting that pizza into slices. Each slice can be used differently - just like you might want different toppings on different slices, you might want different parts of your hard drive to serve different purposes.

### Why Do We Partition Disks?

1. **Organization**: Like having different rooms in a house for different purposes
2. **Security**: Keep sensitive data separate
3. **Performance**: Some types of data work better on their own partition
4. **Backup**: Easier to backup specific parts of your system

## Real-World Scenario: Setting Up a Web Server

Imagine you're setting up a web server for your company. You want to:
- Keep the operating system separate from website files
- Make sure log files don't fill up the whole disk
- Have a separate space for user uploads

Here's how you might partition the disk:
- 50GB for the operating system (/)
- 100GB for website files (/var/www)
- 50GB for logs (/var/log)
- Remaining space for user uploads (/uploads)

## Working with Partitions

### Viewing Current Partitions

#### The `fdisk -l` Command
```bash
sudo fdisk -l
```

Example output explained:
```
Disk /dev/sda: 500 GB
Device      Start        End    Sectors   Size Type
/dev/sda1    2048   20971519   20969472    10G Linux filesystem
/dev/sda2 20971520   41943039   20971520    10G Linux swap
/dev/sda3 41943040  1048575999 1006632960  480G Linux filesystem
```

Think of this like a map of your pizza slices:
- `Device`: The name of each slice
- `Start/End`: Where each slice begins and ends
- `Size`: How big each slice is
- `Type`: What the slice is used for

### Creating a New Partition

#### Scenario: Adding Storage for Database Files

Let's say you've added a new 1TB drive for database storage. Here's how to set it up:

1. **Identify the New Disk**
   ```bash
   lsblk
   ```
   You might see your new disk as `/dev/sdb`

2. **Start the Partition Tool**
   ```bash
   sudo fdisk /dev/sdb
   ```

3. **Create a New Partition (Step by Step)**
   ```
   Command (m for help): n
   Partition type: p (primary)
   Partition number: 1
   First sector: [Press Enter for default]
   Last sector: [Press Enter for default]
   ```
   
   Think of this like:
   - Deciding to cut the pizza (n for new)
   - Choosing a regular slice (p for primary)
   - Deciding where to start the cut (First sector)
   - Deciding where to end the cut (Last sector)

4. **Save Your Changes**
   ```
   Command: w
   ```
   This writes your changes - like actually cutting the pizza!

### Formatting a Partition

After creating a partition, you need to format it (like preparing the surface of your slice to hold food).

```bash
# For general use (like storing files)
sudo mkfs.xfs /dev/sdb1

# For special uses (like swap space)
sudo mkswap /dev/sdb2
```

## Common Partition Layouts

### 1. Basic Desktop Setup
```
/dev/sda1  50GB   /         (Operating System)
/dev/sda2   8GB   [SWAP]    (Virtual Memory)
/dev/sda3  Rest   /home     (User Files)
```

### 2. Server Setup
```
/dev/sda1  50GB   /         (Operating System)
/dev/sda2   8GB   [SWAP]    (Virtual Memory)
/dev/sda3  100GB  /var      (Logs and Variable Data)
/dev/sda4  Rest   /data     (Application Data)
```

## Practical Exercises

### Exercise 1: Create a New Data Partition
Scenario: You've added a new hard drive for storing backups

1. **Check the New Drive**
   ```bash
   sudo fdisk -l
   ```

2. **Create Partition**
   ```bash
   sudo fdisk /dev/sdb
   # n (new partition)
   # p (primary partition)
   # 1 (partition number)
   # [Enter] (default first sector)
   # [Enter] (default last sector)
   # w (write changes)
   ```

3. **Format the Partition**
   ```bash
   sudo mkfs.xfs /dev/sdb1
   ```

4. **Create Mount Point**
   ```bash
   sudo mkdir /backups
   ```

5. **Mount the Partition**
   ```bash
   sudo mount /dev/sdb1 /backups
   ```

### Exercise 2: Resize a Partition
Scenario: Your /var partition is running out of space

1. **Check Current Size**
   ```bash
   df -h /var
   ```

2. **Back Up Data** (Always do this first!)
   ```bash
   sudo tar -czf /tmp/var_backup.tar.gz /var
   ```

3. **Resize Using LVM** (if using LVM)
   ```bash
   sudo lvextend -L +10G /dev/mapper/vg0-var
   sudo xfs_growfs /var
   ```

## Troubleshooting Common Issues

### Problem 1: "Partition Table in Use"
```bash
# List processes using the partition
sudo fuser -m /dev/sdb1

# Safely stop processes
sudo fuser -mk /dev/sdb1
```

### Problem 2: "Unable to Mount Partition"
```bash
# Check filesystem
sudo fsck /dev/sdb1

# Check mount points
cat /proc/mounts
```

## Best Practices

1. **Always Backup Before Partitioning**
   - Make full backups before any partition changes
   - Verify backups are accessible

2. **Plan Your Space**
   - Consider future growth
   - Leave some free space
   - Document your partition scheme

3. **Use LVM When Possible**
   - Makes future resizing easier
   - Allows for snapshots
   - More flexible management

4. **Regular Maintenance**
   - Monitor partition usage
   - Clean up unnecessary files
   - Check filesystem health

## Safety Tips

1. **Double-Check Device Names**
   - Always verify you're working on the correct disk
   - Use `lsblk` to confirm

2. **Never Partition a Mounted Disk**
   - Unmount before making changes
   - Verify with `mount` command

3. **Keep Recovery Tools Ready**
   - Have a live USB ready
   - Know how to use rescue mode

Remember: Partitioning mistakes can lead to data loss. Always double-check commands and have backups before making changes.
