# Chapter 2 Exercises: Programming Logic Fundamentals

## Practice Exercises

### Exercise 1: Sequential Logic
Write step-by-step instructions for the following tasks, being as precise and detailed as possible:

1. Making a cup of coffee using a coffee machine
2. Withdrawing money from an ATM
3. Sorting a deck of cards by suit and number
4. Creating a backup of important files
5. Setting up an email account

### Exercise 2: Variables and Data Storage
For each scenario, identify the variables needed and their purpose:

1. Library Book Management System
   - What variables would you need to track books?
   - What information needs to be stored for each book?
   - What variables would change over time?

2. Restaurant Order System
   - What variables are needed for each order?
   - What information needs to be tracked during service?
   - What totals or summaries need to be maintained?

3. Weather Monitoring Station
   - What environmental variables need to be tracked?
   - What calculated values need to be stored?
   - What historical data should be maintained?

### Exercise 3: Conditional Logic
Write pseudo-code for the following scenarios using IF-THEN-ELSE statements:

1. Movie Ticket Pricing System
```
Input: customer_age, day_of_week, show_time
Output: ticket_price
```

2. Grade Calculator
```
Input: exam_score, homework_completion, attendance
Output: final_grade
```

3. Traffic Light Controller
```
Input: current_color, time_elapsed, emergency_vehicle_present
Output: next_color
```

4. Smart Home Temperature Control
```
Input: current_temp, desired_temp, time_of_day, energy_mode
Output: hvac_action
```

### Exercise 4: Loops and Iteration
Design algorithms using loops for the following tasks:

1. Find the average of a list of numbers
2. Count occurrences of a specific character in a text
3. Generate a multiplication table (1-10)
4. Find all prime numbers up to 100
5. Calculate compound interest over multiple years

### Exercise 5: Logical Operators
Create truth tables and solve these logical problems:

1. Access Control System
```
Conditions:
- User has valid ID
- ID is not expired
- User has security clearance
- Time is within working hours
```

2. Online Purchase Validation
```
Conditions:
- Item is in stock
- User has sufficient funds
- Shipping address is valid
- Payment method is accepted
```

3. File Operation Permission
```
Conditions:
- User is authenticated
- File is not locked
- User has write permissions
- System has available storage
```

### Exercise 6: Error Handling
Identify potential errors and write error handling logic for:

1. User Registration System
2. File Upload Process
3. Database Connection and Query
4. API Request/Response
5. Mathematical Calculations

## Solutions

### Exercise 1: Sequential Logic Solutions

#### Making Coffee with Coffee Machine
```
1. Check Prerequisites:
   1.1. Verify machine is plugged in
   1.2. Check water reservoir level
   1.3. Check coffee bean hopper
   1.4. Ensure cup is available

2. Preparation:
   2.1. Fill water if needed
   2.2. Add coffee beans if needed
   2.3. Place cup in designated area
   
3. Operation:
   3.1. Turn on machine
   3.2. Wait for machine to heat up
   3.3. Select coffee type
   3.4. Press start button
   
4. Completion:
   4.1. Wait for coffee to finish brewing
   4.2. Remove cup when done
   4.3. Clean up any spills
   4.4. Turn off machine if not needed
```

### Exercise 2: Variables Solutions

#### Library Book Management System
```
Variables Needed:
1. Book Information (per book):
   - book_id (unique identifier)
   - title
   - author
   - isbn
   - publication_date
   - current_status (available/checked_out/reserved)
   - location_code
   - condition_rating

2. Lending Information:
   - checkout_date
   - due_date
   - borrower_id
   - renewal_count
   
3. System Tracking:
   - total_books
   - books_checked_out
   - overdue_books
   - daily_transactions
```

### Exercise 3: Conditional Logic Solutions

#### Movie Ticket Pricing
```
IF day_of_week is "Tuesday" THEN
    base_price = 8.00  // Tuesday discount
ELSE
    base_price = 12.00

IF show_time < "17:00" THEN
    base_price = base_price - 2.00  // Matinee discount

IF customer_age < 13 THEN
    final_price = base_price * 0.75  // Child discount
ELSE IF customer_age >= 65 THEN
    final_price = base_price * 0.85  // Senior discount
ELSE
    final_price = base_price

RETURN final_price
```

### Exercise 4: Loops Solutions

#### Average Calculator
```
sum = 0
count = 0

FOR EACH number in number_list
    sum = sum + number
    count = count + 1

IF count > 0 THEN
    average = sum / count
    RETURN average
ELSE
    RETURN "Error: Empty list"
```

### Exercise 5: Logical Operators Solutions

#### Access Control System
```
Truth Table:
Valid ID | Not Expired | Clearance | Work Hours | Access
   0     |     0      |     0     |     0     |   0
   0     |     0      |     0     |     1     |   0
   0     |     0      |     1     |     0     |   0
   0     |     0      |     1     |     1     |   0
   0     |     1      |     0     |     0     |   0
   0     |     1      |     0     |     1     |   0
   0     |     1      |     1     |     0     |   0
   0     |     1      |     1     |     1     |   0
   1     |     0      |     0     |     0     |   0
   1     |     0      |     0     |     1     |   0
   1     |     0      |     1     |     0     |   0
   1     |     0      |     1     |     1     |   0
   1     |     1      |     0     |     0     |   0
   1     |     1      |     0     |     1     |   0
   1     |     1      |     1     |     0     |   0
   1     |     1      |     1     |     1     |   1
```

### Exercise 6: Error Handling Solutions

#### User Registration System
```
FUNCTION register_user(username, email, password):
    // Input Validation
    IF username is empty THEN
        RETURN error("Username cannot be empty")
    
    IF email is empty THEN
        RETURN error("Email cannot be empty")
    
    IF NOT is_valid_email_format(email) THEN
        RETURN error("Invalid email format")
    
    IF password length < 8 THEN
        RETURN error("Password must be at least 8 characters")
    
    // Database Operations
    TRY
        IF user_exists(username) THEN
            RETURN error("Username already taken")
        
        IF email_exists(email) THEN
            RETURN error("Email already registered")
        
        encrypted_password = encrypt(password)
        
        success = save_to_database(username, email, encrypted_password)
        
        IF success THEN
            RETURN success("User registered successfully")
        ELSE
            RETURN error("Database error occurred")
            
    CATCH DatabaseError
        RETURN error("Database connection failed")
    CATCH EncryptionError
        RETURN error("Password encryption failed")
    CATCH ANY_ERROR
        RETURN error("An unexpected error occurred")
```

## Practice Projects

### Project 1: Library Management System
Design a simple library management system that:
1. Tracks books and their status
2. Handles checkouts and returns
3. Manages late fees
4. Generates reports

### Project 2: Temperature Monitoring System
Create a system that:
1. Records temperatures throughout the day
2. Calculates averages
3. Triggers alerts for extreme values
4. Generates daily reports

### Project 3: Shopping Cart Calculator
Design a program that:
1. Adds/removes items
2. Applies discounts
3. Calculates tax
4. Handles payment processing

## Additional Challenges

1. **Logic Puzzle Solver**
   - Create algorithms to solve classic logic puzzles
   - Implement solution checking
   - Generate puzzle variations

2. **Pattern Recognition**
   - Identify patterns in number sequences
   - Generate next numbers in sequence
   - Explain the pattern logic

3. **Decision Tree Implementation**
   - Create a decision tree for a specific scenario
   - Handle multiple decision paths
   - Optimize decision flow

## Conclusion

These exercises are designed to strengthen your understanding of programming logic fundamentals. Remember:

1. Start with simple solutions and gradually add complexity
2. Test your logic with different inputs
3. Consider edge cases and error conditions
4. Document your thinking process
5. Practice regularly to build confidence

As you work through these exercises, focus on:
- Breaking down problems into smaller steps
- Writing clear, unambiguous instructions
- Testing your solutions thoroughly
- Learning from mistakes and refining your approach

The skills you develop here will serve as a foundation for more advanced programming concepts in future chapters.
