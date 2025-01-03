# Chapter 1: Python Basics

## Introduction

Think about learning a new language - you start with basic words and phrases before moving on to complex conversations. Learning Python is similar. In this chapter, we'll set up our Python environment and learn the basic "vocabulary" and "grammar" of Python programming, using familiar examples to make these concepts intuitive.

## 1. Getting Started

### The Kitchen Setup Metaphor

Think of setting up Python like preparing a kitchen:
- Python interpreter: Like your stove/oven
- Text editor/IDE: Like your workspace
- Terminal: Like your kitchen counter
- Package manager (pip): Like your pantry
- Virtual environments: Like separate cooking stations

### Installing Python

```bash
# On macOS (using Homebrew)
brew install python

# On Windows
# Download installer from python.org

# Verify installation
python --version
pip --version
```

### Development Environment

```
Text Editors vs IDEs:

Text Editors (like VS Code):
- Like a basic kitchen
- Lightweight
- Extensible
- Good for beginners

IDEs (like PyCharm):
- Like a professional kitchen
- More features
- Built-in tools
- Better for large projects
```

### Python Interactive Shell

```python
# Launch Python shell
python

# Basic operations
>>> 2 + 2
4
>>> print("Hello, World!")
Hello, World!
>>> exit()  # Exit shell

Like testing ingredients:
- Try small things
- Immediate feedback
- Easy experimentation
```

### Hands-On Exercise: Environment Setup

1. Create project directory:
```bash
mkdir python_practice
cd python_practice
```

2. Create first Python file:
```python
# hello.py
print("Hello, Python!")
```

3. Run the program:
```bash
python hello.py
```

## 2. Basic Syntax

### The Recipe Metaphor

Think of Python syntax like recipe writing:
- Variables are like ingredients
- Statements are like steps
- Functions are like cooking methods
- Comments are like recipe notes

### Variables and Data Types

```python
# Numbers (like measurements)
age = 25              # Integer (whole numbers)
height = 5.9          # Float (decimal numbers)

# Strings (like labels)
name = "Alice"        # Text
message = 'Hello'     # Single or double quotes

# Booleans (like yes/no questions)
is_student = True     # True/False values
has_car = False

# None (like "not applicable")
result = None         # Represents nothing/no value
```

### Basic Operations

```python
# Arithmetic (like cooking measurements)
total = 10 + 5       # Addition
difference = 10 - 5   # Subtraction
product = 10 * 5     # Multiplication
quotient = 10 / 5    # Division
remainder = 10 % 3   # Modulus (remainder)

# String Operations (like combining ingredients)
first = "Hello"
last = "World"
message = first + " " + last  # Concatenation
repeated = "Ha" * 3           # Repetition

# Comparisons (like checking measurements)
is_adult = age >= 18         # Greater than or equal
is_valid = password == "secret"  # Equality
is_empty = name != ""        # Inequality
```

### Comments and Documentation

```python
# Single line comment (like quick notes)
print("Hello")  # End of line comment

"""
Multi-line comment (like detailed notes)
This is useful for longer explanations
or documentation
"""

def greet(name):
    """
    Function documentation (docstring)
    Explains what the function does
    """
    print(f"Hello, {name}!")
```

### Hands-On Exercise: Syntax Practice

Create a basic calculator:
```python
# calculator.py

# Get user input
num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

# Perform calculations
sum_result = num1 + num2
diff_result = num1 - num2
prod_result = num1 * num2
div_result = num1 / num2

# Show results
print(f"Sum: {sum_result}")
print(f"Difference: {diff_result}")
print(f"Product: {prod_result}")
print(f"Quotient: {div_result}")
```

## 3. Input and Output

### The Conversation Metaphor

Think of I/O like having a conversation:
- Input: Like listening
- Output: Like speaking
- Formatting: Like speaking clearly
- Error messages: Like asking for clarification

### Print Function

```python
# Basic output
print("Hello, World!")

# Multiple items
name = "Alice"
age = 25
print(name, age)

# Formatted strings (f-strings)
print(f"{name} is {age} years old")

# Escape characters
print("Line 1\nLine 2")  # New line
print("Tab\tSpace")      # Tab
```

### Input Function

```python
# Basic input
name = input("What's your name? ")

# Converting input
age = int(input("How old are you? "))
height = float(input("How tall are you? "))

# Input validation
while True:
    try:
        age = int(input("Age: "))
        break
    except ValueError:
        print("Please enter a number")
```

### String Formatting

```python
# Old style
name = "Alice"
age = 25
message = "My name is %s and I'm %d" % (name, age)

# Format method
message = "My name is {} and I'm {}".format(name, age)

# f-strings (recommended)
message = f"My name is {name} and I'm {age}"

# Number formatting
price = 19.99
print(f"Price: ${price:.2f}")  # Two decimal places
```

### Hands-On Exercise: Interactive Program

Create a personal greeting program:
```python
# greeting.py

def get_time_of_day():
    """Get appropriate greeting based on hour"""
    import datetime
    hour = datetime.datetime.now().hour
    
    if hour < 12:
        return "morning"
    elif hour < 17:
        return "afternoon"
    else:
        return "evening"

# Get user information
name = input("What's your name? ")
time = get_time_of_day()

# Create personalized greeting
greeting = f"Good {time}, {name}!"
print(greeting)

# Ask about their day
feeling = input("How are you today? ")
print(f"Glad to hear you're {feeling}!")
```

## Practical Exercises

### 1. Temperature Converter
Build program that:
1. Takes Celsius input
2. Converts to Fahrenheit
3. Shows formatted result
4. Handles invalid input
5. Allows multiple conversions

### 2. Personal Info Card
Create program that:
1. Collects user details
2. Formats information
3. Creates nice display
4. Validates input
5. Allows editing

### 3. Simple Calculator
Develop calculator that:
1. Takes two numbers
2. Offers operations
3. Shows result
4. Handles errors
5. Allows continuous use

## Review Questions

1. **Environment Setup**
   - How to check Python version?
   - What's difference between editor and IDE?
   - How to run Python programs?

2. **Basic Syntax**
   - What are main data types?
   - How to name variables?
   - When use different operators?

3. **Input/Output**
   - How to get user input?
   - Different ways to format output?
   - How to handle input errors?

## Additional Resources

### Online Tools
- Python playground
- Interactive tutorials
- Code formatters

### Further Reading
- Python documentation
- Style guides
- Best practices

### Video Resources
- Setup tutorials
- Syntax explanations
- I/O examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Write basic programs
2. Handle user input
3. Format output nicely

Remember: Start simple and build complexity gradually!

## Common Questions and Answers

Q: Which Python version should I use?
A: Start with Python 3.x (latest stable version). Python 2 is no longer supported.

Q: Should I use an IDE or text editor?
A: Start with a text editor like VS Code. Move to an IDE when working on larger projects.

Q: How do I know if my code is "good"?
A: Follow PEP 8 style guide, write clear comments, and make your code readable.

## Glossary

- **Interpreter**: Program that runs Python code
- **Variable**: Named storage location
- **Data Type**: Category of data
- **String**: Text data
- **Integer**: Whole number
- **Float**: Decimal number
- **Boolean**: True/False value
- **Comment**: Code documentation
- **f-string**: Formatted string literal
- **Input**: Data from user

Remember: Python is designed to be readable - write your code as if you're explaining it to someone!
