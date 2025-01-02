"""
Basic Jira API operations example.
Demonstrates common tasks like creating and updating issues.
"""

import requests
from requests.auth import HTTPBasicAuth
import json
from typing import Dict, List, Optional
import logging
from time import sleep

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JiraAPI:
    def __init__(self, domain: str, email: str, api_token: str):
        """
        Initialize Jira API client
        
        Args:
            domain: Your Jira domain (e.g., 'your-domain.atlassian.net')
            email: Your Atlassian account email
            api_token: API token generated from Atlassian account settings
        """
        self.base_url = f"https://{domain}"
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
    def _handle_rate_limit(self, response: requests.Response) -> None:
        """Handle rate limiting with exponential backoff"""
        if response.status_code == 429:  # Too Many Requests
            retry_after = int(response.headers.get('Retry-After', 60))
            logger.warning(f"Rate limited. Waiting {retry_after} seconds")
            sleep(retry_after)
            
    def _make_request(self, method: str, endpoint: str, **kwargs) -> Dict:
        """Make HTTP request with retry logic"""
        url = f"{self.base_url}/rest/api/3/{endpoint.lstrip('/')}"
        
        for attempt in range(3):
            try:
                response = requests.request(
                    method,
                    url,
                    auth=self.auth,
                    headers=self.headers,
                    **kwargs
                )
                
                self._handle_rate_limit(response)
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                if attempt == 2:  # Last attempt
                    raise
                logger.warning(f"Request failed: {e}. Retrying...")
                sleep(2 ** attempt)  # Exponential backoff
    
    def get_issue(self, issue_key: str) -> Dict:
        """
        Get issue details
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            
        Returns:
            Dict containing issue details
        """
        return self._make_request('GET', f'issue/{issue_key}')
    
    def create_issue(
        self,
        project_key: str,
        summary: str,
        description: str,
        issue_type: str = "Task"
    ) -> Dict:
        """
        Create a new issue
        
        Args:
            project_key: Project key (e.g., 'PROJ')
            summary: Issue summary
            description: Issue description
            issue_type: Type of issue (e.g., 'Task', 'Bug', 'Story')
            
        Returns:
            Dict containing created issue details
        """
        payload = {
            "fields": {
                "project": {"key": project_key},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"text": description, "type": "text"}]
                        }
                    ]
                },
                "issuetype": {"name": issue_type}
            }
        }
        
        return self._make_request('POST', 'issue', json=payload)
    
    def update_issue(self, issue_key: str, fields: Dict) -> None:
        """
        Update issue fields
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            fields: Dict of fields to update
        """
        payload = {"fields": fields}
        self._make_request('PUT', f'issue/{issue_key}', json=payload)
    
    def search_issues(
        self,
        jql: str,
        max_results: int = 50,
        start_at: int = 0
    ) -> Dict:
        """
        Search issues using JQL
        
        Args:
            jql: JQL query string
            max_results: Maximum number of results to return
            start_at: Index of first result
            
        Returns:
            Dict containing search results
        """
        params = {
            'jql': jql,
            'maxResults': max_results,
            'startAt': start_at
        }
        return self._make_request('GET', 'search', params=params)
    
    def assign_issue(self, issue_key: str, assignee: str) -> None:
        """
        Assign issue to user
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            assignee: Username or email of assignee
        """
        payload = {
            "fields": {
                "assignee": {"name": assignee}
            }
        }
        self._make_request('PUT', f'issue/{issue_key}', json=payload)
    
    def add_comment(self, issue_key: str, comment: str) -> Dict:
        """
        Add comment to issue
        
        Args:
            issue_key: Issue key (e.g., 'PROJ-123')
            comment: Comment text
            
        Returns:
            Dict containing created comment details
        """
        payload = {
            "body": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [{"text": comment, "type": "text"}]
                    }
                ]
            }
        }
        return self._make_request('POST', f'issue/{issue_key}/comment', json=payload)

# Example usage
if __name__ == "__main__":
    # Initialize client
    jira = JiraAPI(
        domain="your-domain.atlassian.net",
        email="your-email@example.com",
        api_token="your-api-token"
    )
    
    try:
        # Create an issue
        new_issue = jira.create_issue(
            project_key="PROJ",
            summary="Test issue from API",
            description="This is a test issue created via the Jira API",
            issue_type="Task"
        )
        issue_key = new_issue['key']
        logger.info(f"Created issue: {issue_key}")
        
        # Add a comment
        jira.add_comment(issue_key, "Adding a test comment")
        logger.info("Added comment")
        
        # Assign the issue
        jira.assign_issue(issue_key, "john.doe@example.com")
        logger.info("Assigned issue")
        
        # Search for issues
        results = jira.search_issues('project = PROJ AND created >= -1d')
        logger.info(f"Found {len(results['issues'])} recent issues")
        
    except Exception as e:
        logger.error(f"Error: {e}")
