# Search Operations in LDAP3

## Table of Contents
- [Search Operations in LDAP3](#search-operations-in-ldap3)
  - [Basic Search Syntax](#basic-search-syntax)
- [Basic search](#basic-search)
- [Process results](#process-results)
  - [Search Parameters](#search-parameters)
    - [Search Base](#search-base)
- [Search from root](#search-from-root)
- [Search specific organizational unit](#search-specific-organizational-unit)
- [Search specific container](#search-specific-container)
    - [Search Scope](#search-scope)
- [BASE: Search only the specified object](#base:-search-only-the-specified-object)
- [LEVEL: Search immediate children of base](#level:-search-immediate-children-of-base)
- [SUBTREE: Search base and all descendants](#subtree:-search-base-and-all-descendants)
    - [Search Filters](#search-filters)
- [Equality match](#equality-match)
- [Substring match](#substring-match)
- [AND operation](#and-operation)
- [OR operation](#or-operation)
- [NOT operation](#not-operation)
- [Complex filters](#complex-filters)
    - [Attributes](#attributes)
- [Return specific attributes](#return-specific-attributes)
- [Return all user attributes](#return-all-user-attributes)
- [Return operational attributes](#return-operational-attributes)
- [Return specific and operational attributes](#return-specific-and-operational-attributes)
  - [Advanced Search Features](#advanced-search-features)
    - [Paged Search](#paged-search)
- [Set page size](#set-page-size)
- [Create cookie for paging](#create-cookie-for-paging)
    - [Server-Side Sorting](#server-side-sorting)
- [Sort by surname descending](#sort-by-surname-descending)
    - [Virtual List View (VLV)](#virtual-list-view-vlv)
- [VLV search](#vlv-search)
  - [Search Result Processing](#search-result-processing)
    - [Accessing Results](#accessing-results)
- [Check if search was successful](#check-if-search-was-successful)
    - [Result Attributes](#result-attributes)
- [Get all attributes](#get-all-attributes)
- [Get attribute names](#get-attribute-names)
- [Get attribute values](#get-attribute-values)
- [Check if attribute exists](#check-if-attribute-exists)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Performance Tips](#performance-tips)
  - [Troubleshooting](#troubleshooting)
  - [Next Steps](#next-steps)



This guide provides detailed information about performing search operations using the ldap3 package.

## Basic Search Syntax

```python
from ldap3 import Server, Connection, ALL, SUBTREE

server = Server('ldap://localhost:389', get_info=ALL)
conn = Connection(server, 'cn=admin,dc=example,dc=com', 'admin_password', auto_bind=True)

# Basic search
conn.search(
    search_base='dc=example,dc=com',
    search_filter='(objectClass=person)',
    attributes=['cn', 'mail']
)

# Process results
for entry in conn.entries:
    print(f"DN: {entry.entry_dn}")
    print(f"CN: {entry.cn}")
    print(f"Mail: {entry.mail}")
```

## Search Parameters

### Search Base

The starting point in the directory:

```python
# Search from root
conn.search('dc=example,dc=com', '(objectClass=*)')

# Search specific organizational unit
conn.search('ou=users,dc=example,dc=com', '(objectClass=*)')

# Search specific container
conn.search('cn=admins,dc=example,dc=com', '(objectClass=*)')
```

### Search Scope

Control how deep the search goes:

```python
from ldap3 import BASE, LEVEL, SUBTREE

# BASE: Search only the specified object
conn.search('cn=john,ou=users,dc=example,dc=com',
           '(objectClass=person)',
           search_scope=BASE)

# LEVEL: Search immediate children of base
conn.search('ou=users,dc=example,dc=com',
           '(objectClass=person)',
           search_scope=LEVEL)

# SUBTREE: Search base and all descendants
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           search_scope=SUBTREE)
```

### Search Filters

Different types of search filters:

```python
# Equality match
conn.search('dc=example,dc=com',
           '(cn=John Smith)')

# Substring match
conn.search('dc=example,dc=com',
           '(cn=*Smith*)')

# AND operation
conn.search('dc=example,dc=com',
           '(&(objectClass=person)(department=IT))')

# OR operation
conn.search('dc=example,dc=com',
           '(|(department=IT)(department=HR))')

# NOT operation
conn.search('dc=example,dc=com',
           '(!(department=Sales))')

# Complex filters
conn.search('dc=example,dc=com',
           '(&(objectClass=person)(|(department=IT)(department=HR))(!(manager=*)))')
```

### Attributes

Specify which attributes to return:

```python
# Return specific attributes
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['cn', 'mail', 'telephoneNumber'])

# Return all user attributes
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['*'])

# Return operational attributes
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['+'])

# Return specific and operational attributes
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['cn', 'mail', '+'])
```

## Advanced Search Features

### Paged Search

For handling large result sets:

```python
from ldap3 import SUBTREE

# Set page size
page_size = 100
entries = []

# Create cookie for paging
cookie = None

while True:
    conn.search('dc=example,dc=com',
                '(objectClass=person)',
                search_scope=SUBTREE,
                attributes=['cn', 'mail'],
                paged_size=page_size,
                paged_cookie=cookie)
    
    entries.extend(conn.entries)
    cookie = conn.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
    
    if not cookie:
        break

print(f"Total entries found: {len(entries)}")
```

### Server-Side Sorting

Sort results on the server:

```python
from ldap3 import DESCENDING

# Sort by surname descending
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['sn', 'givenName'],
           sort_order=[('sn', DESCENDING)])
```

### Virtual List View (VLV)

For efficient browsing of large lists:

```python
# VLV search
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['cn'],
           virtual_attributes=['entryUUID'],
           vlv={'beforeCount': 0, 'afterCount': 5, 'offset': 1, 'content': 'sn'})
```

## Search Result Processing

### Accessing Results

```python
# Check if search was successful
if conn.search('dc=example,dc=com', '(objectClass=person)'):
    # Access as entries
    for entry in conn.entries:
        print(entry.entry_dn)
        
    # Access as JSON
    json_entries = conn.entries.json
    
    # Access as dictionary
    dict_entries = conn.entries.entry_to_dict()
```

### Result Attributes

```python
# Get all attributes
conn.search('dc=example,dc=com',
           '(cn=john)',
           attributes=['*'])

entry = conn.entries[0]

# Get attribute names
print(entry.entry_attributes)

# Get attribute values
print(entry.entry_attributes_as_dict)

# Check if attribute exists
if 'mail' in entry:
    print(entry.mail)
```

## Error Handling

```python
from ldap3.core.exceptions import LDAPException, LDAPOperationResult

try:
    conn.search('dc=example,dc=com',
                '(invalidFilter=*)')
except LDAPOperationResult as e:
    print(f"Search failed: {e.description}")
except LDAPException as e:
    print(f"LDAP error: {e}")
```

## Best Practices

1. **Use Proper Filter Escaping**
   ```python
   from ldap3.utils.conv import escape_filter_chars
   
   user_input = "John (Smith)"
   safe_filter = f"(cn={escape_filter_chars(user_input)})"
   conn.search('dc=example,dc=com', safe_filter)
   ```

2. **Optimize Attribute Selection**
   ```python
   # Only request needed attributes
   conn.search('dc=example,dc=com',
               '(objectClass=person)',
               attributes=['cn', 'mail'])  # Instead of ['*']
   ```

3. **Use Paging for Large Results**
   ```python
   # Set reasonable page size
   page_size = 500
   
   conn.search('dc=example,dc=com',
               '(objectClass=person)',
               paged_size=page_size)
   ```

4. **Implement Timeouts**
   ```python
   # Set search timeout
   conn.search('dc=example,dc=com',
               '(objectClass=person)',
               time_limit=30)  # 30 seconds
   ```

## Performance Tips

1. **Narrow Search Base**
   - Use specific search bases instead of searching from root
   - Use appropriate search scope

2. **Optimize Filters**
   - Put most selective terms first in AND operations
   - Use indexed attributes in filters
   - Avoid wildcard searches when possible

3. **Control Result Size**
   - Use paging for large results
   - Only request needed attributes
   - Use server-side sorting when available

## Troubleshooting

Common search issues and solutions:

1. **No Results**
   - Verify search base is correct
   - Check filter syntax
   - Confirm user has read permissions

2. **Slow Searches**
   - Review filter optimization
   - Check for unindexed attributes
   - Consider using paging

3. **Size Limit Exceeded**
   - Implement paging
   - Narrow search scope
   - Refine search filter

## Next Steps

1. Learn about [Modify Operations](modify_operations.md)
2. Study [Authentication Methods](authentication.md)
3. Explore [Basic Operations](basic_operations.md)
