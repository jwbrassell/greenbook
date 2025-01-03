# F5 API with PHP Examples

## Table of Contents
- [F5 API with PHP Examples](#f5-api-with-php-examples)
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
   - Authentication and connection
   - Virtual server management
   - Pool management
   - Node management

2. Advanced Features
   - iRules management
   - SSL profile handling
   - Health monitoring
   - Traffic management

3. Integration Features
   - Load balancer automation
   - Configuration management
   - Monitoring integration
   - Backup operations

4. Full Applications
   - Load balancer dashboard
   - Configuration manager
   - Health monitor
   - Deployment automator

## Project Structure

```
php/
├── basic/
│   ├── connection/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── config.php
│   ├── virtual_servers/
│   ├── pools/
│   └── nodes/
├── advanced/
│   ├── irules/
│   ├── ssl_profiles/
│   ├── monitors/
│   └── traffic/
├── integration/
│   ├── automation/
│   ├── config_mgmt/
│   ├── monitoring/
│   └── backup/
└── applications/
    ├── lb_dashboard/
    ├── config_manager/
    ├── health_monitor/
    └── deploy_automator/
```

## Getting Started

1. Install Dependencies:
```bash
composer require guzzlehttp/guzzle
```

2. Configure F5 Connection:
```php
<?php
// config.php
return [
    'f5' => [
        'host' => 'https://your-f5-host',
        'username' => 'admin',
        'password' => 'your-password',
        'verify_ssl' => false  // Set to true in production
    ]
];
```

3. Basic Setup:
```php
<?php
require 'vendor/autoload.php';

use GuzzleHttp\Client;
use GuzzleHttp\Exception\RequestException;
```

## Basic Operations

### Connection Management
```php
<?php
class F5Client {
    private $client;
    private $config;
    private $token;
    
    public function __construct() {
        $this->config = require 'config.php';
        $this->client = new Client([
            'base_uri' => $this->config['f5']['host'],
            'verify' => $this->config['f5']['verify_ssl']
        ]);
    }
    
    public function connect() {
        try {
            $response = $this->client->post('/mgmt/shared/authn/login', [
                'json' => [
                    'username' => $this->config['f5']['username'],
                    'password' => $this->config['f5']['password']
                ]
            ]);
            
            $data = json_decode($response->getBody(), true);
            $this->token = $data['token']['token'];
            return true;
        } catch (RequestException $e) {
            error_log("Connection failed: " . $e->getMessage());
            return false;
        }
    }
    
    public function request($method, $endpoint, $data = null) {
        $options = [
            'headers' => [
                'X-F5-Auth-Token' => $this->token
            ]
        ];
        
        if ($data) {
            $options['json'] = $data;
        }
        
        return $this->client->request($method, $endpoint, $options);
    }
}
```

### Virtual Server Management
```php
<?php
class VirtualServerManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function createVirtual($name, $destination, $port, $pool = null) {
        try {
            $data = [
                'name' => $name,
                'partition' => 'Common',
                'destination' => "/Common/{$destination}:{$port}",
                'sourceAddressTranslation' => ['type' => 'automap'],
                'profiles' => [['name' => 'tcp']]
            ];
            
            if ($pool) {
                $data['pool'] = "/Common/{$pool}";
            }
            
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/ltm/virtual',
                $data
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to create virtual server: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function getVirtual($name) {
        try {
            $response = $this->client->request(
                'GET',
                "/mgmt/tm/ltm/virtual/~Common~{$name}"
            );
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            if ($e->getResponse()->getStatusCode() === 404) {
                return null;
            }
            throw $e;
        }
    }
    
    public function updateVirtual($name, $properties) {
        $virtual = $this->getVirtual($name);
        if (!$virtual) {
            throw new Exception("Virtual server {$name} not found");
        }
        
        try {
            $response = $this->client->request(
                'PATCH',
                "/mgmt/tm/ltm/virtual/~Common~{$name}",
                $properties
            );
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to update virtual server: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function deleteVirtual($name) {
        try {
            $this->client->request(
                'DELETE',
                "/mgmt/tm/ltm/virtual/~Common~{$name}"
            );
            return true;
        } catch (RequestException $e) {
            error_log("Failed to delete virtual server: " . $e->getMessage());
            throw $e;
        }
    }
}
```

### Pool Management
```php
<?php
class PoolManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function createPool($name, $lbMethod = 'round-robin', $monitor = null) {
        try {
            $data = [
                'name' => $name,
                'partition' => 'Common',
                'loadBalancingMode' => $lbMethod
            ];
            
            if ($monitor) {
                $data['monitor'] = "/Common/{$monitor}";
            }
            
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/ltm/pool',
                $data
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to create pool: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function addPoolMember($poolName, $nodeName, $port) {
        try {
            $response = $this->client->request(
                'POST',
                "/mgmt/tm/ltm/pool/~Common~{$poolName}/members",
                [
                    'name' => "{$nodeName}:{$port}",
                    'partition' => 'Common'
                ]
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to add pool member: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function getPoolStatus($name) {
        try {
            $response = $this->client->request(
                'GET',
                "/mgmt/tm/ltm/pool/~Common~{$name}/stats"
            );
            
            $data = json_decode($response->getBody(), true);
            return [
                'status' => $data['entries']['status']['value'],
                'current_connections' => $data['entries']['serverside.curConns']['value'],
                'total_connections' => $data['entries']['serverside.totConns']['value']
            ];
        } catch (RequestException $e) {
            error_log("Failed to get pool status: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Advanced Features

### iRules Management
```php
<?php
class iRuleManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function createIRule($name, $content) {
        try {
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/ltm/rule',
                [
                    'name' => $name,
                    'partition' => 'Common',
                    'apiAnonymous' => $content
                ]
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to create iRule: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function attachIRuleToVirtual($iruleName, $virtualName) {
        try {
            $virtual = $this->getVirtual($virtualName);
            if (!$virtual) {
                throw new Exception("Virtual server not found");
            }
            
            $rules = $virtual['rules'] ?? [];
            $rules[] = "/Common/{$iruleName}";
            
            return $this->updateVirtual($virtualName, ['rules' => $rules]);
        } catch (Exception $e) {
            error_log("Failed to attach iRule: " . $e->getMessage());
            throw $e;
        }
    }
}
```

### SSL Profile Management
```php
<?php
class SSLProfileManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function createClientSSLProfile($name, $cert, $key, $chain = null) {
        try {
            $data = [
                'name' => $name,
                'partition' => 'Common',
                'cert' => "/Common/{$cert}",
                'key' => "/Common/{$key}"
            ];
            
            if ($chain) {
                $data['chain'] = "/Common/{$chain}";
            }
            
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/ltm/profile/client-ssl',
                $data
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to create SSL profile: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Security Considerations

1. Certificate Management:
```php
<?php
class CertificateManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function installCertificate($name, $certContent) {
        try {
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/sys/crypto/cert',
                [
                    'name' => $name,
                    'partition' => 'Common',
                    'fromLocalFile' => $certContent
                ]
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to install certificate: " . $e->getMessage());
            throw $e;
        }
    }
}
```

2. Access Control:
```php
<?php
class AccessManager {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function createAccessPolicy($name, $rules) {
        try {
            $response = $this->client->request(
                'POST',
                '/mgmt/tm/apm/policy/access-policy',
                [
                    'name' => $name,
                    'partition' => 'Common',
                    'rules' => $rules
                ]
            );
            
            return json_decode($response->getBody(), true);
        } catch (RequestException $e) {
            error_log("Failed to create access policy: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Performance Optimization

1. Connection Handling:
```php
<?php
class ConnectionOptimizer {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function optimizeVirtualServer($name) {
        try {
            return $this->updateVirtual($name, [
                'profiles' => [
                    ['name' => 'tcp-wan-optimized'],
                    ['name' => 'http-acceleration']
                ],
                'rateLimitMode' => 'object',
                'maxConnections' => 10000
            ]);
        } catch (Exception $e) {
            error_log("Failed to optimize virtual server: " . $e->getMessage());
            throw $e;
        }
    }
}
```

2. Monitoring:
```php
<?php
class PerformanceMonitor {
    private $client;
    
    public function __construct(F5Client $client) {
        $this->client = $client;
    }
    
    public function getVirtualStats($name) {
        try {
            $response = $this->client->request(
                'GET',
                "/mgmt/tm/ltm/virtual/~Common~{$name}/stats"
            );
            
            $data = json_decode($response->getBody(), true);
            return [
                'current_connections' => $data['entries']['clientside.curConns']['value'],
                'total_connections' => $data['entries']['clientside.totConns']['value'],
                'bytes_in' => $data['entries']['clientside.bitsIn']['value'],
                'bytes_out' => $data['entries']['clientside.bitsOut']['value']
            ];
        } catch (RequestException $e) {
            error_log("Failed to get statistics: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class F5Tests extends TestCase {
    private $client;
    
    protected function setUp(): void {
        $this->client = new F5Client();
        $this->client->connect();
    }
    
    public function testVirtualServerCreation() {
        $manager = new VirtualServerManager($this->client);
        $result = $manager->createVirtual(
            'test_virtual',
            '192.168.1.10',
            80
        );
        
        $this->assertNotNull($result);
    }
    
    public function testPoolOperations() {
        $manager = new PoolManager($this->client);
        
        // Create pool
        $pool = $manager->createPool('test_pool');
        
        // Add member
        $member = $manager->addPoolMember(
            'test_pool',
            '192.168.1.20',
            80
        );
        
        // Verify status
        $status = $manager->getPoolStatus('test_pool');
        $this->assertEquals('available', $status['status']);
    }
}
```

2. Integration Tests:
```php
<?php
class F5IntegrationTests extends TestCase {
    private $client;
    private $vsManager;
    private $poolManager;
    
    protected function setUp(): void {
        $this->client = new F5Client();
        $this->client->connect();
        
        $this->vsManager = new VirtualServerManager($this->client);
        $this->poolManager = new PoolManager($this->client);
    }
    
    public function testLoadBalancingWorkflow() {
        // Create pool
        $pool = $this->poolManager->createPool('integration_pool');
        
        // Add members
        $this->poolManager->addPoolMember(
            'integration_pool',
            '192.168.1.21',
            80
        );
        $this->poolManager->addPoolMember(
            'integration_pool',
            '192.168.1.22',
            80
        );
        
        // Create virtual server
        $vs = $this->vsManager->createVirtual(
            'integration_vs',
            '192.168.1.100',
            80,
            'integration_pool'
        );
        
        // Verify configuration
        $this->assertEquals(
            '/Common/integration_pool',
            $vs['pool']
        );
        
        // Clean up
        $this->vsManager->deleteVirtual('integration_vs');
        $this->poolManager->deletePool('integration_pool');
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
