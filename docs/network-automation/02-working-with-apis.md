# Working with Network APIs

## Table of Contents
1. [Introduction](#introduction)
2. [API Basics](#api-basics)
3. [Authentication Methods](#authentication-methods)
4. [Common Operations](#common-operations)
5. [Error Handling](#error-handling)
6. [Best Practices](#best-practices)
7. [Examples](#examples)
8. [Troubleshooting](#troubleshooting)

## Introduction
Network APIs (Application Programming Interfaces) allow programmatic interaction with network devices and services. This guide covers how to effectively work with various network APIs, including REST, NETCONF, and vendor-specific APIs.

### Why Use APIs?
- Programmatic device configuration
- Automated data collection
- Integration with other systems
- Scalable network management
- Real-time monitoring

## API Basics

### REST API Fundamentals
```python
import requests
from requests.auth import HTTPBasicAuth
import json

def api_request(method, url, auth=None, data=None, verify=False):
    """
    Make an API request to a network device.
    
    Args:
        method (str): HTTP method (GET, POST, PUT, DELETE)
        url (str): API endpoint URL
        auth (tuple): Username and password tuple
        data (dict): Data to send with request
        verify (bool): Verify SSL certificate
    
    Returns:
        dict: Response data
    """
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        if auth:
            auth = HTTPBasicAuth(*auth)
        
        response = requests.request(
            method=method,
            url=url,
            auth=auth,
            headers=headers,
            data=json.dumps(data) if data else None,
            verify=verify
        )
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        return None
```

## Authentication Methods

### Basic Authentication
```python
# Using username and password
auth = ('admin', 'password')
result = api_request('GET', 'https://device/api/v1/interfaces', auth=auth)
```

### Token Authentication
```python
def get_auth_token(url, username, password):
    """Get authentication token from API."""
    auth_data = {
        'username': username,
        'password': password
    }
    
    response = requests.post(
        f"{url}/auth/token",
        json=auth_data,
        verify=False
    )
    
    if response.ok:
        return response.json()['token']
    return None

# Using token authentication
token = get_auth_token('https://device/api', 'admin', 'password')
headers = {'Authorization': f'Bearer {token}'}
```

## Common Operations

### Device Information
```python
def get_device_info(device_ip, auth):
    """Retrieve basic device information."""
    url = f"https://{device_ip}/api/v1/system"
    return api_request('GET', url, auth=auth)

def get_interfaces(device_ip, auth):
    """Get all interface information."""
    url = f"https://{device_ip}/api/v1/interfaces"
    return api_request('GET', url, auth=auth)
```

### Configuration Management
```python
def update_interface(device_ip, auth, interface_name, config):
    """Update interface configuration."""
    url = f"https://{device_ip}/api/v1/interfaces/{interface_name}"
    return api_request('PUT', url, auth=auth, data=config)

def backup_config(device_ip, auth):
    """Backup device configuration."""
    url = f"https://{device_ip}/api/v1/config/backup"
    return api_request('POST', url, auth=auth)
```

## Error Handling
```python
def safe_api_call(func):
    """Decorator for safe API calls with error handling."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            if result is None:
                raise Exception("API call returned None")
            return result
        except requests.exceptions.ConnectionError:
            print("Failed to connect to device")
        except requests.exceptions.Timeout:
            print("Request timed out")
        except requests.exceptions.RequestException as e:
            print(f"API error: {str(e)}")
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
        return None
    return wrapper

@safe_api_call
def get_system_status(device_ip, auth):
    """Get system status with error handling."""
    url = f"https://{device_ip}/api/v1/system/status"
    return api_request('GET', url, auth=auth)
```

## Best Practices

### Security
1. Use HTTPS whenever possible
2. Implement proper authentication
3. Validate SSL certificates in production
4. Secure credential storage
5. Implement rate limiting

### Performance
1. Use connection pooling
2. Implement caching where appropriate
3. Handle pagination for large datasets
4. Use async operations for bulk requests
5. Optimize payload size

### Code Organization
1. Create reusable functions
2. Implement proper error handling
3. Use meaningful variable names
4. Document your code
5. Follow API versioning

## Examples

### Network Inventory
```python
def get_network_inventory(devices, auth):
    """Collect inventory from multiple devices."""
    inventory = []
    
    for device in devices:
        device_info = get_device_info(device, auth)
        if device_info:
            inventory.append({
                'device': device,
                'info': device_info
            })
    
    return inventory
```

### Bulk Configuration
```python
def bulk_interface_update(devices, auth, config):
    """Update configuration on multiple devices."""
    results = []
    
    for device in devices:
        result = update_interface(device, auth, config)
        results.append({
            'device': device,
            'status': 'success' if result else 'failed'
        })
    
    return results
```

## Troubleshooting

### Common Issues
1. Authentication failures
2. SSL certificate errors
3. Rate limiting
4. Timeout issues
5. Data format mismatches

### Debugging Tips
1. Enable debug logging
2. Use API documentation
3. Test with Postman
4. Check network connectivity
5. Verify API versions

## Next Steps
1. Explore vendor-specific APIs
2. Implement automated testing
3. Build CI/CD pipelines
4. Create custom API wrappers
5. Develop monitoring solutions

## Related Resources
- [REST API Best Practices](https://restfulapi.net/)
- [Python Requests Documentation](https://docs.python-requests.org/)
- [API Security Guide](https://owasp.org/www-project-api-security/)
- [Network Automation Community](https://networktocode.com/)
