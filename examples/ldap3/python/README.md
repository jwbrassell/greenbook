# LDAP3 with Python Examples

## Table of Contents
- [LDAP3 with Python Examples](#ldap3-with-python-examples)
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
   - Server connection
   - Authentication
   - User management
   - Group operations

2. Advanced Features
   - Complex searches
   - Attribute management
   - Schema operations
   - Certificate handling

3. Integration Features
   - Active Directory sync
   - User provisioning
   - Group synchronization
   - Access control

4. Full Applications
   - User directory
   - Group manager
   - Access controller
   - Directory sync tool

## Project Structure

```
python/
├── basic/
│   ├── connection/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── config.py
│   ├── authentication/
│   ├── users/
│   └── groups/
├── advanced/
│   ├── search/
│   ├── attributes/
│   ├── schema/
│   └── certificates/
├── integration/
│   ├── active_directory/
│   ├── user_sync/
│   ├── group_sync/
│   └── access_control/
└── applications/
    ├── user_directory/
    ├── group_manager/
    ├── access_controller/
    └── sync_tool/
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

3. Configure LDAP Connection:
```python
# config.py
LDAP_SERVER = "ldap://your-ldap-server:389"
LDAP_BASE_DN = "dc=example,dc=com"
LDAP_BIND_DN = "cn=admin,dc=example,dc=com"
LDAP_BIND_PASSWORD = "your-password"
```

## Basic Operations

### Server Connection
```python
from ldap3 import Server, Connection, ALL, NTLM, SUBTREE
from config import *

def get_ldap_connection():
    """Create authenticated LDAP connection"""
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(
        server,
        user=LDAP_BIND_DN,
        password=LDAP_BIND_PASSWORD,
        authentication=NTLM
    )
    
    if not conn.bind():
        raise Exception(f"Failed to bind: {conn.result}")
    
    return conn

def test_connection():
    """Test LDAP connection"""
    try:
        conn = get_ldap_connection()
        print("Connected successfully")
        conn.unbind()
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
```

### User Management
```python
class UserManager:
    def __init__(self):
        self.conn = get_ldap_connection()
        self.base_dn = LDAP_BASE_DN
    
    def create_user(self, username, firstname, lastname, password):
        """Create new user"""
        user_dn = f"cn={username},{self.base_dn}"
        attributes = {
            'objectClass': ['top', 'person', 'organizationalPerson', 'user'],
            'cn': username,
            'givenName': firstname,
            'sn': lastname,
            'userPassword': password
        }
        
        return self.conn.add(user_dn, attributes=attributes)
    
    def get_user(self, username):
        """Get user by username"""
        search_filter = f"(cn={username})"
        self.conn.search(
            self.base_dn,
            search_filter,
            SUBTREE,
            attributes=['*']
        )
        
        if len(self.conn.entries) == 0:
            return None
        
        return self.conn.entries[0]
    
    def update_user(self, username, attributes):
        """Update user attributes"""
        user = self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        changes = {}
        for attr, value in attributes.items():
            changes[attr] = [(MODIFY_REPLACE, [value])]
        
        return self.conn.modify(user.entry_dn, changes)
    
    def delete_user(self, username):
        """Delete user"""
        user = self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        return self.conn.delete(user.entry_dn)
```

### Group Operations
```python
class GroupManager:
    def __init__(self):
        self.conn = get_ldap_connection()
        self.base_dn = LDAP_BASE_DN
    
    def create_group(self, groupname, description=None):
        """Create new group"""
        group_dn = f"cn={groupname},ou=groups,{self.base_dn}"
        attributes = {
            'objectClass': ['top', 'group'],
            'cn': groupname
        }
        
        if description:
            attributes['description'] = description
        
        return self.conn.add(group_dn, attributes=attributes)
    
    def add_user_to_group(self, username, groupname):
        """Add user to group"""
        user = self.get_user(username)
        group = self.get_group(groupname)
        
        if not user or not group:
            raise ValueError("User or group not found")
        
        return self.conn.modify(
            group.entry_dn,
            {'member': [(MODIFY_ADD, [user.entry_dn])]}
        )
    
    def get_user_groups(self, username):
        """Get groups for user"""
        user = self.get_user(username)
        if not user:
            raise ValueError(f"User {username} not found")
        
        search_filter = f"(&(objectClass=group)(member={user.entry_dn}))"
        self.conn.search(
            self.base_dn,
            search_filter,
            SUBTREE,
            attributes=['cn', 'description']
        )
        
        return self.conn.entries
```

## Advanced Features

### Complex Searches
```python
class DirectorySearcher:
    def __init__(self):
        self.conn = get_ldap_connection()
        self.base_dn = LDAP_BASE_DN
    
    def search_users_by_criteria(self, criteria):
        """Search users by multiple criteria"""
        filters = []
        for attr, value in criteria.items():
            filters.append(f"({attr}={value})")
        
        search_filter = f"(&(objectClass=user){''.join(filters)})"
        self.conn.search(
            self.base_dn,
            search_filter,
            SUBTREE,
            attributes=['*']
        )
        
        return self.conn.entries
    
    def find_inactive_users(self, days=30):
        """Find users inactive for specified days"""
        threshold = (datetime.now() - timedelta(days=days)).strftime(
            '%Y%m%d%H%M%S.0Z'
        )
        search_filter = (
            f"(&(objectClass=user)(lastLogon<={threshold}))"
        )
        
        self.conn.search(
            self.base_dn,
            search_filter,
            SUBTREE,
            attributes=['cn', 'lastLogon']
        )
        
        return self.conn.entries
```

### Schema Operations
```python
class SchemaManager:
    def __init__(self):
        self.conn = get_ldap_connection()
    
    def get_object_classes(self):
        """Get all object classes"""
        self.conn.search(
            'cn=schema,cn=config',
            '(objectClass=ldapSubentry)',
            SUBTREE,
            attributes=['*']
        )
        return self.conn.entries
    
    def add_attribute_type(self, name, syntax, single_value=False):
        """Add new attribute type to schema"""
        attr_oid = '1.3.6.1.4.1.X.Y.Z'  # Replace with your OID
        
        schema_entry = (
            f'( {attr_oid} '
            f'NAME \'{name}\' '
            f'SYNTAX {syntax} '
            f'SINGLE-VALUE {str(single_value).upper()} )'
        )
        
        return self.conn.modify(
            'cn=schema,cn=config',
            {'attributeTypes': [(MODIFY_ADD, [schema_entry])]}
        )
```

## Security Considerations

1. Certificate Handling:
```python
from ldap3 import Tls
import ssl

class SecureConnection:
    def __init__(self, ca_cert_path):
        self.tls = Tls(
            ca_certs_file=ca_cert_path,
            validate=ssl.CERT_REQUIRED
        )
    
    def get_secure_connection(self):
        """Create secure LDAP connection"""
        server = Server(
            LDAP_SERVER,
            use_ssl=True,
            tls=self.tls,
            get_info=ALL
        )
        
        conn = Connection(
            server,
            user=LDAP_BIND_DN,
            password=LDAP_BIND_PASSWORD,
            authentication=NTLM
        )
        
        if not conn.bind():
            raise Exception(f"Failed to bind: {conn.result}")
        
        return conn
```

2. Password Policy:
```python
class PasswordManager:
    def __init__(self):
        self.conn = get_ldap_connection()
    
    def change_password(self, username, old_password, new_password):
        """Change user password with policy check"""
        if not self.validate_password(new_password):
            raise ValueError("Password does not meet requirements")
        
        user = self.get_user(username)
        if not user:
            raise ValueError("User not found")
        
        # Verify old password
        test_conn = Connection(
            self.conn.server,
            user=user.entry_dn,
            password=old_password
        )
        if not test_conn.bind():
            raise ValueError("Invalid old password")
        
        return self.conn.modify(
            user.entry_dn,
            {'userPassword': [(MODIFY_REPLACE, [new_password])]}
        )
    
    def validate_password(self, password):
        """Check password against policy"""
        if len(password) < 8:
            return False
        if not any(c.isupper() for c in password):
            return False
        if not any(c.islower() for c in password):
            return False
        if not any(c.isdigit() for c in password):
            return False
        return True
```

## Performance Optimization

1. Connection Pooling:
```python
from ldap3 import ServerPool, ROUND_ROBIN

class ConnectionPool:
    def __init__(self, servers, pool_size=5):
        self.server_pool = ServerPool(
            servers,
            ROUND_ROBIN,
            active=True,
            exhaust=True
        )
        self.pool_size = pool_size
        self.connections = []
    
    def get_connection(self):
        """Get connection from pool"""
        if len(self.connections) < self.pool_size:
            conn = Connection(
                self.server_pool,
                user=LDAP_BIND_DN,
                password=LDAP_BIND_PASSWORD,
                authentication=NTLM
            )
            conn.bind()
            self.connections.append(conn)
            return conn
        
        return self.connections[0]  # Round-robin
```

2. Search Optimization:
```python
class OptimizedSearcher:
    def __init__(self):
        self.conn = get_ldap_connection()
    
    def paged_search(self, search_base, search_filter, page_size=100):
        """Perform paged search for large results"""
        entry_generator = self.conn.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=SUBTREE,
            attributes=['*'],
            paged_size=page_size,
            generator=True
        )
        
        for entry in entry_generator:
            yield entry
```

## Testing

1. Unit Tests:
```python
import unittest
from unittest.mock import patch

class LDAPTests(unittest.TestCase):
    def setUp(self):
        self.conn = get_ldap_connection()
    
    def test_user_creation(self):
        manager = UserManager()
        result = manager.create_user(
            'testuser',
            'Test',
            'User',
            'password123'
        )
        self.assertTrue(result)
    
    def test_group_operations(self):
        manager = GroupManager()
        
        # Create group
        manager.create_group('testgroup', 'Test Group')
        
        # Add user
        manager.add_user_to_group('testuser', 'testgroup')
        
        # Verify membership
        groups = manager.get_user_groups('testuser')
        self.assertEqual(len(groups), 1)
        self.assertEqual(groups[0].cn, 'testgroup')
```

2. Integration Tests:
```python
class LDAPIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.conn = get_ldap_connection()
        self.user_manager = UserManager()
        self.group_manager = GroupManager()
    
    def test_user_workflow(self):
        # Create user
        username = 'integrationtest'
        self.user_manager.create_user(
            username,
            'Integration',
            'Test',
            'password123'
        )
        
        # Update user
        self.user_manager.update_user(
            username,
            {'title': 'Test User'}
        )
        
        # Verify changes
        user = self.user_manager.get_user(username)
        self.assertEqual(user.title, 'Test User')
        
        # Clean up
        self.user_manager.delete_user(username)
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
