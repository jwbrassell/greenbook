# Basic LDAP Operations

## Table of Contents
- [Basic LDAP Operations](#basic-ldap-operations)
  - [Connecting to the Server](#connecting-to-the-server)
- [Create server instance](#create-server-instance)
- [Create connection](#create-connection)
  - [Binding Operations](#binding-operations)
    - [Simple Bind](#simple-bind)
- [Explicit bind](#explicit-bind)
- [Check bind result](#check-bind-result)
    - [Anonymous Bind](#anonymous-bind)
- [Create anonymous connection](#create-anonymous-connection)
    - [Unbind](#unbind)
- [Explicitly unbind](#explicitly-unbind)
  - [Search Operations](#search-operations)
    - [Basic Search](#basic-search)
- [Search for all users](#search-for-all-users)
- [Print results](#print-results)
    - [Advanced Search](#advanced-search)
- [Search with complex filter](#search-with-complex-filter)
- [Using search scopes](#using-search-scopes)
- [Search entire subtree](#search-entire-subtree)
- [Search single level](#search-single-level)
- [Search base object only](#search-base-object-only)
  - [Add Operations](#add-operations)
    - [Adding Entries](#adding-entries)
- [Add a new user](#add-a-new-user)
- [Check result](#check-result)
  - [Modify Operations](#modify-operations)
    - [Modifying Attributes](#modifying-attributes)
- [Modify single attribute](#modify-single-attribute)
- [Modify multiple attributes](#modify-multiple-attributes)
    - [Modify DN (Rename/Move)](#modify-dn-rename/move)
- [Rename entry](#rename-entry)
  - [Delete Operations](#delete-operations)
- [Delete an entry](#delete-an-entry)
- [Check result](#check-result)
  - [Compare Operations](#compare-operations)
- [Compare attribute value](#compare-attribute-value)
  - [Extended Operations](#extended-operations)
- [Password modify extended operation](#password-modify-extended-operation)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)



This guide covers the fundamental operations you can perform with the ldap3 package.

## Connecting to the Server

```python
from ldap3 import Server, Connection, ALL

# Create server instance
server = Server('ldap://localhost:389', get_info=ALL)

# Create connection
conn = Connection(server, 
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 auto_bind=True)
```

## Binding Operations

### Simple Bind

```python
# Explicit bind
conn = Connection(server, 'cn=admin,dc=example,dc=com', 'admin_password')
conn.bind()

# Check bind result
if conn.bound:
    print("Successfully bound to server")
```

### Anonymous Bind

```python
# Create anonymous connection
anon_conn = Connection(server)
anon_conn.bind()
```

### Unbind

```python
# Explicitly unbind
conn.unbind()
```

## Search Operations

### Basic Search

```python
# Search for all users
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['cn', 'mail'])

# Print results
for entry in conn.entries:
    print(f"Name: {entry.cn}, Email: {entry.mail}")
```

### Advanced Search

```python
# Search with complex filter
search_filter = '(&(objectClass=person)(|(department=IT)(department=HR)))'
conn.search('dc=example,dc=com',
           search_filter,
           attributes=['cn', 'mail', 'department'])

# Using search scopes
from ldap3 import SUBTREE, LEVEL, BASE

# Search entire subtree
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           search_scope=SUBTREE)

# Search single level
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           search_scope=LEVEL)

# Search base object only
conn.search('cn=admin,dc=example,dc=com',
           '(objectClass=person)',
           search_scope=BASE)
```

## Add Operations

### Adding Entries

```python
# Add a new user
dn = 'cn=john,ou=users,dc=example,dc=com'
object_class = ['top', 'person', 'organizationalPerson', 'inetOrgPerson']
attributes = {
    'cn': 'john',
    'sn': 'doe',
    'mail': 'john.doe@example.com',
    'userPassword': 'password123'
}

conn.add(dn, object_class, attributes)

# Check result
if conn.result['result'] == 0:
    print("Successfully added new entry")
else:
    print(f"Failed to add entry: {conn.result['description']}")
```

## Modify Operations

### Modifying Attributes

```python
# Modify single attribute
conn.modify('cn=john,ou=users,dc=example,dc=com',
           {'mail': [('MODIFY_REPLACE', ['new.email@example.com'])]})

# Modify multiple attributes
modifications = {
    'mail': [('MODIFY_REPLACE', ['new.email@example.com'])],
    'telephoneNumber': [('MODIFY_ADD', ['+1234567890'])],
    'title': [('MODIFY_DELETE', [])]
}
conn.modify('cn=john,ou=users,dc=example,dc=com', modifications)
```

### Modify DN (Rename/Move)

```python
# Rename entry
conn.modify_dn('cn=john,ou=users,dc=example,dc=com',
               'cn=john.doe',
               new_superior='ou=staff,dc=example,dc=com')
```

## Delete Operations

```python
# Delete an entry
conn.delete('cn=john.doe,ou=staff,dc=example,dc=com')

# Check result
if conn.result['result'] == 0:
    print("Successfully deleted entry")
else:
    print(f"Failed to delete entry: {conn.result['description']}")
```

## Compare Operations

```python
# Compare attribute value
result = conn.compare('cn=john.doe,ou=staff,dc=example,dc=com',
                     'mail',
                     'john.doe@example.com')

if result:
    print("Attribute value matches")
```

## Extended Operations

```python
# Password modify extended operation
from ldap3 import MODIFY_PASSWORD
conn.extend.standard.modify_password(
    'cn=john.doe,ou=staff,dc=example,dc=com',
    'old_password',
    'new_password'
)
```

## Error Handling

```python
from ldap3.core.exceptions import LDAPException, LDAPOperationResult

try:
    conn.add(dn, object_class, attributes)
    if not conn.result['result'] == 0:
        print(f"Operation failed: {conn.result['description']}")
except LDAPOperationResult as e:
    print(f"Operation error: {e.description}")
except LDAPException as e:
    print(f"LDAP error: {e}")
```

## Best Practices

1. **Use Connection as Context Manager**
   ```python
   with Connection(server, user_dn, password) as conn:
       conn.search(...)
   ```

2. **Always Check Operation Results**
   ```python
   conn.search(...)
   if conn.result['result'] == 0:
       process_entries(conn.entries)
   else:
       handle_error(conn.result)
   ```

3. **Use Proper Exception Handling**
   ```python
   try:
       conn.add(...)
   except LDAPException as e:
       logger.error(f"LDAP operation failed: {e}")
   ```

4. **Properly Escape Search Filters**
   ```python
   from ldap3.utils.conv import escape_filter_chars
   
   user_input = "John (Doe)"
   safe_filter = f"(cn={escape_filter_chars(user_input)})"
   conn.search(..., safe_filter, ...)
   ```

## Next Steps

1. Learn about [Authentication Methods](authentication.md)
2. Explore [Search Operations](search_operations.md) in detail
3. Study [Modify Operations](modify_operations.md)
