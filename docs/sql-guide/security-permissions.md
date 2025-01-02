# Database Security and Permissions Guide

## Table of Contents
- [Database Security and Permissions Guide](#database-security-and-permissions-guide)
  - [Understanding Database Security](#understanding-database-security)
    - [Why Security Matters](#why-security-matters)
  - [User Management](#user-management)
    - [Creating Users](#creating-users)
    - [User Roles](#user-roles)
    - [Permission Levels](#permission-levels)
  - [Best Security Practices](#best-security-practices)
    - [1. Password Policies](#1-password-policies)
    - [2. Network Security](#2-network-security)
- [MySQL configuration (my.cnf)](#mysql-configuration-mycnf)
    - [3. Encryption](#3-encryption)
  - [Regular Security Maintenance](#regular-security-maintenance)
    - [1. Audit User Access](#1-audit-user-access)
    - [2. Remove Unused Accounts](#2-remove-unused-accounts)
    - [3. Review Permissions](#3-review-permissions)
  - [Security Monitoring](#security-monitoring)
    - [1. Login Attempts](#1-login-attempts)
    - [2. Suspicious Activity](#2-suspicious-activity)
  - [Implementing Security with Python](#implementing-security-with-python)
    - [1. Secure Connection Setup](#1-secure-connection-setup)
- [Create SSL context](#create-ssl-context)
- [Connect with SSL](#connect-with-ssl)
    - [2. Password Hashing](#2-password-hashing)
  - [Emergency Security Procedures](#emergency-security-procedures)
    - [1. Security Breach Response](#1-security-breach-response)
    - [2. Audit Trail Review](#2-audit-trail-review)
  - [Security Checklist](#security-checklist)
    - [Daily Tasks](#daily-tasks)
    - [Weekly Tasks](#weekly-tasks)
    - [Monthly Tasks](#monthly-tasks)
  - [Additional Security Tools](#additional-security-tools)
    - [1. Database Firewalls](#1-database-firewalls)
    - [2. Intrusion Detection](#2-intrusion-detection)
    - [3. Encryption Tools](#3-encryption-tools)



## Understanding Database Security

### Why Security Matters
- Protect sensitive data
- Prevent unauthorized access
- Maintain data integrity
- Comply with regulations
- Avoid data breaches

## User Management

### Creating Users
```sql
-- MySQL/MariaDB
CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'strong_password';

-- Oracle
CREATE USER appuser IDENTIFIED BY strong_password;

-- SQLite (uses file permissions instead)
chmod 600 database.db
```

### User Roles
```sql
-- MySQL/MariaDB
CREATE ROLE 'app_read';
CREATE ROLE 'app_write';

-- Oracle
CREATE ROLE app_read;
CREATE ROLE app_write;
```

### Permission Levels

1. **Database Level**
```sql
-- MySQL/MariaDB
GRANT ALL PRIVILEGES ON database_name.* TO 'user'@'localhost';

-- Oracle
GRANT CREATE SESSION TO user;
GRANT CREATE TABLE TO user;
```

2. **Table Level**
```sql
-- MySQL/MariaDB
GRANT SELECT, INSERT ON database_name.table_name TO 'user'@'localhost';

-- Oracle
GRANT SELECT ON schema.table_name TO user;
```

3. **Column Level**
```sql
-- MySQL/MariaDB
GRANT SELECT (column1, column2) ON database_name.table_name TO 'user'@'localhost';

-- Oracle
GRANT SELECT (column1, column2) ON schema.table_name TO user;
```

## Best Security Practices

### 1. Password Policies
```sql
-- MySQL/MariaDB
SET GLOBAL validate_password.policy = STRONG;
SET GLOBAL validate_password.length = 12;

-- Oracle
ALTER PROFILE default LIMIT
  PASSWORD_LIFE_TIME 60
  FAILED_LOGIN_ATTEMPTS 3
  PASSWORD_LOCK_TIME 1/24;
```

### 2. Network Security
```ini
# MySQL configuration (my.cnf)
[mysqld]
bind-address = 127.0.0.1
skip-networking = false
```

### 3. Encryption
```sql
-- MySQL/MariaDB: Enable SSL
ALTER USER 'user'@'localhost' REQUIRE SSL;

-- Oracle: Enable TLS
ALTER SYSTEM SET WALLET_LOCATION = 
  'file:/u01/app/oracle/admin/orcl/wallet' SCOPE = BOTH;
```

## Regular Security Maintenance

### 1. Audit User Access
```sql
-- MySQL/MariaDB
SELECT user, host FROM mysql.user;
SHOW GRANTS FOR 'user'@'localhost';

-- Oracle
SELECT * FROM dba_users WHERE account_status = 'OPEN';
SELECT * FROM dba_role_privs;
```

### 2. Remove Unused Accounts
```sql
-- MySQL/MariaDB
DROP USER 'unused'@'localhost';

-- Oracle
DROP USER unused CASCADE;
```

### 3. Review Permissions
```sql
-- MySQL/MariaDB
SELECT * FROM information_schema.user_privileges;

-- Oracle
SELECT * FROM dba_sys_privs;
SELECT * FROM dba_tab_privs;
```

## Security Monitoring

### 1. Login Attempts
```sql
-- MySQL/MariaDB
SHOW GLOBAL STATUS LIKE '%failed_login%';

-- Oracle
SELECT * FROM dba_audit_trail 
WHERE action_name = 'LOGON' 
AND returncode != 0;
```

### 2. Suspicious Activity
```sql
-- MySQL/MariaDB
SELECT * FROM mysql.general_log 
WHERE event_time > DATE_SUB(NOW(), INTERVAL 1 DAY);

-- Oracle
SELECT * FROM unified_audit_trail 
WHERE event_timestamp > SYSTIMESTAMP - INTERVAL '1' DAY;
```

## Implementing Security with Python

### 1. Secure Connection Setup
```python
import mysql.connector
from ssl import create_default_context

# Create SSL context
ssl_context = create_default_context(
    cafile="/path/to/ca-cert.pem"
)

# Connect with SSL
cnx = mysql.connector.connect(
    user='user',
    password='pass',
    host='localhost',
    database='db',
    ssl_ca='/path/to/ca-cert.pem'
)
```

### 2. Password Hashing
```python
import hashlib
import os

def hash_password(password):
    """Hash a password for storing."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt + key

def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:32]
    stored_key = stored_password[32:]
    key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    return key == stored_key
```

## Emergency Security Procedures

### 1. Security Breach Response
```sql
-- MySQL/MariaDB
-- Lock down all accounts
UPDATE mysql.user SET account_locked = 'Y';
FLUSH PRIVILEGES;

-- Oracle
-- Lock all non-system accounts
BEGIN
  FOR r IN (SELECT username FROM dba_users 
            WHERE account_status = 'OPEN'
            AND username NOT IN ('SYS','SYSTEM'))
  LOOP
    EXECUTE IMMEDIATE 'ALTER USER '||r.username||' ACCOUNT LOCK';
  END LOOP;
END;
/
```

### 2. Audit Trail Review
```sql
-- MySQL/MariaDB
SELECT * FROM mysql.general_log 
WHERE event_time > DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY event_time DESC;

-- Oracle
SELECT username, action_name, event_timestamp
FROM unified_audit_trail
WHERE event_timestamp > SYSTIMESTAMP - INTERVAL '1' HOUR
ORDER BY event_timestamp DESC;
```

## Security Checklist

### Daily Tasks
1. Review failed login attempts
2. Check for unauthorized privilege escalations
3. Monitor database access patterns
4. Verify SSL/TLS certificates

### Weekly Tasks
1. Review user permissions
2. Check for inactive accounts
3. Analyze audit logs
4. Update security patches

### Monthly Tasks
1. Conduct security audit
2. Review security policies
3. Test disaster recovery
4. Update documentation

## Additional Security Tools

### 1. Database Firewalls
- Configure allowed IP ranges
- Set up connection rules
- Monitor traffic patterns

### 2. Intrusion Detection
- Set up alerts for suspicious queries
- Monitor for SQL injection attempts
- Track unusual access patterns

### 3. Encryption Tools
- Data at rest encryption
- Transparent Data Encryption (TDE)
- Secure backup encryption
