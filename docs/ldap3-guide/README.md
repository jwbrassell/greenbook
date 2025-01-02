# Python LDAP3 Guide

This guide provides comprehensive documentation and examples for using the ldap3 package in Python to interact with LDAP (Lightweight Directory Access Protocol) servers.

## Table of Contents
- [Python LDAP3 Guide](#python-ldap3-guide)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Quick Start](#quick-start)
- [Define the LDAP server](#define-the-ldap-server)
- [Create a connection](#create-a-connection)
- [Perform a simple search](#perform-a-simple-search)
- [Print results](#print-results)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Contributing](#contributing)
  - [License](#license)

1. [Installation and Setup](installation.md)
2. [Basic Operations](basic_operations.md)
3. [Authentication Methods](authentication.md)
4. [Search Operations](search_operations.md)
5. [Modify Operations](modify_operations.md)
6. [Examples](examples/)

## Overview

The ldap3 package is a pure-Python LDAP client library that provides support for the full LDAP protocol. It's designed to be:

- Compliant with current RFCs for LDAP v3
- Compatible with Python 2 and 3
- Thread-safe
- Type-annotated
- Fast and lightweight

## Quick Start

```python
from ldap3 import Server, Connection, ALL

# Define the LDAP server
server = Server('ldap://your-server:389', get_info=ALL)

# Create a connection
conn = Connection(server, 
                 'cn=admin,dc=example,dc=com',  # Admin DN
                 'admin_password',               # Admin password
                 auto_bind=True)

# Perform a simple search
conn.search('dc=example,dc=com',
           '(objectClass=person)',
           attributes=['cn', 'mail'])

# Print results
for entry in conn.entries:
    print(entry.cn, entry.mail)
```

## Prerequisites

- Python 3.6 or higher
- ldap3 package
- Basic understanding of LDAP concepts
- Access to an LDAP server (like OpenLDAP or Active Directory)

## Installation

```bash
pip install ldap3
```

## Contributing

Feel free to contribute to this documentation by submitting pull requests or creating issues for any improvements or corrections.

## License

This documentation is provided under the MIT License. See [LICENSE](LICENSE) for details.
