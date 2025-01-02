# Advanced Script Patterns

## Table of Contents
- [Advanced Script Patterns](#advanced-script-patterns)
  - [Table of Contents](#table-of-contents)
          - [tags: advanced, functions, arrays, patterns, libraries, io](#tags:-advanced,-functions,-arrays,-patterns,-libraries,-io)
  - [Advanced Functions](#advanced-functions)
          - [tags: functions, libraries, patterns](#tags:-functions,-libraries,-patterns)
- [Advanced Function Structure](#advanced-function-structure)
- [Function with default arguments](#function-with-default-arguments)
- [Function with validation](#function-with-validation)
- [Function with multiple returns](#function-with-multiple-returns)
  - [Function Libraries](#function-libraries)
          - [tags: libraries, modules, import](#tags:-libraries,-modules,-import)
- [lib/utils.sh](#lib/utilssh)
- [!/bin/bash](#!/bin/bash)
- [Utility functions library](#utility-functions-library)
- [Export functions to be used in other scripts](#export-functions-to-be-used-in-other-scripts)
- [Logging utility](#logging-utility)
- [IP validation](#ip-validation)
- [Retry mechanism](#retry-mechanism)
- [Using the library](#using-the-library)
  - [Associative Arrays](#associative-arrays)
          - [tags: arrays, hash, dictionary](#tags:-arrays,-hash,-dictionary)
- [Declare associative array](#declare-associative-array)
- [Access and manipulation](#access-and-manipulation)
- [Iterate over array](#iterate-over-array)
- [Add/update values](#add/update-values)
- [Check key existence](#check-key-existence)
- [Delete key](#delete-key)
  - [Parameter Expansion](#parameter-expansion)
          - [tags: parameters, expansion, substitution](#tags:-parameters,-expansion,-substitution)
- [Default values](#default-values)
- [String operations](#string-operations)
- [Substring](#substring)
- [Case modification](#case-modification)
- [Array operations](#array-operations)
  - [Signal Handling](#signal-handling)
          - [tags: signals, traps, interrupts](#tags:-signals,-traps,-interrupts)
- [Signal trapping](#signal-trapping)
- [Cleanup function](#cleanup-function)
- [Signal handlers](#signal-handlers)
- [Disable signal trapping](#disable-signal-trapping)
  - [Process Management](#process-management)
          - [tags: process, background, jobs](#tags:-process,-background,-jobs)
- [Background processes](#background-processes)
- [Process groups](#process-groups)
- [Named pipes](#named-pipes)
- [Process substitution](#process-substitution)
  - [Advanced I/O](#advanced-i/o)
          - [tags: io, redirection, descriptors](#tags:-io,-redirection,-descriptors)
- [File descriptors](#file-descriptors)
- [Redirect output](#redirect-output)
- [Close file descriptors](#close-file-descriptors)
- [Redirect multiple outputs](#redirect-multiple-outputs)
- [Here strings with processing](#here-strings-with-processing)
- [Temporary file descriptor](#temporary-file-descriptor)
- [File locking](#file-locking)
  - [See Also](#see-also)



###### tags: `advanced`, `functions`, `arrays`, `patterns`, `libraries`, `io`

## Advanced Functions
###### tags: `functions`, `libraries`, `patterns`

```bash
# Advanced Function Structure
function verbose_logger() {
    local level=$1; shift    # Remove first arg and keep rest
    local message=$@         # Remaining arguments
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    printf "[%s] [%s] %s\n" "$timestamp" "$level" "$message"
}

# Function with default arguments
function greet() {
    local name=${1:-"World"}  # Default value if not provided
    echo "Hello, $name!"
}

# Function with validation
function validate_input() {
    local input=$1
    if [[ ! $input =~ ^[0-9]+$ ]]; then
        echo "Error: Input must be numeric" >&2
        return 1
    fi
    return 0
}

# Function with multiple returns
function get_user_info() {
    local username=$1
    local info=$(getent passwd "$username")
    if [ $? -eq 0 ]; then
        echo "$info" | cut -d: -f1  # username
        echo "$info" | cut -d: -f6  # home directory
        return 0
    fi
    return 1
}
```

## Function Libraries
###### tags: `libraries`, `modules`, `import`

```bash
# lib/utils.sh
#!/bin/bash
# Utility functions library

# Export functions to be used in other scripts
export -f log_message
export -f is_valid_ip
export -f retry_command

# Logging utility
log_message() {
    local level=$1
    local message=$2
    logger -t "$(basename "$0")" -p "user.$level" "$message"
}

# IP validation
is_valid_ip() {
    local ip=$1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        return 0
    fi
    return 1
}

# Retry mechanism
retry_command() {
    local -r -i max_attempts="$1"; shift
    local -r command="$@"
    local -i attempt_num=1

    until $command; do
        if ((attempt_num == max_attempts)); then
            echo "Attempt $attempt_num failed and there are no more attempts left!"
            return 1
        else
            echo "Attempt $attempt_num failed! Trying again in $attempt_num seconds..."
            sleep $((attempt_num++))
        fi
    done
}

# Using the library
source ./lib/utils.sh
log_message "info" "Starting application"
if is_valid_ip "192.168.1.1"; then
    echo "Valid IP"
fi
```

## Associative Arrays
###### tags: `arrays`, `hash`, `dictionary`

```bash
# Declare associative array
declare -A config=(
    [host]="localhost"
    [port]="8080"
    [user]="admin"
    [password]="secret"
)

# Access and manipulation
echo "${config[host]}"     # Access value
echo "${!config[@]}"       # List all keys
echo "${config[@]}"        # List all values
echo "${#config[@]}"       # Array size

# Iterate over array
for key in "${!config[@]}"; do
    echo "$key -> ${config[$key]}"
done

# Add/update values
config[timeout]=30
config[host]="newhost"     # Update existing

# Check key existence
if [[ -v config[host] ]]; then
    echo "Host is defined"
fi

# Delete key
unset config[password]
```

## Parameter Expansion
###### tags: `parameters`, `expansion`, `substitution`

```bash
# Default values
${var:-default}        # Use default if unset
${var:=default}        # Set default if unset
${var:?error}         # Error if unset
${var:+value}         # Use alternate if set

# String operations
${var#pattern}        # Remove shortest match from start
${var##pattern}       # Remove longest match from start
${var%pattern}        # Remove shortest match from end
${var%%pattern}       # Remove longest match from end
${var/pattern/replace} # Replace first match
${var//pattern/replace} # Replace all matches
${var/#pattern/replace} # Replace at start
${var/%pattern/replace} # Replace at end

# Substring
${var:offset}         # Substring from offset
${var:offset:length} # Substring with length
${#var}              # String length

# Case modification
${var^}              # Uppercase first char
${var^^}             # Uppercase all chars
${var,}              # Lowercase first char
${var,,}             # Lowercase all chars

# Array operations
${array[@]:offset:length} # Array slice
${array[@]/pattern/replace} # Replace in array
${!array[@]}         # Array indices
```

## Signal Handling
###### tags: `signals`, `traps`, `interrupts`

```bash
# Signal trapping
trap 'cleanup' EXIT
trap 'handle_sigint' SIGINT
trap 'handle_sigterm' SIGTERM
trap 'handle_error $? $LINENO $BASH_LINENO "$BASH_COMMAND" $(printf "::%s" ${FUNCNAME[@]:-})' ERR

# Cleanup function
cleanup() {
    # Remove temporary files
    rm -f "$tmpfile"
    # Kill background processes
    jobs -p | xargs kill
}

# Signal handlers
handle_sigint() {
    echo "Caught SIGINT, cleaning up..."
    cleanup
    exit 130
}

handle_sigterm() {
    echo "Caught SIGTERM, cleaning up..."
    cleanup
    exit 143
}

handle_error() {
    local err=$1
    local line=$2
    local linecallfunc=$3
    local command="$4"
    local funcstack="$5"
    echo "Error in ${funcstack} '$command' on line $line" >&2
    exit "$err"
}

# Disable signal trapping
trap - SIGINT SIGTERM
```

## Process Management
###### tags: `process`, `background`, `jobs`

```bash
# Background processes
coproc { long_running_command; }  # Start coprocess
echo "data" >&"${COPROC[1]}"     # Write to coprocess
read -r response <&"${COPROC[0]}" # Read from coprocess

# Process groups
set -m              # Enable job control
command1 &          # Start in background
command2 &          # Another background process
wait                # Wait for all background processes

# Named pipes
mkfifo pipe        # Create named pipe
exec 3<> pipe      # Open for read/write
echo "data" >&3    # Write to pipe
read -r data <&3   # Read from pipe
exec 3>&-          # Close pipe

# Process substitution
diff <(command1) <(command2)
while read -r line; do
    echo "$line"
done < <(command)
```

## Advanced I/O
###### tags: `io`, `redirection`, `descriptors`

```bash
# File descriptors
exec 3> output.log   # Open for writing
exec 4< input.txt    # Open for reading
exec 5<> file        # Open for both

# Redirect output
echo "log" >&3       # Write to FD 3
read -r line <&4     # Read from FD 4
echo "both" >&5      # Write to FD 5

# Close file descriptors
exec 3>&-            # Close FD 3
exec 4<&-            # Close FD 4
exec 5<&-            # Close FD 5

# Redirect multiple outputs
tee >(command1) >(command2) > file

# Here strings with processing
while read -r line; do
    echo "$line"
done <<< "$multiline_var"

# Temporary file descriptor
{ 
    command1
    command2
} 3> output.log

# File locking
(
    flock -x 200    # Exclusive lock
    # Critical section
) 200> lock_file
```

## See Also
- [Shell Scripting Fundamentals](scripting.md)
- [System Monitoring](monitoring.md)
- [Advanced Error Handling](error_handling.md)
