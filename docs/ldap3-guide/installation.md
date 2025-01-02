# Installation and Setup Guide

## Table of Contents
- [Installation and Setup Guide](#installation-and-setup-guide)
  - [Basic Installation](#basic-installation)
  - [Dependencies](#dependencies)
  - [Optional Dependencies](#optional-dependencies)
- [For NTLM authentication support](#for-ntlm-authentication-support)
- [For KERBEROS authentication support](#for-kerberos-authentication-support)
- [For SASL authentication support](#for-sasl-authentication-support)
  - [Verifying Installation](#verifying-installation)
  - [Basic Configuration](#basic-configuration)
    - [Server Configuration](#server-configuration)
- [Basic server configuration](#basic-server-configuration)
- [Server with SSL](#server-with-ssl)
- [Server with detailed information](#server-with-detailed-information)
    - [Connection Configuration](#connection-configuration)
- [Basic connection](#basic-connection)
- [Connection with auto-bind](#connection-with-auto-bind)
- [Anonymous connection](#anonymous-connection)
- [Connection with specific settings](#connection-with-specific-settings)
  - [SSL/TLS Configuration](#ssl/tls-configuration)
    - [Using SSL](#using-ssl)
- [Create a TLS configuration](#create-a-tls-configuration)
- [Create server with TLS](#create-server-with-tls)
- [Create connection](#create-connection)
    - [Start TLS](#start-tls)
- [Create connection](#create-connection)
- [Start TLS](#start-tls)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Troubleshooting](#troubleshooting)
  - [Next Steps](#next-steps)



This guide covers the installation and initial setup of the ldap3 package for Python.

## Basic Installation

The simplest way to install ldap3 is using pip:

```bash
pip install ldap3
```

For a specific version:

```bash
pip install ldap3==2.9.1
```

## Dependencies

The ldap3 package has minimal dependencies:
- pyasn1 >= 0.4.6
- Python 3.6 or higher

## Optional Dependencies

For enhanced functionality:

```bash
# For NTLM authentication support
pip install ldap3[ntlm]

# For KERBEROS authentication support
pip install ldap3[kerberos]

# For SASL authentication support
pip install ldap3[sasl]
```

## Verifying Installation

```python
import ldap3
print(ldap3.__version__)
```

## Basic Configuration

### Server Configuration

```python
from ldap3 import Server, Connection, ALL

# Basic server configuration
server = Server('ldap://localhost:389')

# Server with SSL
server_ssl = Server('ldaps://localhost:636', use_ssl=True)

# Server with detailed information
server_detailed = Server('ldap://localhost:389',
                        get_info=ALL,
                        use_ssl=True,
                        connect_timeout=5)
```

### Connection Configuration

```python
from ldap3 import Connection, SIMPLE, SYNC, ASYNC

# Basic connection
conn = Connection(server, 
                 'cn=admin,dc=example,dc=com',
                 'admin_password')

# Connection with auto-bind
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 auto_bind=True)

# Anonymous connection
conn = Connection(server)

# Connection with specific settings
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 client_strategy=SYNC,
                 authentication=SIMPLE,
                 auto_bind=True,
                 receive_timeout=10)
```

## SSL/TLS Configuration

### Using SSL

```python
from ldap3 import Server, Connection, Tls
import ssl

# Create a TLS configuration
tls_config = Tls(validate=ssl.CERT_REQUIRED,
                 ca_certs_file='path/to/ca_cert.pem')

# Create server with TLS
server = Server('ldaps://localhost:636',
               use_ssl=True,
               tls=tls_config)

# Create connection
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 auto_bind=True)
```

### Start TLS

```python
# Create connection
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password')

# Start TLS
conn.start_tls()
```

## Error Handling

```python
from ldap3.core.exceptions import LDAPException, LDAPBindError

try:
    conn = Connection(server,
                     'cn=admin,dc=example,dc=com',
                     'wrong_password',
                     auto_bind=True)
except LDAPBindError:
    print("Failed to bind to server")
except LDAPException as e:
    print(f"LDAP error occurred: {e}")
```

## Best Practices

1. **Always Close Connections**
   ```python
   with Connection(server, 'cn=admin,dc=example,dc=com', 'admin_password') as conn:
       conn.search(...)
   # Connection automatically closed after with block
   ```

2. **Use SSL/TLS in Production**
   - Always use SSL/TLS in production environments
   - Validate certificates properly
   - Keep CA certificates updated

3. **Handle Timeouts**
   - Set appropriate timeout values
   - Implement retry logic for important operations

4. **Connection Pooling**
   ```python
   from ldap3 import ServerPool, ROUND_ROBIN
   
   # Create server pool
   server1 = Server('ldap://server1:389')
   server2 = Server('ldap://server2:389')
   server_pool = ServerPool([server1, server2], ROUND_ROBIN)
   
   # Use pool in connection
   conn = Connection(server_pool, 
                    'cn=admin,dc=example,dc=com',
                    'admin_password')
   ```

## Troubleshooting

Common issues and solutions:

1. **Connection Refused**
   - Verify server address and port
   - Check firewall settings
   - Ensure LDAP service is running

2. **Authentication Failed**
   - Verify DN and password
   - Check user account status
   - Verify SSL/TLS configuration

3. **Certificate Errors**
   - Verify CA certificate path
   - Check certificate validity
   - Ensure proper certificate chain

4. **Timeout Issues**
   - Adjust timeout settings
   - Check network connectivity
   - Verify server load

## Next Steps

After successful installation and basic setup:
1. Review [Basic Operations](basic_operations.md)
2. Explore [Authentication Methods](authentication.md)
3. Learn about [Search Operations](search_operations.md)
