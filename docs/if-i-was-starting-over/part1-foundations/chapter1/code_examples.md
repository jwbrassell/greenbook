# Chapter 1 Code Examples: How Computers Think

This document provides practical code implementations of the concepts discussed in Chapter 1. We'll use Python for most examples as it's readable and beginner-friendly, but the concepts apply to any programming language.

## 1. Binary Operations

### Binary Number Conversion
```python
def decimal_to_binary(decimal_num):
    """Convert a decimal number to its binary representation."""
    if decimal_num == 0:
        return "0"
    
    binary = ""
    num = abs(decimal_num)
    
    while num > 0:
        binary = str(num % 2) + binary
        num //= 2
    
    return "-" + binary if decimal_num < 0 else binary

# Example usage
print(decimal_to_binary(42))  # Output: 101010
print(decimal_to_binary(-15)) # Output: -1111
```

### Binary Arithmetic
```python
def binary_add(bin1, bin2):
    """Add two binary numbers (represented as strings)."""
    # Convert to integers, add, then convert back to binary
    num1 = int(bin1, 2)
    num2 = int(bin2, 2)
    sum_decimal = num1 + num2
    return bin(sum_decimal)[2:]  # Remove '0b' prefix

# Example usage
print(binary_add('1010', '1011'))  # Output: 10101
```

## 2. Boolean Logic Operations

### Basic Logic Gates
```python
def AND(a, b):
    return a and b

def OR(a, b):
    return a or b

def NOT(a):
    return not a

def XOR(a, b):
    return a != b

def NAND(a, b):
    return not (a and b)

def NOR(a, b):
    return not (a or b)

# Example usage
print("Truth Table for AND Gate:")
print("A | B | Output")
print("-" * 13)
for a in [False, True]:
    for b in [False, True]:
        print(f"{int(a)} | {int(b)} | {int(AND(a, b))}")
```

## 3. Memory Management Simulation

### Simple Memory Allocator
```python
class MemoryBlock:
    def __init__(self, size, is_free=True):
        self.size = size
        self.is_free = is_free
        self.data = None

class MemoryManager:
    def __init__(self, total_size):
        self.total_size = total_size
        self.blocks = [MemoryBlock(total_size)]
    
    def allocate(self, size):
        """Attempt to allocate a block of memory."""
        for i, block in enumerate(self.blocks):
            if block.is_free and block.size >= size:
                if block.size > size:
                    # Split block
                    new_block = MemoryBlock(block.size - size)
                    block.size = size
                    self.blocks.insert(i + 1, new_block)
                
                block.is_free = False
                block.data = bytearray(size)  # Simulate memory allocation
                return block
        
        raise MemoryError("Not enough memory")
    
    def free(self, block):
        """Free a block of memory."""
        block.is_free = True
        block.data = None
        self._merge_free_blocks()
    
    def _merge_free_blocks(self):
        """Merge adjacent free blocks to reduce fragmentation."""
        i = 0
        while i < len(self.blocks) - 1:
            if self.blocks[i].is_free and self.blocks[i + 1].is_free:
                self.blocks[i].size += self.blocks[i + 1].size
                self.blocks.pop(i + 1)
            else:
                i += 1
    
    def get_status(self):
        """Return current memory status."""
        used = sum(b.size for b in self.blocks if not b.is_free)
        free = self.total_size - used
        return {
            'total': self.total_size,
            'used': used,
            'free': free,
            'blocks': len(self.blocks)
        }

# Example usage
memory = MemoryManager(1024)  # 1KB of memory

try:
    # Allocate some memory blocks
    block1 = memory.allocate(256)  # 256 bytes
    block2 = memory.allocate(128)  # 128 bytes
    
    # Print memory status
    print("After allocations:", memory.get_status())
    
    # Free a block
    memory.free(block1)
    print("After freeing block1:", memory.get_status())
    
except MemoryError as e:
    print(f"Memory allocation failed: {e}")
```

## 4. Problem Decomposition Example

### Making a Sandwich (Object-Oriented Approach)
```python
class Ingredient:
    def __init__(self, name, needs_preparation=False):
        self.name = name
        self.needs_preparation = needs_preparation
        self.is_prepared = False
    
    def prepare(self):
        if self.needs_preparation and not self.is_prepared:
            print(f"Preparing {self.name}")
            self.is_prepared = True

class SandwichMaker:
    def __init__(self):
        self.workspace_clean = False
        self.hands_clean = False
    
    def check_prerequisites(self):
        if not self.hands_clean:
            print("Washing hands")
            self.hands_clean = True
        
        if not self.workspace_clean:
            print("Cleaning workspace")
            self.workspace_clean = True
    
    def prepare_ingredients(self, ingredients):
        for ingredient in ingredients:
            ingredient.prepare()
    
    def make_sandwich(self, ingredients):
        # Check prerequisites
        self.check_prerequisites()
        
        # Prepare ingredients
        self.prepare_ingredients(ingredients)
        
        # Assemble sandwich
        print("\nAssembling sandwich:")
        print("1. Placing first slice of bread")
        for ingredient in ingredients[1:-1]:  # Skip bread slices
            print(f"2. Adding {ingredient.name}")
        print("3. Placing second slice of bread")
        
        # Clean up
        print("\nCleaning workspace")
        self.workspace_clean = False

# Example usage
def make_sandwich_demo():
    # Create ingredients
    ingredients = [
        Ingredient("bread slice"),
        Ingredient("lettuce", needs_preparation=True),
        Ingredient("tomato", needs_preparation=True),
        Ingredient("cheese"),
        Ingredient("bread slice")
    ]
    
    # Create sandwich maker and make sandwich
    maker = SandwichMaker()
    maker.make_sandwich(ingredients)

make_sandwich_demo()
```

## 5. Algorithm Implementation

### Finding Largest Number
```python
def find_largest(numbers):
    """
    Find the largest number in a list using explicit computer thinking.
    Demonstrates how computers process lists step by step.
    """
    if not numbers:  # Edge case: empty list
        raise ValueError("Cannot find largest in empty list")
    
    largest = numbers[0]  # Start with first number
    position = 0  # Keep track of position for demonstration
    
    print(f"Starting with {largest} at position {position}")
    
    # Check each number one by one
    for i, number in enumerate(numbers[1:], 1):
        print(f"Comparing {number} with current largest {largest}")
        
        if number > largest:
            largest = number
            position = i
            print(f"New largest number found: {largest} at position {position}")
    
    return largest, position

# Example usage
numbers = [4, 2, 7, 1, 9, 3, 6]
largest, pos = find_largest(numbers)
print(f"\nFinal result: {largest} at position {pos}")
```

## 6. Edge Case Handling

### Date Parser with Edge Cases
```python
from datetime import datetime

def parse_date(date_string):
    """
    Parse a date string with comprehensive edge case handling.
    Demonstrates how computers need explicit handling for all cases.
    """
    if not date_string:
        raise ValueError("Date string cannot be empty")
    
    # Try multiple date formats
    formats = [
        "%Y-%m-%d",      # 2023-12-31
        "%d/%m/%Y",      # 31/12/2023
        "%Y/%m/%d",      # 2023/12/31
        "%d-%m-%Y",      # 31-12-2023
        "%Y.%m.%d",      # 2023.12.31
    ]
    
    # Track all attempted formats for error reporting
    attempted = []
    
    for fmt in formats:
        try:
            date = datetime.strptime(date_string, fmt)
            
            # Additional validation
            year = date.year
            if year < 1900:
                raise ValueError("Year cannot be before 1900")
            if year > 2100:
                raise ValueError("Year cannot be after 2100")
            
            return date
            
        except ValueError as e:
            attempted.append(fmt)
            continue
    
    # If we get here, no format worked
    raise ValueError(
        f"Could not parse date '{date_string}'. "
        f"Tried formats: {', '.join(attempted)}"
    )

# Example usage with edge cases
test_dates = [
    "2023-12-31",    # Valid ISO format
    "31/12/2023",    # Valid UK format
    "",              # Empty string
    "2023-13-45",    # Invalid month/day
    "1800-01-01",    # Too old
    "2200-01-01",    # Too far in future
    "not a date",    # Invalid format
]

for date_string in test_dates:
    try:
        result = parse_date(date_string)
        print(f"Successfully parsed '{date_string}' to {result}")
    except ValueError as e:
        print(f"Error parsing '{date_string}': {e}")
```

## Conclusion

These code examples demonstrate how theoretical computer concepts translate into practical implementations. Key takeaways:

1. Computers need explicit instructions for every operation
2. Edge cases must be handled explicitly
3. Complex operations are built from simple ones
4. Memory and resources must be managed carefully
5. Problem decomposition is essential for clean solutions

The examples also show how high-level programming languages abstract away many low-level details while still following the fundamental principles of how computers think and process information.

Remember that while these examples use Python, the underlying concepts apply to any programming language or system. The key is understanding how to break down problems into steps that a computer can execute.
