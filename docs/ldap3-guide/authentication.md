# Authentication Methods in LDAP3

## Table of Contents
- [Authentication Methods in LDAP3](#authentication-methods-in-ldap3)
  - [Simple Authentication](#simple-authentication)
- [Simple authentication](#simple-authentication)
  - [Anonymous Authentication](#anonymous-authentication)
- [Anonymous bind](#anonymous-bind)
  - [SASL Authentication](#sasl-authentication)
    - [DIGEST-MD5](#digest-md5)
- [DIGEST-MD5 authentication](#digest-md5-authentication)
    - [GSSAPI (Kerberos)](#gssapi-kerberos)
- [Kerberos authentication](#kerberos-authentication)
    - [EXTERNAL](#external)
- [Configure TLS](#configure-tls)
- [Create server with TLS](#create-server-with-tls)
- [EXTERNAL authentication](#external-authentication)
  - [NTLM Authentication](#ntlm-authentication)
- [NTLM authentication](#ntlm-authentication)
  - [Secure Authentication](#secure-authentication)
    - [Using SSL/TLS](#using-ssl/tls)
- [SSL/TLS configuration](#ssl/tls-configuration)
- [LDAPS connection](#ldaps-connection)
    - [Using StartTLS](#using-starttls)
- [Server with StartTLS support](#server-with-starttls-support)
- [Create connection](#create-connection)
- [Start TLS before binding](#start-tls-before-binding)
  - [Advanced Authentication Scenarios](#advanced-authentication-scenarios)
    - [Connection Pooling with Authentication](#connection-pooling-with-authentication)
- [Create server pool](#create-server-pool)
- [Authenticate using pool](#authenticate-using-pool)
    - [Rebinding with Different Credentials](#rebinding-with-different-credentials)
- [Initial bind](#initial-bind)
- [Perform operations...](#perform-operations)
- [Rebind as different user](#rebind-as-different-user)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Security Considerations](#security-considerations)
  - [Troubleshooting](#troubleshooting)
  - [Next Steps](#next-steps)



This guide covers the various authentication methods available in the ldap3 package.

## Simple Authentication

The most basic form of authentication using DN and password.

```python
from ldap3 import Server, Connection, ALL

server = Server('ldap://localhost:389', get_info=ALL)

# Simple authentication
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 authentication='SIMPLE')
conn.bind()
```

## Anonymous Authentication

Access without credentials, typically with limited permissions.

```python
# Anonymous bind
anon_conn = Connection(server)
anon_conn.bind()

if anon_conn.bound:
    print("Anonymous bind successful")
```

## SASL Authentication

### DIGEST-MD5

```python
from ldap3 import SASL

# DIGEST-MD5 authentication
conn = Connection(server,
                 authentication=SASL,
                 sasl_mechanism='DIGEST-MD5',
                 sasl_credentials=(
                     'username',
                     'password',
                     'realm',
                     'authorization_id'
                 ))
conn.bind()
```

### GSSAPI (Kerberos)

```python
# Kerberos authentication
conn = Connection(server,
                 authentication=SASL,
                 sasl_mechanism='GSSAPI',
                 sasl_credentials=(
                     'username@REALM',
                     'password'
                 ))
conn.bind()
```

### EXTERNAL

Using client certificates for authentication.

```python
import ssl
from ldap3 import Tls

# Configure TLS
tls_config = Tls(
    local_private_key_file='client_key.pem',
    local_certificate_file='client_cert.pem',
    validate=ssl.CERT_REQUIRED,
    version=ssl.PROTOCOL_TLSv1_2,
    ca_certs_file='ca_cert.pem'
)

# Create server with TLS
server = Server('ldaps://localhost:636',
               use_ssl=True,
               tls=tls_config)

# EXTERNAL authentication
conn = Connection(server,
                 authentication=SASL,
                 sasl_mechanism='EXTERNAL')
conn.bind()
```

## NTLM Authentication

Windows-specific authentication method.

```python
from ldap3 import NTLM

# NTLM authentication
conn = Connection(server,
                 user="DOMAIN\\username",
                 password="password",
                 authentication=NTLM)
conn.bind()
```

## Secure Authentication

### Using SSL/TLS

```python
# SSL/TLS configuration
tls_config = Tls(validate=ssl.CERT_REQUIRED,
                 ca_certs_file='ca_cert.pem')

# LDAPS connection
server_ssl = Server('ldaps://localhost:636',
                   use_ssl=True,
                   tls=tls_config)

conn = Connection(server_ssl,
                 'cn=admin,dc=example,dc=com',
                 'admin_password')
conn.bind()
```

### Using StartTLS

```python
# Server with StartTLS support
server = Server('ldap://localhost:389')

# Create connection
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password')

# Start TLS before binding
conn.start_tls()
conn.bind()
```

## Advanced Authentication Scenarios

### Connection Pooling with Authentication

```python
from ldap3 import ServerPool, ROUND_ROBIN

# Create server pool
server1 = Server('ldap://server1:389')
server2 = Server('ldap://server2:389')
server_pool = ServerPool([server1, server2],
                        ROUND_ROBIN,
                        active=True,
                        exhaust=True)

# Authenticate using pool
conn = Connection(server_pool,
                 'cn=admin,dc=example,dc=com',
                 'admin_password',
                 authentication='SIMPLE')
conn.bind()
```

### Rebinding with Different Credentials

```python
# Initial bind
conn = Connection(server,
                 'cn=admin,dc=example,dc=com',
                 'admin_password')
conn.bind()

# Perform operations...

# Rebind as different user
conn.rebind('cn=user,dc=example,dc=com',
            'user_password')
```

## Error Handling

```python
from ldap3.core.exceptions import LDAPBindError, LDAPInvalidCredentialsResult

try:
    conn = Connection(server,
                     'cn=admin,dc=example,dc=com',
                     'wrong_password',
                     authentication='SIMPLE')
    conn.bind()
except LDAPBindError as e:
    print(f"Bind failed: {e}")
except LDAPInvalidCredentialsResult as e:
    print(f"Invalid credentials: {e}")
```

## Best Practices

1. **Always Use SSL/TLS**
   ```python
   # Secure connection setup
   tls_config = Tls(validate=ssl.CERT_REQUIRED,
                   ca_certs_file='ca_cert.pem')
   server = Server('ldaps://localhost:636',
                  use_ssl=True,
                  tls=tls_config)
   ```

2. **Implement Timeout Handling**
   ```python
   conn = Connection(server,
                    'cn=admin,dc=example,dc=com',
                    'admin_password',
                    receive_timeout=10,
                    auto_bind=True)
   ```

3. **Use Context Managers**
   ```python
   with Connection(server,
                  'cn=admin,dc=example,dc=com',
                  'admin_password') as conn:
       if not conn.bind():
           print(f"Failed to bind: {conn.result}")
   ```

4. **Implement Retry Logic**
   ```python
   from time import sleep
   
   def bind_with_retry(conn, max_retries=3):
       for attempt in range(max_retries):
           try:
               if conn.bind():
                   return True
           except LDAPBindError:
               if attempt < max_retries - 1:
                   sleep(2 ** attempt)  # Exponential backoff
                   continue
               raise
       return False
   ```

## Security Considerations

1. **Credential Protection**
   - Never store passwords in plain text
   - Use environment variables or secure vaults
   - Implement proper access controls

2. **Certificate Management**
   - Regularly update certificates
   - Implement certificate rotation
   - Validate certificate chains

3. **Network Security**
   - Use firewalls to restrict LDAP access
   - Monitor failed authentication attempts
   - Implement rate limiting

## Troubleshooting

Common authentication issues and solutions:

1. **Bind Failures**
   - Verify DN format
   - Check password correctness
   - Ensure user account is active

2. **SSL/TLS Issues**
   - Verify certificate validity
   - Check certificate paths
   - Confirm proper CA chain

3. **SASL Problems**
   - Verify SASL library installation
   - Check realm configuration
   - Confirm mechanism support

## Next Steps

1. Explore [Search Operations](search_operations.md)
2. Learn about [Modify Operations](modify_operations.md)
3. Study [Basic Operations](basic_operations.md)
