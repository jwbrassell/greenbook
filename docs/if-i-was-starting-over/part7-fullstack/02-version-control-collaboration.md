# Chapter 2: Version Control and Collaboration

## Introduction

Think about writing a book with multiple authors - you need to track changes, merge different versions, and coordinate work between writers. Similarly, software development requires managing code changes and collaborating with team members. In this chapter, we'll learn how to use Git and work effectively in teams.

## 1. Git Fundamentals

### The Document Versioning Metaphor

Think of Git like a document versioning system:
- Commits like saved versions
- Branches like different drafts
- Merging like combining drafts
- Conflicts like overlapping edits
- History like revision history

### Basic Git Commands

```bash
# Initialize repository
git init

# Check status
git status

# Stage changes
git add file.txt
git add .  # Stage all changes

# Commit changes
git commit -m "Add new feature"

# View history
git log
git log --oneline

# View changes
git diff
git diff file.txt
```

### Branching and Merging

```bash
# Create branch
git branch feature
git checkout feature
# or
git checkout -b feature

# List branches
git branch

# Switch branches
git checkout main

# Merge branch
git merge feature

# Delete branch
git branch -d feature
```

### Hands-On Exercise: Git Workflow

Create a project with Git:
```bash
# Initialize project
mkdir project
cd project
git init

# Create initial files
echo "# Project Title" > README.md
mkdir src
touch src/app.py

# First commit
git add .
git commit -m "Initial commit"

# Create feature branch
git checkout -b feature/login

# Add login feature
cat > src/login.py << EOL
def login(username, password):
    # TODO: Implement login
    pass
EOL

# Commit feature
git add src/login.py
git commit -m "Add login function"

# Update README
cat >> README.md << EOL

## Features
- User login
EOL

git add README.md
git commit -m "Update README with login feature"

# Switch to main
git checkout main

# Create another feature branch
git checkout -b feature/profile

# Add profile feature
cat > src/profile.py << EOL
def get_profile(user_id):
    # TODO: Implement profile
    pass
EOL

# Commit feature
git add src/profile.py
git commit -m "Add profile function"

# Update README
cat >> README.md << EOL
- User profiles
EOL

git add README.md
git commit -m "Update README with profile feature"

# Switch to main and merge features
git checkout main
git merge feature/login
git merge feature/profile  # May cause conflict in README.md

# Resolve conflict if needed
# Edit README.md manually, then:
git add README.md
git commit -m "Merge profile feature and resolve conflicts"
```

## 2. Collaboration Workflows

### The Team Sports Metaphor

Think of collaboration like team sports:
- Repository like playing field
- Branches like different plays
- Pull requests like team reviews
- Code review like coaching
- Issues like game strategy

### GitHub Workflow

```bash
# Clone repository
git clone https://github.com/user/repo.git

# Add remote
git remote add upstream https://github.com/original/repo.git

# Create feature branch
git checkout -b feature/new-feature

# Push branch
git push origin feature/new-feature

# Create pull request (on GitHub)
# After review and approval...

# Update main
git checkout main
git pull upstream main

# Delete feature branch
git branch -d feature/new-feature
```

### Code Review Process

```plaintext
# Pull Request Template
## Description
What does this PR do?

## Changes
- List of changes
- Impact on existing code
- New dependencies

## Testing
- Test cases covered
- How to test

## Screenshots
If applicable

## Checklist
- [ ] Tests added
- [ ] Documentation updated
- [ ] Code follows style guide
- [ ] Reviewed by team member
```

### Hands-On Exercise: Team Workflow

Create a collaborative project:
```bash
# Team Lead: Create repository
mkdir team-project
cd team-project
git init

# Create project structure
mkdir src tests docs
touch src/__init__.py
touch src/app.py
touch tests/__init__.py
touch docs/README.md

# Create development guidelines
cat > CONTRIBUTING.md << EOL
# Contributing Guidelines

## Branching Strategy
- main: Production code
- develop: Development code
- feature/*: New features
- bugfix/*: Bug fixes

## Pull Request Process
1. Create feature branch
2. Write tests
3. Update documentation
4. Submit PR
5. Code review
6. Merge

## Code Style
- Follow PEP 8
- Write docstrings
- Add comments
EOL

# Initial commit
git add .
git commit -m "Initial project setup"

# Create develop branch
git checkout -b develop

# Push to remote
git remote add origin https://github.com/team/project.git
git push -u origin main
git push -u origin develop

# Team Member: Clone and work
git clone https://github.com/team/project.git
cd project
git checkout develop
git checkout -b feature/user-auth

# Add feature code
cat > src/auth.py << EOL
class Auth:
    def __init__(self):
        self.users = {}
    
    def register(self, username, password):
        if username in self.users:
            raise ValueError("User exists")
        self.users[username] = password
    
    def login(self, username, password):
        if username not in self.users:
            return False
        return self.users[username] == password
EOL

# Add tests
cat > tests/test_auth.py << EOL
import unittest
from src.auth import Auth

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.auth = Auth()
    
    def test_register(self):
        self.auth.register("user1", "pass123")
        self.assertIn("user1", self.auth.users)
    
    def test_login(self):
        self.auth.register("user1", "pass123")
        self.assertTrue(self.auth.login("user1", "pass123"))
        self.assertFalse(self.auth.login("user1", "wrong"))
EOL

# Commit changes
git add src/auth.py tests/test_auth.py
git commit -m "Add user authentication"

# Push and create PR
git push origin feature/user-auth

# Team Lead: Review and merge
git checkout develop
git pull origin feature/user-auth
# Review code, run tests
git merge feature/user-auth
git push origin develop
```

## 3. Project Management

### The Construction Project Metaphor

Think of project management like construction:
- Issues like building plans
- Milestones like construction phases
- Projects like building sites
- Labels like material types
- Assignments like work crews

### Issue Management

```markdown
# Issue Template
## Problem
Describe the problem

## Expected Behavior
What should happen

## Current Behavior
What happens instead

## Steps to Reproduce
1. Step one
2. Step two
3. Step three

## Environment
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 90]
- Version: [e.g. 1.2.3]

## Additional Context
Any other information
```

### Project Planning

```markdown
# Sprint Planning

## Goals
- Implement user authentication
- Add profile management
- Create admin dashboard

## Tasks
1. User Authentication
   - [ ] Login form
   - [ ] Registration
   - [ ] Password reset
   - [ ] Email verification

2. Profile Management
   - [ ] View profile
   - [ ] Edit profile
   - [ ] Upload avatar
   - [ ] Privacy settings

3. Admin Dashboard
   - [ ] User list
   - [ ] User management
   - [ ] Activity logs
   - [ ] System settings

## Timeline
Week 1-2: Authentication
Week 3-4: Profiles
Week 5-6: Admin features

## Team Assignments
- Alice: Authentication
- Bob: Profiles
- Charlie: Admin
- Dave: Testing
```

### Hands-On Exercise: Project Setup

Create project management system:
```bash
# Create project structure
mkdir project-management
cd project-management

# Create documentation
mkdir .github docs issues

# Create issue templates
cat > .github/ISSUE_TEMPLATE/bug_report.md << EOL
---
name: Bug Report
about: Create a report to help us improve
---

## Description
A clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. See error

## Expected Behavior
What should happen

## Screenshots
If applicable

## Environment
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome]
- Version: [e.g. 22]

## Additional Context
Add any other context about the problem
EOL

cat > .github/ISSUE_TEMPLATE/feature_request.md << EOL
---
name: Feature Request
about: Suggest an idea for this project
---

## Problem
A clear description of the problem

## Proposed Solution
A clear description of what you want to happen

## Alternatives Considered
A clear description of any alternative solutions

## Additional Context
Add any other context or screenshots
EOL

# Create pull request template
cat > .github/pull_request_template.md << EOL
## Description
Please include a summary of the change

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## How Has This Been Tested?
Please describe the tests you ran

## Checklist
- [ ] My code follows style guidelines
- [ ] I have added tests
- [ ] I have updated documentation
- [ ] I have reviewed my own code
EOL

# Create project documentation
cat > docs/README.md << EOL
# Project Documentation

## Getting Started
Instructions for setting up the project

## Development
Guidelines for development

## Testing
How to run tests

## Deployment
Deployment procedures

## Contributing
How to contribute
EOL

# Create development guidelines
cat > docs/CONTRIBUTING.md << EOL
# Contributing Guidelines

## Code Style
- Follow language style guide
- Write clear comments
- Add documentation

## Branching
- main: Production
- develop: Development
- feature/*: Features
- bugfix/*: Bug fixes

## Pull Requests
1. Create feature branch
2. Write tests
3. Update docs
4. Submit PR
5. Code review

## Issues
- Use templates
- Add labels
- Assign owners
EOL

# Initialize git
git init
git add .
git commit -m "Setup project management"

# Create project board (on GitHub)
# Set up columns:
# - To Do
# - In Progress
# - Review
# - Done

# Create labels
# - bug: Bug fixes
# - feature: New features
# - docs: Documentation
# - test: Testing
# - priority: High priority
```

## Practical Exercises

### 1. Git Practice
Work with repository:
1. Create branches
2. Merge changes
3. Resolve conflicts
4. Review history
5. Revert changes

### 2. Team Workflow
Practice collaboration:
1. Clone repository
2. Create features
3. Submit PRs
4. Review code
5. Merge changes

### 3. Project Setup
Create management:
1. Issue templates
2. PR templates
3. Project boards
4. Documentation
5. Guidelines

## Review Questions

1. **Git Basics**
   - How handle branches?
   - When create commits?
   - Best practices for messages?

2. **Collaboration**
   - How review code?
   - When merge changes?
   - Best practices for PRs?

3. **Management**
   - How track issues?
   - When create milestones?
   - Best practices for planning?

## Additional Resources

### Online Tools
- Git visualizers
- PR reviewers
- Project boards

### Further Reading
- Git documentation
- Collaboration guides
- Management strategies

### Video Resources
- Git tutorials
- Team workflows
- Project planning

## Next Steps

After mastering these concepts, you'll be ready to:
1. Manage code changes
2. Collaborate with teams
3. Plan projects

Remember: Good version control makes collaboration easier!

## Common Questions and Answers

Q: When should I create a branch?
A: Create branches for new features, bug fixes, or experiments.

Q: How detailed should commit messages be?
A: Include what changes were made and why they were needed.

Q: How often should I commit?
A: Commit when you complete a logical unit of work.

## Glossary

- **Repository**: Code storage
- **Branch**: Code version
- **Commit**: Save point
- **Merge**: Combine changes
- **Pull Request**: Change review
- **Issue**: Task/bug tracking
- **Milestone**: Goal marker
- **Project**: Work organization
- **Label**: Category marker
- **Assignment**: Task owner

Remember: Version control is essential for team development!
