# RHEL/Rocky Linux Disk Management Guide

This guide covers essential disk management tasks for RHEL/Rocky Linux systems.

## Table of Contents
- [RHEL/Rocky Linux Disk Management Guide](#rhel/rocky-linux-disk-management-guide)
  - [Table of Contents](#table-of-contents)
  - [Disk Information Commands](#disk-information-commands)
    - [View Disk Space Usage](#view-disk-space-usage)
- [Show disk space usage of mounted filesystems](#show-disk-space-usage-of-mounted-filesystems)
- [Show disk space usage in inodes](#show-disk-space-usage-in-inodes)
- [Show disk usage for specific directory](#show-disk-usage-for-specific-directory)
- [Show disk usage for all directories in current path](#show-disk-usage-for-all-directories-in-current-path)
    - [List Block Devices](#list-block-devices)
- [List all block devices with details](#list-all-block-devices-with-details)
- [Show detailed information about specific device](#show-detailed-information-about-specific-device)
- [Show disk information including serial numbers](#show-disk-information-including-serial-numbers)
  - [Partition Management](#partition-management)
    - [List Partitions](#list-partitions)
- [List all partitions](#list-all-partitions)
- [List partitions on specific device](#list-partitions-on-specific-device)
    - [Create New Partition](#create-new-partition)
- [Start fdisk for specific device](#start-fdisk-for-specific-device)
- [Common fdisk commands:](#common-fdisk-commands:)
- [n - create new partition](#n---create-new-partition)
- [p - print partition table](#p---print-partition-table)
- [d - delete partition](#d---delete-partition)
- [w - write changes and exit](#w---write-changes-and-exit)
- [q - quit without saving](#q---quit-without-saving)
    - [Format Partitions](#format-partitions)
- [Format as ext4](#format-as-ext4)
- [Format as XFS (recommended for RHEL/Rocky)](#format-as-xfs-recommended-for-rhel/rocky)
- [Format swap partition](#format-swap-partition)
  - [Mount Operations](#mount-operations)
    - [Temporary Mounts](#temporary-mounts)
- [Mount a partition](#mount-a-partition)
- [Mount with specific options](#mount-with-specific-options)
- [Unmount a partition](#unmount-a-partition)
    - [Persistent Mounts (fstab)](#persistent-mounts-fstab)
- [View current fstab entries](#view-current-fstab-entries)
- [Add new mount (example format):](#add-new-mount-example-format:)
- [/dev/sda1 /mnt/data ext4 defaults 0 0](#/dev/sda1-/mnt/data-ext4-defaults-0-0)
    - [Working with fstab](#working-with-fstab)
- [Test fstab entry](#test-fstab-entry)
- [Get device UUID](#get-device-uuid)
- [Example fstab entry using UUID](#example-fstab-entry-using-uuid)
  - [Storage Analysis](#storage-analysis)
    - [Find Large Files](#find-large-files)
- [Find files larger than 100MB](#find-files-larger-than-100mb)
- [Find and sort by size](#find-and-sort-by-size)
- [List top 10 largest files in directory](#list-top-10-largest-files-in-directory)
    - [Directory Size Analysis](#directory-size-analysis)
- [Show directory sizes, sorted](#show-directory-sizes,-sorted)
- [Analyze disk usage with ncdu (needs installation)](#analyze-disk-usage-with-ncdu-needs-installation)
    - [Disk Usage Visualization](#disk-usage-visualization)
- [Install disk usage analyzers](#install-disk-usage-analyzers)
  - [Symbolic Links](#symbolic-links)
    - [Create Symbolic Links](#create-symbolic-links)
- [Create symbolic link](#create-symbolic-link)
- [Create hard link](#create-hard-link)
    - [Manage Symbolic Links](#manage-symbolic-links)
- [List symbolic links in directory](#list-symbolic-links-in-directory)
- [Find broken symbolic links](#find-broken-symbolic-links)
- [Remove symbolic link](#remove-symbolic-link)
- [or](#or)
  - [Advanced Operations](#advanced-operations)
    - [Resize Partitions](#resize-partitions)
- [Extend XFS filesystem to use all available space](#extend-xfs-filesystem-to-use-all-available-space)
- [Resize ext4 filesystem](#resize-ext4-filesystem)
- [Extend LVM volume](#extend-lvm-volume)
    - [LVM Operations](#lvm-operations)
- [Display LVM information](#display-lvm-information)
- [Create LVM components](#create-lvm-components)
    - [RAID Management](#raid-management)
- [View RAID status](#view-raid-status)
- [Create RAID array](#create-raid-array)
  - [Troubleshooting](#troubleshooting)
    - [Check Filesystem](#check-filesystem)
- [Check ext4 filesystem](#check-ext4-filesystem)
- [Check XFS filesystem](#check-xfs-filesystem)
- [Force fsck on next boot](#force-fsck-on-next-boot)
    - [Monitor I/O Activity](#monitor-i/o-activity)
- [Monitor I/O in real-time](#monitor-i/o-in-real-time)
- [View I/O statistics](#view-i/o-statistics)
- [Monitor disk activity](#monitor-disk-activity)
    - [Recovery](#recovery)
- [Recover deleted files (if ext3/4)](#recover-deleted-files-if-ext3/4)
- [Create disk image for recovery](#create-disk-image-for-recovery)
  - [Best Practices](#best-practices)
  - [Additional Resources](#additional-resources)

## Disk Information Commands

### View Disk Space Usage
```bash
# Show disk space usage of mounted filesystems
df -h

# Show disk space usage in inodes
df -i

# Show disk usage for specific directory
du -sh /path/to/directory

# Show disk usage for all directories in current path
du -h --max-depth=1
```

### List Block Devices
```bash
# List all block devices with details
lsblk

# Show detailed information about specific device
lsblk /dev/sda

# Show disk information including serial numbers
lsblk -o NAME,SIZE,TYPE,SERIAL
```

## Partition Management

### List Partitions
```bash
# List all partitions
fdisk -l

# List partitions on specific device
fdisk -l /dev/sda
```

### Create New Partition
```bash
# Start fdisk for specific device
fdisk /dev/sda

# Common fdisk commands:
# n - create new partition
# p - print partition table
# d - delete partition
# w - write changes and exit
# q - quit without saving
```

### Format Partitions
```bash
# Format as ext4
mkfs.ext4 /dev/sda1

# Format as XFS (recommended for RHEL/Rocky)
mkfs.xfs /dev/sda1

# Format swap partition
mkswap /dev/sda2
```

## Mount Operations

### Temporary Mounts
```bash
# Mount a partition
mount /dev/sda1 /mnt/data

# Mount with specific options
mount -o rw,noexec /dev/sda1 /mnt/data

# Unmount a partition
umount /mnt/data
```

### Persistent Mounts (fstab)
```bash
# View current fstab entries
cat /etc/fstab

# Add new mount (example format):
# /dev/sda1 /mnt/data ext4 defaults 0 0
```

### Working with fstab
```bash
# Test fstab entry
mount -a

# Get device UUID
blkid /dev/sda1

# Example fstab entry using UUID
UUID=1234-5678 /mnt/data ext4 defaults 0 0
```

## Storage Analysis

### Find Large Files
```bash
# Find files larger than 100MB
find /path -type f -size +100M

# Find and sort by size
find /path -type f -exec du -h {} \; | sort -rh

# List top 10 largest files in directory
du -ah /path | sort -rh | head -n 10
```

### Directory Size Analysis
```bash
# Show directory sizes, sorted
du -h --max-depth=1 /path | sort -rh

# Analyze disk usage with ncdu (needs installation)
ncdu /path
```

### Disk Usage Visualization
```bash
# Install disk usage analyzers
dnf install baobab    # GNOME Disk Usage Analyzer
dnf install qdirstat  # QDirStat
```

## Symbolic Links

### Create Symbolic Links
```bash
# Create symbolic link
ln -s /path/to/target /path/to/link

# Create hard link
ln /path/to/target /path/to/link
```

### Manage Symbolic Links
```bash
# List symbolic links in directory
ls -la | grep ^l

# Find broken symbolic links
find /path -type l -! -exec test -e {} \; -print

# Remove symbolic link
unlink /path/to/link
# or
rm /path/to/link
```

## Advanced Operations

### Resize Partitions
```bash
# Extend XFS filesystem to use all available space
xfs_growfs /mount/point

# Resize ext4 filesystem
resize2fs /dev/sda1

# Extend LVM volume
lvextend -L +10G /dev/vg0/lv0
lvextend -l +100%FREE /dev/vg0/lv0
```

### LVM Operations
```bash
# Display LVM information
pvdisplay  # Physical volumes
vgdisplay  # Volume groups
lvdisplay  # Logical volumes

# Create LVM components
pvcreate /dev/sdb
vgcreate vg0 /dev/sdb
lvcreate -L 10G -n lv0 vg0
```

### RAID Management
```bash
# View RAID status
cat /proc/mdstat
mdadm --detail /dev/md0

# Create RAID array
mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1
```

## Troubleshooting

### Check Filesystem
```bash
# Check ext4 filesystem
fsck.ext4 -f /dev/sda1

# Check XFS filesystem
xfs_repair /dev/sda1

# Force fsck on next boot
touch /forcefsck
```

### Monitor I/O Activity
```bash
# Monitor I/O in real-time
iotop

# View I/O statistics
iostat -x 1

# Monitor disk activity
vmstat 1
```

### Recovery
```bash
# Recover deleted files (if ext3/4)
extundelete /dev/sda1 --restore-file /path/to/file

# Create disk image for recovery
dd if=/dev/sda of=/path/to/disk.img bs=4M status=progress
```

## Best Practices

1. Always backup important data before partition operations
2. Use LVM when possible for flexibility
3. Monitor disk space regularly with automated alerts
4. Keep filesystem journal enabled for better recovery
5. Use UUIDs in fstab instead of device names
6. Regularly check for and remove unnecessary large files
7. Document all storage configurations
8. Test recovery procedures periodically

## Additional Resources

- RHEL Documentation: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9
- Rocky Linux Documentation: https://docs.rockylinux.org/
- Linux Documentation Project: https://tldp.org/
