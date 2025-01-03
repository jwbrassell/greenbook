# OpenStack with PHP Examples

## Table of Contents
- [OpenStack with PHP Examples](#openstack-with-php-examples)
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
   - Instance management
   - Volume management
   - Network management

2. Advanced Features
   - Load balancing
   - Auto scaling
   - High availability
   - Monitoring

3. Integration Features
   - Service orchestration
   - Resource management
   - Backup automation
   - Monitoring integration

4. Full Applications
   - Cloud dashboard
   - Resource manager
   - Monitoring system
   - Deployment automator

## Project Structure

```
php/
├── basic/
│   ├── connection/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── config.php
│   ├── instances/
│   ├── volumes/
│   └── networks/
├── advanced/
│   ├── load_balancing/
│   ├── auto_scaling/
│   ├── high_availability/
│   └── monitoring/
├── integration/
│   ├── orchestration/
│   ├── resource_mgmt/
│   ├── backup/
│   └── monitoring/
└── applications/
    ├── cloud_dashboard/
    ├── resource_manager/
    ├── monitor_system/
    └── deploy_automator/
```

## Getting Started

1. Install Dependencies:
```bash
composer require php-opencloud/openstack
```

2. Configure OpenStack Connection:
```php
<?php
// config.php
return [
    'openstack' => [
        'auth_url' => 'http://your-openstack-host:5000/v3',
        'username' => 'admin',
        'password' => 'your-password',
        'project_name' => 'admin',
        'user_domain_name' => 'Default',
        'project_domain_name' => 'Default'
    ]
];
```

3. Basic Setup:
```php
<?php
require 'vendor/autoload.php';

use OpenStack\OpenStack;
```

## Basic Operations

### Connection Management
```php
<?php
class OpenStackClient {
    private $client;
    private $config;
    
    public function __construct() {
        $this->config = require 'config.php';
        $this->client = new OpenStack([
            'authUrl' => $this->config['openstack']['auth_url'],
            'region'  => 'RegionOne',
            'user'    => [
                'name'     => $this->config['openstack']['username'],
                'password' => $this->config['openstack']['password'],
                'domain'   => ['name' => $this->config['openstack']['user_domain_name']]
            ],
            'scope'   => [
                'project' => [
                    'name'   => $this->config['openstack']['project_name'],
                    'domain' => ['name' => $this->config['openstack']['project_domain_name']]
                ]
            ]
        ]);
    }
    
    public function getService($type, $version = null) {
        return $this->client->serviceBuilder->get($type, $version);
    }
    
    public function testConnection() {
        try {
            $compute = $this->getService('compute');
            $compute->listFlavors();
            return true;
        } catch (Exception $e) {
            error_log("Connection failed: " . $e->getMessage());
            return false;
        }
    }
}
```

### Instance Management
```php
<?php
class InstanceManager {
    private $compute;
    private $network;
    
    public function __construct(OpenStackClient $client) {
        $this->compute = $client->getService('compute');
        $this->network = $client->getService('network');
    }
    
    public function createInstance($name, $flavorName, $imageName, $networkName) {
        try {
            // Get required resources
            $flavor = $this->getFlavor($flavorName);
            $image = $this->getImage($imageName);
            $network = $this->getNetwork($networkName);
            
            // Create instance
            $server = $this->compute->createServer([
                'name'     => $name,
                'flavorId' => $flavor->id,
                'imageId'  => $image->id,
                'networks' => [['uuid' => $network->id]]
            ]);
            
            // Wait for instance to be ready
            $this->waitForStatus($server, 'ACTIVE');
            return $server;
        } catch (Exception $e) {
            error_log("Failed to create instance: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function getInstance($name) {
        try {
            $servers = $this->compute->listServers([
                'name' => $name
            ]);
            
            foreach ($servers as $server) {
                if ($server->name === $name) {
                    return $server;
                }
            }
            return null;
        } catch (Exception $e) {
            error_log("Failed to get instance: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function deleteInstance($name) {
        try {
            $server = $this->getInstance($name);
            if (!$server) {
                throw new Exception("Instance $name not found");
            }
            
            $server->delete();
            return true;
        } catch (Exception $e) {
            error_log("Failed to delete instance: " . $e->getMessage());
            throw $e;
        }
    }
    
    private function waitForStatus($server, $status, $timeout = 300) {
        $start = time();
        while (time() - $start < $timeout) {
            $server->retrieve();
            if ($server->status === $status) {
                return true;
            }
            sleep(5);
        }
        throw new Exception("Timeout waiting for status $status");
    }
}
```

### Volume Management
```php
<?php
class VolumeManager {
    private $volume;
    private $compute;
    
    public function __construct(OpenStackClient $client) {
        $this->volume = $client->getService('block-storage');
        $this->compute = $client->getService('compute');
    }
    
    public function createVolume($name, $size, $volumeType = null) {
        try {
            $options = [
                'name' => $name,
                'size' => $size
            ];
            
            if ($volumeType) {
                $options['volumeType'] = $volumeType;
            }
            
            $volume = $this->volume->createVolume($options);
            $this->waitForStatus($volume, 'available');
            return $volume;
        } catch (Exception $e) {
            error_log("Failed to create volume: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function attachVolume($volumeName, $instanceName, $device = '/dev/vdb') {
        try {
            $volume = $this->getVolume($volumeName);
            $server = $this->compute->getServer(['name' => $instanceName]);
            
            if (!$volume || !$server) {
                throw new Exception("Volume or instance not found");
            }
            
            $server->attachVolume($volume->id, [
                'mountpoint' => $device
            ]);
            
            $this->waitForStatus($volume, 'in-use');
            return true;
        } catch (Exception $e) {
            error_log("Failed to attach volume: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Advanced Features

### Load Balancing
```php
<?php
class LoadBalancerManager {
    private $network;
    
    public function __construct(OpenStackClient $client) {
        $this->network = $client->getService('network');
    }
    
    public function createLoadBalancer($name, $subnetName, $algorithm = 'ROUND_ROBIN') {
        try {
            $subnet = $this->getSubnet($subnetName);
            
            $lb = $this->network->createLoadBalancer([
                'name' => $name,
                'vipSubnetId' => $subnet->id,
                'adminStateUp' => true
            ]);
            
            $this->waitForStatus($lb, 'ACTIVE');
            return $lb;
        } catch (Exception $e) {
            error_log("Failed to create load balancer: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function addListener($lbName, $protocol, $port) {
        try {
            $lb = $this->getLoadBalancer($lbName);
            
            $listener = $this->network->createListener([
                'name' => "{$lbName}-listener",
                'loadbalancerId' => $lb->id,
                'protocol' => $protocol,
                'protocolPort' => $port,
                'adminStateUp' => true
            ]);
            
            return $listener;
        } catch (Exception $e) {
            error_log("Failed to add listener: " . $e->getMessage());
            throw $e;
        }
    }
}
```

### Auto Scaling
```php
<?php
class AutoScalingManager {
    private $orchestration;
    
    public function __construct(OpenStackClient $client) {
        $this->orchestration = $client->getService('orchestration');
    }
    
    public function createScalingGroup($name, $minSize, $maxSize, $template) {
        try {
            $stack = $this->orchestration->createStack([
                'name' => $name,
                'template' => $template,
                'parameters' => [
                    'min_size' => $minSize,
                    'max_size' => $maxSize
                ]
            ]);
            
            $this->waitForStackStatus($stack, 'CREATE_COMPLETE');
            return $stack;
        } catch (Exception $e) {
            error_log("Failed to create scaling group: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Security Considerations

1. Network Security:
```php
<?php
class SecurityManager {
    private $network;
    
    public function __construct(OpenStackClient $client) {
        $this->network = $client->getService('network');
    }
    
    public function createSecurityGroup($name, $description) {
        try {
            $secgroup = $this->network->createSecurityGroup([
                'name' => $name,
                'description' => $description
            ]);
            return $secgroup;
        } catch (Exception $e) {
            error_log("Failed to create security group: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function addSecurityRule($groupName, $protocol, $portRange) {
        try {
            $group = $this->getSecurityGroup($groupName);
            
            $rule = $this->network->createSecurityGroupRule([
                'securityGroupId' => $group->id,
                'protocol' => $protocol,
                'portRangeMin' => $portRange[0],
                'portRangeMax' => $portRange[1],
                'direction' => 'ingress'
            ]);
            
            return $rule;
        } catch (Exception $e) {
            error_log("Failed to add security rule: " . $e->getMessage());
            throw $e;
        }
    }
}
```

2. Access Control:
```php
<?php
class RoleManager {
    private $identity;
    
    public function __construct(OpenStackClient $client) {
        $this->identity = $client->getService('identity');
    }
    
    public function createRole($name) {
        try {
            $role = $this->identity->createRole([
                'name' => $name
            ]);
            return $role;
        } catch (Exception $e) {
            error_log("Failed to create role: " . $e->getMessage());
            throw $e;
        }
    }
    
    public function assignRole($roleName, $userName, $projectName) {
        try {
            $role = $this->getRole($roleName);
            $user = $this->getUser($userName);
            $project = $this->getProject($projectName);
            
            $this->identity->grantProjectUserRole([
                'roleId' => $role->id,
                'userId' => $user->id,
                'projectId' => $project->id
            ]);
            
            return true;
        } catch (Exception $e) {
            error_log("Failed to assign role: " . $e->getMessage());
            throw $e;
        }
    }
}
```

## Performance Optimization

1. Resource Management:
```php
<?php
class ResourceOptimizer {
    private $compute;
    
    public function __construct(OpenStackClient $client) {
        $this->compute = $client->getService('compute');
    }
    
    public function optimizeFlavor($instanceName) {
        try {
            $server = $this->compute->getServer(['name' => $instanceName]);
            $stats = $this->getInstanceStats($server);
            
            if ($stats['cpu_util'] < 20 && $stats['memory_util'] < 30) {
                $smallerFlavor = $this->findSmallerFlavor($server->flavor);
                if ($smallerFlavor) {
                    $server->resize($smallerFlavor->id);
                    return true;
                }
            }
            
            return false;
        } catch (Exception $e) {
            error_log("Failed to optimize flavor: " . $e->getMessage());
            throw $e;
        }
    }
}
```

2. Monitoring:
```php
<?php
class PerformanceMonitor {
    private $telemetry;
    
    public function __construct(OpenStackClient $client) {
        $this->telemetry = $client->getService('telemetry');
    }
    
    public function getInstanceMetrics($instanceName, $metricName, $period = 3600) {
        try {
            $server = $this->compute->getServer(['name' => $instanceName]);
            
            $samples = $this->telemetry->listSamples([
                'meter' => $metricName,
                'q' => [
                    ['field' => 'resource_id', 'op' => 'eq', 'value' => $server->id]
                ],
                'limit' => 100
            ]);
            
            return array_map(function($sample) {
                return [
                    'timestamp' => $sample->timestamp,
                    'value' => $sample->volume
                ];
            }, iterator_to_array($samples));
        } catch (Exception $e) {
            error_log("Failed to get metrics: " . $e->getMessage());
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

class OpenStackTests extends TestCase {
    private $client;
    
    protected function setUp(): void {
        $this->client = new OpenStackClient();
    }
    
    public function testInstanceCreation() {
        $manager = new InstanceManager($this->client);
        $instance = $manager->createInstance(
            'test-instance',
            'm1.small',
            'ubuntu-20.04',
            'private-net'
        );
        
        $this->assertNotNull($instance);
        $this->assertEquals('ACTIVE', $instance->status);
    }
    
    public function testVolumeOperations() {
        $manager = new VolumeManager($this->client);
        
        // Create volume
        $volume = $manager->createVolume('test-volume', 10);
        
        // Attach to instance
        $result = $manager->attachVolume(
            'test-volume',
            'test-instance'
        );
        
        $this->assertTrue($result);
        $this->assertEquals('in-use', $volume->status);
    }
}
```

2. Integration Tests:
```php
<?php
class OpenStackIntegrationTests extends TestCase {
    private $instanceManager;
    private $volumeManager;
    private $networkManager;
    
    protected function setUp(): void {
        $client = new OpenStackClient();
        $this->instanceManager = new InstanceManager($client);
        $this->volumeManager = new VolumeManager($client);
        $this->networkManager = new NetworkManager($client);
    }
    
    public function testFullDeployment() {
        // Create network
        $network = $this->networkManager->createNetwork(
            'test-net',
            'test-subnet',
            '192.168.1.0/24'
        );
        
        // Create instance
        $instance = $this->instanceManager->createInstance(
            'test-instance',
            'm1.small',
            'ubuntu-20.04',
            'test-net'
        );
        
        // Create and attach volume
        $volume = $this->volumeManager->createVolume(
            'test-volume',
            10
        );
        $this->volumeManager->attachVolume(
            'test-volume',
            'test-instance'
        );
        
        // Verify setup
        $this->assertEquals('ACTIVE', $instance->status);
        $this->assertEquals('in-use', $volume->status);
        
        // Clean up
        $this->volumeManager->detachVolume('test-volume');
        $this->instanceManager->deleteInstance('test-instance');
        $this->networkManager->deleteNetwork('test-net');
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
