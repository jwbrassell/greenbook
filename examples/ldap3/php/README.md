# LDAP3 with PHP Examples

## Table of Contents
- [LDAP3 with PHP Examples](#ldap3-with-php-examples)
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
php/
├── basic/
│   ├── connection/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── config.php
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

1. Install Dependencies:
```bash
composer require symfony/ldap
```

2. Configure LDAP Connection:
```php
<?php
// config.php
return [
    'ldap' => [
        'host' => 'ldap://your-ldap-server:389',
        'base_dn' => 'dc=example,dc=com',
        'bind_dn' => 'cn=admin,dc=example,dc=com',
        'bind_password' => 'your-password'
    ]
];
```

3. Basic Setup:
```php
<?php
require 'vendor/autoload.php';

use Symfony\Component\Ldap\Ldap;
use Symfony\Component\Ldap\Entry;
```

## Basic Operations

### Server Connection
```php
<?php
class LdapClient {
    private $ldap;
    private $config;
    
    public function __construct() {
        $this->config = require 'config.php';
        $this->ldap = Ldap::create('ext_ldap', [
            'host' => $this->config['ldap']['host']
        ]);
    }
    
    public function connect() {
        try {
            $this->ldap->bind(
                $this->config['ldap']['bind_dn'],
                $this->config['ldap']['bind_password']
            );
            return true;
        } catch (Exception $e) {
            error_log("Connection failed: " . $e->getMessage());
            return false;
        }
    }
}
```

### User Management
```php
<?php
class UserManager {
    private $ldap;
    private $base_dn;
    
    public function __construct(Ldap $ldap, $base_dn) {
        $this->ldap = $ldap;
        $this->base_dn = $base_dn;
    }
    
    public function createUser($username, $firstname, $lastname, $password) {
        $dn = "cn=$username," . $this->base_dn;
        
        $entry = new Entry($dn, [
            'objectClass' => ['top', 'person', 'organizationalPerson', 'user'],
            'cn' => [$username],
            'givenName' => [$firstname],
            'sn' => [$lastname],
            'userPassword' => [$password]
        ]);
        
        return $this->ldap->add($entry);
    }
    
    public function getUser($username) {
        $query = $this->ldap->query(
            $this->base_dn,
            "(cn=$username)"
        );
        
        $results = $query->execute();
        return $results->count() > 0 ? $results[0] : null;
    }
    
    public function updateUser($username, $attributes) {
        $user = $this->getUser($username);
        if (!$user) {
            throw new Exception("User not found");
        }
        
        $entry = new Entry($user->getDn(), $attributes);
        return $this->ldap->update($entry);
    }
    
    public function deleteUser($username) {
        $user = $this->getUser($username);
        if (!$user) {
            throw new Exception("User not found");
        }
        
        return $this->ldap->delete($user);
    }
}
```

### Group Operations
```php
<?php
class GroupManager {
    private $ldap;
    private $base_dn;
    
    public function __construct(Ldap $ldap, $base_dn) {
        $this->ldap = $ldap;
        $this->base_dn = $base_dn;
    }
    
    public function createGroup($groupname, $description = null) {
        $dn = "cn=$groupname,ou=groups," . $this->base_dn;
        
        $attributes = [
            'objectClass' => ['top', 'group'],
            'cn' => [$groupname]
        ];
        
        if ($description) {
            $attributes['description'] = [$description];
        }
        
        $entry = new Entry($dn, $attributes);
        return $this->ldap->add($entry);
    }
    
    public function addUserToGroup($username, $groupname) {
        $user = $this->getUser($username);
        $group = $this->getGroup($groupname);
        
        if (!$user || !$group) {
            throw new Exception("User or group not found");
        }
        
        $entry = $group->getEntry();
        $entry->setAttribute('member', [$user->getDn()]);
        
        return $this->ldap->update($entry);
    }
    
    public function getUserGroups($username) {
        $user = $this->getUser($username);
        if (!$user) {
            throw new Exception("User not found");
        }
        
        $query = $this->ldap->query(
            $this->base_dn,
            "(&(objectClass=group)(member={$user->getDn()}))"
        );
        
        return $query->execute();
    }
}
```

## Advanced Features

### Complex Searches
```php
<?php
class DirectorySearcher {
    private $ldap;
    private $base_dn;
    
    public function __construct(Ldap $ldap, $base_dn) {
        $this->ldap = $ldap;
        $this->base_dn = $base_dn;
    }
    
    public function searchUsersByCriteria($criteria) {
        $filters = [];
        foreach ($criteria as $attr => $value) {
            $filters[] = "($attr=$value)";
        }
        
        $filter = "(&(objectClass=user)" . implode('', $filters) . ")";
        $query = $this->ldap->query($this->base_dn, $filter);
        
        return $query->execute();
    }
    
    public function findInactiveUsers($days = 30) {
        $threshold = date('YmdHis.0Z', strtotime("-$days days"));
        $filter = "(&(objectClass=user)(lastLogon<=$threshold))";
        
        $query = $this->ldap->query(
            $this->base_dn,
            $filter,
            ['filter' => ['cn', 'lastLogon']]
        );
        
        return $query->execute();
    }
}
```

### Schema Operations
```php
<?php
class SchemaManager {
    private $ldap;
    
    public function __construct(Ldap $ldap) {
        $this->ldap = $ldap;
    }
    
    public function getObjectClasses() {
        $query = $this->ldap->query(
            'cn=schema,cn=config',
            '(objectClass=ldapSubentry)'
        );
        
        return $query->execute();
    }
    
    public function addAttributeType($name, $syntax, $singleValue = false) {
        $oid = '1.3.6.1.4.1.X.Y.Z';  // Replace with your OID
        
        $schemaEntry = sprintf(
            '( %s NAME \'%s\' SYNTAX %s SINGLE-VALUE %s )',
            $oid,
            $name,
            $syntax,
            $singleValue ? 'TRUE' : 'FALSE'
        );
        
        $entry = new Entry('cn=schema,cn=config', [
            'attributeTypes' => [$schemaEntry]
        ]);
        
        return $this->ldap->update($entry);
    }
}
```

## Security Considerations

1. Certificate Handling:
```php
<?php
class SecureConnection {
    private $config;
    
    public function __construct($config) {
        $this->config = $config;
    }
    
    public function getSecureConnection() {
        $ldap = Ldap::create('ext_ldap', [
            'host' => $this->config['ldap']['host'],
            'encryption' => 'ssl',
            'options' => [
                'protocol_version' => 3,
                'referrals' => false,
                LDAP_OPT_X_TLS_REQUIRE_CERT => LDAP_OPT_X_TLS_HARD,
                LDAP_OPT_X_TLS_CACERTFILE => $this->config['ldap']['ca_cert']
            ]
        ]);
        
        $ldap->bind(
            $this->config['ldap']['bind_dn'],
            $this->config['ldap']['bind_password']
        );
        
        return $ldap;
    }
}
```

2. Password Policy:
```php
<?php
class PasswordManager {
    private $ldap;
    
    public function __construct(Ldap $ldap) {
        $this->ldap = $ldap;
    }
    
    public function changePassword($username, $oldPassword, $newPassword) {
        if (!$this->validatePassword($newPassword)) {
            throw new Exception("Password does not meet requirements");
        }
        
        $user = $this->getUser($username);
        if (!$user) {
            throw new Exception("User not found");
        }
        
        // Verify old password
        try {
            $this->ldap->bind($user->getDn(), $oldPassword);
        } catch (Exception $e) {
            throw new Exception("Invalid old password");
        }
        
        $entry = $user->getEntry();
        $entry->setAttribute('userPassword', [$newPassword]);
        
        return $this->ldap->update($entry);
    }
    
    private function validatePassword($password) {
        if (strlen($password) < 8) return false;
        if (!preg_match('/[A-Z]/', $password)) return false;
        if (!preg_match('/[a-z]/', $password)) return false;
        if (!preg_match('/[0-9]/', $password)) return false;
        return true;
    }
}
```

## Performance Optimization

1. Connection Pooling:
```php
<?php
class ConnectionPool {
    private static $instances = [];
    private static $maxInstances = 5;
    private $config;
    
    public function __construct($config) {
        $this->config = $config;
    }
    
    public function getConnection() {
        if (count(self::$instances) < self::$maxInstances) {
            $ldap = Ldap::create('ext_ldap', [
                'host' => $this->config['ldap']['host']
            ]);
            
            $ldap->bind(
                $this->config['ldap']['bind_dn'],
                $this->config['ldap']['bind_password']
            );
            
            self::$instances[] = $ldap;
            return $ldap;
        }
        
        return self::$instances[0];  // Round-robin
    }
}
```

2. Search Optimization:
```php
<?php
class OptimizedSearcher {
    private $ldap;
    
    public function __construct(Ldap $ldap) {
        $this->ldap = $ldap;
    }
    
    public function pagedSearch($base, $filter, $pageSize = 100) {
        $cookie = '';
        
        do {
            $query = $this->ldap->query(
                $base,
                $filter,
                [
                    'maxItems' => $pageSize,
                    'pageSize' => $pageSize,
                    'cookie' => $cookie
                ]
            );
            
            $results = $query->execute();
            foreach ($results as $entry) {
                yield $entry;
            }
            
            $cookie = $query->getResponseServerControls()['1.2.840.113556.1.4.319']['cookie'];
        } while (!empty($cookie));
    }
}
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class LdapTests extends TestCase {
    private $ldap;
    
    protected function setUp(): void {
        $config = require 'config.php';
        $this->ldap = Ldap::create('ext_ldap', [
            'host' => $config['ldap']['host']
        ]);
    }
    
    public function testUserCreation() {
        $manager = new UserManager($this->ldap);
        $result = $manager->createUser(
            'testuser',
            'Test',
            'User',
            'password123'
        );
        
        $this->assertTrue($result);
    }
    
    public function testGroupOperations() {
        $manager = new GroupManager($this->ldap);
        
        // Create group
        $manager->createGroup('testgroup', 'Test Group');
        
        // Add user
        $manager->addUserToGroup('testuser', 'testgroup');
        
        // Verify membership
        $groups = $manager->getUserGroups('testuser');
        $this->assertEquals(1, count($groups));
        $this->assertEquals('testgroup', $groups[0]->get('cn')[0]);
    }
}
```

2. Integration Tests:
```php
<?php
class LdapIntegrationTests extends TestCase {
    private $ldap;
    private $userManager;
    private $groupManager;
    
    protected function setUp(): void {
        $config = require 'config.php';
        $this->ldap = Ldap::create('ext_ldap', [
            'host' => $config['ldap']['host']
        ]);
        
        $this->userManager = new UserManager($this->ldap);
        $this->groupManager = new GroupManager($this->ldap);
    }
    
    public function testUserWorkflow() {
        // Create user
        $username = 'integrationtest';
        $this->userManager->createUser(
            $username,
            'Integration',
            'Test',
            'password123'
        );
        
        // Update user
        $this->userManager->updateUser(
            $username,
            ['title' => 'Test User']
        );
        
        // Verify changes
        $user = $this->userManager->getUser($username);
        $this->assertEquals('Test User', $user->get('title')[0]);
        
        // Clean up
        $this->userManager->deleteUser($username);
    }
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
