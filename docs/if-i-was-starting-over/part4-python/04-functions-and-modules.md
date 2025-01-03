# Chapter 4: Functions and Modules

## Introduction

Think about building with LEGO blocks - you have basic pieces that you can combine in different ways to create larger structures. Similarly, functions and modules are the building blocks of Python programs. They let you write reusable code and organize your programs into manageable pieces. In this chapter, we'll learn how to create and use these powerful programming tools.

## 1. Functions

### The Building Blocks Metaphor

Think of functions like specialized tools:
- Each has a specific purpose
- Can be used repeatedly
- Takes inputs (parameters)
- Produces outputs (returns)
- Can be combined for complex tasks

### Basic Function Structure

```python
# Simple function (like a basic tool)
def greet(name):
    """Say hello to someone"""
    return f"Hello, {name}!"

# Using the function
message = greet("Alice")
print(message)

# Function with multiple parameters
def calculate_total(price, quantity, tax_rate=0.1):
    """Calculate total price including tax"""
    subtotal = price * quantity
    tax = subtotal * tax_rate
    return subtotal + tax

# Using with different arguments
total = calculate_total(9.99, 2)        # Default tax rate
total = calculate_total(9.99, 2, 0.15)  # Custom tax rate
```

### Parameters and Arguments

```python
# Positional arguments (like ingredients in order)
def make_sandwich(bread, filling, sauce):
    return f"{filling} sandwich with {sauce} on {bread}"

sandwich = make_sandwich("rye", "tuna", "mayo")

# Keyword arguments (like labeled ingredients)
sandwich = make_sandwich(
    bread="wheat",
    filling="chicken",
    sauce="mustard"
)

# Default parameters (like recipe defaults)
def make_coffee(type="regular", size="medium", milk=False):
    order = f"{size} {type} coffee"
    if milk:
        order += " with milk"
    return order

coffee = make_coffee()                    # Use defaults
coffee = make_coffee("espresso", milk=True)  # Override some
```

### Return Values

```python
# Single return value
def square(x):
    return x * x

# Multiple return values
def get_dimensions():
    return 1920, 1080  # Returns tuple

# Early returns
def check_age(age):
    if age < 0:
        return "Invalid age"
    if age < 18:
        return "Minor"
    return "Adult"

# Return None (implicit)
def log_message(msg):
    print(f"Log: {msg}")
    # No return statement needed
```

### Hands-On Exercise: Function Builder

Create a calculator library:
```python
def calculator():
    def add(x, y):
        return x + y
        
    def subtract(x, y):
        return x - y
        
    def multiply(x, y):
        return x * y
        
    def divide(x, y):
        if y == 0:
            return "Cannot divide by zero"
        return x / y
    
    while True:
        print("\nCalculator")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Exit")
        
        choice = input("Choose operation: ")
        if choice == '5':
            break
            
        try:
            num1 = float(input("First number: "))
            num2 = float(input("Second number: "))
            
            if choice == '1':
                print("Result:", add(num1, num2))
            elif choice == '2':
                print("Result:", subtract(num1, num2))
            elif choice == '3':
                print("Result:", multiply(num1, num2))
            elif choice == '4':
                print("Result:", divide(num1, num2))
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter valid numbers!")

# Run calculator
calculator()
```

## 2. Modules

### The Tool Collection Metaphor

Think of modules like toolboxes:
- Each contains related tools (functions)
- Can be imported when needed
- Keeps code organized
- Promotes reusability
- Avoids naming conflicts

### Creating Modules

```python
# math_tools.py
"""Basic math operations module"""

def add(x, y):
    return x + y
    
def subtract(x, y):
    return x - y
    
def multiply(x, y):
    return x * y
    
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

# Constants
PI = 3.14159
E = 2.71828
```

### Importing Modules

```python
# Import entire module
import math_tools
result = math_tools.add(5, 3)

# Import specific items
from math_tools import add, subtract, PI
result = add(5, 3)

# Import with alias
import math_tools as mt
result = mt.multiply(4, 2)

# Import all (not recommended)
from math_tools import *
result = divide(10, 2)
```

### Module Organization

```python
# Project structure
my_project/
    ├── main.py
    ├── utils/
    │   ├── __init__.py
    │   ├── math_tools.py
    │   └── string_tools.py
    └── tests/
        ├── __init__.py
        └── test_math.py

# Using modules from packages
from utils.math_tools import add
from utils.string_tools import reverse
```

### Hands-On Exercise: Module Creator

Create a utility package:
```python
# utils/string_tools.py
def reverse_string(text):
    """Reverse a string"""
    return text[::-1]

def count_words(text):
    """Count words in text"""
    return len(text.split())

def is_palindrome(text):
    """Check if text is palindrome"""
    cleaned = ''.join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]

# utils/math_tools.py
def factorial(n):
    """Calculate factorial"""
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0:
        return 1
    return n * factorial(n - 1)

def fibonacci(n):
    """Generate Fibonacci sequence"""
    sequence = []
    a, b = 0, 1
    for _ in range(n):
        sequence.append(a)
        a, b = b, a + b
    return sequence

# main.py
from utils.string_tools import reverse_string, is_palindrome
from utils.math_tools import factorial, fibonacci

# Test functions
text = "Hello, World!"
print(f"Reversed: {reverse_string(text)}")

num = 5
print(f"Factorial of {num}: {factorial(num)}")

palindrome = "A man a plan a canal Panama"
print(f"Is palindrome? {is_palindrome(palindrome)}")

fib_sequence = fibonacci(10)
print(f"Fibonacci sequence: {fib_sequence}")
```

## 3. Package Management

### The Recipe Ingredients Metaphor

Think of packages like ingredients:
- Some are built-in (standard library)
- Others need to be installed (pip)
- Have specific versions
- May depend on other packages
- Need to be managed carefully

### Using pip

```bash
# Install package
pip install requests

# Install specific version
pip install requests==2.25.1

# Install with requirements
pip install -r requirements.txt

# List installed packages
pip list

# Show package info
pip show requests

# Uninstall package
pip uninstall requests
```

### Virtual Environments

```bash
# Create virtual environment
python -m venv myenv

# Activate environment
# On Windows:
myenv\Scripts\activate
# On Unix/macOS:
source myenv/bin/activate

# Deactivate environment
deactivate
```

### Requirements File

```
# requirements.txt
requests==2.25.1
pandas>=1.2.0
numpy
python-dotenv>=0.15.0
```

### Hands-On Exercise: Project Setup

Create a new project with dependencies:
```bash
# Create project structure
mkdir my_project
cd my_project

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Create requirements.txt
echo "requests==2.25.1" > requirements.txt
echo "python-dotenv>=0.15.0" >> requirements.txt

# Install dependencies
pip install -r requirements.txt

# Create main.py
echo "import requests" > main.py
echo "response = requests.get('https://api.example.com/data')" >> main.py
echo "print(response.json())" >> main.py

# Create .gitignore
echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
```

## Practical Exercises

### 1. Utility Library
Build package that:
1. Provides common functions
2. Handles file operations
3. Processes data
4. Includes documentation
5. Has error handling

### 2. API Client
Create module that:
1. Makes HTTP requests
2. Handles authentication
3. Processes responses
4. Manages errors
5. Provides simple interface

### 3. Data Processor
Develop package that:
1. Reads various formats
2. Transforms data
3. Validates input
4. Generates reports
5. Handles large files

## Review Questions

1. **Functions**
   - When use default parameters?
   - How handle multiple returns?
   - Best practices for arguments?

2. **Modules**
   - When create new module?
   - How organize large projects?
   - Best import practices?

3. **Package Management**
   - Why use virtual environments?
   - How manage dependencies?
   - When freeze requirements?

## Additional Resources

### Online Tools
- Package index (PyPI)
- Documentation generators
- Code quality checkers

### Further Reading
- Python packaging guide
- Module system documentation
- Virtual environment guide

### Video Resources
- Project organization tutorials
- Package management guides
- Best practices videos

## Next Steps

After mastering these concepts, you'll be ready to:
1. Create reusable code
2. Organize large projects
3. Manage dependencies

Remember: Good organization makes code maintainable!

## Common Questions and Answers

Q: When should I create a new module?
A: Create a module when you have related functions that could be reused across projects.

Q: Why use virtual environments?
A: They keep project dependencies isolated, preventing conflicts between different projects.

Q: How do I choose between relative and absolute imports?
A: Use absolute imports for clarity unless you have a specific need for relative imports.

## Glossary

- **Function**: Reusable code block
- **Module**: Python file with code
- **Package**: Directory of modules
- **Import**: Include external code
- **Parameter**: Function input definition
- **Argument**: Function input value
- **Virtual Environment**: Isolated Python setup
- **Dependency**: Required package
- **pip**: Package installer
- **Requirements**: Package list

Remember: Well-organized code is easier to maintain and reuse!
