# Advanced Disk Operations in RHEL/Rocky Linux

## Table of Contents
- [Advanced Disk Operations in RHEL/Rocky Linux](#advanced-disk-operations-in-rhel/rocky-linux)
  - [Table of Contents](#table-of-contents)
  - [Understanding LVM (Logical Volume Management)](#understanding-lvm-logical-volume-management)
    - [What is LVM?](#what-is-lvm?)
    - [Real-World Scenario: Growing Business Needs](#real-world-scenario:-growing-business-needs)
  - [LVM Operations](#lvm-operations)
    - [Setting Up LVM](#setting-up-lvm)
    - [Growing LVM Storage](#growing-lvm-storage)
- [Add new disk to volume group](#add-new-disk-to-volume-group)
- [Extend logical volume](#extend-logical-volume)
- [Resize filesystem](#resize-filesystem)
- [or](#or)
  - [RAID Configuration](#raid-configuration)
    - [What is RAID?](#what-is-raid?)
    - [Setting Up Software RAID](#setting-up-software-raid)
      - [Example: Creating a RAID 1 Mirror](#example:-creating-a-raid-1-mirror)
- [Create RAID 1 array](#create-raid-1-array)
- [Watch RAID build progress](#watch-raid-build-progress)
- [Format the RAID array](#format-the-raid-array)
- [Mount the array](#mount-the-array)
    - [RAID Maintenance](#raid-maintenance)
- [Check RAID status](#check-raid-status)
- [Mark disk as failed](#mark-disk-as-failed)
- [Remove failed disk](#remove-failed-disk)
- [Add new disk](#add-new-disk)
  - [Partition Resizing](#partition-resizing)
    - [Online Resizing (No Downtime)](#online-resizing-no-downtime)
      - [Growing a Partition](#growing-a-partition)
- [For LVM](#for-lvm)
- [or](#or)
- [Check new size](#check-new-size)
    - [Offline Resizing](#offline-resizing)
  - [Real-World Examples](#real-world-examples)
    - [Example 1: Setting Up Redundant Storage](#example-1:-setting-up-redundant-storage)
- [Create RAID 1 array](#create-raid-1-array)
- [Create LVM on top of RAID](#create-lvm-on-top-of-raid)
- [Format and mount](#format-and-mount)
    - [Example 2: Expanding Web Server Storage](#example-2:-expanding-web-server-storage)
- [Add new disk](#add-new-disk)
- [Expand logical volume](#expand-logical-volume)
- [Resize filesystem](#resize-filesystem)
  - [Troubleshooting](#troubleshooting)
    - [Problem 1: RAID Array Degraded](#problem-1:-raid-array-degraded)
- [Check RAID status](#check-raid-status)
- [If disk failed, replace it](#if-disk-failed,-replace-it)
    - [Problem 2: LVM Space Issues](#problem-2:-lvm-space-issues)
- [Check space](#check-space)
- [Find large files](#find-large-files)
  - [Best Practices](#best-practices)



This guide covers advanced disk operations including Logical Volume Management (LVM), RAID configuration, and partition resizing. We'll explain these complex topics in simple terms with real-world examples.

## Understanding LVM (Logical Volume Management)

### What is LVM?

Think of LVM like building with LEGO blocks:
- Physical disks are like individual LEGO pieces
- You can combine them into bigger structures (volume groups)
- Then divide that space however you want (logical volumes)
- You can even add or remove pieces while your structure is built!

### Real-World Scenario: Growing Business Needs

Imagine you're running a photo storage service:
1. You start with a 1TB drive
2. As you get more customers, you add another 1TB drive
3. LVM lets you combine these drives and use them as one big storage space
4. You can even resize storage spaces while the system is running!

## LVM Operations

### Setting Up LVM

1. **Create Physical Volumes**
   ```bash
   # Initialize disks for LVM
   sudo pvcreate /dev/sdb
   sudo pvcreate /dev/sdc
   
   # View physical volumes
   sudo pvdisplay
   ```

2. **Create Volume Group**
   ```bash
   # Combine physical volumes into a group
   sudo vgcreate data_vg /dev/sdb /dev/sdc
   
   # View volume groups
   sudo vgdisplay
   ```

3. **Create Logical Volumes**
   ```bash
   # Create logical volumes from the group
   sudo lvcreate -n photos_lv -L 500G data_vg
   sudo lvcreate -n backups_lv -L 1T data_vg
   
   # View logical volumes
   sudo lvdisplay
   ```

### Growing LVM Storage

Scenario: Your photos volume is running out of space

```bash
# Add new disk to volume group
sudo pvcreate /dev/sdd
sudo vgextend data_vg /dev/sdd

# Extend logical volume
sudo lvextend -L +500G /dev/data_vg/photos_lv

# Resize filesystem
sudo xfs_growfs /photos    # for XFS
# or
sudo resize2fs /dev/data_vg/photos_lv  # for ext4
```

## RAID Configuration

### What is RAID?

Think of RAID like making copies of your important documents:
- RAID 0: Splitting documents across multiple folders (faster access, but risky)
- RAID 1: Making exact copies (safer, but uses more space)
- RAID 5: Clever way of keeping partial copies (good balance)
- RAID 10: Making copies AND splitting them (very safe and fast, but expensive)

### Setting Up Software RAID

#### Example: Creating a RAID 1 Mirror

Scenario: Setting up redundant storage for critical data

```bash
# Create RAID 1 array
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# Watch RAID build progress
sudo cat /proc/mdstat

# Format the RAID array
sudo mkfs.xfs /dev/md0

# Mount the array
sudo mount /dev/md0 /mnt/raid
```

### RAID Maintenance

```bash
# Check RAID status
sudo mdadm --detail /dev/md0

# Mark disk as failed
sudo mdadm /dev/md0 --fail /dev/sdb1

# Remove failed disk
sudo mdadm /dev/md0 --remove /dev/sdb1

# Add new disk
sudo mdadm /dev/md0 --add /dev/sdd1
```

## Partition Resizing

### Online Resizing (No Downtime)

#### Growing a Partition
Scenario: Your /var partition needs more space

```bash
# For LVM
sudo lvextend -L +10G /dev/mapper/vg0-var
sudo xfs_growfs /var    # for XFS
# or
sudo resize2fs /dev/mapper/vg0-var  # for ext4

# Check new size
df -h /var
```

### Offline Resizing

Sometimes you need to resize partitions that can't be done online:

1. **Backup First!**
   ```bash
   sudo tar -czf /backup/var_backup.tar.gz /var
   ```

2. **Boot to Recovery Mode**
   ```bash
   # Resize partition using fdisk
   sudo fdisk /dev/sda
   
   # Update filesystem
   sudo resize2fs /dev/sda2
   ```

## Real-World Examples

### Example 1: Setting Up Redundant Storage

Scenario: Creating safe storage for company documents

```bash
# Create RAID 1 array
sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sdb1 /dev/sdc1

# Create LVM on top of RAID
sudo pvcreate /dev/md0
sudo vgcreate secure_vg /dev/md0
sudo lvcreate -n docs_lv -L 500G secure_vg

# Format and mount
sudo mkfs.xfs /dev/secure_vg/docs_lv
sudo mount /dev/secure_vg/docs_lv /company_docs
```

### Example 2: Expanding Web Server Storage

Scenario: Your website's storage is running low

```bash
# Add new disk
sudo pvcreate /dev/sdd
sudo vgextend webdata_vg /dev/sdd

# Expand logical volume
sudo lvextend -l +100%FREE /dev/webdata_vg/www_lv

# Resize filesystem
sudo xfs_growfs /var/www
```

## Troubleshooting

### Problem 1: RAID Array Degraded
```bash
# Check RAID status
sudo mdadm --detail /dev/md0

# If disk failed, replace it
sudo mdadm /dev/md0 --remove /dev/sdb1
sudo mdadm /dev/md0 --add /dev/sdd1
```

### Problem 2: LVM Space Issues
```bash
# Check space
sudo vgdisplay
sudo lvdisplay

# Find large files
sudo du -sh /* | sort -rh
```

## Best Practices

1. **Always Backup First**
   ```bash
   # Create backup
   sudo tar -czf /backup/data_backup.tar.gz /data
   
   # Verify backup
   tar -tzf /backup/data_backup.tar.gz
   ```

2. **Document Your Setup**
   ```bash
   # Save RAID configuration
   sudo mdadm --detail --scan >> /etc/mdadm.conf
   
   # Document LVM setup
   sudo vgdisplay > /root/vg_setup.txt
   sudo lvdisplay >> /root/vg_setup.txt
   ```

3. **Regular Monitoring**
   ```bash
   # Check RAID health
   sudo cat /proc/mdstat
   
   # Check LVM space
   sudo vgs
   sudo lvs
   ```

4. **Test Recovery Procedures**
   ```bash
   # Simulate disk failure
   sudo mdadm --fail /dev/md0 /dev/sdb1
   
   # Practice recovery
   sudo mdadm --remove /dev/md0 /dev/sdb1
   sudo mdadm --add /dev/md0 /dev/sdd1
   ```

Remember: These operations can be risky. Always have backups and test procedures in a non-production environment first!
