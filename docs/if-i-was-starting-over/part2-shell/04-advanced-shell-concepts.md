# Chapter 4: Advanced Shell Concepts

## Introduction

Think about how water flows through pipes in your home, or how an assembly line passes products from one station to another. The shell has similar concepts for moving data between commands and managing running processes. In this chapter, we'll explore these powerful features that let you combine commands and control program execution.

## 1. Pipes and Redirection

### The Water Pipeline Metaphor

Think of data flow like water in pipes:
- Commands are like stations that process the water
- Pipes (|) connect stations together
- Redirection (>, <) is like changing water flow direction
- Each station can modify what passes through

### Basic Redirection

```bash
# Output Redirection (>)
# Like filling a bucket with water
echo "Hello" > greeting.txt     # Create/overwrite
echo "World" >> greeting.txt    # Append

# Input Redirection (<)
# Like pouring from bucket
sort < names.txt               # Sort contents of file
grep "error" < log.txt         # Search in file

# Error Redirection (2>)
# Like catching spills
command 2> errors.log         # Save errors only
command > output.log 2>&1     # Save both output and errors
```

### Pipes

```bash
# The Assembly Line Metaphor
# Each command processes and passes result to next

# Example 1: Find large files
du -h | sort -hr | head -5
# 1. List files with sizes
# 2. Sort by size
# 3. Show top 5

# Example 2: Process log file
cat log.txt | grep "ERROR" | wc -l
# 1. Read file
# 2. Find error lines
# 3. Count lines
```

### Hands-On Exercise: Data Pipeline

Create a log analyzer:
```bash
#!/bin/bash

# Generate sample log
cat << EOF > sample.log
2024-01-01 INFO: System start
2024-01-01 ERROR: Connection failed
2024-01-01 INFO: Retry connection
2024-01-01 ERROR: Database offline
2024-01-01 INFO: Using backup
EOF

# Process log different ways
echo "Error count:"
cat sample.log | grep ERROR | wc -l

echo "Unique errors:"
cat sample.log | grep ERROR | cut -d: -f2 | sort -u
```

## 2. Process Management

### The Factory Workers Metaphor

Think of processes like factory workers:
- Each does specific job
- Can work in foreground or background
- Need resources (CPU, memory)
- Can be started, paused, or stopped

### Viewing Processes

```bash
# Basic Process List
ps
# Like taking attendance

# All Processes
ps aux
# Like full factory inspection

# Process Tree
ps afjx
# Like organizational chart

# Real-time Monitor
top
# Like security camera feed
```

### Process Control

```bash
# Start Background Process
command &
# Like assigning background task

# Bring to Foreground
fg %1
# Like calling worker to front

# Send to Background
ctrl+z    # Pause
bg        # Resume in background
# Like sending worker to back

# Stop Process
kill PID
# Like dismissing worker

kill -9 PID
# Like emergency stop
```

### Job Control

```bash
# List Jobs
jobs
# Like checking task board

# Resume Specific Job
fg %2
# Like selecting specific task

# Kill Job
kill %1
# Like canceling task
```

### Hands-On Exercise: Process Manager

Create process control script:
```bash
#!/bin/bash

# Function to show running processes
show_processes() {
    echo "=== Current Processes ==="
    ps aux | head -5
    echo "======================="
}

# Function to monitor system
monitor_system() {
    echo "=== System Monitor ==="
    top -n 1 | head -10
    echo "===================="
}

# Main menu
while true; do
    echo "1. Show processes"
    echo "2. Monitor system"
    echo "3. Exit"
    read -p "Choice: " choice
    
    case $choice in
        1) show_processes ;;
        2) monitor_system ;;
        3) exit 0 ;;
        *) echo "Invalid choice" ;;
    esac
done
```

## 3. Advanced Scripting Techniques

### Error Handling

```bash
# The Safety Net Metaphor
# Like having backup plans

# Exit on Error
set -e
# Like stopping assembly line on problem

# Debug Mode
set -x
# Like turning on all cameras

# Custom Error Handler
trap 'echo "Error on line $LINENO"' ERR
# Like having safety inspector
```

### Script Debugging

```bash
# Debug Whole Script
bash -x script.sh
# Like slow-motion replay

# Debug Section
set -x    # Start debug
commands
set +x    # Stop debug
# Like focusing on specific area

# Check Shell Syntax
bash -n script.sh
# Like dry run
```

### Performance Optimization

```bash
# Minimize External Commands
# Instead of:
count=$(ls | wc -l)
# Use:
count=$(find . -maxdepth 1 -type f | wc -l)

# Use Built-in Features
# Instead of:
echo $var | grep pattern
# Use:
[[ $var =~ pattern ]]
```

### Hands-On Exercise: Robust Script

Create error-handling script:
```bash
#!/bin/bash
set -e
trap 'echo "Error on line $LINENO"' ERR

# Function with error checking
check_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo "Error: $file not found"
        return 1
    fi
    return 0
}

# Main script with error handling
main() {
    local input_file="data.txt"
    
    if ! check_file "$input_file"; then
        echo "Creating sample file..."
        echo "sample data" > "$input_file"
    fi
    
    echo "Processing $input_file..."
    cat "$input_file"
}

# Run with error handling
main || echo "Script failed"
```

## Practical Exercises

### 1. Log Analyzer
Build script that:
1. Reads log file
2. Filters specific patterns
3. Counts occurrences
4. Generates report
5. Handles errors gracefully

### 2. Process Monitor
Create script to:
1. Watch specific process
2. Track resource usage
3. Alert on high usage
4. Log statistics
5. Handle termination

### 3. Data Pipeline
Develop script that:
1. Reads input file
2. Processes data
3. Filters results
4. Sorts output
5. Saves to file

## Review Questions

1. **Pipes and Redirection**
   - Difference between > and >>?
   - When use 2> vs >?
   - How do pipes work?

2. **Process Management**
   - How to list all processes?
   - Difference between kill and kill -9?
   - When use bg vs fg?

3. **Advanced Techniques**
   - Purpose of set -e?
   - When use trap?
   - How to debug scripts?

## Additional Resources

### Online Tools
- Process monitors
- Pipeline visualizers
- Debug tools

### Further Reading
- Advanced shell features
- Process management
- Performance tuning

### Video Resources
- Pipeline tutorials
- Process management guides
- Debugging techniques

## Next Steps

After mastering these concepts, you'll be ready to:
1. Build complex pipelines
2. Manage system processes
3. Create robust scripts

Remember: With great power comes great responsibility - especially with process management!

## Common Questions and Answers

Q: When should I use pipes vs redirection?
A: Use pipes to connect commands in memory, redirection for file operations.

Q: How do I know if a background process is still running?
A: Use jobs command or ps to check process status.

Q: What's the safest way to kill a process?
A: Start with regular kill, use kill -9 only as last resort.

## Glossary

- **Pipe**: Command output connector
- **Redirection**: Input/output flow control
- **Process**: Running program instance
- **Job**: Shell-managed task
- **PID**: Process identifier
- **Background**: Running without terminal
- **Foreground**: Running in terminal
- **Signal**: Process control message
- **Exit Code**: Process return status
- **Debug Mode**: Detailed execution trace

Remember: Advanced shell features are powerful tools - practice in a safe environment first!
