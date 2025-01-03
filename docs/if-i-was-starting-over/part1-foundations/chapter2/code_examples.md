# Chapter 2 Code Examples: Programming Logic Fundamentals

This document provides practical code implementations of the programming logic concepts discussed in Chapter 2. We'll use Python for these examples due to its readable syntax and beginner-friendly nature.

## 1. Sequential Logic Implementation

### Basic Sequential Program
```python
def make_coffee():
    """
    Demonstrates sequential logic in a coffee-making program.
    Shows how instructions are executed in order.
    """
    print("Starting coffee preparation...")
    
    # Sequential steps
    water_available = check_water_level()
    if not water_available:
        fill_water_tank()
    
    beans_available = check_coffee_beans()
    if not beans_available:
        add_coffee_beans()
    
    # Main preparation steps
    heat_water()
    grind_beans()
    brew_coffee()
    
    print("Coffee is ready!")

def check_water_level():
    # Simulation of checking water level
    return False

def fill_water_tank():
    print("Filling water tank...")

def check_coffee_beans():
    # Simulation of checking coffee beans
    return True

def heat_water():
    print("Heating water to optimal temperature...")

def grind_beans():
    print("Grinding coffee beans...")

def brew_coffee():
    print("Brewing coffee...")

def add_coffee_beans():
    print("Adding coffee beans...")

# Example usage
make_coffee()
```

## 2. Variables and Data Storage

### Variable Types and Usage
```python
def demonstrate_variables():
    """
    Shows different types of variables and their uses.
    Demonstrates type checking and conversion.
    """
    # Numeric variables
    count = 42                  # Integer
    price = 19.99              # Float
    quantity = 1000000         # Large integer
    
    # Text variables
    name = "Alice"             # String
    message = 'Hello, World!'  # String (single quotes)
    
    # Boolean variables
    is_active = True
    has_permission = False
    
    # Collections
    numbers = [1, 2, 3, 4, 5]  # List
    user = {                   # Dictionary
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }
    
    # Demonstrating variable operations
    print(f"Original count: {count}")
    count += 1
    print(f"After increment: {count}")
    
    # String operations
    full_message = f"{message} My name is {name}"
    print(full_message)
    
    # Type conversion
    price_string = str(price)
    price_integer = int(price)
    print(f"Price as string: {price_string}, as integer: {price_integer}")

# Example usage
demonstrate_variables()
```

## 3. Conditional Logic

### Complex Decision Making
```python
def calculate_ticket_price(age, day, time, is_holiday):
    """
    Demonstrates complex conditional logic for ticket pricing.
    Shows nested if statements and multiple conditions.
    """
    base_price = 15.00
    
    # Early bird discount (before 12:00)
    if time < 12:
        base_price *= 0.8  # 20% discount
    
    # Holiday surcharge
    if is_holiday:
        base_price *= 1.2  # 20% surcharge
    
    # Age-based discounts
    if age < 5:
        base_price = 0  # Free for under 5
    elif age < 13:
        base_price *= 0.5  # 50% off for children
    elif age >= 65:
        base_price *= 0.7  # 30% off for seniors
    
    # Special Tuesday discount
    if day.lower() == "tuesday" and not is_holiday:
        base_price *= 0.8  # Additional 20% off
    
    return round(base_price, 2)

# Example usage
scenarios = [
    {"age": 25, "day": "Monday", "time": 14, "is_holiday": False},
    {"age": 8, "day": "Tuesday", "time": 10, "is_holiday": False},
    {"age": 70, "day": "Friday", "time": 18, "is_holiday": True}
]

for scenario in scenarios:
    price = calculate_ticket_price(
        scenario["age"],
        scenario["day"],
        scenario["time"],
        scenario["is_holiday"]
    )
    print(f"Scenario: {scenario}")
    print(f"Ticket price: ${price}\n")
```

## 4. Loops and Iteration

### Different Types of Loops
```python
def demonstrate_loops():
    """
    Shows different types of loops and their use cases.
    Demonstrates when to use each type of loop.
    """
    # For loop with range
    print("Counting from 1 to 5:")
    for i in range(1, 6):
        print(i)
    
    # For loop with list
    fruits = ["apple", "banana", "orange"]
    print("\nFruit inventory:")
    for fruit in fruits:
        print(f"- {fruit}")
    
    # While loop with condition
    print("\nCountdown:")
    countdown = 5
    while countdown > 0:
        print(countdown)
        countdown -= 1
    print("Blast off!")
    
    # Nested loops
    print("\nMultiplication table (1-3):")
    for i in range(1, 4):
        for j in range(1, 4):
            print(f"{i} x {j} = {i*j}")
        print()  # Empty line between rows
    
    # Loop with break
    print("Finding first even number divisible by 7:")
    for num in range(1, 50):
        if num % 2 == 0 and num % 7 == 0:
            print(f"Found it: {num}")
            break
    
    # Loop with continue
    print("\nPrinting odd numbers up to 5:")
    for num in range(1, 6):
        if num % 2 == 0:
            continue
        print(num)

# Example usage
demonstrate_loops()
```

## 5. Error Handling

### Comprehensive Error Handling
```python
def divide_numbers(a, b):
    """
    Demonstrates comprehensive error handling.
    Shows how to handle multiple types of errors.
    """
    try:
        # Convert string inputs to numbers
        num_a = float(a)
        num_b = float(b)
        
        # Check for zero division
        if num_b == 0:
            raise ValueError("Cannot divide by zero")
        
        # Perform division
        result = num_a / num_b
        
        # Check if result is too large
        if result > 1e308:  # Max float value
            raise OverflowError("Result too large")
        
        return result
    
    except ValueError as e:
        return f"Value Error: {str(e)}"
    except OverflowError as e:
        return f"Overflow Error: {str(e)}"
    except Exception as e:
        return f"Unexpected Error: {str(e)}"
    finally:
        print("Division operation completed")

# Example usage with different scenarios
test_cases = [
    (10, 2),          # Normal division
    (10, 0),          # Division by zero
    ("abc", 2),       # Invalid input
    (1e308, 0.1),     # Very large number
]

for a, b in test_cases:
    print(f"\nDividing {a} by {b}:")
    result = divide_numbers(a, b)
    print(f"Result: {result}")
```

## 6. Combining Concepts

### Library Management System
```python
class Book:
    def __init__(self, title, author, isbn):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.is_checked_out = False
        self.due_date = None

class Library:
    def __init__(self):
        self.books = {}
        self.members = set()
    
    def add_book(self, title, author, isbn):
        """Add a new book to the library."""
        try:
            if isbn in self.books:
                raise ValueError(f"Book with ISBN {isbn} already exists")
            
            book = Book(title, author, isbn)
            self.books[isbn] = book
            return f"Added: {title} by {author}"
        
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def check_out_book(self, isbn, member_id):
        """Check out a book to a member."""
        try:
            # Validate member
            if member_id not in self.members:
                raise ValueError("Invalid member ID")
            
            # Find book
            book = self.books.get(isbn)
            if not book:
                raise ValueError("Book not found")
            
            # Check availability
            if book.is_checked_out:
                raise ValueError("Book is already checked out")
            
            # Process checkout
            book.is_checked_out = True
            book.due_date = "2 weeks from now"  # Simplified
            
            return f"Checked out: {book.title}"
        
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"
    
    def return_book(self, isbn):
        """Process a book return."""
        try:
            book = self.books.get(isbn)
            if not book:
                raise ValueError("Book not found")
            
            if not book.is_checked_out:
                raise ValueError("Book is not checked out")
            
            book.is_checked_out = False
            book.due_date = None
            
            return f"Returned: {book.title}"
        
        except ValueError as e:
            return f"Error: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

# Example usage
def demonstrate_library():
    library = Library()
    
    # Add members
    library.members.add("M001")
    library.members.add("M002")
    
    # Add books
    print(library.add_book("Python Programming", "John Smith", "123456"))
    print(library.add_book("Data Structures", "Jane Doe", "789012"))
    
    # Demonstrate checkout and return
    print("\nChecking out books:")
    print(library.check_out_book("123456", "M001"))
    print(library.check_out_book("123456", "M002"))  # Should fail
    
    print("\nReturning books:")
    print(library.return_book("123456"))
    print(library.return_book("999999"))  # Should fail

# Run demonstration
demonstrate_library()
```

## Conclusion

These code examples demonstrate how programming logic concepts translate into actual code. Key takeaways:

1. Sequential logic ensures operations happen in the correct order
2. Variables provide storage and tracking of data
3. Conditional statements enable decision-making
4. Loops allow efficient repetition of tasks
5. Error handling ensures robust program operation
6. Complex systems combine multiple concepts

Remember:
- Start with simple implementations
- Test thoroughly with different inputs
- Handle edge cases and errors
- Document your code
- Build complexity gradually

The next chapter will build upon these fundamentals to explore more advanced programming concepts.
