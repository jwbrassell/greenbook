# Advanced Error Handling

## Table of Contents
- [Advanced Error Handling](#advanced-error-handling)
  - [Table of Contents](#table-of-contents)
          - [tags: error, debugging, recovery, logging, exceptions](#tags:-error,-debugging,-recovery,-logging,-exceptions)
  - [Error Trapping Framework](#error-trapping-framework)
          - [tags: trapping, errors, handling](#tags:-trapping,-errors,-handling)
- [Error Handling Framework](#error-handling-framework)
- [!/bin/bash](#!/bin/bash)
- [Global error log](#global-error-log)
- [Error handler function](#error-handler-function)
- [Set trap for errors](#set-trap-for-errors)
- [Debug logging function](#debug-logging-function)
- [Example usage](#example-usage)
  - [Graceful Degradation](#graceful-degradation)
          - [tags: degradation, fallback, recovery](#tags:-degradation,-fallback,-recovery)
- [Graceful Degradation Framework](#graceful-degradation-framework)
- [!/bin/bash](#!/bin/bash)
- [Configuration](#configuration)
- [Service check with fallback](#service-check-with-fallback)
- [Graceful degradation handler](#graceful-degradation-handler)
- [Emergency mode handler](#emergency-mode-handler)
- [Resource check with degradation](#resource-check-with-degradation)
  - [Logging and Debugging](#logging-and-debugging)
          - [tags: logging, debugging, tracing](#tags:-logging,-debugging,-tracing)
- [Advanced Logging Framework](#advanced-logging-framework)
- [!/bin/bash](#!/bin/bash)
- [Log levels](#log-levels)
- [Logging function](#logging-function)
- [Debug trace function](#debug-trace-function)
- [Function call tracer](#function-call-tracer)
- [Variable inspector](#variable-inspector)
  - [Exception Handling](#exception-handling)
          - [tags: exceptions, errors, handling](#tags:-exceptions,-errors,-handling)
- [Exception Handling Framework](#exception-handling-framework)
- [!/bin/bash](#!/bin/bash)
- [Custom exception types](#custom-exception-types)
- [Throw exception](#throw-exception)
- [Try-catch implementation](#try-catch-implementation)
- [Example usage](#example-usage)
  - [Cleanup and Recovery](#cleanup-and-recovery)
          - [tags: cleanup, recovery, restoration](#tags:-cleanup,-recovery,-restoration)
- [Cleanup and Recovery Framework](#cleanup-and-recovery-framework)
- [!/bin/bash](#!/bin/bash)
- [Temporary files and cleanup](#temporary-files-and-cleanup)
- [Register cleanup handlers](#register-cleanup-handlers)
- [Cleanup function](#cleanup-function)
- [Create temporary file with cleanup](#create-temporary-file-with-cleanup)
- [Create temporary directory with cleanup](#create-temporary-directory-with-cleanup)
- [Mount device with cleanup](#mount-device-with-cleanup)
- [Start background process with cleanup](#start-background-process-with-cleanup)
- [Recovery function](#recovery-function)
- [Create restore point](#create-restore-point)
- [Restore from backup](#restore-from-backup)
  - [See Also](#see-also)



###### tags: `error`, `debugging`, `recovery`, `logging`, `exceptions`

## Error Trapping Framework
###### tags: `trapping`, `errors`, `handling`

```bash
# Error Handling Framework
#!/bin/bash
set -eE  # Exit on error and error trap inheritance
set -o pipefail  # Catch pipe failures

# Global error log
ERROR_LOG="/var/log/script_errors.log"
DEBUG=false

# Error handler function
error_handler() {
    local line_no=$1
    local error_code=$2
    local last_command="${BASH_COMMAND}"
    
    # Log error details
    {
        echo "=== Error Report ==="
        echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
        echo "Script: $0"
        echo "Line: $line_no"
        echo "Command: $last_command"
        echo "Exit code: $error_code"
        echo "Stack trace:"
        
        # Print stack trace
        local frame=0
        while caller $frame; do
            ((frame++))
        done
        
        echo "=== End Error Report ==="
    } >> "$ERROR_LOG"
    
    # Cleanup and exit
    cleanup
    exit $error_code
}

# Set trap for errors
trap 'error_handler ${LINENO} $?' ERR

# Debug logging function
debug() {
    if [ "$DEBUG" = true ]; then
        echo "[DEBUG] $*" >&2
    fi
}

# Example usage
debug "Starting script execution"
if ! some_command; then
    error_handler ${LINENO} $?
fi
```

## Graceful Degradation
###### tags: `degradation`, `fallback`, `recovery`

```bash
# Graceful Degradation Framework
#!/bin/bash

# Configuration
PRIMARY_SERVICE="main_service"
BACKUP_SERVICE="backup_service"
FALLBACK_MODE=false
MAX_RETRIES=3
RETRY_DELAY=5

# Service check with fallback
check_service() {
    local service="$1"
    local retry_count=0
    
    while [ $retry_count -lt $MAX_RETRIES ]; do
        if systemctl is-active --quiet "$service"; then
            return 0
        fi
        
        ((retry_count++))
        echo "Service $service check failed, attempt $retry_count of $MAX_RETRIES"
        sleep $RETRY_DELAY
    done
    
    return 1
}

# Graceful degradation handler
handle_degradation() {
    local service="$1"
    echo "Service $service failed, initiating graceful degradation"
    
    case "$service" in
        "$PRIMARY_SERVICE")
            if check_service "$BACKUP_SERVICE"; then
                FALLBACK_MODE=true
                echo "Switched to backup service"
                return 0
            fi
            ;;
        "$BACKUP_SERVICE")
            if [ "$FALLBACK_MODE" = true ]; then
                echo "Backup service failed, entering emergency mode"
                enter_emergency_mode
                return 1
            fi
            ;;
    esac
    
    return 1
}

# Emergency mode handler
enter_emergency_mode() {
    echo "Entering emergency mode"
    
    # Disable non-critical services
    for service in $NON_CRITICAL_SERVICES; do
        systemctl stop "$service"
    done
    
    # Enable minimal functionality
    enable_minimal_mode
    
    # Notify administrators
    send_emergency_alert
}

# Resource check with degradation
check_resources() {
    local cpu_threshold=90
    local mem_threshold=90
    local disk_threshold=90
    
    # Check CPU usage
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}')
    if [ "${cpu_usage%.*}" -gt "$cpu_threshold" ]; then
        handle_high_cpu_usage
    fi
    
    # Check memory usage
    mem_usage=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    if [ "${mem_usage%.*}" -gt "$mem_threshold" ]; then
        handle_high_memory_usage
    fi
    
    # Check disk usage
    disk_usage=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
    if [ "$disk_usage" -gt "$disk_threshold" ]; then
        handle_high_disk_usage
    fi
}
```

## Logging and Debugging
###### tags: `logging`, `debugging`, `tracing`

```bash
# Advanced Logging Framework
#!/bin/bash

# Log levels
declare -A LOG_LEVELS=([DEBUG]=0 [INFO]=1 [WARN]=2 [ERROR]=3 [FATAL]=4)
LOG_LEVEL="INFO"
LOG_FILE="/var/log/script.log"
LOG_FORMAT="[%s] [%-5s] %s\n"

# Logging function
log() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Check if we should log this level
    if [ "${LOG_LEVELS[$level]}" -ge "${LOG_LEVELS[$LOG_LEVEL]}" ]; then
        printf "$LOG_FORMAT" "$timestamp" "$level" "$message" >> "$LOG_FILE"
        
        # Also print to stderr for ERROR and FATAL
        if [ "$level" = "ERROR" ] || [ "$level" = "FATAL" ]; then
            printf "$LOG_FORMAT" "$timestamp" "$level" "$message" >&2
        fi
    fi
}

# Debug trace function
enable_debug_trace() {
    export PS4='+(${BASH_SOURCE}:${LINENO}): ${FUNCNAME[0]:+${FUNCNAME[0]}(): }'
    set -x
}

# Function call tracer
trace_calls() {
    local func_name="$1"
    local original_definition=$(declare -f "$func_name")
    local new_definition="$func_name() {
        log 'DEBUG' \"Entering $func_name with args: \$@\"
        local start_time=\$(date +%s%N)
        ${original_definition#*{}"
        local end_time=\$(date +%s%N)
        local duration=\$(( (end_time - start_time) / 1000000 ))
        log 'DEBUG' \"Exiting $func_name (duration: \${duration}ms)\"
    }"
    eval "$new_definition"
}

# Variable inspector
inspect_var() {
    local var_name="$1"
    local var_value="${!var_name}"
    local var_type=$(declare -p "$var_name" 2>/dev/null || echo "undefined")
    
    log "DEBUG" "Variable: $var_name"
    log "DEBUG" "Type: $var_type"
    log "DEBUG" "Value: $var_value"
    if [ -n "$var_value" ]; then
        log "DEBUG" "Length: ${#var_value}"
    fi
}
```

## Exception Handling
###### tags: `exceptions`, `errors`, `handling`

```bash
# Exception Handling Framework
#!/bin/bash

# Custom exception types
declare -A EXCEPTIONS=(
    [InvalidArgument]="Invalid argument provided"
    [FileNotFound]="File not found"
    [PermissionDenied]="Permission denied"
    [NetworkError]="Network operation failed"
    [DatabaseError]="Database operation failed"
)

# Throw exception
throw() {
    local exception_type="$1"
    local message="${2:-${EXCEPTIONS[$exception_type]}}"
    
    echo "Exception: $exception_type" >&2
    echo "Message: $message" >&2
    echo "Location: ${BASH_SOURCE[1]}:${BASH_LINENO[0]}" >&2
    
    # Generate stack trace
    local frame=0
    echo "Stack trace:" >&2
    while caller $frame; do
        ((frame++))
    done >&2
    
    exit 1
}

# Try-catch implementation
try() {
    local try_result
    {
        try_result=$("$@")
    } 2> >(read line; echo "$line" > "$TMP_ERROR_FILE")
    
    echo "$try_result"
    return $?
}

catch() {
    local error_type="$1"
    if [ -f "$TMP_ERROR_FILE" ]; then
        local error=$(cat "$TMP_ERROR_FILE")
        if [[ "$error" == *"$error_type"* ]]; then
            shift
            "$@"
            return 0
        fi
    fi
    return 1
}

# Example usage
validate_input() {
    local input="$1"
    if [ -z "$input" ]; then
        throw InvalidArgument "Input cannot be empty"
    fi
    echo "$input"
}

process_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        throw FileNotFound "File $file does not exist"
    fi
    if [ ! -r "$file" ]; then
        throw PermissionDenied "Cannot read file $file"
    fi
    cat "$file"
}
```

## Cleanup and Recovery
###### tags: `cleanup`, `recovery`, `restoration`

```bash
# Cleanup and Recovery Framework
#!/bin/bash

# Temporary files and cleanup
declare -a TEMP_FILES=()
declare -a TEMP_DIRS=()
declare -a MOUNTED_DEVICES=()
declare -a BACKGROUND_PIDS=()

# Register cleanup handlers
trap cleanup EXIT
trap 'cleanup; exit 1' INT TERM

# Cleanup function
cleanup() {
    local exit_code=$?
    echo "Performing cleanup..."
    
    # Stop background processes
    for pid in "${BACKGROUND_PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
        fi
    done
    
    # Unmount devices
    for device in "${MOUNTED_DEVICES[@]}"; do
        if mountpoint -q "$device"; then
            umount "$device"
        fi
    done
    
    # Remove temporary files
    for file in "${TEMP_FILES[@]}"; do
        if [ -f "$file" ]; then
            rm -f "$file"
        fi
    done
    
    # Remove temporary directories
    for dir in "${TEMP_DIRS[@]}"; do
        if [ -d "$dir" ]; then
            rm -rf "$dir"
        fi
    done
    
    return $exit_code
}

# Create temporary file with cleanup
create_temp_file() {
    local temp_file=$(mktemp)
    TEMP_FILES+=("$temp_file")
    echo "$temp_file"
}

# Create temporary directory with cleanup
create_temp_dir() {
    local temp_dir=$(mktemp -d)
    TEMP_DIRS+=("$temp_dir")
    echo "$temp_dir"
}

# Mount device with cleanup
mount_device() {
    local device="$1"
    local mount_point="$2"
    
    mount "$device" "$mount_point"
    MOUNTED_DEVICES+=("$mount_point")
}

# Start background process with cleanup
start_background_process() {
    "$@" &
    local pid=$!
    BACKGROUND_PIDS+=("$pid")
    echo "$pid"
}

# Recovery function
recover() {
    local backup_file="$1"
    local restore_point="$2"
    
    echo "Starting recovery process..."
    
    # Verify backup
    if ! verify_backup "$backup_file"; then
        throw InvalidBackup "Backup file is corrupted"
    fi
    
    # Create restore point
    create_restore_point "$restore_point"
    
    # Perform recovery
    restore_from_backup "$backup_file" "$restore_point"
    
    echo "Recovery completed successfully"
}

# Create restore point
create_restore_point() {
    local point_name="$1"
    local point_dir="/var/backups/restore_points/$point_name"
    
    mkdir -p "$point_dir"
    
    # Backup current state
    tar czf "$point_dir/state.tar.gz" -C / etc var/lib/mysql
    
    # Save package list
    dpkg --get-selections > "$point_dir/packages.list"
    
    # Save configuration files
    cp -r /etc/nginx/conf.d "$point_dir/nginx_conf"
    cp /etc/mysql/my.cnf "$point_dir/mysql_conf"
}

# Restore from backup
restore_from_backup() {
    local backup_file="$1"
    local restore_point="$2"
    
    echo "Restoring from backup..."
    
    # Stop services
    systemctl stop nginx mysql
    
    # Restore files
    tar xzf "$backup_file" -C /
    
    # Restore configurations
    cp -r "$restore_point/nginx_conf"/* /etc/nginx/conf.d/
    cp "$restore_point/mysql_conf" /etc/mysql/my.cnf
    
    # Restore packages
    dpkg --set-selections < "$restore_point/packages.list"
    apt-get dselect-upgrade -y
    
    # Start services
    systemctl start mysql nginx
    
    echo "Restore completed"
}
```

## See Also
- [Basic Operations](basics.md)
- [Advanced Script Patterns](advanced_patterns.md)
- [System Monitoring](monitoring.md)
