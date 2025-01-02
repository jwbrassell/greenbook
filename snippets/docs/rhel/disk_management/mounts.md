# Understanding Mount Operations in RHEL/Rocky Linux

## Table of Contents
- [Understanding Mount Operations in RHEL/Rocky Linux](#understanding-mount-operations-in-rhel/rocky-linux)
  - [Table of Contents](#table-of-contents)
  - [What is Mounting?](#what-is-mounting?)
    - [Real-World Analogy](#real-world-analogy)
  - [Basic Mount Operations](#basic-mount-operations)
    - [Viewing Current Mounts](#viewing-current-mounts)
- [Show all mounted filesystems](#show-all-mounted-filesystems)
- [Show in a more readable format](#show-in-a-more-readable-format)
- [Show specific filesystem type (like ext4)](#show-specific-filesystem-type-like-ext4)
  - [Real-World Scenarios](#real-world-scenarios)
    - [Scenario 1: Mounting a USB Drive](#scenario-1:-mounting-a-usb-drive)
    - [Scenario 2: Mounting a Network Share](#scenario-2:-mounting-a-network-share)
  - [Mount Options Explained](#mount-options-explained)
    - [Read/Write Options](#read/write-options)
- [Mount as read-only (like a "Do Not Touch" sign)](#mount-as-read-only-like-a-"do-not-touch"-sign)
- [Mount as read-write (default)](#mount-as-read-write-default)
    - [User Permissions](#user-permissions)
- [Allow regular users to access](#allow-regular-users-to-access)
- [Restrict to specific group](#restrict-to-specific-group)
  - [Automatic Mounting (fstab)](#automatic-mounting-fstab)
    - [Adding an Entry to fstab](#adding-an-entry-to-fstab)
  - [Common Problems and Solutions](#common-problems-and-solutions)
    - [Problem 1: "Device is Busy"](#problem-1:-"device-is-busy")
- [Find what's using it](#find-what's-using-it)
- [Force unmount (be careful!)](#force-unmount-be-careful!)
    - [Problem 2: "Wrong Filesystem Type"](#problem-2:-"wrong-filesystem-type")
- [Check filesystem type](#check-filesystem-type)
- [Mount with specific type](#mount-with-specific-type)
  - [Practical Exercises](#practical-exercises)
    - [Exercise 1: Create a Data Drive](#exercise-1:-create-a-data-drive)
    - [Exercise 2: Temporary Work Drive](#exercise-2:-temporary-work-drive)
- [Create temporary mount point](#create-temporary-mount-point)
- [Mount with specific options](#mount-with-specific-options)
- [Work on project...](#work-on-project)
- [Unmount when done](#unmount-when-done)
  - [Best Practices](#best-practices)
  - [Monitoring Mounted Filesystems](#monitoring-mounted-filesystems)
    - [Check Space Usage](#check-space-usage)
- [Show space on all mounted filesystems](#show-space-on-all-mounted-filesystems)
- [Check specific mount point](#check-specific-mount-point)
    - [Check Mount Options](#check-mount-options)
- [View current mount options](#view-current-mount-options)
- [Check specific filesystem](#check-specific-filesystem)
  - [Recovery Operations](#recovery-operations)
    - [If a Mount Fails](#if-a-mount-fails)



This guide will help you understand how to mount and manage storage devices in Linux. We'll use real-world examples and simple explanations to make these concepts easy to understand.

## What is Mounting?

Think of mounting like plugging in a USB drive to your computer, but you get to choose exactly where and how it connects. It's like creating a doorway (mount point) that leads to your storage device.

### Real-World Analogy
Imagine you have several storage rooms (hard drives/partitions) in a building (your computer). Mounting is like:
1. Creating a door (mount point)
2. Connecting it to a specific room (storage device)
3. Deciding who can go through the door and what they can do inside (permissions)

## Basic Mount Operations

### Viewing Current Mounts

```bash
# Show all mounted filesystems
mount

# Show in a more readable format
df -h

# Show specific filesystem type (like ext4)
mount | grep "ext4"
```

Example output explained:
```
/dev/sda1 on / type ext4 (rw,relatime)
```
This means:
- `/dev/sda1` is the storage device
- `/` is where it's mounted (root directory)
- `ext4` is the type of filesystem
- `rw,relatime` are the mount options

## Real-World Scenarios

### Scenario 1: Mounting a USB Drive
Imagine you've just plugged in a USB drive to backup some files.

1. **Find the Device**
   ```bash
   # List new devices
   lsblk
   ```
   You might see something like:
   ```
   sdb      8:16   1   32G  0 disk
   └─sdb1   8:17   1   32G  0 part
   ```

2. **Create a Mount Point**
   ```bash
   sudo mkdir /mnt/usb
   ```

3. **Mount the Drive**
   ```bash
   sudo mount /dev/sdb1 /mnt/usb
   ```

4. **Verify the Mount**
   ```bash
   df -h /mnt/usb
   ```

5. **When Finished**
   ```bash
   sudo umount /mnt/usb
   ```

### Scenario 2: Mounting a Network Share
Let's say you need to access a company file server.

1. **Install Required Tools**
   ```bash
   sudo dnf install cifs-utils
   ```

2. **Create Mount Point**
   ```bash
   sudo mkdir /mnt/company_files
   ```

3. **Mount Network Share**
   ```bash
   sudo mount -t cifs //server/share /mnt/company_files -o username=user
   ```

## Mount Options Explained

Think of mount options like rules for using the storage. Here are common options:

### Read/Write Options
```bash
# Mount as read-only (like a "Do Not Touch" sign)
sudo mount -o ro /dev/sdb1 /mnt/usb

# Mount as read-write (default)
sudo mount -o rw /dev/sdb1 /mnt/usb
```

### User Permissions
```bash
# Allow regular users to access
sudo mount -o user,uid=1000 /dev/sdb1 /mnt/usb

# Restrict to specific group
sudo mount -o gid=1000 /dev/sdb1 /mnt/usb
```

## Automatic Mounting (fstab)

Think of `/etc/fstab` as your storage device phonebook - it tells Linux how to automatically connect to your storage when the system starts.

### Adding an Entry to fstab

1. **Get Device UUID** (like a fingerprint for your device)
   ```bash
   sudo blkid
   ```

2. **Edit fstab**
   ```bash
   sudo nano /etc/fstab
   ```

3. **Add Entry**
   ```
   UUID=1234-5678  /mnt/data  ext4  defaults  0  2
   ```

Let's break down each field:
- `UUID=1234-5678`: Device identifier
- `/mnt/data`: Mount point
- `ext4`: Filesystem type
- `defaults`: Mount options
- `0`: Backup operation flag
- `2`: Filesystem check order

## Common Problems and Solutions

### Problem 1: "Device is Busy"
When you can't unmount because something's using the device.

```bash
# Find what's using it
sudo lsof /mnt/usb

# Force unmount (be careful!)
sudo umount -f /mnt/usb
```

### Problem 2: "Wrong Filesystem Type"
When Linux can't recognize the filesystem.

```bash
# Check filesystem type
sudo file -s /dev/sdb1

# Mount with specific type
sudo mount -t ntfs /dev/sdb1 /mnt/usb
```

## Practical Exercises

### Exercise 1: Create a Data Drive

Scenario: Setting up a new drive for data storage

1. **Prepare the Drive**
   ```bash
   sudo fdisk /dev/sdb
   # Create new partition
   sudo mkfs.ext4 /dev/sdb1
   ```

2. **Create Mount Point**
   ```bash
   sudo mkdir /data
   ```

3. **Add to fstab**
   ```bash
   # Get UUID
   sudo blkid /dev/sdb1
   
   # Add to fstab
   echo "UUID=<your-uuid> /data ext4 defaults 0 2" | sudo tee -a /etc/fstab
   ```

4. **Test Mount**
   ```bash
   sudo mount -a
   ```

### Exercise 2: Temporary Work Drive

Scenario: Mounting a temporary drive for a project

```bash
# Create temporary mount point
sudo mkdir /mnt/project

# Mount with specific options
sudo mount -o rw,noexec /dev/sdc1 /mnt/project

# Work on project...

# Unmount when done
sudo umount /mnt/project
```

## Best Practices

1. **Always Use Mount Points**
   - Create in /mnt for temporary mounts
   - Create in /media for removable media
   - Use meaningful names

2. **Check Before Mounting**
   - Verify device name
   - Check filesystem type
   - Ensure mount point exists

3. **Safe Unmounting**
   - Always unmount before removing
   - Check for active users/processes
   - Sync data before unmounting

4. **Security Considerations**
   - Use appropriate permissions
   - Consider encryption for sensitive data
   - Limit mount options to necessary ones

## Monitoring Mounted Filesystems

### Check Space Usage
```bash
# Show space on all mounted filesystems
df -h

# Check specific mount point
du -sh /mnt/data/*
```

### Check Mount Options
```bash
# View current mount options
cat /proc/mounts

# Check specific filesystem
findmnt /mnt/data
```

## Recovery Operations

### If a Mount Fails
1. Check system logs:
   ```bash
   sudo journalctl -xe
   ```

2. Verify device exists:
   ```bash
   ls -l /dev/sdX
   ```

3. Check filesystem:
   ```bash
   sudo fsck /dev/sdX
   ```

Remember: Always unmount properly and keep backups of important data. Improper unmounting can lead to data corruption.
