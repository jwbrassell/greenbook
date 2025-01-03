# Chapter 1: Full-Stack Development

## Introduction

Think about building a house - you need architects to design the structure, builders for the foundation and walls, electricians for wiring, and interior designers for the finishing touches. Similarly, full-stack development requires combining different layers of technology to create complete applications. In this chapter, we'll learn how to bring together frontend and backend development.

## 1. Architecture Planning

### The Building Construction Metaphor

Think of system architecture like building a house:
- Frontend like interior design
- Backend like structural framework
- Database like foundation
- APIs like utilities (plumbing/electrical)
- Authentication like security system

### System Design

```plaintext
# Basic Architecture
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|    Frontend    | --> |      API      | --> |    Backend    |
|    (React)     |     |    (Flask)    |     |  (Database)   |
|                | <-- |                | <-- |                |
+----------------+     +----------------+     +----------------+

# Component Structure
Frontend/
├── src/
│   ├── components/    # UI components
│   ├── services/     # API calls
│   ├── store/        # State management
│   └── utils/        # Helper functions
└── public/           # Static assets

Backend/
├── app/
│   ├── models/       # Database models
│   ├── routes/       # API endpoints
│   ├── services/     # Business logic
│   └── utils/        # Helper functions
└── config/           # Configuration files
```

### Data Flow

```javascript
// Frontend API service
class ApiService {
    async getItems() {
        const response = await fetch('/api/items');
        return response.json();
    }
    
    async createItem(data) {
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        return response.json();
    }
}

// Backend API route
@app.route('/api/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = Item(**data)
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict())
```

### Hands-On Exercise: Task Manager

Create a full-stack task manager:

```python
# backend/app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')
    if status:
        tasks = Task.query.filter_by(status=status).all()
    else:
        tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict())

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    if 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=datetime.fromisoformat(data['due_date']) 
            if 'due_date' in data else None,
        status=data.get('status', 'pending')
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'due_date' in data:
        task.due_date = datetime.fromisoformat(data['due_date'])
    if 'status' in data:
        task.status = data['status']
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
```

```html
<!-- frontend/index.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Task Manager</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 800px;
            margin: 0 auto;
        }

        .task-form {
            margin-bottom: 20px;
            padding: 20px;
            background-color: #f5f5f5;
            border-radius: 4px;
        }

        .form-group {
            margin-bottom: 15px;
        }

        label {
            display: block;
            margin-bottom: 5px;
        }

        input, textarea, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }

        button {
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }

        button:hover {
            background-color: #45a049;
        }

        .task-list {
            list-style: none;
            padding: 0;
        }

        .task-item {
            padding: 15px;
            margin-bottom: 10px;
            background-color: white;
            border: 1px solid #ddd;
            border-radius: 4px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .task-item.completed {
            background-color: #f9f9f9;
            opacity: 0.7;
        }

        .task-meta {
            font-size: 0.9em;
            color: #666;
        }

        .filters {
            margin-bottom: 20px;
        }

        .error {
            color: #d32f2f;
            margin-bottom: 10px;
        }

        .success {
            color: #388e3c;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Task Manager</h1>
        
        <div class="task-form">
            <h2>Add New Task</h2>
            <form id="task-form">
                <div class="form-group">
                    <label for="title">Title:</label>
                    <input type="text" id="title" required>
                </div>
                
                <div class="form-group">
                    <label for="description">Description:</label>
                    <textarea id="description" rows="3"></textarea>
                </div>
                
                <div class="form-group">
                    <label for="due-date">Due Date:</label>
                    <input type="datetime-local" id="due-date">
                </div>
                
                <button type="submit">Add Task</button>
            </form>
        </div>

        <div class="filters">
            <label>Filter by status:</label>
            <select id="status-filter">
                <option value="">All</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
            </select>
        </div>

        <div id="message"></div>
        
        <ul class="task-list" id="task-list"></ul>
    </div>

    <script>
        // API service
        class TaskApi {
            constructor(baseUrl) {
                this.baseUrl = baseUrl;
            }
            
            async getTasks(status = '') {
                const url = status 
                    ? `${this.baseUrl}/tasks?status=${status}`
                    : `${this.baseUrl}/tasks`;
                const response = await fetch(url);
                return response.json();
            }
            
            async createTask(task) {
                const response = await fetch(`${this.baseUrl}/tasks`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(task)
                });
                return response.json();
            }
            
            async updateTask(id, updates) {
                const response = await fetch(`${this.baseUrl}/tasks/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(updates)
                });
                return response.json();
            }
            
            async deleteTask(id) {
                await fetch(`${this.baseUrl}/tasks/${id}`, {
                    method: 'DELETE'
                });
            }
        }

        // App
        class TaskManager {
            constructor() {
                this.api = new TaskApi('http://localhost:5000/api');
                this.taskForm = document.getElementById('task-form');
                this.taskList = document.getElementById('task-list');
                this.statusFilter = document.getElementById('status-filter');
                this.messageDiv = document.getElementById('message');
                
                this.setupEventListeners();
                this.loadTasks();
            }
            
            setupEventListeners() {
                this.taskForm.addEventListener('submit', (e) => {
                    e.preventDefault();
                    this.handleSubmit();
                });
                
                this.statusFilter.addEventListener('change', () => {
                    this.loadTasks();
                });
            }
            
            async loadTasks() {
                try {
                    const status = this.statusFilter.value;
                    const tasks = await this.api.getTasks(status);
                    this.renderTasks(tasks);
                } catch (error) {
                    this.showMessage('Error loading tasks', 'error');
                }
            }
            
            async handleSubmit() {
                try {
                    const task = {
                        title: document.getElementById('title').value,
                        description: document.getElementById('description').value,
                        due_date: document.getElementById('due-date').value
                    };
                    
                    await this.api.createTask(task);
                    this.taskForm.reset();
                    this.showMessage('Task created successfully', 'success');
                    this.loadTasks();
                } catch (error) {
                    this.showMessage('Error creating task', 'error');
                }
            }
            
            async handleStatusChange(id, status) {
                try {
                    await this.api.updateTask(id, { status });
                    this.loadTasks();
                } catch (error) {
                    this.showMessage('Error updating task', 'error');
                }
            }
            
            async handleDelete(id) {
                if (confirm('Are you sure you want to delete this task?')) {
                    try {
                        await this.api.deleteTask(id);
                        this.loadTasks();
                        this.showMessage('Task deleted successfully', 'success');
                    } catch (error) {
                        this.showMessage('Error deleting task', 'error');
                    }
                }
            }
            
            renderTasks(tasks) {
                this.taskList.innerHTML = tasks.map(task => `
                    <li class="task-item ${task.status === 'completed' ? 'completed' : ''}">
                        <div>
                            <h3>${task.title}</h3>
                            <p>${task.description || ''}</p>
                            <div class="task-meta">
                                ${task.due_date ? `Due: ${new Date(task.due_date).toLocaleString()}` : ''}
                            </div>
                        </div>
                        <div>
                            <select onchange="app.handleStatusChange(${task.id}, this.value)">
                                <option value="pending" ${task.status === 'pending' ? 'selected' : ''}>
                                    Pending
                                </option>
                                <option value="in_progress" ${task.status === 'in_progress' ? 'selected' : ''}>
                                    In Progress
                                </option>
                                <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>
                                    Completed
                                </option>
                            </select>
                            <button onclick="app.handleDelete(${task.id})">Delete</button>
                        </div>
                    </li>
                `).join('');
            }
            
            showMessage(text, type) {
                this.messageDiv.textContent = text;
                this.messageDiv.className = type;
                setTimeout(() => {
                    this.messageDiv.textContent = '';
                    this.messageDiv.className = '';
                }, 3000);
            }
        }

        // Initialize app
        const app = new TaskManager();
    </script>
</body>
</html>
```

## 2. Frontend-Backend Integration

### The Restaurant Service Metaphor

Think of integration like restaurant service:
- Frontend like waiters
- Backend like kitchen
- API like order tickets
- State like order status
- Errors like service issues

### API Integration

```javascript
// API service class
class ApiService {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
    }
    
    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        try {
            const response = await fetch(url, { ...options, headers });
            
            if (!response.ok) {
                throw new Error(`API error: ${response.status}`);
            }
            
            return response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    // CRUD operations
    async get(endpoint) {
        return this.request(endpoint);
    }
    
    async post(endpoint, data) {
        return this.request(endpoint, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async put(endpoint, data) {
        return this.request(endpoint, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async delete(endpoint) {
        return this.request(endpoint, {
            method: 'DELETE'
        });
    }
}

// State management
class Store {
    constructor() {
        this.state = {
            items: [],
            loading: false,
            error: null
        };
        this.listeners = [];
    }
    
    subscribe(listener) {
        this.listeners.push(listener);
        return () => {
            this.listeners = this.listeners.filter(l => l !== listener);
        };
    }
    
    setState(updates) {
        this.state = { ...this.state, ...updates };
        this.listeners.forEach(listener => listener(this.state));
    }
    
    getState() {
        return this.state;
    }
}

// Application class
class App {
    constructor() {
        this.api = new ApiService('http://localhost:5000/api');
        this.store = new Store();
        
        // Subscribe to state changes
        this.store.subscribe(state => {
            this.render(state);
        });
    }
    
    async loadItems() {
        this.store.setState({ loading: true });
        
        try {
            const items = await this.api.get('/items');
            this.store.setState({ items, loading: false });
        } catch (error) {
            this.store.setState({ error, loading: false });
        }
    }
    
    render(state) {
        if (state.loading) {
            this.showLoading();
        } else if (state.error) {
            this.showError(state.error);
        } else {
            this.showItems(state.items);
        }
    }
}
```

### Error Handling

```javascript
// Frontend error handling
class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.status = status;
    }
}

async function handleApiRequest(request) {
    try {
        const response = await request();
        
        if (!response.ok) {
            throw new ApiError('API request failed', response.status);
        }
        
        return response.json();
    } catch (error) {
        if (error instanceof ApiError) {
            // Handle specific API errors
            switch (error.status) {
                case 401:
                    redirectToLogin();
                    break;
                case 403:
                    showPermissionError();
                    break;
                case 404:
                    showNotFound();
                    break;
                default:
                    showError('API request failed');
            }
        } else {
            // Handle network/other errors
            showError('Network error');
        }
        throw error;
    }
}

// Backend error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'error': 'Bad request',
        'message': str(error)
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not found',
        'message': 'Resource not found'
    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
        'error': 'Server error',
        'message': 'Internal server error'
    }), 500
```

## 3. Feature Implementation

### The Recipe Creation Metaphor

Think of feature implementation like creating a recipe:
- Planning like ingredients list
- Development like cooking steps
- Testing like tasting
- Deployment like serving
- Maintenance like adjusting recipe

### Feature Planning

```plaintext
Feature: User Registration

User Story:
As a new user
I want to create an account
So that I can access the application

Acceptance Criteria:
1. User can enter email and password
2. Password must meet security requirements
3. Email must be unique
4. User receives confirmation email
5. User can verify email address

Technical Requirements:
1. Frontend form validation
2. Backend email validation
3. Secure password hashing
4. Email service integration
5. Database storage
```

### Implementation Example

```python
# Backend implementation
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_verified = db.Column(db.Boolean, default=False)
    verification_token = db.Column(db.String(100))

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Validate input
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password required'}), 400
    
    # Check existing user
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        verification_token=generate_token()
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Send verification email
    send_verification_email(user)
    
    return jsonify({'message': 'Registration successful'}), 201
```

```javascript
// Frontend implementation
class RegistrationForm {
    constructor(formElement) {
        this.form = formElement;
        this.setupValidation();
    }
    
    setupValidation() {
        this.form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            if (this.validateForm()) {
                await this.submitForm();
            }
        });
    }
    
    validateForm() {
        const email = this.form.email.value;
        const password = this.form.password.value;
        
        // Clear previous errors
        this.clearErrors();
        
        let isValid = true;
        
        // Validate email
        if (!this.isValidEmail(email)) {
            this.showError('email', 'Invalid email address');
            isValid = false;
        }
        
        // Validate password
        if (!this.isValidPassword(password)) {
            this.showError('password', 'Password must be at least 8 characters');
            isValid = false;
        }
        
        return isValid;
    }
    
    async submitForm() {
        try {
            const response = await fetch('/api/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: this.form.email.value,
                    password: this.form.password.value
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showSuccess('Registration successful! Please check your email.');
                this.form.reset();
            } else {
                this.showError('form', data.error);
            }
        } catch (error) {
            this.showError('form', 'Registration failed. Please try again.');
        }
    }
}
```

## Practical Exercises

### 1. User Management
Build complete system:
1. Registration/login
2. Profile management
3. Password reset
4. Email verification
5. Admin dashboard

### 2. Content Management
Create CMS with:
1. Content creation
2. Media uploads
3. Categories/tags
4. Search/filter
5. User permissions

### 3. E-commerce Features
Implement store with:
1. Product catalog
2. Shopping cart
3. Checkout process
4. Order management
5. Payment integration

## Review Questions

1. **Architecture**
   - How plan system design?
   - When use different patterns?
   - Best practices for structure?

2. **Integration**
   - How handle API calls?
   - When use state management?
   - Best practices for errors?

3. **Features**
   - How plan implementation?
   - When write tests?
   - Best practices for deployment?

## Additional Resources

### Online Tools
- System design tools
- API testing tools
- Project management tools

### Further Reading
- Architecture patterns
- Integration strategies
- Feature planning

### Video Resources
- System design tutorials
- Integration guides
- Feature implementation

## Next Steps

After mastering these concepts, you'll be ready to:
1. Design complete systems
2. Implement full features
3. Deploy applications

Remember: Good architecture makes development easier!

## Common Questions and Answers

Q: How do I structure a large application?
A: Use modular architecture with clear separation of concerns.

Q: When should I use state management?
A: When multiple components need to share data or state becomes complex.

Q: How do I handle API errors?
A: Implement consistent error handling at both frontend and backend.

## Glossary

- **Architecture**: System design
- **Integration**: Component connection
- **Feature**: User functionality
- **State**: Application data
- **API**: Interface contract
- **Frontend**: User interface
- **Backend**: Server logic
- **Database**: Data storage
- **Testing**: Verification
- **Deployment**: Release process

Remember: Full-stack development requires understanding all layers of an application!
