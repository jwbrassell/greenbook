# Chapter 3: Data Types and Structures

## Introduction

Think about organizing your kitchen. You have different types of containers for different items: spice jars, tupperware for leftovers, boxes for dry goods, etc. Similarly, computers need different ways to store different types of information. In this chapter, we'll explore how computers organize and store various kinds of data, using examples from everyday life.

## 1. Basic Data Types

### The Measuring Tools Metaphor

Just as we use different tools to measure different things (ruler for length, scale for weight, thermometer for temperature), computers use different data types to store different kinds of information.

### Numbers

#### Integers (Whole Numbers)
```
Examples:
- Age: 25
- Number of pets: 2
- Year: 2024
- Temperature: -5

Like counting marbles - you can't have half a marble!
```

#### Floating Point (Decimal Numbers)
```
Examples:
- Price: $19.99
- Height: 5.9
- Weight: 155.5
- Temperature: 98.6

Like measuring ingredients - you can have partial amounts!
```

### Text (Strings)

#### The Beads on a String Metaphor
Think of text as beads on a string:
- Each character is a bead
- They maintain their order
- Can be different lengths
- Can include any characters

```
Examples:
- Name: "John Smith"
- Address: "123 Main St"
- Email: "john@email.com"
- Message: "Hello, World!"
```

### Boolean (True/False)

#### The Light Switch Metaphor
Like a light switch that can only be ON or OFF:
```
Examples:
- Is it raining? true/false
- Is the door locked? true/false
- Is the system ready? true/false
- Are there errors? true/false
```

### Hands-On Exercise: Type Identifier

Create cards with different values:
1. Write various values on index cards
   - Numbers (42, 3.14, -7, 1000)
   - Text ("Hello", "A", "12345")
   - True/False values
2. Sort them by type
3. Explain why each belongs in its category

## 2. Variables and Storage

### The Labeled Boxes Metaphor

Think of variables like labeled boxes:
- The label is the variable name
- The contents are the value
- You can change the contents
- The label stays the same

### Variable Naming

```
Good names:
userAge = 25
firstName = "John"
isLoggedIn = true

Bad names:
a = 25        // Too vague
x1 = "John"   // Unclear purpose
thing = true  // Not descriptive
```

### Variable Assignment

```
Think of it like labeling containers:

age = 25
// Put the number 25 in the box labeled "age"

name = "Alice"
// Put the text "Alice" in the box labeled "name"

isStudent = true
// Put the value true in the box labeled "isStudent"
```

### Changing Values

```
price = 10
// Box labeled "price" contains 10

price = 15
// Same box now contains 15

Like using the same container for different things:
- Lunch container: sandwich → leftovers → salad
- Variable: 10 → 15 → 20
```

### Hands-On Exercise: Variable Practice

Use sticky notes as variables:
1. Write variable names on sticky notes
2. Write values on separate papers
3. Practice "assigning" values by placing papers on notes
4. Practice "changing" values by replacing papers

## 3. Simple Data Structures

### Lists (Arrays)

#### The Shopping List Metaphor
Like a numbered shopping list:
- Items are in order
- Each has a position (index)
- Can add/remove items
- Can change items

```
groceryList = ["milk", "eggs", "bread", "cheese"]
Indexes:         0       1       2        3

Like numbered shelves:
Shelf 0: milk
Shelf 1: eggs
Shelf 2: bread
Shelf 3: cheese
```

#### List Operations
```
// Adding items
groceryList.add("apples")

// Removing items
groceryList.remove("bread")

// Changing items
groceryList[1] = "butter"

// Accessing items
firstItem = groceryList[0]
```

### Key-Value Pairs (Dictionaries)

#### The Recipe Ingredients Metaphor
Like a recipe with measurements:
- Each ingredient (key) has an amount (value)
- No numbered order
- Easy to look up specific items

```
recipe = {
    "flour": "2 cups",
    "sugar": "1 cup",
    "eggs": 2,
    "milk": "1/2 cup"
}

Like a recipe card:
flour → 2 cups
sugar → 1 cup
eggs → 2
milk → 1/2 cup
```

#### Dictionary Operations
```
// Adding pairs
recipe["vanilla"] = "1 tsp"

// Removing pairs
recipe.remove("milk")

// Changing values
recipe["sugar"] = "3/4 cup"

// Looking up values
flourNeeded = recipe["flour"]
```

### Sets

#### The Stamp Collection Metaphor
Like a stamp collection:
- No duplicates
- No specific order
- Either have it or don't

```
uniqueColors = {"red", "blue", "green"}

Like a collector's album:
- Can't have duplicate stamps
- Order doesn't matter
- Easy to check if you have something
```

### Hands-On Exercise: Data Structure Organizer

Create physical versions of data structures:
1. List: Use a row of cups with numbered labels
2. Dictionary: Use pairs of sticky notes
3. Set: Use a collection box with rules

## 4. Choosing the Right Structure

### Decision Guide

```
Use a List when:
- Order matters
- Items are similar
- Need to process in sequence
Example: playlist, todo list

Use a Dictionary when:
- Need to look up values
- Items have labels
- Order doesn't matter
Example: contact list, settings

Use a Set when:
- Need unique items
- Order doesn't matter
- Just need yes/no existence
Example: registered users, available colors
```

### Real-World Examples

#### Student Management System
```
// List for attendance
attendance = ["present", "absent", "present", "present"]

// Dictionary for grades
grades = {
    "John": 85,
    "Alice": 92,
    "Bob": 78
}

// Set for unique student IDs
studentIDs = {"S001", "S002", "S003"}
```

#### Online Shopping Cart
```
// List for order history
orderHistory = ["Book", "Shoes", "Phone"]

// Dictionary for product details
product = {
    "name": "Laptop",
    "price": 999.99,
    "inStock": true
}

// Set for categories
categories = {"Electronics", "Books", "Clothing"}
```

## Practical Exercises

### 1. Type Classifier
Create a game where players:
1. Draw cards with values
2. Identify the data type
3. Explain their reasoning
4. Score points for correct answers

### 2. Data Structure Builder
Using household items:
1. Build a list using boxes
2. Create a dictionary with labels
3. Make a set with rules
4. Practice operations on each

### 3. Real-World Mapper
Take a real situation and map it to data structures:
1. Choose a scenario (library, store, school)
2. Identify different data types needed
3. Choose appropriate structures
4. Show how data would be organized

## Review Questions

1. **Data Types**
   - What are the main basic data types?
   - When do you use float vs integer?
   - How do you choose between data types?

2. **Variables**
   - What makes a good variable name?
   - How does assignment work?
   - Why use variables?

3. **Data Structures**
   - What's the difference between lists and sets?
   - When would you use a dictionary?
   - How do you choose the right structure?

## Additional Resources

### Online Tools
- Data type visualizers
- Structure animators
- Practice problems

### Further Reading
- Data organization principles
- Memory management
- Efficiency considerations

### Video Resources
- Visual data type explanations
- Structure manipulation demos
- Real-world applications

## Next Steps

After mastering these concepts, you'll be ready to:
1. Work with complex data
2. Build data-driven programs
3. Optimize data organization

Remember: Choosing the right data type and structure is crucial for writing efficient programs!

## Common Questions and Answers

Q: Why can't I just use lists for everything?
A: Different structures have different strengths. Using the right one makes your program more efficient and easier to understand.

Q: When should I use integers vs floating point numbers?
A: Use integers when you need whole numbers (counting things) and floating point when you need decimal precision (measurements, calculations).

Q: How do I know if I need a dictionary instead of a list?
A: If you find yourself looking up items by name rather than position, a dictionary is probably better.

## Glossary

- **Data Type**: Category of data (number, text, etc.)
- **Variable**: Named storage location
- **List**: Ordered collection of items
- **Dictionary**: Collection of key-value pairs
- **Set**: Unordered collection of unique items
- **Integer**: Whole number
- **Float**: Decimal number
- **String**: Text data
- **Boolean**: True/False value
- **Index**: Position in a list

Remember: Data organization is like organizing your home - using the right container for each item makes everything easier to find and use!
