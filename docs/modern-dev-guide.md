# Modern Development Guide for Linux Environment

## Table of Contents
1. [Git Version Control](#git-version-control)
2. [Python Development](#python-development)
3. [JavaScript Development](#javascript-development)
4. [Package Management](#package-management)
5. [Testing & Quality Assurance](#testing--quality-assurance)
6. [Debugging Tools & Techniques](#debugging-tools--techniques)
7. [Development Environment Setup](#development-environment-setup)

## Git Version Control

### Essential Git Commands
```bash
git init                  # Initialize a new repository
git clone <url>          # Clone a repository
git add .                # Stage all changes
git commit -m "message"  # Commit changes
git push origin main     # Push to remote
git pull origin main     # Pull from remote
git branch              # List branches
git checkout -b feature  # Create and switch to new branch
git merge feature       # Merge branch into current branch
```

### Git Best Practices
- Write meaningful commit messages
- Use feature branches for new development
- Regular commits with atomic changes
- Pull before pushing to avoid conflicts
- Use .gitignore for project-specific exclusions

### Git Workflow
1. Create feature branch
2. Make changes and test
3. Commit changes with clear messages
4. Pull latest main branch
5. Merge main into feature branch
6. Resolve conflicts if any
7. Push feature branch
8. Create pull request

## Python Development

### Virtual Environments
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Generate requirements file
pip freeze > requirements.txt
```

### Project Structure
```
project/
├── src/
│   └── package/
│       ├── __init__.py
│       └── module.py
├── tests/
│   └── test_module.py
├── docs/
├── requirements.txt
└── setup.py
```

### Code Quality Tools
- pylint: Static code analysis
- black: Code formatting
- mypy: Type checking
- pytest: Testing framework
- coverage: Code coverage

## JavaScript Development

### Node.js and npm
```bash
# Initialize new project
npm init

# Install dependencies
npm install package-name

# Install development dependencies
npm install --save-dev package-name

# Run scripts
npm run script-name
```

### Project Structure
```
project/
├── src/
│   └── components/
├── public/
├── tests/
├── package.json
└── package-lock.json
```

### Essential Tools
- ESLint: Code linting
- Prettier: Code formatting
- Jest: Testing framework
- webpack: Module bundler
- Babel: JavaScript compiler

## Package Management

### Python (pip)
```bash
pip install package-name
pip uninstall package-name
pip list
pip show package-name
pip install --upgrade package-name
```

### Node.js (npm)
```bash
npm install package-name
npm uninstall package-name
npm list
npm outdated
npm update
```

## Testing & Quality Assurance

### Python Testing
```bash
# Run pytest
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_module.py
```

### JavaScript Testing
```bash
# Run Jest tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- path/to/test.js
```

## Debugging Tools & Techniques

### Python Debugging
```python
# Using pdb
import pdb; pdb.set_trace()

# Using breakpoint() (Python 3.7+)
breakpoint()

# Common pdb commands:
# n (next line)
# s (step into)
# c (continue)
# p variable (print variable)
# l (list source)
```

### JavaScript Debugging
```javascript
// Browser debugging
console.log(variable);
console.table(array);
debugger;

// Node.js debugging
node --inspect app.js
node --inspect-brk app.js  // Break on first line
```

## Development Environment Setup

### Essential Tools
```bash
# Version control
sudo apt install git

# Python development
sudo apt install python3 python3-pip python3-venv

# Node.js development
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt install nodejs

# Build tools
sudo apt install build-essential

# Text editor (VS Code)
sudo snap install code --classic
```

### VS Code Extensions
- Python
- ESLint
- Prettier
- GitLens
- Live Server
- Python Test Explorer
- JavaScript Debugger

### Shell Configuration
```bash
# Add to ~/.bashrc or ~/.zshrc
# Python virtual environment
alias venv="python3 -m venv venv"
alias activate="source venv/bin/activate"

# Git shortcuts
alias gs="git status"
alias ga="git add"
alias gc="git commit"
alias gp="git push"
alias gl="git pull"

# npm shortcuts
alias ni="npm install"
alias nr="npm run"
alias nrd="npm run dev"
alias nrt="npm run test"
```

### Environment Variables
```bash
# Add to ~/.bashrc or ~/.zshrc
export PYTHONPATH="${PYTHONPATH}:${HOME}/projects/python"
export NODE_ENV="development"
export PATH="${PATH}:${HOME}/.local/bin"
```

This guide provides a solid foundation for modern development practices in a Linux environment. Remember to regularly update tools and dependencies, and stay informed about security updates and best practices in each ecosystem.
