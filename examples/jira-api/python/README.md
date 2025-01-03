# JIRA API with Python Examples

## Table of Contents
- [JIRA API with Python Examples](#jira-api-with-python-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Operations
   - Authentication and connection
   - Issue CRUD operations
   - Project management
   - User management

2. Advanced Features
   - Custom field handling
   - Workflow automation
   - Bulk operations
   - Attachments handling

3. Integration Features
   - Webhook handling
   - Custom field sync
   - External tool integration
   - Reporting automation

4. Full Applications
   - Issue tracker dashboard
   - Project management tool
   - Reporting system
   - Workflow automator

## Project Structure

```
python/
├── basic/
│   ├── authentication/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── config.py
│   ├── issues/
│   ├── projects/
│   └── users/
├── advanced/
│   ├── workflows/
│   ├── custom_fields/
│   ├── bulk_operations/
│   └── attachments/
├── integration/
│   ├── webhooks/
│   ├── field_sync/
│   ├── external_tools/
│   └── reporting/
└── applications/
    ├── issue_dashboard/
    ├── project_manager/
    ├── report_generator/
    └── workflow_automator/
```

## Getting Started

1. Setup Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Configure JIRA Connection:
```python
# config.py
JIRA_URL = "https://your-domain.atlassian.net"
JIRA_EMAIL = "your-email@example.com"
JIRA_API_TOKEN = "your-api-token"
```

## Basic Operations

### Authentication and Connection
```python
from jira import JIRA
from config import JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN

def get_jira_client():
    """Create authenticated JIRA client"""
    return JIRA(
        server=JIRA_URL,
        basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
    )

def test_connection():
    """Test JIRA connection"""
    jira = get_jira_client()
    try:
        user = jira.current_user()
        print(f"Connected as: {user}")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
```

### Issue Management
```python
class IssueManager:
    def __init__(self):
        self.jira = get_jira_client()
    
    def create_issue(self, project_key, summary, description, issue_type="Task"):
        """Create a new issue"""
        issue_dict = {
            'project': {'key': project_key},
            'summary': summary,
            'description': description,
            'issuetype': {'name': issue_type},
        }
        return self.jira.create_issue(fields=issue_dict)
    
    def update_issue(self, issue_key, fields):
        """Update an existing issue"""
        issue = self.jira.issue(issue_key)
        issue.update(fields=fields)
        return issue
    
    def transition_issue(self, issue_key, transition_name):
        """Move issue through workflow"""
        issue = self.jira.issue(issue_key)
        transitions = self.jira.transitions(issue)
        
        for t in transitions:
            if t['name'].lower() == transition_name.lower():
                self.jira.transition_issue(issue, t['id'])
                return True
        
        raise ValueError(f"Transition '{transition_name}' not found")
```

## Advanced Features

### Custom Field Management
```python
class CustomFieldManager:
    def __init__(self):
        self.jira = get_jira_client()
    
    def get_custom_field_id(self, field_name):
        """Get custom field ID by name"""
        fields = self.jira.fields()
        for field in fields:
            if field['name'] == field_name:
                return field['id']
        return None
    
    def update_custom_field(self, issue_key, field_name, value):
        """Update custom field value"""
        field_id = self.get_custom_field_id(field_name)
        if not field_id:
            raise ValueError(f"Custom field '{field_name}' not found")
        
        return self.jira.issue(issue_key).update(fields={field_id: value})
```

### Workflow Automation
```python
class WorkflowAutomator:
    def __init__(self):
        self.jira = get_jira_client()
    
    def auto_assign_issues(self, project_key, assignee_map):
        """Auto-assign issues based on criteria"""
        jql = f'project = {project_key} AND assignee IS EMPTY'
        issues = self.jira.search_issues(jql)
        
        for issue in issues:
            component = issue.fields.components[0].name if issue.fields.components else None
            if component in assignee_map:
                issue.update(assignee={'name': assignee_map[component]})
    
    def auto_transition_issues(self, project_key, conditions):
        """Auto-transition issues based on conditions"""
        for condition in conditions:
            jql = f'project = {project_key} AND {condition["jql"]}'
            issues = self.jira.search_issues(jql)
            
            for issue in issues:
                try:
                    self.transition_issue(
                        issue.key,
                        condition['transition']
                    )
                except Exception as e:
                    print(f"Failed to transition {issue.key}: {str(e)}")
```

## Security Considerations

1. Token Management:
```python
import os
from cryptography.fernet import Fernet

class TokenManager:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher_suite = Fernet(self.key)
    
    def encrypt_token(self, token):
        """Encrypt API token"""
        return self.cipher_suite.encrypt(token.encode())
    
    def decrypt_token(self, encrypted_token):
        """Decrypt API token"""
        return self.cipher_suite.decrypt(encrypted_token).decode()
```

2. Request Validation:
```python
from functools import wraps
from flask import request, abort

def validate_webhook(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        secret = request.headers.get('X-Atlassian-Token')
        if not secret or secret != 'no-check':
            abort(403)
        return func(*args, **kwargs)
    return wrapper

@app.route('/webhook/jira', methods=['POST'])
@validate_webhook
def handle_webhook():
    event = request.json
    # Process webhook event
    return '', 200
```

## Performance Optimization

1. Batch Processing:
```python
class BatchProcessor:
    def __init__(self):
        self.jira = get_jira_client()
    
    def bulk_create_issues(self, issues, batch_size=50):
        """Create issues in batches"""
        results = []
        for i in range(0, len(issues), batch_size):
            batch = issues[i:i + batch_size]
            results.extend(
                self.jira.create_issues(batch)
            )
        return results
    
    def bulk_update_issues(self, updates, batch_size=50):
        """Update issues in batches"""
        for i in range(0, len(updates), batch_size):
            batch = updates[i:i + batch_size]
            self.jira.bulk_update(batch)
```

2. Caching:
```python
from functools import lru_cache
import time

class CachedJiraClient:
    def __init__(self):
        self.jira = get_jira_client()
    
    @lru_cache(maxsize=100)
    def get_project(self, project_key):
        """Cache project data"""
        return self.jira.project(project_key)
    
    @lru_cache(maxsize=1000)
    def get_issue(self, issue_key):
        """Cache issue data"""
        return self.jira.issue(issue_key)
    
    def clear_cache(self):
        """Clear all caches"""
        self.get_project.cache_clear()
        self.get_issue.cache_clear()
```

## Testing

1. Unit Tests:
```python
import unittest
from unittest.mock import patch

class JiraTests(unittest.TestCase):
    def setUp(self):
        self.jira = get_jira_client()
    
    @patch('jira.JIRA.create_issue')
    def test_create_issue(self, mock_create):
        manager = IssueManager()
        manager.create_issue('TEST', 'Test Issue', 'Description')
        mock_create.assert_called_once()
    
    @patch('jira.JIRA.search_issues')
    def test_search_issues(self, mock_search):
        mock_search.return_value = []
        issues = self.jira.search_issues('project = TEST')
        self.assertEqual(len(issues), 0)
```

2. Integration Tests:
```python
class JiraIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.jira = get_jira_client()
        self.project_key = 'TEST'
    
    def test_issue_workflow(self):
        # Create issue
        issue = self.jira.create_issue(
            project=self.project_key,
            summary='Integration Test',
            issuetype={'name': 'Task'}
        )
        
        # Update issue
        issue.update(description='Updated description')
        
        # Verify changes
        updated = self.jira.issue(issue.key)
        self.assertEqual(
            updated.fields.description,
            'Updated description'
        )
        
        # Clean up
        issue.delete()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
