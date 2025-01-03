# Chapter 3: Shell Scripting Basics

## Introduction

Think about writing down a recipe or creating a checklist for a routine task. Shell scripts are similar - they're sets of instructions that automate tasks you'd otherwise do manually. Instead of typing the same commands over and over, you can create a script once and run it whenever needed. In this chapter, we'll learn how to write scripts that make your computer work for you.

## 1. Script Fundamentals

### The Recipe Metaphor

Think of a shell script like a cooking recipe:
- Recipe title (script name)
- Ingredients list (required resources)
- Step-by-step instructions (commands)
- Notes and tips (comments)
- Expected result (output)

### Basic Script Structure

```bash
#!/bin/bash                  # Shebang line (tells system this is a bash script)
# Script: backup_docs.sh     # Comment describing script
# Author: Your Name         # Additional information
# Date: 2024-01-01

# Variables
backup_dir="$HOME/backups"   # Like measuring cups in kitchen
source_dir="$HOME/Documents"

# Main script
echo "Starting backup..."    # Like "Preheat oven to 350°F"
```

### Creating Your First Script

1. Create script file:
```bash
touch myscript.sh
chmod +x myscript.sh    # Make executable (like turning on stove)
```

2. Basic script example:
```bash
#!/bin/bash
echo "Hello, World!"
date
pwd
```

### Hands-On Exercise: Script Creator

1. Create a simple system info script:
```bash
#!/bin/bash
echo "=== System Information ==="
echo "Current user: $USER"
echo "Current directory: $PWD"
echo "Today's date: $(date)"
echo "======================="
```

2. Run the script:
```bash
./system_info.sh
```

## 2. Variables and Input

### The Container Metaphor

Think of variables like labeled containers:
- Store ingredients (data)
- Can be emptied and refilled
- Contents can be used multiple times
- Label (name) stays the same

### Variable Basics

```bash
# Assignment
name="Alice"              # No spaces around =
age=25
current_date=$(date)      # Store command output

# Usage
echo "Hello, $name!"      # Use $ to get value
echo "You are $age years old"
echo "Today is $current_date"
```

### User Input

```bash
# The Conversation Metaphor
# Like asking questions while cooking

# Read single value
echo "What's your name?"
read username

# Read with prompt
read -p "Enter your age: " user_age

# Read secret (password)
read -s -p "Password: " password
echo # New line after password
```

### Environment Variables

```bash
# Built-in variables (like kitchen equipment)
echo "Home directory: $HOME"
echo "User name: $USER"
echo "Shell type: $SHELL"

# Setting environment variables
export MY_VAR="value"    # Available to other scripts
```

### Hands-On Exercise: Interactive Script

Create a greeting script:
```bash
#!/bin/bash

# Get user information
read -p "Enter your name: " user_name
read -p "Enter your favorite color: " favorite_color

# Create personalized message
echo "Hello, $user_name!"
echo "I hear you like the color $favorite_color"
```

## 3. Control Structures

### The Decision Tree Metaphor

Like following a recipe with choices:
- If soup is too thick, add water
- While rice isn't done, keep cooking
- For each vegetable, chop and add

### If Statements

```bash
# Basic if
if [ "$age" -gt 18 ]; then
    echo "You're an adult"
fi

# If-else
if [ "$password" == "secret" ]; then
    echo "Access granted"
else
    echo "Access denied"
fi

# If-elif-else
if [ "$grade" -ge 90 ]; then
    echo "A"
elif [ "$grade" -ge 80 ]; then
    echo "B"
else
    echo "Study more"
fi
```

### Loops

```bash
# For loop (like recipe steps)
for fruit in apple banana orange; do
    echo "Processing $fruit"
done

# While loop (like "cook until done")
count=1
while [ $count -le 5 ]; do
    echo "Count: $count"
    count=$((count + 1))
done

# Until loop (like "stir until smooth")
until [ "$answer" == "yes" ]; do
    read -p "Are we there yet? " answer
done
```

### Case Statements

```bash
# Like a recipe's "depending on ingredient" section
read -p "Choose a fruit (apple/banana/orange): " fruit

case $fruit in
    "apple")
        echo "Makes good pie"
        ;;
    "banana")
        echo "Good for smoothies"
        ;;
    "orange")
        echo "Makes juice"
        ;;
    *)
        echo "Unknown fruit"
        ;;
esac
```

### Hands-On Exercise: Decision Maker

Create a simple backup script:
```bash
#!/bin/bash

read -p "What directory to backup? " source_dir

if [ ! -d "$source_dir" ]; then
    echo "Directory doesn't exist!"
    exit 1
fi

backup_name="backup_$(date +%Y%m%d)"

if [ -d "$backup_name" ]; then
    read -p "Backup exists. Overwrite? (y/n) " answer
    if [ "$answer" != "y" ]; then
        echo "Backup cancelled"
        exit 0
    fi
fi

cp -r "$source_dir" "$backup_name"
echo "Backup completed!"
```

## 4. Functions

### The Recipe Components Metaphor

Think of functions like common cooking procedures:
- "Dice vegetables" procedure
- "Make sauce" procedure
- Can be used in multiple recipes
- Makes recipes cleaner and reusable

### Function Basics

```bash
# Define function
say_hello() {
    echo "Hello, $1!"    # $1 is first argument
}

# Use function
say_hello "Alice"
say_hello "Bob"

# Function with return
is_adult() {
    if [ "$1" -ge 18 ]; then
        return 0    # Success (true)
    else
        return 1    # Failure (false)
    fi
}
```

### Function Examples

```bash
# Reusable backup function
backup_files() {
    local source="$1"
    local dest="$2"
    
    if [ ! -d "$source" ]; then
        echo "Source doesn't exist"
        return 1
    fi
    
    cp -r "$source" "$dest"
    echo "Backed up $source to $dest"
}

# Use function
backup_files ~/Documents ~/Backups
```

### Hands-On Exercise: Function Library

Create a utility script:
```bash
#!/bin/bash

# Print line of characters
print_line() {
    local char="${1:-=}"    # Default to =
    local length="${2:-40}" # Default to 40
    printf "%${length}s\n" | tr " " "$char"
}

# Print centered text
center_text() {
    local text="$1"
    local width="${2:-40}"
    local padding=$(( (width - ${#text}) / 2 ))
    printf "%${padding}s%s%${padding}s\n" "" "$text" ""
}

# Use functions
print_line
center_text "Main Menu"
print_line
```

## Practical Exercises

### 1. System Status Script
Create script that shows:
1. System uptime
2. Disk usage
3. Memory usage
4. Current users
5. Recent logins

### 2. File Organizer
Build script that:
1. Asks for directory
2. Lists files by type
3. Creates sorted folders
4. Moves files accordingly
5. Reports results

### 3. Backup Manager
Develop script to:
1. Check backup location
2. Compare file dates
3. Copy new/changed files
4. Create log file
5. Send completion notice

## Review Questions

1. **Script Basics**
   - What's the purpose of shebang?
   - How make script executable?
   - Why use comments?

2. **Variables**
   - Difference between local and environment variables?
   - How to capture command output?
   - When use read command?

3. **Control Structures**
   - When use if vs case?
   - Difference between while and until?
   - How to exit script with status?

## Additional Resources

### Online Tools
- Script checkers
- Shell formatters
- Debug tools

### Further Reading
- Advanced scripting
- Best practices
- Security considerations

### Video Resources
- Scripting tutorials
- Automation examples
- Debugging techniques

## Next Steps

After mastering these concepts, you'll be ready to:
1. Automate routine tasks
2. Create maintenance scripts
3. Build system tools

Remember: Start with simple scripts and gradually add complexity as you learn!

## Common Questions and Answers

Q: How do I debug my scripts?
A: Use set -x for debug output, echo statements for tracking, and test in small sections.

Q: Should I use bash or another shell?
A: Bash is most common and portable. Learn it first, then explore others as needed.

Q: How do I handle errors in scripts?
A: Use exit codes, error checking, and the set -e option to stop on errors.

## Glossary

- **Shebang**: Script interpreter indicator
- **Variable**: Named storage location
- **Function**: Reusable code block
- **Control Structure**: Flow control mechanism
- **Exit Code**: Script return status
- **Parameter**: Value passed to script/function
- **Local Variable**: Function-scope variable
- **Environment Variable**: System-wide variable
- **Conditional**: Decision-making construct
- **Loop**: Repetition construct

Remember: Shell scripts are powerful automation tools. Start with simple tasks and gradually build up to more complex operations!
