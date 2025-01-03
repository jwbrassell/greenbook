# Chapter 1 Exercises: How Computers Think

## Practice Exercises

### Exercise 1: Binary Conversion
Convert the following decimal numbers to binary:
1. 15
2. 27
3. 64
4. 100
5. 255

### Exercise 2: Boolean Logic
Complete the following truth tables:

```
A | B | A AND B
0 | 0 |
0 | 1 |
1 | 0 |
1 | 1 |

A | B | A OR B
0 | 0 |
0 | 1 |
1 | 0 |
1 | 1 |

A | NOT A
0 |
1 |
```

### Exercise 3: Problem Decomposition
Break down the process of making a sandwich into its smallest possible steps, as if explaining it to a computer. Be explicit about every movement and decision.

### Exercise 4: Algorithm Design
Write step-by-step instructions for:
1. Finding the largest number in a list
2. Sorting three numbers in ascending order
3. Determining if a year is a leap year
4. Calculating the average of a set of numbers
5. Finding all prime numbers up to 100

### Exercise 5: Memory Allocation
Given a computer with:
- 8GB RAM
- 256GB SSD
- 4MB L3 Cache

Design a memory usage plan for:
1. A text editor processing a 1GB file
2. A web browser with 10 tabs open
3. A video game loading a new level
4. A photo editing application working with a 50MB image

### Exercise 6: Edge Case Identification
For each of the following programs, identify at least five edge cases that need to be handled:
1. A calculator application
2. A user registration form
3. A file upload system
4. A search function
5. A date parsing utility

## Solutions

### Exercise 1: Binary Conversion Solutions
```
15 = 1111
    (8 + 4 + 2 + 1)
    
27 = 11011
    (16 + 8 + 0 + 2 + 1)
    
64 = 1000000
    (64 + 0 + 0 + 0 + 0 + 0 + 0)
    
100 = 1100100
    (64 + 32 + 0 + 0 + 4 + 0 + 0)
    
255 = 11111111
    (128 + 64 + 32 + 16 + 8 + 4 + 2 + 1)
```

### Exercise 2: Boolean Logic Solutions
```
A | B | A AND B
0 | 0 | 0
0 | 1 | 0
1 | 0 | 0
1 | 1 | 1

A | B | A OR B
0 | 0 | 0
0 | 1 | 1
1 | 0 | 1
1 | 1 | 1

A | NOT A
0 | 1
1 | 0
```

### Exercise 3: Problem Decomposition Solution
Making a Sandwich Algorithm:
```
1. Initialize sandwich_making_process
2. Check prerequisites:
   - Check if hands are clean
   - Check if workspace is clean
   - Check if all ingredients are available
   
3. Gather materials:
   - Get cutting board
   - Get knife
   - Get plate
   
4. Prepare bread:
   - Open bread bag
   - Remove two slices
   - Close bread bag
   - Place slices on cutting board
   
5. Prepare ingredients:
   For each ingredient:
   - Remove from storage
   - Check if needs preparation
   - If needs cutting:
     - Place on cutting board
     - Cut to appropriate size
   - If needs spreading:
     - Get spreading utensil
     
6. Assemble sandwich:
   - Place first bread slice on plate
   - For each ingredient:
     - Add appropriate amount
     - Ensure even distribution
   - Place second bread slice on top
   
7. Final steps:
   - If sandwich needs cutting:
     - Cut diagonally
   - Clean workspace
   - Return ingredients to storage
   
8. End sandwich_making_process
```

### Exercise 4: Algorithm Solutions

#### 1. Finding the Largest Number
```
1. Initialize largest = first number in list
2. For each remaining number in list:
   - If current number > largest:
     - Set largest = current number
3. Return largest
```

#### 2. Sorting Three Numbers
```
1. Input numbers a, b, c
2. Compare a and b:
   - If a > b, swap them
3. Compare b and c:
   - If b > c, swap them
4. Compare a and b again:
   - If a > b, swap them
5. Numbers are now sorted
```

#### 3. Leap Year Check
```
1. If year is divisible by 4:
   - If year is divisible by 100:
     - If year is divisible by 400:
       - Is leap year
     - Else:
       - Not leap year
   - Else:
     - Is leap year
2. Else:
   - Not leap year
```

#### 4. Calculate Average
```
1. Initialize sum = 0
2. Initialize count = 0
3. For each number:
   - Add number to sum
   - Increment count
4. If count > 0:
   - Return sum divided by count
5. Else:
   - Return error (cannot divide by zero)
```

#### 5. Find Prime Numbers
```
1. Create list numbers from 2 to 100
2. Start with first number (2)
3. For each number in list:
   - If number is marked as prime:
     - Mark all its multiples as not prime
4. Return all numbers still marked as prime
```

### Exercise 5: Memory Allocation Solutions

#### 1. Text Editor (1GB file)
```
RAM Allocation:
- 256MB for application code and UI
- 512MB for file buffer
- 256MB for undo/redo history
- Remaining RAM for system processes

Cache Usage:
- L3: Frequently accessed file portions
- Virtual memory: Swap less used portions to SSD
```

#### 2. Web Browser (10 tabs)
```
RAM Allocation:
- 200MB base browser process
- 100-200MB per tab (dynamic)
- 512MB shared resource cache
- 1GB for media content

Cache Usage:
- L3: Active tab DOM and JavaScript
- SSD: Cache for static resources
```

#### 3. Video Game Level
```
RAM Allocation:
- 2GB for game engine
- 3GB for level assets
- 1GB for physics/AI
- 1GB for audio/effects

Cache Usage:
- L3: Frequently accessed textures
- SSD: Level streaming data
```

#### 4. Photo Editor (50MB image)
```
RAM Allocation:
- 500MB for application
- 200MB for image data
- 300MB for undo history
- 1GB for filters/effects

Cache Usage:
- L3: Active layer data
- RAM: Layer compositing
- SSD: Temporary files
```

### Exercise 6: Edge Cases Solutions

#### 1. Calculator Application
- Division by zero
- Overflow/underflow
- Invalid input (letters, symbols)
- Multiple decimal points
- Negative numbers in square root

#### 2. User Registration Form
- Empty required fields
- Invalid email format
- Password too short/long
- Username already exists
- Special characters in name fields

#### 3. File Upload System
- Zero byte files
- File too large
- Invalid file type
- Duplicate file names
- Corrupted files

#### 4. Search Function
- Empty search term
- Special characters
- Very long search terms
- No results found
- Too many results

#### 5. Date Parsing Utility
- Invalid date format
- Leap year dates
- Different timezone formats
- Future dates
- Historical dates before certain cutoff

## Additional Practice Projects

### Project 1: Binary Calculator Implementation
Create a flowchart for implementing a binary calculator that:
1. Accepts two binary numbers
2. Validates input
3. Performs basic arithmetic
4. Handles overflow
5. Displays results in both binary and decimal

### Project 2: Memory Management Simulation
Design a program that simulates memory management:
1. Fixed memory size (e.g., 1024 units)
2. Allocation requests
3. Deallocation requests
4. Memory fragmentation handling
5. Performance metrics tracking

### Project 3: Logic Gate Simulator
Plan a logic gate simulator that:
1. Implements basic gates (AND, OR, NOT)
2. Allows gate combinations
3. Generates truth tables
4. Validates circuit design
5. Handles timing considerations

## Conclusion

These exercises are designed to develop your computational thinking skills and understanding of how computers process information. Remember:

1. Break down complex problems into smaller steps
2. Think in terms of explicit instructions
3. Consider all possible cases and edge conditions
4. Understand resource limitations
5. Practice systematic problem-solving

As you work through these exercises, focus on developing clear, precise solutions that a computer could execute. This mindset will serve you well as you progress in your programming journey.
