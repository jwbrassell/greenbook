# Python LDAP3 Guide

## Table of Contents
- [Python LDAP3 Guide](#python-ldap3-guide)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Basic Usage](#basic-usage)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing Strategies](#testing-strategies)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
The ldap3 package is a pure-Python LDAP client library that provides comprehensive support for the LDAP v3 protocol. This guide covers everything from basic setup to advanced operations, focusing on real-world applications and best practices.

## Prerequisites
- Python 3.6+
- Basic understanding of:
  - LDAP concepts and terminology
  - Directory services
  - Authentication protocols
  - Network protocols
- Access to an LDAP server
- Required permissions

## Installation and Setup
1. Install required packages:
```bash
pip install ldap3 python-dotenv
```

2. Environment setup:
```python
# .env file
LDAP_SERVER="ldap://your-server:389"
LDAP_ADMIN_DN="cn=admin,dc=example,dc=com"
LDAP_ADMIN_PASSWORD="your-password"
```

3. Basic configuration:
```python
from ldap3 import Server, Connection, ALL
import os
from dotenv import load_dotenv

load_dotenv()

def get_ldap_connection():
    server = Server(
        os.getenv('LDAP_SERVER'),
        get_info=ALL,
        use_ssl=True
    )
    return Connection(
        server,
        os.getenv('LDAP_ADMIN_DN'),
        os.getenv('LDAP_ADMIN_PASSWORD'),
        auto_bind=True
    )
```

## Basic Usage
1. Connection Management:
```python
from ldap3 import Server, Connection, ALL, SUBTREE

def search_users(search_base, search_filter):
    with get_ldap_connection() as conn:
        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['cn', 'mail', 'uid']
        )
        return conn.entries
```

2. User Operations:
```python
def add_user(dn, attributes):
    with get_ldap_connection() as conn:
        success = conn.add(dn, ['inetOrgPerson'], attributes)
        if not success:
            raise Exception(f"Failed to add user: {conn.result}")
        return success

def modify_user(dn, changes):
    with get_ldap_connection() as conn:
        success = conn.modify(dn, changes)
        if not success:
            raise Exception(f"Failed to modify user: {conn.result}")
        return success
```

## Advanced Features
1. Group Management:
```python
def add_to_group(user_dn, group_dn):
    with get_ldap_connection() as conn:
        return conn.modify(
            group_dn,
            {'member': [(MODIFY_ADD, [user_dn])]}
        )
```

2. Password Management:
```python
from ldap3.extend.microsoft.modifyPassword import ad_modify_password

def change_password(user_dn, new_password):
    with get_ldap_connection() as conn:
        success = ad_modify_password(
            conn,
            user_dn,
            new_password,
            old_password=None
        )
        return success
```

## Security Considerations
1. SSL/TLS Configuration:
```python
from ldap3 import Tls
import ssl

def get_secure_connection():
    tls = Tls(
        validate=ssl.CERT_REQUIRED,
        ca_certs_file='/path/to/ca_cert.pem'
    )
    server = Server(
        os.getenv('LDAP_SERVER'),
        use_ssl=True,
        tls=tls
    )
    return Connection(server, ...)
```

2. Password Policies:
```python
def validate_password_policy(password):
    # Implement password policy checks
    min_length = 8
    requires_upper = any(c.isupper() for c in password)
    requires_lower = any(c.islower() for c in password)
    requires_digit = any(c.isdigit() for c in password)
    
    if not all([
        len(password) >= min_length,
        requires_upper,
        requires_lower,
        requires_digit
    ]):
        raise ValueError("Password does not meet policy requirements")
```

## Performance Optimization
1. Connection Pooling:
```python
from ldap3 import ServerPool, ROUND_ROBIN

def get_connection_pool():
    servers = [
        Server('ldap://server1:389'),
        Server('ldap://server2:389')
    ]
    server_pool = ServerPool(
        servers,
        ROUND_ROBIN,
        active=True,
        exhaust=True
    )
    return Connection(server_pool, ...)
```

2. Attribute Selection:
```python
def optimized_search(search_base, search_filter, attributes=None):
    """Only retrieve needed attributes"""
    with get_ldap_connection() as conn:
        conn.search(
            search_base,
            search_filter,
            attributes=attributes or ['*']
        )
        return conn.entries
```

## Testing Strategies
1. Unit Testing:
```python
import unittest
from unittest.mock import patch

class TestLDAPOperations(unittest.TestCase):
    def setUp(self):
        self.conn = get_test_connection()
    
    def test_user_search(self):
        result = search_users(
            'dc=example,dc=com',
            '(objectClass=person)'
        )
        self.assertTrue(len(result) > 0)
```

2. Integration Testing:
```python
def test_user_lifecycle():
    # Create user
    user_dn = "cn=testuser,dc=example,dc=com"
    add_user(user_dn, {
        'cn': 'Test User',
        'mail': 'test@example.com'
    })
    
    # Modify user
    modify_user(user_dn, {
        'mail': [(MODIFY_REPLACE, ['new@example.com'])]
    })
    
    # Verify changes
    user = search_users(user_dn, '(objectClass=person)')[0]
    assert user.mail == 'new@example.com'
```

## Troubleshooting
1. Error Handling:
```python
class LDAPOperationError(Exception):
    pass

def handle_ldap_operation(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise LDAPOperationError(f"LDAP operation failed: {str(e)}")
    return wrapper

@handle_ldap_operation
def safe_search(search_base, search_filter):
    return search_users(search_base, search_filter)
```

2. Logging:
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('ldap3-operations')

def log_operation(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Starting {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Completed {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Failed {func.__name__}: {str(e)}")
            raise
    return wrapper
```

## Best Practices
1. Connection Management:
```python
from contextlib import contextmanager

@contextmanager
def ldap_connection():
    conn = get_ldap_connection()
    try:
        yield conn
    finally:
        conn.unbind()
```

2. Error Recovery:
```python
def retry_operation(max_attempts=3):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(2 ** attempt)
        return wrapper
    return decorator
```

## Integration Points
1. Active Directory Integration:
```python
def sync_with_active_directory():
    with get_ldap_connection() as conn:
        conn.search(
            'dc=example,dc=com',
            '(&(objectClass=user)(memberOf=CN=Sync,DC=example,DC=com))',
            attributes=['sAMAccountName', 'mail']
        )
        return [entry for entry in conn.entries]
```

2. Authentication Integration:
```python
def authenticate_user(username, password):
    user_dn = f"cn={username},dc=example,dc=com"
    try:
        with Connection(
            server,
            user=user_dn,
            password=password
        ) as conn:
            return conn.bound
    except Exception:
        return False
```

## Next Steps
1. Advanced Topics
   - Schema management
   - Replication monitoring
   - Custom controls
   - Extended operations

2. Further Learning
   - [LDAP RFC Documentation](https://tools.ietf.org/html/rfc4511)
   - [ldap3 Documentation](https://ldap3.readthedocs.io/)
   - [Security Best Practices](https://www.openldap.org/doc/admin24/security.html)
   - Community resources
