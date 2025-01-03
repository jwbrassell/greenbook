# Security Best Practices for Network Automation

## Table of Contents
1. [Introduction](#introduction)
2. [Credential Management](#credential-management)
3. [API Security](#api-security)
4. [Network Access Control](#network-access-control)
5. [Secure Communication](#secure-communication)
6. [Audit and Logging](#audit-and-logging)
7. [Error Handling](#error-handling)
8. [Testing and Validation](#testing-and-validation)

## Introduction

Security is paramount in network automation. This guide covers essential security practices to protect your network automation systems and infrastructure.

### Why Security Matters
- Prevent unauthorized access
- Protect sensitive network data
- Maintain network integrity
- Ensure compliance requirements
- Prevent configuration errors

## Credential Management

### Environment Variables
```python
from dotenv import load_dotenv
import os

# Load credentials from environment
load_dotenv()
username = os.getenv('NETWORK_USER')
password = os.getenv('NETWORK_PASSWORD')
```

### Best Practices
1. Never hardcode credentials
2. Use environment variables
3. Implement secure storage solutions
4. Rotate credentials regularly
5. Use separate credentials for automation

### Secure Storage
```python
from cryptography.fernet import Fernet
import base64

def encrypt_credential(credential: str, key: bytes) -> str:
    """Encrypt sensitive credentials."""
    f = Fernet(key)
    return f.encrypt(credential.encode()).decode()

def decrypt_credential(encrypted: str, key: bytes) -> str:
    """Decrypt sensitive credentials."""
    f = Fernet(key)
    return f.decrypt(encrypted.encode()).decode()
```

## API Security

### Authentication
1. Use token-based authentication
2. Implement OAuth 2.0 where possible
3. Use client certificates
4. Enable API key rotation
5. Implement rate limiting

### Example Implementation
```python
import requests
from requests.auth import HTTPBasicAuth

class SecureAPIClient:
    def __init__(self, base_url: str, verify_ssl: bool = True):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.verify = verify_ssl
        
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with API."""
        try:
            response = self.session.post(
                f"{self.base_url}/auth",
                auth=HTTPBasicAuth(username, password)
            )
            return response.ok
        except requests.exceptions.RequestException:
            return False
```

## Network Access Control

### Access Policies
1. Implement least privilege principle
2. Use role-based access control
3. Segment automation networks
4. Control API access
5. Monitor access attempts

### Implementation Example
```python
from typing import List, Dict

class AccessControl:
    def __init__(self):
        self.roles: Dict[str, List[str]] = {
            'readonly': ['GET'],
            'operator': ['GET', 'POST'],
            'admin': ['GET', 'POST', 'PUT', 'DELETE']
        }
    
    def check_permission(self, role: str, method: str) -> bool:
        """Check if role has permission for method."""
        if role not in self.roles:
            return False
        return method in self.roles[role]
```

## Secure Communication

### SSL/TLS Configuration
```python
import ssl
import requests

def create_secure_session():
    """Create secure HTTPS session."""
    session = requests.Session()
    session.verify = True  # Enable SSL verification
    
    # Configure SSL context
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    
    return session
```

### Best Practices
1. Enable SSL/TLS verification
2. Use modern TLS versions
3. Implement certificate validation
4. Handle SSL errors properly
5. Keep SSL libraries updated

## Audit and Logging

### Logging Configuration
```python
import logging
from datetime import datetime

def setup_secure_logging():
    """Configure secure logging."""
    logging.basicConfig(
        filename=f"network_automation_{datetime.now():%Y%m%d}.log",
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Add sensitive data filter
    class SensitiveFilter(logging.Filter):
        def filter(self, record):
            sensitive = ['password', 'token', 'key']
            for item in sensitive:
                if item in record.msg.lower():
                    record.msg = '[REDACTED]'
            return True
    
    logging.getLogger().addFilter(SensitiveFilter())
```

### Audit Trail
1. Log all configuration changes
2. Track access attempts
3. Monitor API usage
4. Record automation actions
5. Implement log rotation

## Error Handling

### Secure Error Handling
```python
class SecureErrorHandler:
    @staticmethod
    def handle_error(error: Exception, context: str = None):
        """Handle errors securely."""
        # Log error without sensitive data
        logging.error(
            f"Error in {context}: {type(error).__name__}",
            exc_info=False
        )
        
        # Return safe error message
        return {
            'error': 'An error occurred',
            'type': type(error).__name__,
            'context': context
        }
```

### Best Practices
1. Never expose internal errors
2. Sanitize error messages
3. Log errors securely
4. Implement proper exception handling
5. Monitor error patterns

## Testing and Validation

### Security Testing
```python
def validate_config(config: dict) -> bool:
    """Validate configuration security."""
    required = ['ssl_verify', 'min_tls_version', 'access_control']
    
    # Check required security settings
    if not all(item in config for item in required):
        return False
    
    # Validate SSL settings
    if not config['ssl_verify']:
        logging.warning('SSL verification disabled')
        return False
    
    return True
```

### Implementation Steps
1. Test in isolated environment
2. Validate configurations
3. Implement security checks
4. Test error handling
5. Perform security audits

## Related Resources
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [Network Security Best Practices](https://www.cisco.com/c/en/us/support/docs/ip/access-lists/13608-21.html)
- [Python Security Guide](https://python-security.readthedocs.io/)
