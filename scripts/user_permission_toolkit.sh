#!/bin/bash
# user_permission_toolkit.sh - Comprehensive User and Permission Management Toolkit

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    local level=$1
    shift
    local message=$@
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        "INFO")
            echo -e "${GREEN}[INFO]${NC} ${timestamp} - $message"
            ;;
        "WARN")
            echo -e "${YELLOW}[WARN]${NC} ${timestamp} - $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} ${timestamp} - $message"
            ;;
    esac
}

# User Management Functions
create_user() {
    local username=$1
    local fullname=$2
    local groups=$3

    if id "$username" &>/dev/null; then
        log "ERROR" "User $username already exists"
        return 1
    }

    useradd -m -c "$fullname" -s /bin/bash "$username"
    if [ $? -eq 0 ]; then
        # Set password expiry
        chage -M 90 -W 7 "$username"
        
        # Add to additional groups if specified
        if [ -n "$groups" ]; then
            usermod -aG "$groups" "$username"
        fi

        # Force password change on first login
        passwd -e "$username"
        
        log "INFO" "User $username created successfully"
    else
        log "ERROR" "Failed to create user $username"
        return 1
    fi
}

delete_user() {
    local username=$1
    local keep_home=$2

    if ! id "$username" &>/dev/null; then
        log "ERROR" "User $username does not exist"
        return 1
    }

    if [ "$keep_home" = "true" ]; then
        userdel "$username"
    else
        userdel -r "$username"
    fi

    if [ $? -eq 0 ]; then
        log "INFO" "User $username deleted successfully"
    else
        log "ERROR" "Failed to delete user $username"
        return 1
    fi
}

modify_user() {
    local username=$1
    local action=$2
    shift 2
    local value=$@

    if ! id "$username" &>/dev/null; then
        log "ERROR" "User $username does not exist"
        return 1
    }

    case "$action" in
        "shell")
            usermod -s "$value" "$username"
            ;;
        "groups")
            usermod -aG "$value" "$username"
            ;;
        "lock")
            usermod -L "$username"
            ;;
        "unlock")
            usermod -U "$username"
            ;;
        *)
            log "ERROR" "Invalid action: $action"
            return 1
            ;;
    esac

    if [ $? -eq 0 ]; then
        log "INFO" "Modified user $username: $action"
    else
        log "ERROR" "Failed to modify user $username"
        return 1
    fi
}

# Group Management Functions
create_group() {
    local groupname=$1
    local gid=$2

    if getent group "$groupname" &>/dev/null; then
        log "ERROR" "Group $groupname already exists"
        return 1
    }

    if [ -n "$gid" ]; then
        groupadd -g "$gid" "$groupname"
    else
        groupadd "$groupname"
    fi

    if [ $? -eq 0 ]; then
        log "INFO" "Group $groupname created successfully"
    else
        log "ERROR" "Failed to create group $groupname"
        return 1
    fi
}

manage_group_members() {
    local groupname=$1
    local action=$2
    local username=$3

    if ! getent group "$groupname" &>/dev/null; then
        log "ERROR" "Group $groupname does not exist"
        return 1
    }

    if ! id "$username" &>/dev/null; then
        log "ERROR" "User $username does not exist"
        return 1
    }

    case "$action" in
        "add")
            usermod -aG "$groupname" "$username"
            ;;
        "remove")
            gpasswd -d "$username" "$groupname"
            ;;
        *)
            log "ERROR" "Invalid action: $action"
            return 1
            ;;
    esac

    if [ $? -eq 0 ]; then
        log "INFO" "$action user $username ${action}ed to/from group $groupname"
    else
        log "ERROR" "Failed to $action user $username to/from group $groupname"
        return 1
    fi
}

# Permission Management Functions
set_permissions() {
    local path=$1
    local owner=$2
    local group=$3
    local perms=$4
    local recursive=$5

    if [ ! -e "$path" ]; then
        log "ERROR" "Path $path does not exist"
        return 1
    }

    if [ "$recursive" = "true" ]; then
        chown -R "$owner:$group" "$path"
        chmod -R "$perms" "$path"
    else
        chown "$owner:$group" "$path"
        chmod "$perms" "$path"
    fi

    if [ $? -eq 0 ]; then
        log "INFO" "Permissions set successfully for $path"
    else
        log "ERROR" "Failed to set permissions for $path"
        return 1
    fi
}

# ACL Management Functions
manage_acl() {
    local path=$1
    local entity=$2
    local name=$3
    local perms=$4
    local action=$5
    local default=$6

    if [ ! -e "$path" ]; then
        log "ERROR" "Path $path does not exist"
        return 1
    }

    local entity_type
    case "$entity" in
        "user") entity_type="u" ;;
        "group") entity_type="g" ;;
        *)
            log "ERROR" "Invalid entity type. Use 'user' or 'group'"
            return 1
            ;;
    esac

    case "$action" in
        "set")
            if [ "$default" = "true" ] && [ -d "$path" ]; then
                setfacl -d -m "$entity_type:$name:$perms" "$path"
            else
                setfacl -m "$entity_type:$name:$perms" "$path"
            fi
            ;;
        "remove")
            if [ "$default" = "true" ] && [ -d "$path" ]; then
                setfacl -d -x "$entity_type:$name" "$path"
            else
                setfacl -x "$entity_type:$name" "$path"
            fi
            ;;
        *)
            log "ERROR" "Invalid action. Use 'set' or 'remove'"
            return 1
            ;;
    esac

    if [ $? -eq 0 ]; then
        log "INFO" "ACL updated successfully for $path"
    else
        log "ERROR" "Failed to update ACL for $path"
        return 1
    fi
}

# Security Audit Functions
audit_users() {
    log "INFO" "=== User Audit ==="
    log "INFO" "Users with UID 0:"
    awk -F: '($3 == 0) {print}' /etc/passwd
    
    log "INFO" "Users with empty passwords:"
    awk -F: '($2 == "") {print}' /etc/shadow
    
    log "INFO" "Users with login shell:"
    grep -v '/nologin\|/false' /etc/passwd
}

audit_sudo() {
    log "INFO" "=== Sudo Access Audit ==="
    grep -v '^#' /etc/sudoers
    ls -l /etc/sudoers.d/
}

audit_permissions() {
    log "INFO" "=== Permission Audit ==="
    log "INFO" "World-writable files:"
    find / -type f -perm -0002 -ls 2>/dev/null
    
    log "INFO" "SUID files:"
    find / -type f -perm -4000 -ls 2>/dev/null
}

# Main menu function
show_menu() {
    echo -e "\n${GREEN}=== User and Permission Management Toolkit ===${NC}"
    echo "1. Create User"
    echo "2. Delete User"
    echo "3. Modify User"
    echo "4. Create Group"
    echo "5. Manage Group Members"
    echo "6. Set Permissions"
    echo "7. Manage ACLs"
    echo "8. Run Security Audit"
    echo "9. Exit"
    echo -n "Select an option: "
}

# Main script execution
while true; do
    show_menu
    read -r choice

    case $choice in
        1)
            read -p "Enter username: " username
            read -p "Enter full name: " fullname
            read -p "Enter additional groups (comma-separated, or press enter to skip): " groups
            create_user "$username" "$fullname" "$groups"
            ;;
        2)
            read -p "Enter username: " username
            read -p "Keep home directory? (true/false): " keep_home
            delete_user "$username" "$keep_home"
            ;;
        3)
            read -p "Enter username: " username
            echo "Select action:"
            echo "1. Change shell"
            echo "2. Add to groups"
            echo "3. Lock account"
            echo "4. Unlock account"
            read -p "Enter choice (1-4): " action_choice
            case $action_choice in
                1)
                    read -p "Enter new shell: " shell
                    modify_user "$username" "shell" "$shell"
                    ;;
                2)
                    read -p "Enter groups (comma-separated): " groups
                    modify_user "$username" "groups" "$groups"
                    ;;
                3)
                    modify_user "$username" "lock"
                    ;;
                4)
                    modify_user "$username" "unlock"
                    ;;
                *)
                    log "ERROR" "Invalid choice"
                    ;;
            esac
            ;;
        4)
            read -p "Enter group name: " groupname
            read -p "Enter GID (optional, press enter to skip): " gid
            create_group "$groupname" "$gid"
            ;;
        5)
            read -p "Enter group name: " groupname
            read -p "Enter action (add/remove): " action
            read -p "Enter username: " username
            manage_group_members "$groupname" "$action" "$username"
            ;;
        6)
            read -p "Enter path: " path
            read -p "Enter owner: " owner
            read -p "Enter group: " group
            read -p "Enter permissions (e.g., 755): " perms
            read -p "Recursive? (true/false): " recursive
            set_permissions "$path" "$owner" "$group" "$perms" "$recursive"
            ;;
        7)
            read -p "Enter path: " path
            read -p "Enter entity type (user/group): " entity
            read -p "Enter name: " name
            read -p "Enter permissions (e.g., rwx): " perms
            read -p "Enter action (set/remove): " action
            read -p "Set as default ACL? (true/false): " default
            manage_acl "$path" "$entity" "$name" "$perms" "$action" "$default"
            ;;
        8)
            audit_users
            audit_sudo
            audit_permissions
            ;;
        9)
            log "INFO" "Exiting..."
            exit 0
            ;;
        *)
            log "ERROR" "Invalid option"
            ;;
    esac
done
