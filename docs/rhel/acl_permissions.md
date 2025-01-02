# ACL (Access Control List) Permissions in RHEL-based Linux

This guide covers ACL permissions management in RHEL-based Linux distributions (RHEL, CentOS, Rocky Linux). ACLs provide more granular access control beyond traditional Unix permissions.

## Table of Contents
- [ACL (Access Control List) Permissions in RHEL-based Linux](#acl-access-control-list-permissions-in-rhel-based-linux)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
- [Check if ACL is enabled on your filesystem](#check-if-acl-is-enabled-on-your-filesystem)
- [Should show "acl" in the options](#should-show-"acl"-in-the-options)
- [Or check mount options](#or-check-mount-options)
- [Should include "acl" in the options](#should-include-"acl"-in-the-options)
- [RHEL/CentOS/Rocky Linux](#rhel/centos/rocky-linux)
  - [Basic Concepts](#basic-concepts)
    - [Types of ACL Entries](#types-of-acl-entries)
  - [Managing ACLs](#managing-acls)
    - [Viewing ACLs](#viewing-acls)
- [View ACLs for a file](#view-acls-for-a-file)
- [View ACLs for a directory](#view-acls-for-a-directory)
    - [Setting ACLs](#setting-acls)
- [Set ACL for a specific user](#set-acl-for-a-specific-user)
- [Set ACL for a specific group](#set-acl-for-a-specific-group)
- [Set default ACLs for a directory (applies to new files)](#set-default-acls-for-a-directory-applies-to-new-files)
- [Set multiple ACL entries at once](#set-multiple-acl-entries-at-once)
    - [Removing ACLs](#removing-acls)
- [Remove specific user ACL](#remove-specific-user-acl)
- [Remove specific group ACL](#remove-specific-group-acl)
- [Remove all ACLs](#remove-all-acls)
    - [Recursive ACL Operations](#recursive-acl-operations)
- [Set ACLs recursively on existing files and directories](#set-acls-recursively-on-existing-files-and-directories)
- [Set default ACLs recursively (affects future files)](#set-default-acls-recursively-affects-future-files)
  - [Common Use Cases](#common-use-cases)
    - [1. Shared Project Directory](#1-shared-project-directory)
- [Create project directory](#create-project-directory)
- [Set base permissions](#set-base-permissions)
- [Add ACL for developer team](#add-acl-for-developer-team)
- [Add ACL for QA team (read-only)](#add-acl-for-qa-team-read-only)
- [Set default ACLs for new files](#set-default-acls-for-new-files)
    - [2. Restricted Log Access](#2-restricted-log-access)
- [Allow security team read access to logs](#allow-security-team-read-access-to-logs)
- [Allow security team read access to new log files](#allow-security-team-read-access-to-new-log-files)
    - [3. Shared Web Content](#3-shared-web-content)
- [Set up web content directory](#set-up-web-content-directory)
- [Give web developers write access](#give-web-developers-write-access)
- [Give web server read access](#give-web-server-read-access)
- [Set defaults for new files](#set-defaults-for-new-files)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)
    - [Best Practices](#best-practices)

## Prerequisites

1. Ensure ACL support is enabled in your filesystem:
```bash
# Check if ACL is enabled on your filesystem
tune2fs -l /dev/sda1 | grep "Default mount options"
# Should show "acl" in the options

# Or check mount options
mount | grep " / "
# Should include "acl" in the options
```

2. Install ACL utilities if not already present:
```bash
# RHEL/CentOS/Rocky Linux
sudo dnf install acl
```

## Basic Concepts

ACLs extend the traditional Unix permissions (user, group, others) by allowing you to:
- Set permissions for multiple users and groups
- Define more precise access controls
- Maintain compatibility with standard permissions

### Types of ACL Entries
- **User ACL**: Permissions for a specific user
- **Group ACL**: Permissions for a specific group
- **Mask ACL**: Maximum permissions for all entries except the owner
- **Other ACL**: Default permissions for users not covered by other entries

## Managing ACLs

### Viewing ACLs

```bash
# View ACLs for a file
getfacl myfile.txt

# View ACLs for a directory
getfacl mydirectory/
```

### Setting ACLs

```bash
# Set ACL for a specific user
setfacl -m u:username:rwx myfile.txt

# Set ACL for a specific group
setfacl -m g:groupname:rx myfile.txt

# Set default ACLs for a directory (applies to new files)
setfacl -d -m u:username:rwx mydirectory/

# Set multiple ACL entries at once
setfacl -m u:user1:rw,g:group1:rx myfile.txt
```

### Removing ACLs

```bash
# Remove specific user ACL
setfacl -x u:username myfile.txt

# Remove specific group ACL
setfacl -x g:groupname myfile.txt

# Remove all ACLs
setfacl -b myfile.txt
```

### Recursive ACL Operations

```bash
# Set ACLs recursively on existing files and directories
setfacl -R -m u:username:rwx directory/

# Set default ACLs recursively (affects future files)
setfacl -R -d -m u:username:rwx directory/
```

## Common Use Cases

### 1. Shared Project Directory

```bash
# Create project directory
mkdir /projects/website
# Set base permissions
chmod 770 /projects/website
# Add ACL for developer team
setfacl -m g:developers:rwx /projects/website
# Add ACL for QA team (read-only)
setfacl -m g:qa:rx /projects/website
# Set default ACLs for new files
setfacl -d -m g:developers:rwx,g:qa:rx /projects/website
```

### 2. Restricted Log Access

```bash
# Allow security team read access to logs
setfacl -m g:security:r /var/log/secure
# Allow security team read access to new log files
setfacl -d -m g:security:r /var/log
```

### 3. Shared Web Content

```bash
# Set up web content directory
mkdir /var/www/content
# Give web developers write access
setfacl -m g:webdev:rwx /var/www/content
# Give web server read access
setfacl -m u:apache:rx /var/www/content
# Set defaults for new files
setfacl -d -m g:webdev:rwx,u:apache:rx /var/www/content
```

## Troubleshooting

### Common Issues

1. **ACLs Not Working**
   ```bash
   # Check if filesystem is mounted with ACL support
   mount | grep acl
   
   # Check if ACLs are properly set
   getfacl -e filename
   ```

2. **Permission Denied Despite ACL**
   ```bash
   # Check effective permissions
   getfacl --omit-header filename
   
   # Verify mask isn't restricting access
   getfacl -e filename | grep mask
   ```

3. **ACLs Not Inherited**
   ```bash
   # Check if default ACLs are set
   getfacl directory | grep default
   
   # Set default ACLs if missing
   setfacl -d -m u:username:rwx directory
   ```

### Best Practices

1. **Regular Auditing**
   ```bash
   # List all files with ACLs in a directory
   find /path/to/dir -exec getfacl {} \;
   ```

2. **Backup ACLs**
   ```bash
   # Backup ACLs
   getfacl -R /directory > acl_backup.txt
   
   # Restore ACLs
   setfacl --restore=acl_backup.txt
   ```

3. **Maintaining ACL Consistency**
   ```bash
   # Check mask consistency
   getfacl -R /directory | grep mask
   
   # Update masks if needed
   setfacl -R -m m::rwx /directory
   ```

Remember that ACLs provide powerful access control capabilities but should be used judiciously to maintain system security and manageability. Regular auditing and documentation of ACL configurations is recommended for system maintenance.
