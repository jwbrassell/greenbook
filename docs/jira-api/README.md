# Jira API Documentation

## Table of Contents
- [Jira API Documentation](#jira-api-documentation)
  - [Table of Contents](#table-of-contents)
  - [Authentication](#authentication)
- [Using API Token](#using-api-token)
  - [Required Permissions](#required-permissions)
  - [Issue Types](#issue-types)
  - [Core API Endpoints](#core-api-endpoints)
    - [Get Issue Details](#get-issue-details)
    - [Create Issue](#create-issue)
    - [Search Issues](#search-issues)
    - [Update Issue](#update-issue)
    - [Get Project Information](#get-project-information)
  - [Python Example](#python-example)
- [Configuration](#configuration)
  - [Common JQL Examples](#common-jql-examples)
  - [Rate Limits](#rate-limits)
  - [Best Practices](#best-practices)



This guide covers essential Jira API functionality for working with issues and projects.

## Authentication

Jira API requires authentication using one of these methods:

1. **Basic Authentication** (username/password)
2. **API Token** (recommended)
   - Generate from: Jira Settings > Security > API Token
   - More secure than password auth
   - Can be revoked individually
3. **OAuth 2.0** (for applications)

Example authentication header:
```bash
# Using API Token
curl -H "Authorization: Bearer YOUR_API_TOKEN" \
     -H "Content-Type: application/json" \
     https://your-domain.atlassian.net/rest/api/3/issue/PROJ-123
```

## Required Permissions

To work with issues, you need these permissions:

| Operation | Required Permission |
|-----------|-------------------|
| View Issues | Browse Projects |
| Create Issues | Create Issues |
| Edit Issues | Edit Issues |
| Delete Issues | Delete Issues |
| Transition Issues | Transition Issues |

These permissions are typically managed through:
- Project Roles
- Groups
- Permission Schemes

## Issue Types

Common issue types and their typical icons:

| Type | Icon | Description |
|------|------|-------------|
| Story | 📗 | User story or feature request |
| Bug | 🐞 | Software defect |
| Task | ✅ | General task |
| Epic | 🌟 | Large body of work |
| Subtask | ↳ | Component of a parent issue |

Note: Actual icons may vary based on your Jira instance theme.

## Core API Endpoints

### Get Issue Details
```bash
GET /rest/api/3/issue/{issueIdOrKey}
```

### Create Issue
```bash
POST /rest/api/3/issue
Content-Type: application/json

{
  "fields": {
    "project": {
      "key": "PROJ"
    },
    "summary": "Issue summary",
    "description": {
      "type": "doc",
      "version": 1,
      "content": [
        {
          "type": "paragraph",
          "content": [
            {
              "text": "Issue description",
              "type": "text"
            }
          ]
        }
      ]
    },
    "issuetype": {
      "name": "Task"
    }
  }
}
```

### Search Issues
```bash
GET /rest/api/3/search?jql=project=PROJ AND status="To Do"
```

### Update Issue
```bash
PUT /rest/api/3/issue/{issueIdOrKey}
Content-Type: application/json

{
  "fields": {
    "summary": "Updated summary"
  }
}
```

### Get Project Information
```bash
GET /rest/api/3/project/{projectIdOrKey}
```

## Python Example

```python
import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration
url = "https://your-domain.atlassian.net"
email = "your-email@example.com"
api_token = "your-api-token"
auth = HTTPBasicAuth(email, api_token)

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json"
}

def get_issue(issue_key):
    """Fetch issue details"""
    response = requests.get(
        f"{url}/rest/api/3/issue/{issue_key}",
        auth=auth,
        headers=headers
    )
    return response.json()

def create_issue(project_key, summary, description, issue_type="Task"):
    """Create a new issue"""
    payload = {
        "fields": {
            "project": {
                "key": project_key
            },
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {
                                "text": description,
                                "type": "text"
                            }
                        ]
                    }
                ]
            },
            "issuetype": {
                "name": issue_type
            }
        }
    }
    
    response = requests.post(
        f"{url}/rest/api/3/issue",
        auth=auth,
        headers=headers,
        data=json.dumps(payload)
    )
    return response.json()

def search_issues(jql):
    """Search issues using JQL"""
    response = requests.get(
        f"{url}/rest/api/3/search",
        auth=auth,
        headers=headers,
        params={'jql': jql}
    )
    return response.json()
```

## Common JQL Examples

JQL (Jira Query Language) is used for searching issues:

```sql
-- All open issues in a project
project = "PROJ" AND status != Done

-- Issues assigned to current user
assignee = currentUser() AND status = "In Progress"

-- Recently updated issues
project = "PROJ" AND updated >= -7d

-- High priority bugs
project = "PROJ" AND issuetype = Bug AND priority = High

-- Issues in multiple projects
project in ("PROJ1", "PROJ2") AND status = "To Do"
```

## Rate Limits

- Basic plans: 50 requests per minute
- Premium plans: Higher limits available
- Consider implementing retry logic with exponential backoff
- Monitor `X-RateLimit-*` headers in responses

## Best Practices

1. Always use API tokens instead of passwords
2. Cache responses when possible to avoid rate limits
3. Use bulk operations when available
4. Include error handling for API responses
5. Monitor API usage through response headers
6. Use appropriate issue types for different work items
7. Leverage JQL for efficient searching
