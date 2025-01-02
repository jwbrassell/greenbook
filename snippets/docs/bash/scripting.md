# Shell Scripting Fundamentals

## Table of Contents
- [Shell Scripting Fundamentals](#shell-scripting-fundamentals)
  - [Table of Contents](#table-of-contents)
          - [tags: scripting, variables, functions, control, input, output, error](#tags:-scripting,-variables,-functions,-control,-input,-output,-error)
  - [Script Structure](#script-structure)
          - [tags: structure, shebang, comments](#tags:-structure,-shebang,-comments)
- [!/bin/bash          # Shebang line - ALWAYS start with this](#!/bin/bash----------#-shebang-line---always-start-with-this)
- [](#)
- [Script Name: example.sh](#script-name:-examplesh)
- [Description: Example script showing basic structure](#description:-example-script-showing-basic-structure)
- [Author: Your Name](#author:-your-name)
- [Date: YYYY-MM-DD](#date:-yyyy-mm-dd)
- [](#)
- [Set script options](#set-script-options)
- [Define constants](#define-constants)
- [Main script logic below](#main-script-logic-below)
  - [Variables and Data Types](#variables-and-data-types)
          - [tags: variables, strings, numbers, arrays](#tags:-variables,-strings,-numbers,-arrays)
- [String variables](#string-variables)
- [Number variables](#number-variables)
- [Arrays](#arrays)
- [Environment variables](#environment-variables)
  - [Control Structures](#control-structures)
          - [tags: if, loops, case, select](#tags:-if,-loops,-case,-select)
- [If statements](#if-statements)
- [File conditions](#file-conditions)
- [Numeric comparisons](#numeric-comparisons)
- [String comparisons](#string-comparisons)
- [For loops](#for-loops)
- [While loops](#while-loops)
- [Until loops](#until-loops)
- [Case statements](#case-statements)
- [Select menus](#select-menus)
  - [Functions](#functions)
          - [tags: functions, arguments, return](#tags:-functions,-arguments,-return)
- [Basic function](#basic-function)
- [Alternative syntax](#alternative-syntax)
- [Function with return value](#function-with-return-value)
- [Function with local variables](#function-with-local-variables)
- [Function usage](#function-usage)
  - [Input/Output](#input/output)
          - [tags: input, output, redirection](#tags:-input,-output,-redirection)
- [Command line arguments](#command-line-arguments)
- [User input](#user-input)
- [Output](#output)
- [Redirection](#redirection)
- [Here documents](#here-documents)
- [Here strings](#here-strings)
  - [Basic Error Handling](#basic-error-handling)
          - [tags: errors, exit, traps](#tags:-errors,-exit,-traps)
- [Exit codes](#exit-codes)
- [Error checking](#error-checking)
- [Command success/failure](#command-success/failure)
- [Error trapping](#error-trapping)
- [Safe operations](#safe-operations)
- [Cleanup function](#cleanup-function)
  - [See Also](#see-also)



###### tags: `scripting`, `variables`, `functions`, `control`, `input`, `output`, `error`

## Script Structure
###### tags: `structure`, `shebang`, `comments`

```bash
#!/bin/bash          # Shebang line - ALWAYS start with this
#
# Script Name: example.sh
# Description: Example script showing basic structure
# Author: Your Name
# Date: YYYY-MM-DD
#

# Set script options
set -e              # Exit on error
set -u              # Exit on undefined variable
set -o pipefail     # Exit on pipe failure

# Define constants
readonly CONFIG_FILE="/etc/app/config.conf"
readonly LOG_FILE="/var/log/app.log"

# Main script logic below
```

## Variables and Data Types
###### tags: `variables`, `strings`, `numbers`, `arrays`

```bash
# String variables
name="John Doe"     # Define string
echo "$name"        # Use variable
echo "${name}"      # Alternative syntax
echo '$name'        # Literal string (no expansion)

# Number variables
count=42            # Define number
total=$((count + 5)) # Arithmetic
((count++))         # Increment
let "count += 1"    # Alternative arithmetic

# Arrays
fruits=("apple" "banana" "orange")
echo "${fruits[0]}"  # Access element
echo "${fruits[@]}"  # All elements
echo "${#fruits[@]}" # Array length

# Environment variables
export PATH="$PATH:/new/path"  # Modify PATH
echo "$HOME"        # Use env variable
printenv            # Show all env vars
```

## Control Structures
###### tags: `if`, `loops`, `case`, `select`

```bash
# If statements
if [ "$a" = "$b" ]; then
    echo "Equal"
elif [ "$a" != "$b" ]; then
    echo "Not equal"
else
    echo "Other"
fi

# File conditions
if [ -f "$file" ]; then    # If file exists
    echo "File exists"
elif [ -d "$dir" ]; then   # If directory exists
    echo "Directory exists"
fi

# Numeric comparisons
if (( $num > 10 )); then
    echo "Greater than 10"
fi

# String comparisons
if [[ "$string" == *"pattern"* ]]; then
    echo "Pattern found"
fi

# For loops
for i in {1..5}; do
    echo "$i"
done

for file in *.txt; do
    echo "Processing $file"
done

# While loops
while [ "$count" -gt 0 ]; do
    echo "$count"
    ((count--))
done

# Until loops
until [ "$count" -eq 0 ]; do
    echo "$count"
    ((count--))
done

# Case statements
case "$option" in
    start)
        start_service
        ;;
    stop)
        stop_service
        ;;
    restart)
        restart_service
        ;;
    *)
        echo "Unknown option"
        ;;
esac

# Select menus
select option in "Start" "Stop" "Restart" "Exit"; do
    case $option in
        "Start")
            start_service
            ;;
        "Stop")
            stop_service
            ;;
        "Restart")
            restart_service
            ;;
        "Exit")
            break
            ;;
    esac
done
```

## Functions
###### tags: `functions`, `arguments`, `return`

```bash
# Basic function
function greet() {
    echo "Hello, $1!"
}

# Alternative syntax
say_goodbye() {
    echo "Goodbye, $1!"
}

# Function with return value
is_number() {
    [[ "$1" =~ ^[0-9]+$ ]]
    return $?
}

# Function with local variables
process_file() {
    local filename="$1"
    local count=0
    while read -r line; do
        ((count++))
    done < "$filename"
    echo "$count"
}

# Function usage
greet "John"              # Call function
result=$(process_file "input.txt")  # Capture output
if is_number "$var"; then          # Use return value
    echo "Is a number"
fi
```

## Input/Output
###### tags: `input`, `output`, `redirection`

```bash
# Command line arguments
echo "$1"           # First argument
echo "$@"           # All arguments
echo "$#"           # Number of arguments
echo "$0"           # Script name

# User input
read -p "Name: " name    # Prompt for input
read -s -p "Password: " pass  # Silent input
read -r line            # Read line
read -a array          # Read into array

# Output
echo "Standard output"
echo "Error message" >&2  # Error output
printf "%-10s %d\n" "Count:" 42  # Formatted output

# Redirection
command > file      # Redirect stdout
command >> file     # Append stdout
command 2> file     # Redirect stderr
command &> file     # Redirect both
command < file      # Input from file

# Here documents
cat << EOF > file.txt
Line 1
Line 2
EOF

# Here strings
grep "pattern" <<< "$string"
```

## Basic Error Handling
###### tags: `errors`, `exit`, `traps`

```bash
# Exit codes
exit 0             # Success
exit 1             # General error
exit 2             # Incorrect usage

# Error checking
if ! command; then
    echo "Command failed" >&2
    exit 1
fi

# Command success/failure
command && echo "Success" || echo "Failed"

# Error trapping
trap 'echo "Error on line $LINENO"' ERR
trap 'cleanup' EXIT

# Safe operations
set -e            # Exit on error
set -u            # Exit on undefined variable
set -o pipefail   # Check pipe failures

# Cleanup function
cleanup() {
    # Remove temporary files
    rm -f "$tmpfile"
}
```

## See Also
- [Basic Operations](basics.md)
- [Advanced Script Patterns](advanced_patterns.md)
- [Advanced Error Handling](error_handling.md)
