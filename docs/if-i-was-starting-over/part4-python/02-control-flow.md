# Chapter 2: Control Flow

## Introduction

Think about following a recipe - sometimes you need to make decisions ("if the dough is too dry, add water"), repeat steps ("stir until smooth"), or handle problems ("if you run out of an ingredient, use a substitute"). In programming, we call these control flow structures. They help your program make decisions and handle different situations.

## 1. Conditional Statements

### The Decision Tree Metaphor

Think of conditionals like a flowchart:
- if statements are like yes/no questions
- elif statements are like "what about..." questions
- else statements are like "otherwise..." fallbacks

### Basic If Statements

```python
# Simple if (like basic decision)
age = 20
if age >= 18:
    print("You're an adult")

# if-else (like two options)
if age >= 18:
    print("You can vote")
else:
    print("Too young to vote")

# if-elif-else (like multiple options)
if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")
```

### Comparison Operators

```python
# Numeric Comparisons
x = 10
y = 5

x > y    # Greater than
x < y    # Less than
x >= y   # Greater than or equal
x <= y   # Less than or equal
x == y   # Equal to
x != y   # Not equal to

# String Comparisons
name = "Alice"
name == "Alice"    # Exact match
name != "Bob"      # Not equal
"A" < "B"         # Alphabetical order
```

### Logical Operators

```python
# and (like requiring all conditions)
if age >= 18 and has_id:
    print("Can enter club")

# or (like accepting any condition)
if is_weekend or is_holiday:
    print("No work today")

# not (like opposite condition)
if not is_working:
    print("Free time")

# Combining operators
if (age >= 18 and has_id) or is_vip:
    print("Welcome to the club")
```

### Hands-On Exercise: Decision Maker

Create a movie rating checker:
```python
def check_movie_access():
    age = int(input("Enter your age: "))
    has_parent = input("With a parent? (yes/no): ").lower() == "yes"
    
    if age >= 17:
        print("Can watch any movie")
    elif age >= 13 or has_parent:
        print("Can watch PG-13 movies")
    else:
        print("Can only watch PG movies")

# Test with different ages
check_movie_access()
```

## 2. Loops

### The Assembly Line Metaphor

Think of loops like an assembly line:
- for loops are like processing each item
- while loops are like "keep going until done"
- break is like emergency stop
- continue is like skipping an item

### For Loops

```python
# Iterate over sequence (like processing items)
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"Processing {fruit}")

# Range for counting (like numbered steps)
for i in range(5):    # 0 to 4
    print(f"Step {i}")

# Nested loops (like grid processing)
for row in range(3):
    for col in range(3):
        print(f"Position ({row},{col})")
```

### While Loops

```python
# Basic while (like "keep going until")
count = 0
while count < 5:
    print(count)
    count += 1

# With condition (like "until perfect")
password = ""
while password != "secret":
    password = input("Enter password: ")

# Infinite with break (like "until told to stop")
while True:
    response = input("Continue? (y/n): ")
    if response == 'n':
        break
```

### Loop Control

```python
# break (like emergency stop)
for i in range(10):
    if i == 5:
        break    # Exit loop
    print(i)

# continue (like skipping item)
for i in range(5):
    if i == 2:
        continue    # Skip to next iteration
    print(i)

# else in loops (like completion check)
for i in range(3):
    print(i)
else:
    print("Loop completed normally")
```

### Hands-On Exercise: Loop Practice

Create a number guessing game:
```python
import random

def guess_number():
    number = random.randint(1, 100)
    attempts = 0
    
    while True:
        guess = int(input("Guess the number (1-100): "))
        attempts += 1
        
        if guess == number:
            print(f"Correct! Took {attempts} attempts")
            break
        elif guess < number:
            print("Too low!")
        else:
            print("Too high!")

# Play the game
guess_number()
```

## 3. Error Handling

### The Safety Net Metaphor

Think of error handling like safety measures:
- try is like "attempt carefully"
- except is like "if something goes wrong"
- else is like "if nothing went wrong"
- finally is like "cleanup regardless"

### Basic Error Handling

```python
# Simple try-except
try:
    number = int(input("Enter a number: "))
except ValueError:
    print("That's not a number!")

# Multiple exceptions
try:
    result = x / y
except ZeroDivisionError:
    print("Can't divide by zero!")
except TypeError:
    print("Invalid types for division!")

# With else and finally
try:
    file = open("data.txt")
except FileNotFoundError:
    print("File not found!")
else:
    print("File opened successfully!")
finally:
    file.close()    # Always runs
```

### Common Exceptions

```python
# ValueError (invalid value)
try:
    age = int("not a number")
except ValueError:
    print("Invalid age")

# TypeError (wrong type)
try:
    result = "5" + 5
except TypeError:
    print("Can't add string and number")

# IndexError (invalid index)
try:
    list = [1, 2, 3]
    print(list[10])
except IndexError:
    print("Index out of range")
```

### Custom Error Handling

```python
# Raising exceptions
def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

# Custom exception class
class AgeError(Exception):
    pass

def set_age(age):
    if age < 0:
        raise AgeError("Age cannot be negative")
    return age
```

### Hands-On Exercise: Error Handler

Create a robust calculator:
```python
def safe_calculator():
    while True:
        try:
            # Get input
            num1 = float(input("First number: "))
            op = input("Operation (+,-,*,/): ")
            num2 = float(input("Second number: "))
            
            # Perform calculation
            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    raise ValueError("Cannot divide by zero")
                result = num1 / num2
            else:
                raise ValueError("Invalid operator")
                
            print(f"Result: {result}")
            break
            
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        retry = input("Try again? (y/n): ")
        if retry.lower() != 'y':
            break

# Run calculator
safe_calculator()
```

## Practical Exercises

### 1. Input Validator
Build program that:
1. Takes various inputs
2. Validates each type
3. Handles all errors
4. Provides feedback
5. Allows corrections

### 2. Menu System
Create program that:
1. Shows options menu
2. Handles choices
3. Processes commands
4. Manages errors
5. Allows exit

### 3. Data Processor
Develop program that:
1. Reads data file
2. Processes each line
3. Handles bad data
4. Reports problems
5. Saves results

## Review Questions

1. **Conditionals**
   - When use if vs elif?
   - How combine conditions?
   - Best practices for nesting?

2. **Loops**
   - When use for vs while?
   - How to exit loops early?
   - When use loop else?

3. **Error Handling**
   - Common exception types?
   - When raise exceptions?
   - How to clean up resources?

## Additional Resources

### Online Tools
- Python visualizer
- Flow diagram makers
- Exception hierarchy charts

### Further Reading
- Python control flow
- Exception handling
- Best practices

### Video Resources
- Control flow tutorials
- Error handling guides
- Loop pattern examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Write robust programs
2. Handle edge cases
3. Process complex data

Remember: Good error handling makes programs reliable!

## Common Questions and Answers

Q: When should I use try-except?
A: Use it when errors are possible and recoverable, like user input or file operations.

Q: How do I choose between for and while loops?
A: Use for when you know the number of iterations, while when you don't know how many loops needed.

Q: Should I catch all exceptions?
A: No, catch only exceptions you can handle meaningfully. Let others propagate up.

## Glossary

- **Conditional**: Decision-making structure
- **Loop**: Repetition structure
- **Iterator**: Object that can be looped over
- **Exception**: Error that occurs during execution
- **Try**: Block of code that might raise exception
- **Except**: Handler for exceptions
- **Break**: Exit loop immediately
- **Continue**: Skip to next iteration
- **Raise**: Trigger an exception
- **Finally**: Cleanup code block

Remember: Control flow is about making your program smart and resilient!
