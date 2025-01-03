# Chapter 3: JavaScript Basics

## Introduction

Think about bringing a house to life - after building the structure (HTML) and decorating it (CSS), you need to add functionality like light switches, door handles, and appliances. JavaScript is like adding interactivity to your webpage. It lets users interact with elements, updates content dynamically, and responds to events. In this chapter, we'll learn how to make web pages interactive.

## 1. JavaScript Fundamentals

### The Remote Control Metaphor

Think of JavaScript like a remote control:
- Variables store information (like channel presets)
- Functions perform actions (like buttons)
- Events trigger responses (like pressing buttons)
- DOM manipulation changes display (like changing channels)

### Adding JavaScript to HTML

```html
<!-- Internal JavaScript -->
<script>
    console.log("Hello, World!");
</script>

<!-- External JavaScript -->
<script src="script.js"></script>

<!-- Inline JavaScript (avoid) -->
<button onclick="alert('Hello!')">Click me</button>
```

### Basic Syntax

```javascript
// Variables (like storage containers)
let name = "Alice";              // Can be reassigned
const age = 25;                  // Cannot be reassigned
var oldWay = "avoid using var";  // Old way, avoid

// Data Types
let text = "Hello";              // String
let number = 42;                 // Number
let isTrue = true;               // Boolean
let nothing = null;              // Null
let undefined;                   // Undefined
let person = {                   // Object
    name: "Bob",
    age: 30
};
let colors = ["red", "blue"];    // Array

// Functions (like remote control buttons)
function greet(name) {
    return `Hello, ${name}!`;
}

// Arrow Functions (modern way)
const greet = (name) => {
    return `Hello, ${name}!`;
};

// Short Arrow Function
const add = (a, b) => a + b;
```

### Hands-On Exercise: Basic Calculator

Create a simple calculator:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Calculator</title>
    <style>
        .calculator {
            max-width: 300px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        input, button {
            margin: 5px;
            padding: 5px;
        }

        button {
            width: 40px;
            height: 40px;
        }
    </style>
</head>
<body>
    <div class="calculator">
        <input type="text" id="display" readonly>
        <br>
        <button onclick="appendNumber('1')">1</button>
        <button onclick="appendNumber('2')">2</button>
        <button onclick="appendNumber('3')">3</button>
        <button onclick="setOperation('+')">+</button>
        <br>
        <button onclick="appendNumber('4')">4</button>
        <button onclick="appendNumber('5')">5</button>
        <button onclick="appendNumber('6')">6</button>
        <button onclick="setOperation('-')">-</button>
        <br>
        <button onclick="appendNumber('7')">7</button>
        <button onclick="appendNumber('8')">8</button>
        <button onclick="appendNumber('9')">9</button>
        <button onclick="setOperation('*')">*</button>
        <br>
        <button onclick="clearDisplay()">C</button>
        <button onclick="appendNumber('0')">0</button>
        <button onclick="calculate()">=</button>
        <button onclick="setOperation('/')">/</button>
    </div>

    <script>
        let currentNumber = '';
        let previousNumber = '';
        let operation = null;

        const display = document.getElementById('display');

        function appendNumber(num) {
            currentNumber += num;
            display.value = currentNumber;
        }

        function setOperation(op) {
            if (currentNumber !== '') {
                if (previousNumber !== '') {
                    calculate();
                }
                operation = op;
                previousNumber = currentNumber;
                currentNumber = '';
            }
        }

        function calculate() {
            if (previousNumber !== '' && currentNumber !== '' && operation) {
                const prev = parseFloat(previousNumber);
                const curr = parseFloat(currentNumber);
                let result;

                switch(operation) {
                    case '+':
                        result = prev + curr;
                        break;
                    case '-':
                        result = prev - curr;
                        break;
                    case '*':
                        result = prev * curr;
                        break;
                    case '/':
                        result = prev / curr;
                        break;
                }

                display.value = result;
                currentNumber = result.toString();
                previousNumber = '';
                operation = null;
            }
        }

        function clearDisplay() {
            currentNumber = '';
            previousNumber = '';
            operation = null;
            display.value = '';
        }
    </script>
</body>
</html>
```

## 2. DOM Manipulation

### The Puppet Show Metaphor

Think of DOM manipulation like controlling puppets:
- DOM is like the puppet theater
- Elements are like puppets
- JavaScript is like the puppeteer
- Events are like audience reactions

### Selecting Elements

```javascript
// Single element selectors
const element = document.getElementById('myId');
const element = document.querySelector('.myClass');

// Multiple element selectors
const elements = document.getElementsByClassName('myClass');
const elements = document.getElementsByTagName('div');
const elements = document.querySelectorAll('.myClass');

// Traversing the DOM
const parent = element.parentElement;
const children = element.children;
const next = element.nextElementSibling;
const prev = element.previousElementSibling;
```

### Modifying Elements

```javascript
// Changing content
element.textContent = 'New text';
element.innerHTML = '<span>New HTML</span>';

// Modifying attributes
element.setAttribute('class', 'newClass');
element.removeAttribute('class');
element.id = 'newId';

// Styling
element.style.color = 'red';
element.style.backgroundColor = 'blue';
element.classList.add('newClass');
element.classList.remove('oldClass');
element.classList.toggle('active');

// Creating elements
const div = document.createElement('div');
div.textContent = 'New element';
parentElement.appendChild(div);

// Removing elements
element.remove();
parentElement.removeChild(element);
```

### Hands-On Exercise: Dynamic List

Create an interactive todo list:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo List</title>
    <style>
        .todo-app {
            max-width: 500px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }

        .todo-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            margin: 5px 0;
            background-color: #f9f9f9;
            border-radius: 4px;
        }

        .completed {
            text-decoration: line-through;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="todo-app">
        <h2>Todo List</h2>
        <form id="todo-form">
            <input type="text" id="todo-input" placeholder="Add new task">
            <button type="submit">Add</button>
        </form>
        <ul id="todo-list"></ul>
    </div>

    <script>
        const form = document.getElementById('todo-form');
        const input = document.getElementById('todo-input');
        const list = document.getElementById('todo-list');

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const text = input.value.trim();
            if (text !== '') {
                addTodoItem(text);
                input.value = '';
            }
        });

        function addTodoItem(text) {
            const li = document.createElement('li');
            li.className = 'todo-item';

            const span = document.createElement('span');
            span.textContent = text;

            const buttons = document.createElement('div');
            
            const completeBtn = document.createElement('button');
            completeBtn.textContent = '✓';
            completeBtn.onclick = () => {
                span.classList.toggle('completed');
            };

            const deleteBtn = document.createElement('button');
            deleteBtn.textContent = '×';
            deleteBtn.onclick = () => {
                li.remove();
            };

            buttons.appendChild(completeBtn);
            buttons.appendChild(deleteBtn);

            li.appendChild(span);
            li.appendChild(buttons);
            list.appendChild(li);
        }
    </script>
</body>
</html>
```

## 3. Event Handling

### The Restaurant Service Metaphor

Think of events like restaurant service:
- Events are like customer requests
- Event listeners are like waiters
- Event handlers are like kitchen responses
- Event bubbling is like passing orders up

### Common Events

```javascript
// Mouse events
element.addEventListener('click', handleClick);
element.addEventListener('mouseover', handleHover);
element.addEventListener('mouseout', handleOut);

// Keyboard events
element.addEventListener('keydown', handleKeyDown);
element.addEventListener('keyup', handleKeyUp);
element.addEventListener('keypress', handleKeyPress);

// Form events
form.addEventListener('submit', handleSubmit);
input.addEventListener('change', handleChange);
input.addEventListener('input', handleInput);

// Document/Window events
window.addEventListener('load', handleLoad);
window.addEventListener('resize', handleResize);
document.addEventListener('DOMContentLoaded', handleReady);
```

### Event Object

```javascript
element.addEventListener('click', (event) => {
    // Event information
    console.log(event.type);          // Type of event
    console.log(event.target);        // Element that triggered
    console.log(event.currentTarget); // Element handling
    
    // Mouse information
    console.log(event.clientX);       // Mouse X position
    console.log(event.clientY);       // Mouse Y position
    
    // Keyboard information
    console.log(event.key);           // Key pressed
    console.log(event.keyCode);       // Key code
    
    // Control flow
    event.preventDefault();           // Stop default action
    event.stopPropagation();         // Stop bubbling
});
```

### Hands-On Exercise: Interactive Form

Create a form with validation:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interactive Form</title>
    <style>
        .form-container {
            max-width: 500px;
            margin: 20px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        .error {
            color: red;
            font-size: 0.8em;
            display: none;
        }

        input.invalid {
            border-color: red;
        }
    </style>
</head>
<body>
    <div class="form-container">
        <form id="registration-form">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username">
                <div class="error" id="username-error">
                    Username must be at least 3 characters
                </div>
            </div>

            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" name="email">
                <div class="error" id="email-error">
                    Please enter a valid email
                </div>
            </div>

            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" name="password">
                <div class="error" id="password-error">
                    Password must be at least 6 characters
                </div>
            </div>

            <div class="form-group">
                <label for="confirm-password">Confirm Password:</label>
                <input type="password" id="confirm-password" name="confirm-password">
                <div class="error" id="confirm-password-error">
                    Passwords must match
                </div>
            </div>

            <button type="submit">Register</button>
        </form>
    </div>

    <script>
        const form = document.getElementById('registration-form');
        const fields = {
            username: {
                element: document.getElementById('username'),
                error: document.getElementById('username-error'),
                validate: (value) => value.length >= 3
            },
            email: {
                element: document.getElementById('email'),
                error: document.getElementById('email-error'),
                validate: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)
            },
            password: {
                element: document.getElementById('password'),
                error: document.getElementById('password-error'),
                validate: (value) => value.length >= 6
            },
            confirmPassword: {
                element: document.getElementById('confirm-password'),
                error: document.getElementById('confirm-password-error'),
                validate: (value) => value === fields.password.element.value
            }
        };

        // Add input event listeners
        Object.keys(fields).forEach(fieldName => {
            const field = fields[fieldName];
            
            field.element.addEventListener('input', () => {
                validateField(fieldName);
            });
        });

        // Form submission
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            
            let isValid = true;
            
            // Validate all fields
            Object.keys(fields).forEach(fieldName => {
                if (!validateField(fieldName)) {
                    isValid = false;
                }
            });
            
            if (isValid) {
                alert('Form submitted successfully!');
                form.reset();
            }
        });

        function validateField(fieldName) {
            const field = fields[fieldName];
            const value = field.element.value;
            const isValid = field.validate(value);
            
            if (isValid) {
                field.element.classList.remove('invalid');
                field.error.style.display = 'none';
            } else {
                field.element.classList.add('invalid');
                field.error.style.display = 'block';
            }
            
            return isValid;
        }
    </script>
</body>
</html>
```

## Practical Exercises

### 1. Image Gallery
Build interactive gallery:
1. Display thumbnails
2. Show full image on click
3. Add navigation buttons
4. Implement slideshow
5. Add image captions

### 2. Form Validator
Create form checker:
1. Real-time validation
2. Custom error messages
3. Password strength meter
4. Form submission
5. Success feedback

### 3. Interactive Menu
Develop dropdown menu:
1. Toggle submenu
2. Hover effects
3. Click handling
4. Keyboard navigation
5. Mobile support

## Review Questions

1. **JavaScript Basics**
   - What are different data types?
   - How declare variables?
   - When use const vs let?

2. **DOM Manipulation**
   - How select elements?
   - Ways to modify content?
   - Best practices for creation/removal?

3. **Events**
   - Common event types?
   - How handle events?
   - When stop propagation?

## Additional Resources

### Online Tools
- JavaScript playground
- DOM visualizer
- Event debugger

### Further Reading
- JavaScript documentation
- DOM specifications
- Event handling patterns

### Video Resources
- JavaScript tutorials
- DOM manipulation guides
- Event handling examples

## Next Steps

After mastering these concepts, you'll be ready to:
1. Create interactive websites
2. Handle user input
3. Build dynamic interfaces

Remember: JavaScript brings your web pages to life!

## Common Questions and Answers

Q: When use innerHTML vs textContent?
A: Use textContent for plain text, innerHTML when you need to insert HTML.

Q: How handle browser compatibility?
A: Test in multiple browsers and consider using polyfills for older browsers.

Q: Should I use jQuery?
A: Modern JavaScript can do most things jQuery was needed for. Learn vanilla JS first.

## Glossary

- **DOM**: Document Object Model
- **Event**: User or system action
- **Listener**: Event monitor
- **Handler**: Event response
- **Bubbling**: Event propagation
- **Method**: Object function
- **Property**: Object attribute
- **Callback**: Function parameter
- **Promise**: Async operation
- **Scope**: Variable access

Remember: Practice is key to mastering JavaScript!
