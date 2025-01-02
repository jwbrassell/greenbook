# F5 API Installation and Setup

## Table of Contents
- [F5 API Installation and Setup](#f5-api-installation-and-setup)
  - [Required Packages](#required-packages)
  - [Environment Setup](#environment-setup)
- [F5 credentials](#f5-credentials)
- [OpenStack credentials](#openstack-credentials)
  - [Connection Utilities](#connection-utilities)
  - [SSL Certificate Verification](#ssl-certificate-verification)
  - [Connection Testing](#connection-testing)
  - [Error Handling](#error-handling)
  - [Configuration Management](#configuration-management)
  - [Next Steps](#next-steps)



## Required Packages

```bash
pip install f5-sdk
pip install requests
pip install python-openstack-client
```

## Environment Setup

```python
import os
from f5.bigip import ManagementRoot
from openstack import connection

# F5 credentials
F5_HOST = "f5-device.example.com"
F5_USER = "admin"
F5_PASS = "your-password"

# OpenStack credentials
OS_AUTH_URL = "http://controller:5000/v3"
OS_PROJECT_NAME = "admin"
OS_USERNAME = "admin"
OS_PASSWORD = "your-password"
```

## Connection Utilities

```python
def get_f5_connection(host=F5_HOST, username=F5_USER, password=F5_PASS):
    """Establish connection to F5 device"""
    try:
        mgmt = ManagementRoot(host, username, password)
        return mgmt
    except Exception as e:
        print(f"Failed to connect to F5: {str(e)}")
        return None

def get_openstack_connection():
    """Establish connection to OpenStack"""
    try:
        conn = connection.Connection(
            auth_url=OS_AUTH_URL,
            project_name=OS_PROJECT_NAME,
            username=OS_USERNAME,
            password=OS_PASSWORD,
            user_domain_id="default",
            project_domain_id="default"
        )
        return conn
    except Exception as e:
        print(f"Failed to connect to OpenStack: {str(e)}")
        return None
```

## SSL Certificate Verification

For production environments, proper SSL certificate verification is crucial:

```python
def get_f5_connection_secure(host=F5_HOST, username=F5_USER, password=F5_PASS, 
                           verify_ssl=True, ca_cert_path=None):
    """Establish secure connection to F5 device with SSL verification"""
    try:
        mgmt = ManagementRoot(
            host, 
            username, 
            password,
            verify=verify_ssl if not ca_cert_path else ca_cert_path
        )
        return mgmt
    except Exception as e:
        print(f"Failed to connect to F5: {str(e)}")
        return None
```

## Connection Testing

```python
def test_connections():
    """Test both F5 and OpenStack connections"""
    # Test F5 connection
    f5_conn = get_f5_connection()
    if f5_conn:
        print(f"Successfully connected to F5 version: {f5_conn.tmos_version}")
    else:
        print("F5 connection failed")

    # Test OpenStack connection
    os_conn = get_openstack_connection()
    if os_conn:
        print("Successfully connected to OpenStack")
        # List some basic info
        for project in os_conn.identity.projects():
            print(f"Found project: {project.name}")
    else:
        print("OpenStack connection failed")

if __name__ == "__main__":
    test_connections()
```

## Error Handling

```python
class F5ConnectionError(Exception):
    """Custom exception for F5 connection issues"""
    pass

def handle_f5_error(func):
    """Decorator for handling F5 API errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise F5ConnectionError(f"F5 operation failed: {str(e)}")
    return wrapper

@handle_f5_error
def get_system_info(mgmt):
    """Example of using error handling decorator"""
    return {
        'version': mgmt.tmos_version,
        'hostname': mgmt.hostname,
        'platform': mgmt.platform
    }
```

## Configuration Management

```python
def save_f5_config(mgmt):
    """Save the current F5 configuration"""
    try:
        mgmt.tm.sys.config.exec_cmd('save')
        print("Configuration saved successfully")
    except Exception as e:
        print(f"Failed to save configuration: {str(e)}")

def backup_f5_config(mgmt, filename=None):
    """Create a backup of F5 configuration"""
    if not filename:
        filename = f"f5_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ucs"
    
    try:
        mgmt.tm.sys.ucs.exec_cmd('save', name=filename)
        print(f"Backup created successfully: {filename}")
    except Exception as e:
        print(f"Failed to create backup: {str(e)}")
```

## Next Steps

After setting up the connections, you can proceed to:
1. [Authentication and Session Management](authentication.md)
2. [GTM Management](gtm_management.md)
3. [LTM Management](ltm_management.md)
