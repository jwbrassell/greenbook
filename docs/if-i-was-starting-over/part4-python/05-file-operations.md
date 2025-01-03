# Chapter 5: File Operations

## Introduction

Think about working with a filing cabinet - you need to open drawers, read documents, write new information, and organize files in folders. Python provides similar operations for working with files on your computer. In this chapter, we'll learn how to read, write, and manage files effectively, using familiar examples to understand these operations.

## 1. Basic File Operations

### The Filing Cabinet Metaphor

Think of file operations like working with a filing cabinet:
- Opening file (like opening a drawer)
- Reading file (like reading a document)
- Writing file (like filling out a form)
- Closing file (like closing a drawer)
- File modes (like access permissions)

### Opening and Closing Files

```python
# Basic file opening (like pulling out a file)
file = open('data.txt', 'r')  # 'r' for read
content = file.read()
file.close()

# Using with statement (automatically closes)
with open('data.txt', 'r') as file:
    content = file.read()
    # File closes automatically when done

# File modes
'r'  # Read (default)
'w'  # Write (overwrites)
'a'  # Append (adds to end)
'x'  # Exclusive creation
'b'  # Binary mode
't'  # Text mode (default)
```

### Reading Files

```python
# Read entire file
with open('data.txt', 'r') as file:
    content = file.read()

# Read line by line
with open('data.txt', 'r') as file:
    for line in file:
        print(line.strip())

# Read specific number of bytes
with open('data.txt', 'r') as file:
    chunk = file.read(1024)  # Read 1KB

# Read all lines into list
with open('data.txt', 'r') as file:
    lines = file.readlines()
```

### Writing Files

```python
# Write string to file
with open('output.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('Another line\n')

# Write multiple lines
lines = ['Line 1\n', 'Line 2\n', 'Line 3\n']
with open('output.txt', 'w') as file:
    file.writelines(lines)

# Append to file
with open('log.txt', 'a') as file:
    file.write('New log entry\n')
```

### Hands-On Exercise: File Manager

Create a simple file manager:
```python
def file_manager():
    def read_file(filename):
        try:
            with open(filename, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return "File not found!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def write_file(filename, content):
        try:
            with open(filename, 'w') as file:
                file.write(content)
            return "File written successfully!"
        except Exception as e:
            return f"Error: {str(e)}"
    
    while True:
        print("\nFile Manager")
        print("1. Read file")
        print("2. Write file")
        print("3. Exit")
        
        choice = input("Choose option: ")
        
        if choice == '1':
            filename = input("Enter filename: ")
            content = read_file(filename)
            print("\nContent:")
            print(content)
            
        elif choice == '2':
            filename = input("Enter filename: ")
            content = input("Enter content: ")
            result = write_file(filename, content)
            print(result)
            
        elif choice == '3':
            break

# Run file manager
file_manager()
```

## 2. Working with Different Formats

### The Document Types Metaphor

Think of file formats like different types of documents:
- Text files (like plain notes)
- CSV files (like spreadsheets)
- JSON files (like structured forms)
- Binary files (like sealed packages)

### CSV Files

```python
import csv

# Reading CSV
with open('data.csv', 'r') as file:
    # Read as dictionary
    reader = csv.DictReader(file)
    for row in reader:
        print(row['name'], row['age'])

# Writing CSV
data = [
    {'name': 'Alice', 'age': '25'},
    {'name': 'Bob', 'age': '30'}
]
with open('output.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['name', 'age'])
    writer.writeheader()
    writer.writerows(data)
```

### JSON Files

```python
import json

# Reading JSON
with open('data.json', 'r') as file:
    data = json.load(file)

# Writing JSON
data = {
    'name': 'Alice',
    'age': 25,
    'cities': ['New York', 'London']
}
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)

# Pretty printing
print(json.dumps(data, indent=4))
```

### Binary Files

```python
# Reading binary
with open('image.jpg', 'rb') as file:
    content = file.read()

# Writing binary
with open('copy.jpg', 'wb') as file:
    file.write(content)

# Reading chunks
chunk_size = 1024
with open('large.bin', 'rb') as file:
    while True:
        chunk = file.read(chunk_size)
        if not chunk:
            break
        process_chunk(chunk)
```

### Hands-On Exercise: Data Converter

Create a format conversion tool:
```python
import csv
import json

def convert_csv_to_json(csv_file, json_file):
    # Read CSV
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    
    # Write JSON
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    return f"Converted {csv_file} to {json_file}"

def convert_json_to_csv(json_file, csv_file):
    # Read JSON
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    # Get fieldnames from first item
    if data and isinstance(data, list):
        fieldnames = data[0].keys()
    else:
        return "Invalid JSON format"
    
    # Write CSV
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    
    return f"Converted {json_file} to {csv_file}"

# Test conversions
data = [
    {'name': 'Alice', 'age': '25', 'city': 'New York'},
    {'name': 'Bob', 'age': '30', 'city': 'London'}
]

# Create test files
with open('test.json', 'w') as f:
    json.dump(data, f)

with open('test.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['name', 'age', 'city'])
    writer.writeheader()
    writer.writerows(data)

# Test conversions
print(convert_csv_to_json('test.csv', 'output.json'))
print(convert_json_to_csv('test.json', 'output.csv'))
```

## 3. File System Operations

### The Office Organization Metaphor

Think of file system operations like organizing an office:
- Creating folders (like making new cabinets)
- Moving files (like relocating documents)
- Copying files (like making duplicates)
- Deleting files (like shredding papers)

### Path Operations

```python
import os
from pathlib import Path

# Current directory
current = os.getcwd()
current = Path.cwd()

# Join paths
path = os.path.join('folder', 'subfolder', 'file.txt')
path = Path('folder') / 'subfolder' / 'file.txt'

# Path components
dirname = os.path.dirname(path)
basename = os.path.basename(path)
filename, ext = os.path.splitext(path)
```

### Directory Operations

```python
# Create directory
os.mkdir('new_folder')
os.makedirs('path/to/new/folder')  # Create parents too

# List directory contents
files = os.listdir('.')
files = [f for f in os.listdir('.') if f.endswith('.txt')]

# Walk directory tree
for root, dirs, files in os.walk('.'):
    print(f"Directory: {root}")
    print(f"Subdirectories: {dirs}")
    print(f"Files: {files}")
```

### File Management

```python
import shutil

# Copy files
shutil.copy('source.txt', 'dest.txt')
shutil.copy2('source.txt', 'dest.txt')  # With metadata

# Move/rename files
os.rename('old.txt', 'new.txt')
shutil.move('file.txt', 'folder/file.txt')

# Delete files
os.remove('file.txt')
os.unlink('file.txt')  # Same as remove

# Delete directories
os.rmdir('empty_folder')  # Must be empty
shutil.rmtree('folder')   # Remove with contents
```

### Hands-On Exercise: File Organizer

Create a file organization script:
```python
import os
import shutil
from pathlib import Path

def organize_files(directory):
    """Organize files by extension"""
    # Create category directories
    categories = {
        'Images': ['.jpg', '.jpeg', '.png', '.gif'],
        'Documents': ['.pdf', '.doc', '.docx', '.txt'],
        'Audio': ['.mp3', '.wav', '.flac'],
        'Video': ['.mp4', '.avi', '.mkv']
    }
    
    # Create directories if they don't exist
    for category in categories:
        os.makedirs(os.path.join(directory, category), exist_ok=True)
    
    # Process files
    for filename in os.listdir(directory):
        # Skip directories
        if os.path.isdir(os.path.join(directory, filename)):
            continue
        
        # Get file extension
        file_path = os.path.join(directory, filename)
        _, ext = os.path.splitext(filename)
        
        # Find category for file
        for category, extensions in categories.items():
            if ext.lower() in extensions:
                # Move file to category directory
                dest = os.path.join(directory, category, filename)
                shutil.move(file_path, dest)
                print(f"Moved {filename} to {category}")
                break

# Test the organizer
test_dir = "test_files"
os.makedirs(test_dir, exist_ok=True)

# Create some test files
test_files = {
    'document.txt': 'Documents',
    'image.jpg': 'Images',
    'song.mp3': 'Audio',
    'movie.mp4': 'Video'
}

for file, _ in test_files.items():
    Path(os.path.join(test_dir, file)).touch()

# Organize files
organize_files(test_dir)
```

## Practical Exercises

### 1. Log Analyzer
Build program that:
1. Reads log files
2. Parses entries
3. Generates statistics
4. Creates reports
5. Archives old logs

### 2. Data Processor
Create tool that:
1. Watches directory
2. Processes new files
3. Converts formats
4. Organizes results
5. Handles errors

### 3. Backup System
Develop script that:
1. Identifies important files
2. Creates backups
3. Manages versions
4. Compresses archives
5. Maintains log

## Review Questions

1. **File Basics**
   - When use different modes?
   - How handle large files?
   - Best practices for closing?

2. **File Formats**
   - When use CSV vs JSON?
   - How handle encoding?
   - Best practices for parsing?

3. **File System**
   - How manage paths safely?
   - When use different copy methods?
   - Best practices for deletion?

## Additional Resources

### Online Tools
- File format validators
- Path manipulation tools
- Data converters

### Further Reading
- File handling guide
- Format specifications
- System operations

### Video Resources
- File operation tutorials
- Format conversion guides
- Organization strategies

## Next Steps

After mastering these concepts, you'll be ready to:
1. Process data files
2. Convert formats
3. Automate file management

Remember: Always handle files safely and check for errors!

## Common Questions and Answers

Q: When should I use 'with' statements?
A: Always use 'with' for file operations - it ensures proper closing even if errors occur.

Q: How do I handle different encodings?
A: Specify encoding when opening files: open('file.txt', encoding='utf-8')

Q: What's the best way to handle large files?
A: Read/write in chunks instead of loading entire file into memory.

## Glossary

- **File**: Named location for storing data
- **Mode**: File access type (read/write)
- **Buffer**: Temporary storage for data
- **Stream**: Sequence of data
- **Path**: File location identifier
- **Directory**: Folder containing files
- **Extension**: File type identifier
- **Encoding**: Character representation
- **Binary**: Non-text data
- **Archive**: Compressed file collection

Remember: Good file handling makes programs reliable and efficient!
