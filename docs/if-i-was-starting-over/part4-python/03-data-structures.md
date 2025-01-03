# Chapter 3: Data Structures

## Introduction

Think about organizing your closet - you have different ways to store different items (hangers for clothes, boxes for shoes, drawers for accessories). Similarly, Python provides different data structures to organize and store different types of data efficiently. In this chapter, we'll explore these structures and learn when to use each one.

## 1. Lists and Tuples

### The Shopping List Metaphor

Think of lists like a shopping list:
- Can add/remove items (lists)
- Can't modify once created (tuples)
- Items are ordered
- Can contain duplicates
- Can mix different types

### Lists

```python
# Creating lists
fruits = ["apple", "banana", "cherry"]
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]

# Accessing elements
first = fruits[0]        # First item
last = fruits[-1]        # Last item
subset = fruits[1:3]     # Slice (items 1 and 2)

# Modifying lists
fruits.append("orange")   # Add to end
fruits.insert(1, "kiwi") # Add at position
fruits.remove("banana")   # Remove item
fruits.pop()             # Remove and return last item
fruits.sort()            # Sort in place
```

### Tuples

```python
# Creating tuples (immutable lists)
coordinates = (10, 20)
rgb = (255, 128, 0)
single = (42,)    # Note the comma

# Accessing elements (same as lists)
x = coordinates[0]
y = coordinates[1]

# Tuple unpacking
x, y = coordinates
r, g, b = rgb

# Common uses
def get_dimensions():
    return (1920, 1080)  # Return multiple values

width, height = get_dimensions()
```

### List Comprehensions

```python
# Traditional loop
squares = []
for x in range(5):
    squares.append(x ** 2)

# List comprehension
squares = [x ** 2 for x in range(5)]

# With condition
evens = [x for x in range(10) if x % 2 == 0]

# Nested comprehension
matrix = [[i+j for j in range(3)] for i in range(3)]
```

### Hands-On Exercise: List Processor

Create a task manager:
```python
def task_manager():
    tasks = []
    
    while True:
        print("\nTask Manager")
        print("1. Add task")
        print("2. View tasks")
        print("3. Complete task")
        print("4. Exit")
        
        choice = input("Choose option: ")
        
        if choice == "1":
            task = input("Enter task: ")
            tasks.append(task)
            print("Task added!")
            
        elif choice == "2":
            if tasks:
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task}")
            else:
                print("No tasks!")
                
        elif choice == "3":
            if tasks:
                task_num = int(input("Enter task number: ")) - 1
                if 0 <= task_num < len(tasks):
                    completed = tasks.pop(task_num)
                    print(f"Completed: {completed}")
                else:
                    print("Invalid task number!")
            else:
                print("No tasks!")
                
        elif choice == "4":
            break

# Run task manager
task_manager()
```

## 2. Dictionaries and Sets

### The Library Catalog Metaphor

Think of dictionaries like a library catalog:
- Keys are like book codes
- Values are like book information
- Each key is unique
- Quick lookups by key
- Unordered (traditionally)

### Dictionaries

```python
# Creating dictionaries
person = {
    "name": "Alice",
    "age": 25,
    "city": "New York"
}

# Accessing values
name = person["name"]           # Direct access
age = person.get("age", 0)      # With default value

# Modifying dictionaries
person["email"] = "alice@example.com"  # Add new
person["age"] = 26                     # Update
del person["city"]                     # Remove

# Dictionary methods
keys = person.keys()           # Get all keys
values = person.values()       # Get all values
items = person.items()         # Get key-value pairs

# Dictionary comprehension
squares = {x: x**2 for x in range(5)}
```

### Sets

```python
# Creating sets (unique items)
fruits = {"apple", "banana", "cherry"}
numbers = set([1, 2, 2, 3, 3, 4])  # Duplicates removed

# Set operations
fruits.add("orange")        # Add item
fruits.remove("banana")     # Remove item
fruits.discard("kiwi")      # Remove if exists

# Set mathematics
a = {1, 2, 3}
b = {3, 4, 5}
union = a | b              # All items
intersection = a & b       # Common items
difference = a - b         # Items in a but not b
symmetric = a ^ b          # Items in one but not both
```

### Hands-On Exercise: Contact Manager

Create a contact management system:
```python
def contact_manager():
    contacts = {}
    
    while True:
        print("\nContact Manager")
        print("1. Add contact")
        print("2. View contact")
        print("3. List contacts")
        print("4. Delete contact")
        print("5. Exit")
        
        choice = input("Choose option: ")
        
        if choice == "1":
            name = input("Name: ")
            phone = input("Phone: ")
            email = input("Email: ")
            
            contacts[name] = {
                "phone": phone,
                "email": email
            }
            print("Contact added!")
            
        elif choice == "2":
            name = input("Enter name: ")
            if name in contacts:
                info = contacts[name]
                print(f"Phone: {info['phone']}")
                print(f"Email: {info['email']}")
            else:
                print("Contact not found!")
                
        elif choice == "3":
            if contacts:
                for name, info in contacts.items():
                    print(f"\n{name}:")
                    print(f"  Phone: {info['phone']}")
                    print(f"  Email: {info['email']}")
            else:
                print("No contacts!")
                
        elif choice == "4":
            name = input("Enter name: ")
            if name in contacts:
                del contacts[name]
                print("Contact deleted!")
            else:
                print("Contact not found!")
                
        elif choice == "5":
            break

# Run contact manager
contact_manager()
```

## 3. Advanced Operations

### The Recipe Modification Metaphor

Think of data operations like modifying recipes:
- Slicing is like selecting portions
- Sorting is like organizing ingredients
- Filtering is like removing unwanted items

### Slicing Operations

```python
# List slicing
items = [0, 1, 2, 3, 4, 5]
first_three = items[:3]     # [0, 1, 2]
last_three = items[-3:]     # [3, 4, 5]
steps = items[::2]          # [0, 2, 4]
reversed = items[::-1]      # [5, 4, 3, 2, 1, 0]

# String slicing
text = "Hello, World!"
hello = text[:5]           # "Hello"
world = text[7:-1]         # "World"
```

### Sorting and Filtering

```python
# Sorting lists
numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
sorted_nums = sorted(numbers)              # New sorted list
numbers.sort()                            # Sort in place
numbers.sort(reverse=True)                # Descending order

# Custom sorting
words = ["banana", "apple", "cherry"]
by_length = sorted(words, key=len)        # Sort by length
by_last = sorted(words, key=lambda x: x[-1])  # Sort by last letter

# Filtering
numbers = [1, 2, 3, 4, 5, 6]
evens = list(filter(lambda x: x % 2 == 0, numbers))
odds = [x for x in numbers if x % 2 != 0]
```

### Advanced Dictionary Operations

```python
# Dictionary merging
defaults = {"color": "red", "size": "medium"}
preferences = {"color": "blue", "type": "shirt"}
settings = {**defaults, **preferences}  # Preference wins

# Dictionary views
for key in settings:              # Iterate keys
    print(key)

for key, value in settings.items():  # Iterate pairs
    print(f"{key}: {value}")

# Nested dictionaries
users = {
    "alice": {
        "email": "alice@example.com",
        "roles": ["admin", "user"]
    },
    "bob": {
        "email": "bob@example.com",
        "roles": ["user"]
    }
}
```

### Hands-On Exercise: Data Analyzer

Create a data analysis tool:
```python
def analyze_data(data):
    """Analyze a list of numbers"""
    # Basic statistics
    count = len(data)
    total = sum(data)
    average = total / count
    
    # Sorted copy for median
    sorted_data = sorted(data)
    mid = count // 2
    median = (sorted_data[mid] + sorted_data[~mid]) / 2
    
    # Find mode
    from collections import Counter
    counts = Counter(data)
    mode = counts.most_common(1)[0][0]
    
    # Results dictionary
    return {
        "count": count,
        "sum": total,
        "average": average,
        "median": median,
        "mode": mode,
        "min": min(data),
        "max": max(data)
    }

# Test the analyzer
numbers = [4, 2, 6, 8, 4, 5, 3, 4, 9, 7]
results = analyze_data(numbers)

for key, value in results.items():
    print(f"{key.capitalize()}: {value}")
```

## Practical Exercises

### 1. Data Transformer
Build program that:
1. Reads structured data
2. Transforms format
3. Filters entries
4. Sorts results
5. Saves output

### 2. Inventory System
Create system that:
1. Tracks items
2. Manages quantities
3. Handles categories
4. Processes orders
5. Generates reports

### 3. Student Database
Develop program that:
1. Stores student info
2. Manages grades
3. Calculates statistics
4. Generates transcripts
5. Handles multiple classes

## Review Questions

1. **Lists and Tuples**
   - When use list vs tuple?
   - How slice sequences?
   - Best practices for comprehensions?

2. **Dictionaries and Sets**
   - When use dictionary vs list?
   - How handle missing keys?
   - When use sets?

3. **Advanced Operations**
   - How choose sorting method?
   - When use lambda functions?
   - Best practices for nested structures?

## Additional Resources

### Online Tools
- Python data structure visualizer
- Time complexity calculator
- Collection type chooser

### Further Reading
- Python collections module
- Time complexity guide
- Best practices guide

### Video Resources
- Data structure tutorials
- Algorithm visualizations
- Performance comparisons

## Next Steps

After mastering these concepts, you'll be ready to:
1. Design efficient data structures
2. Process complex data
3. Build robust applications

Remember: Choose the right data structure for your needs!

## Common Questions and Answers

Q: When should I use a list versus a dictionary?
A: Use lists for ordered collections, dictionaries when you need key-based lookup.

Q: Are sets faster than lists for lookups?
A: Yes, sets are optimized for checking membership, while lists require linear search.

Q: How do I choose between list and tuple?
A: Use tuples for immutable sequences (like coordinates) and lists for collections that might change.

## Glossary

- **List**: Mutable sequence
- **Tuple**: Immutable sequence
- **Dictionary**: Key-value store
- **Set**: Unique items collection
- **Slice**: Sequence subset
- **Comprehension**: Compact creation syntax
- **Key**: Dictionary identifier
- **Value**: Dictionary data
- **Immutable**: Cannot be changed
- **Mutable**: Can be modified

Remember: The right data structure makes your code cleaner and more efficient!
