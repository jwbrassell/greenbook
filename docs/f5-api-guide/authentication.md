# F5 Authentication and Security Guide

## Table of Contents
- [F5 Authentication and Security Guide](#f5-authentication-and-security-guide)
  - [Basic Authentication](#basic-authentication)
  - [Token-Based Authentication](#token-based-authentication)
  - [Certificate-Based Authentication](#certificate-based-authentication)
  - [Session Management](#session-management)
  - [Secure Connection Utilities](#secure-connection-utilities)
  - [Usage Examples](#usage-examples)
  - [Security Best Practices](#security-best-practices)
  - [Common Security Issues](#common-security-issues)



This guide covers authentication, session management, and security best practices when working with F5 devices through the API.

## Basic Authentication

```python
from f5.bigip import ManagementRoot
from requests.exceptions import RequestException
import ssl
import urllib3

def create_basic_connection(host: str, username: str, password: str, 
                          verify_ssl: bool = True):
    """
    Create a basic authenticated connection to F5 device
    
    Args:
        host: F5 device hostname or IP
        username: Admin username
        password: Admin password
        verify_ssl: Whether to verify SSL certificates
    """
    try:
        if not verify_ssl:
            urllib3.disable_warnings()
        
        mgmt = ManagementRoot(
            host,
            username,
            password,
            verify=verify_ssl
        )
        print(f"Connected to F5 device: {host}")
        return mgmt
    except Exception as e:
        print(f"Failed to connect to F5 device: {str(e)}")
        return None

def verify_connection(mgmt) -> bool:
    """Verify connection is valid"""
    try:
        # Try to access device info
        version = mgmt.tmos_version
        return True
    except Exception:
        return False
```

## Token-Based Authentication

```python
def get_auth_token(host: str, username: str, password: str, 
                   verify_ssl: bool = True):
    """Get authentication token for API access"""
    import requests
    
    url = f"https://{host}/mgmt/shared/authn/login"
    payload = {
        'username': username,
        'password': password,
        'loginProviderName': 'tmos'
    }
    
    try:
        response = requests.post(
            url,
            json=payload,
            verify=verify_ssl
        )
        response.raise_for_status()
        token = response.json()['token']['token']
        print("Successfully obtained auth token")
        return token
    except Exception as e:
        print(f"Failed to get auth token: {str(e)}")
        return None

def create_token_connection(host: str, token: str, verify_ssl: bool = True):
    """Create connection using authentication token"""
    try:
        mgmt = ManagementRoot(
            host,
            token=token,
            verify=verify_ssl
        )
        print(f"Connected to F5 device using token: {host}")
        return mgmt
    except Exception as e:
        print(f"Failed to connect with token: {str(e)}")
        return None
```

## Certificate-Based Authentication

```python
def create_cert_connection(host: str, cert_file: str, key_file: str, 
                         verify_ssl: bool = True):
    """Create connection using client certificate"""
    try:
        mgmt = ManagementRoot(
            host,
            cert=(cert_file, key_file),
            verify=verify_ssl
        )
        print(f"Connected to F5 device using certificate: {host}")
        return mgmt
    except Exception as e:
        print(f"Failed to connect with certificate: {str(e)}")
        return None

def validate_cert_files(cert_file: str, key_file: str) -> bool:
    """Validate certificate and key files"""
    try:
        with open(cert_file, 'r') as f:
            cert_content = f.read()
        with open(key_file, 'r') as f:
            key_content = f.read()
            
        # Basic validation
        if 'BEGIN CERTIFICATE' not in cert_content:
            print("Invalid certificate file")
            return False
        if 'BEGIN PRIVATE KEY' not in key_content:
            print("Invalid private key file")
            return False
            
        return True
    except Exception as e:
        print(f"Failed to validate cert files: {str(e)}")
        return False
```

## Session Management

```python
class F5Session:
    """Manage F5 connection session"""
    
    def __init__(self, host: str, username: str = None, password: str = None,
                 token: str = None, cert_file: str = None, key_file: str = None,
                 verify_ssl: bool = True):
        self.host = host
        self.username = username
        self.password = password
        self.token = token
        self.cert_file = cert_file
        self.key_file = key_file
        self.verify_ssl = verify_ssl
        self.mgmt = None
        
    def connect(self):
        """Establish connection based on provided credentials"""
        try:
            if self.token:
                self.mgmt = create_token_connection(
                    self.host,
                    self.token,
                    self.verify_ssl
                )
            elif self.cert_file and self.key_file:
                self.mgmt = create_cert_connection(
                    self.host,
                    self.cert_file,
                    self.key_file,
                    self.verify_ssl
                )
            elif self.username and self.password:
                self.mgmt = create_basic_connection(
                    self.host,
                    self.username,
                    self.password,
                    self.verify_ssl
                )
            else:
                raise ValueError("No valid authentication method provided")
                
            return verify_connection(self.mgmt)
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False
    
    def reconnect(self):
        """Attempt to reconnect if session is lost"""
        try:
            if not verify_connection(self.mgmt):
                print("Session expired, reconnecting...")
                return self.connect()
            return True
        except Exception as e:
            print(f"Reconnection failed: {str(e)}")
            return False
    
    def close(self):
        """Close the connection"""
        try:
            if self.mgmt:
                self.mgmt.session.close()
                print("Connection closed successfully")
        except Exception as e:
            print(f"Failed to close connection: {str(e)}")
```

## Secure Connection Utilities

```python
def create_secure_connection(config_file: str):
    """Create connection from secure config file"""
    import json
    from pathlib import Path
    
    try:
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_file}")
            
        with open(config_path, 'r') as f:
            config = json.load(f)
            
        required_fields = ['host']
        if not all(field in config for field in required_fields):
            raise ValueError("Missing required fields in config")
            
        session = F5Session(
            host=config['host'],
            username=config.get('username'),
            password=config.get('password'),
            token=config.get('token'),
            cert_file=config.get('cert_file'),
            key_file=config.get('key_file'),
            verify_ssl=config.get('verify_ssl', True)
        )
        
        if session.connect():
            return session
        return None
    except Exception as e:
        print(f"Failed to create secure connection: {str(e)}")
        return None
```

## Usage Examples

```python
if __name__ == "__main__":
    # Basic authentication
    mgmt = create_basic_connection(
        "f5-device.example.com",
        "admin",
        "password",
        verify_ssl=True
    )
    
    # Token-based authentication
    token = get_auth_token(
        "f5-device.example.com",
        "admin",
        "password"
    )
    if token:
        mgmt = create_token_connection(
            "f5-device.example.com",
            token
        )
    
    # Certificate-based authentication
    mgmt = create_cert_connection(
        "f5-device.example.com",
        "/path/to/cert.pem",
        "/path/to/key.pem"
    )
    
    # Using session management
    session = F5Session(
        host="f5-device.example.com",
        username="admin",
        password="password"
    )
    if session.connect():
        # Use session.mgmt for operations
        version = session.mgmt.tmos_version
        print(f"Connected to F5 version: {version}")
        
        # Close session when done
        session.close()
```

## Security Best Practices

1. Authentication:
   - Use token-based or certificate-based authentication over basic auth
   - Rotate credentials regularly
   - Use strong passwords
   - Implement multi-factor authentication where possible

2. SSL/TLS:
   - Always verify SSL certificates in production
   - Use strong cipher suites
   - Keep certificates up to date
   - Implement proper certificate management

3. Session Management:
   - Implement session timeouts
   - Monitor active sessions
   - Close sessions properly
   - Handle session expiration

4. Access Control:
   - Use role-based access control
   - Implement least privilege principle
   - Regular access audits
   - Monitor failed login attempts

## Common Security Issues

1. Authentication Issues:
   - Invalid credentials
   - Expired certificates
   - Token expiration
   - Session timeout

2. SSL/TLS Issues:
   - Certificate validation failures
   - Cipher suite mismatches
   - Expired certificates
   - Chain validation problems

3. Access Control Issues:
   - Insufficient permissions
   - Role configuration problems
   - Audit logging failures
   - Authorization errors
