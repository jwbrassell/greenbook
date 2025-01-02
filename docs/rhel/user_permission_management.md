# Linux User and Permission Management Guide for RHEL Variants

## Table of Contents
- [Linux User and Permission Management Guide for RHEL Variants](#linux-user-and-permission-management-guide-for-rhel-variants)
  - [Table of Contents](#table-of-contents)
  - [Basic Concepts](#basic-concepts)
    - [Users and Groups](#users-and-groups)
  - [User Management](#user-management)
    - [Creating Users](#creating-users)
- [Basic user creation](#basic-user-creation)
- [Create user with specific settings](#create-user-with-specific-settings)
- [Options explained:](#options-explained:)
- [-m: Create home directory](#-m:-create-home-directory)
- [-d: Specify custom home directory](#-d:-specify-custom-home-directory)
- [-s: Set login shell](#-s:-set-login-shell)
- [-c: Add comment/full name](#-c:-add-comment/full-name)
- [-g: Set primary group](#-g:-set-primary-group)
    - [User Management Script](#user-management-script)
- [!/bin/bash](#!/bin/bash)
- [user_manager.sh - User Management Script](#user_managersh---user-management-script)
- [Usage examples:](#usage-examples:)
- [./user_manager.sh create "john" "John Doe" "developers,docker"](#/user_managersh-create-"john"-"john-doe"-"developers,docker")
- [./user_manager.sh delete "john" true](#/user_managersh-delete-"john"-true)
    - [Modifying Users](#modifying-users)
- [Change user's shell](#change-user's-shell)
- [Add user to supplementary groups](#add-user-to-supplementary-groups)
- [Lock/Unlock user account](#lock/unlock-user-account)
- [Set password expiry](#set-password-expiry)
  - [Group Management](#group-management)
    - [Creating and Managing Groups](#creating-and-managing-groups)
- [Create new group](#create-new-group)
- [Add user to group](#add-user-to-group)
- [Create group with specific GID](#create-group-with-specific-gid)
    - [Group Management Script](#group-management-script)
- [!/bin/bash](#!/bin/bash)
- [group_manager.sh - Group Management Script](#group_managersh---group-management-script)
- [Usage examples:](#usage-examples:)
- [./group_manager.sh create "developers" "5000"](#/group_managersh-create-"developers"-"5000")
- [./group_manager.sh manage developers add john](#/group_managersh-manage-developers-add-john)
  - [Permission Management](#permission-management)
    - [Basic Permissions](#basic-permissions)
- [Change ownership](#change-ownership)
- [Change permissions](#change-permissions)
- [Numeric permissions explained:](#numeric-permissions-explained:)
- [4 (read) + 2 (write) + 1 (execute) = 7](#4-read-+-2-write-+-1-execute-=-7)
- [Common combinations:](#common-combinations:)
- [777 - rwxrwxrwx (full access for all)](#777---rwxrwxrwx-full-access-for-all)
- [755 - rwxr-xr-x (executable files/directories)](#755---rwxr-xr-x-executable-files/directories)
- [644 - rw-r--r-- (regular files)](#644---rw-r--r---regular-files)
- [600 - rw------- (sensitive files)](#600---rw--------sensitive-files)
    - [Permission Management Script](#permission-management-script)
- [!/bin/bash](#!/bin/bash)
- [permission_manager.sh - Permission Management Script](#permission_managersh---permission-management-script)
- [Special directory permissions](#special-directory-permissions)
- [Usage examples:](#usage-examples:)
- [./permission_manager.sh set "/var/www/html" "apache" "developers" "755" "true"](#/permission_managersh-set-"/var/www/html"-"apache"-"developers"-"755"-"true")
- [./permission_manager.sh directory "/shared"](#/permission_managersh-directory-"/shared")
  - [Access Control Lists (ACLs)](#access-control-lists-acls)
    - [Managing ACLs](#managing-acls)
- [Install ACL package](#install-acl-package)
- [Set ACL](#set-acl)
- [Set default ACL for directory](#set-default-acl-for-directory)
- [Remove ACL](#remove-acl)
- [View ACLs](#view-acls)
    - [ACL Management Script](#acl-management-script)
- [!/bin/bash](#!/bin/bash)
- [acl_manager.sh - ACL Management Script](#acl_managersh---acl-management-script)
- [Usage examples:](#usage-examples:)
- [./acl_manager.sh "/shared" "user" "john" "rwx" "set" "false"](#/acl_managersh-"/shared"-"user"-"john"-"rwx"-"set"-"false")
- [./acl_manager.sh "/shared" "group" "developers" "rx" "set" "true"](#/acl_managersh-"/shared"-"group"-"developers"-"rx"-"set"-"true")
  - [Best Practices](#best-practices)
    - [Security Audit Script](#security-audit-script)
- [!/bin/bash](#!/bin/bash)
- [security_audit.sh - Security Audit Script](#security_auditsh---security-audit-script)
- [Run all audits](#run-all-audits)
  - [Automation Tips](#automation-tips)

## Basic Concepts

### Users and Groups
- Every user has a unique UID (User ID)
- Primary group (GID) and supplementary groups
- System users (UID < 1000) vs Regular users (UID >= 1000)
- Key files: `/etc/passwd`, `/etc/shadow`, `/etc/group`

## User Management

### Creating Users
```bash
# Basic user creation
useradd username

# Create user with specific settings
useradd -m -d /home/customhome -s /bin/bash -c "Full Name" -g primarygroup username

# Options explained:
# -m: Create home directory
# -d: Specify custom home directory
# -s: Set login shell
# -c: Add comment/full name
# -g: Set primary group
```

### User Management Script
```bash
#!/bin/bash
# user_manager.sh - User Management Script

create_user() {
    local username=$1
    local fullname=$2
    local groups=$3

    # Check if user exists
    if id "$username" &>/dev/null; then
        echo "User $username already exists"
        return 1
    }

    # Create user with home directory
    useradd -m -c "$fullname" -s /bin/bash "$username"
    
    # Set password expiry
    chage -M 90 -W 7 "$username"
    
    # Add to additional groups if specified
    if [ -n "$groups" ]; then
        usermod -aG "$groups" "$username"
    fi

    # Force password change on first login
    passwd -e "$username"

    echo "User $username created successfully"
}

delete_user() {
    local username=$1
    local keep_home=$2

    if ! id "$username" &>/dev/null; then
        echo "User $username does not exist"
        return 1
    }

    if [ "$keep_home" = "true" ]; then
        userdel "$username"
    else
        userdel -r "$username"
    fi

    echo "User $username deleted successfully"
}

# Usage examples:
# ./user_manager.sh create "john" "John Doe" "developers,docker"
# ./user_manager.sh delete "john" true
```

### Modifying Users
```bash
# Change user's shell
usermod -s /bin/bash username

# Add user to supplementary groups
usermod -aG group1,group2 username

# Lock/Unlock user account
usermod -L username  # Lock
usermod -U username  # Unlock

# Set password expiry
chage -M 90 username  # Maximum password age
chage -W 7 username   # Warning period
```

## Group Management

### Creating and Managing Groups
```bash
# Create new group
groupadd groupname

# Add user to group
usermod -aG groupname username

# Create group with specific GID
groupadd -g 5000 groupname
```

### Group Management Script
```bash
#!/bin/bash
# group_manager.sh - Group Management Script

create_group() {
    local groupname=$1
    local gid=$2

    # Check if group exists
    if getent group "$groupname" &>/dev/null; then
        echo "Group $groupname already exists"
        return 1
    }

    # Create group with specific GID if provided
    if [ -n "$gid" ]; then
        groupadd -g "$gid" "$groupname"
    else
        groupadd "$groupname"
    fi

    echo "Group $groupname created successfully"
}

manage_group_members() {
    local groupname=$1
    local action=$2  # add or remove
    local username=$3

    # Check if group exists
    if ! getent group "$groupname" &>/dev/null; then
        echo "Group $groupname does not exist"
        return 1
    }

    # Check if user exists
    if ! id "$username" &>/dev/null; then
        echo "User $username does not exist"
        return 1
    }

    case "$action" in
        add)
            usermod -aG "$groupname" "$username"
            echo "Added $username to $groupname"
            ;;
        remove)
            gpasswd -d "$username" "$groupname"
            echo "Removed $username from $groupname"
            ;;
        *)
            echo "Invalid action. Use 'add' or 'remove'"
            return 1
            ;;
    esac
}

# Usage examples:
# ./group_manager.sh create "developers" "5000"
# ./group_manager.sh manage developers add john
```

## Permission Management

### Basic Permissions
```bash
# Change ownership
chown user:group file
chown -R user:group directory  # Recursive

# Change permissions
chmod 755 file  # rwxr-xr-x
chmod -R 644 directory  # rw-r--r--

# Numeric permissions explained:
# 4 (read) + 2 (write) + 1 (execute) = 7
# Common combinations:
# 777 - rwxrwxrwx (full access for all)
# 755 - rwxr-xr-x (executable files/directories)
# 644 - rw-r--r-- (regular files)
# 600 - rw------- (sensitive files)
```

### Permission Management Script
```bash
#!/bin/bash
# permission_manager.sh - Permission Management Script

set_permissions() {
    local path=$1
    local owner=$2
    local group=$3
    local perms=$4
    local recursive=$5

    # Validate path
    if [ ! -e "$path" ]; then
        echo "Path $path does not exist"
        return 1
    }

    # Set ownership
    if [ "$recursive" = "true" ]; then
        chown -R "$owner:$group" "$path"
        chmod -R "$perms" "$path"
    else
        chown "$owner:$group" "$path"
        chmod "$perms" "$path"
    fi

    echo "Permissions set successfully for $path"
}

# Special directory permissions
set_directory_permissions() {
    local directory=$1
    
    # Set SGID bit to inherit group ownership
    chmod g+s "$directory"
    
    # Set sticky bit for shared directories
    chmod +t "$directory"
    
    # Set default ACLs
    setfacl -d -m g::rwx "$directory"
    setfacl -d -m o::rx "$directory"
}

# Usage examples:
# ./permission_manager.sh set "/var/www/html" "apache" "developers" "755" "true"
# ./permission_manager.sh directory "/shared"
```

## Access Control Lists (ACLs)

### Managing ACLs
```bash
# Install ACL package
dnf install acl

# Set ACL
setfacl -m u:username:rwx file
setfacl -m g:groupname:rx file

# Set default ACL for directory
setfacl -d -m u:username:rwx directory

# Remove ACL
setfacl -x u:username file

# View ACLs
getfacl file
```

### ACL Management Script
```bash
#!/bin/bash
# acl_manager.sh - ACL Management Script

manage_acl() {
    local path=$1
    local entity=$2    # user or group
    local name=$3      # username or groupname
    local perms=$4
    local action=$5    # set or remove
    local default=$6   # true or false

    # Validate path
    if [ ! -e "$path" ]; then
        echo "Path $path does not exist"
        return 1
    }

    local entity_type
    case "$entity" in
        user) entity_type="u" ;;
        group) entity_type="g" ;;
        *)
            echo "Invalid entity type. Use 'user' or 'group'"
            return 1
            ;;
    esac

    case "$action" in
        set)
            if [ "$default" = "true" ] && [ -d "$path" ]; then
                setfacl -d -m "$entity_type:$name:$perms" "$path"
            else
                setfacl -m "$entity_type:$name:$perms" "$path"
            fi
            ;;
        remove)
            if [ "$default" = "true" ] && [ -d "$path" ]; then
                setfacl -d -x "$entity_type:$name" "$path"
            else
                setfacl -x "$entity_type:$name" "$path"
            fi
            ;;
        *)
            echo "Invalid action. Use 'set' or 'remove'"
            return 1
            ;;
    esac

    echo "ACL updated successfully for $path"
}

# Usage examples:
# ./acl_manager.sh "/shared" "user" "john" "rwx" "set" "false"
# ./acl_manager.sh "/shared" "group" "developers" "rx" "set" "true"
```

## Best Practices

1. **User Management**
   - Use strong password policies
   - Implement password aging
   - Regular audit of user accounts
   - Remove inactive accounts

2. **Group Management**
   - Use groups for role-based access
   - Maintain clear group naming conventions
   - Regular review of group memberships

3. **Permissions**
   - Follow principle of least privilege
   - Use ACLs for complex permission requirements
   - Regular permission audits
   - Document special permissions

4. **Security**
   - Regular security audits
   - Monitor failed login attempts
   - Use sudo instead of root access
   - Implement file system quotas

### Security Audit Script
```bash
#!/bin/bash
# security_audit.sh - Security Audit Script

audit_users() {
    echo "=== User Audit ==="
    echo "Users with UID 0:"
    awk -F: '($3 == 0) {print}' /etc/passwd
    
    echo -e "\nUsers with empty passwords:"
    awk -F: '($2 == "") {print}' /etc/shadow
    
    echo -e "\nUsers with login shell:"
    grep -v '/nologin\|/false' /etc/passwd
}

audit_sudo() {
    echo -e "\n=== Sudo Access Audit ==="
    grep -v '^#' /etc/sudoers
    ls -l /etc/sudoers.d/
}

audit_permissions() {
    echo -e "\n=== Permission Audit ==="
    echo "World-writable files:"
    find / -type f -perm -0002 -ls 2>/dev/null
    
    echo -e "\nSUID files:"
    find / -type f -perm -4000 -ls 2>/dev/null
}

# Run all audits
audit_users
audit_sudo
audit_permissions
```

## Automation Tips

1. Use configuration management tools (Ansible, Puppet) for large-scale deployments
2. Implement user provisioning workflows
3. Regular backup of user/group configurations
4. Automated permission checks and corrections

Remember to always test scripts in a non-production environment first and maintain proper documentation of all changes.
