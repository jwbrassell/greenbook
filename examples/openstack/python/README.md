# OpenStack with Python Examples

## Table of Contents
- [OpenStack with Python Examples](#openstack-with-python-examples)
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
python/
├── basic/
│   ├── connection/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── config.py
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

3. Configure OpenStack Connection:
```python
# config.py
OPENSTACK_AUTH_URL = "http://your-openstack-host:5000/v3"
OPENSTACK_USERNAME = "admin"
OPENSTACK_PASSWORD = "your-password"
OPENSTACK_PROJECT_NAME = "admin"
OPENSTACK_USER_DOMAIN_NAME = "Default"
OPENSTACK_PROJECT_DOMAIN_NAME = "Default"
```

## Basic Operations

### Connection Management
```python
from keystoneauth1.identity import v3
from keystoneauth1 import session
from novaclient import client as nova_client
from cinderclient import client as cinder_client
from neutronclient.v2_0 import client as neutron_client
from config import *

def get_openstack_clients():
    """Create authenticated OpenStack clients"""
    try:
        auth = v3.Password(
            auth_url=OPENSTACK_AUTH_URL,
            username=OPENSTACK_USERNAME,
            password=OPENSTACK_PASSWORD,
            project_name=OPENSTACK_PROJECT_NAME,
            user_domain_name=OPENSTACK_USER_DOMAIN_NAME,
            project_domain_name=OPENSTACK_PROJECT_DOMAIN_NAME
        )
        
        sess = session.Session(auth=auth)
        
        return {
            'compute': nova_client.Client('2', session=sess),
            'volume': cinder_client.Client('3', session=sess),
            'network': neutron_client.Client(session=sess)
        }
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        raise

def test_connection():
    """Test OpenStack connection"""
    try:
        clients = get_openstack_clients()
        # Test compute service
        clients['compute'].flavors.list()
        print("Connected successfully")
        return True
    except Exception as e:
        print(f"Connection failed: {str(e)}")
        return False
```

### Instance Management
```python
class InstanceManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.nova = clients['compute']
        self.neutron = clients['network']
    
    def create_instance(self, name, flavor_name, image_name, network_name):
        """Create new instance"""
        try:
            # Get required resources
            flavor = self.nova.flavors.find(name=flavor_name)
            image = self.nova.images.find(name=image_name)
            network = self.neutron.list_networks(name=network_name)['networks'][0]
            
            # Create instance
            instance = self.nova.servers.create(
                name=name,
                flavor=flavor,
                image=image,
                nics=[{'net-id': network['id']}]
            )
            
            # Wait for instance to be ready
            self._wait_for_status(instance, 'ACTIVE')
            return instance
        except Exception as e:
            print(f"Failed to create instance: {str(e)}")
            raise
    
    def get_instance(self, name):
        """Get instance by name"""
        try:
            return self.nova.servers.find(name=name)
        except Exception as e:
            print(f"Instance not found: {str(e)}")
            return None
    
    def delete_instance(self, name):
        """Delete instance"""
        instance = self.get_instance(name)
        if not instance:
            raise ValueError(f"Instance {name} not found")
        
        try:
            instance.delete()
            self._wait_for_deletion(instance)
            return True
        except Exception as e:
            print(f"Failed to delete instance: {str(e)}")
            raise
    
    def _wait_for_status(self, instance, status, timeout=300):
        """Wait for instance to reach desired status"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            instance.get()
            if instance.status == status:
                return True
            time.sleep(5)
        raise TimeoutError(f"Instance failed to reach {status} status")
    
    def _wait_for_deletion(self, instance, timeout=300):
        """Wait for instance to be deleted"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                instance.get()
                time.sleep(5)
            except Exception:
                return True
        raise TimeoutError("Instance deletion timed out")
```

### Volume Management
```python
class VolumeManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.cinder = clients['volume']
        self.nova = clients['compute']
    
    def create_volume(self, name, size, volume_type=None):
        """Create new volume"""
        try:
            volume = self.cinder.volumes.create(
                name=name,
                size=size,
                volume_type=volume_type
            )
            self._wait_for_status(volume, 'available')
            return volume
        except Exception as e:
            print(f"Failed to create volume: {str(e)}")
            raise
    
    def attach_volume(self, volume_name, instance_name, device="/dev/vdb"):
        """Attach volume to instance"""
        volume = self.get_volume(volume_name)
        instance = self.nova.servers.find(name=instance_name)
        
        if not volume or not instance:
            raise ValueError("Volume or instance not found")
        
        try:
            self.nova.volumes.create_server_volume(
                instance.id,
                volume.id,
                device
            )
            self._wait_for_status(volume, 'in-use')
            return True
        except Exception as e:
            print(f"Failed to attach volume: {str(e)}")
            raise
```

## Advanced Features

### Load Balancing
```python
class LoadBalancerManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.neutron = clients['network']
    
    def create_load_balancer(self, name, subnet_name, algorithm='ROUND_ROBIN'):
        """Create load balancer"""
        try:
            subnet = self.neutron.list_subnets(name=subnet_name)['subnets'][0]
            
            lb = self.neutron.create_loadbalancer({
                'loadbalancer': {
                    'name': name,
                    'vip_subnet_id': subnet['id'],
                    'admin_state_up': True
                }
            })
            
            self._wait_for_status(lb['loadbalancer']['id'], 'ACTIVE')
            return lb
        except Exception as e:
            print(f"Failed to create load balancer: {str(e)}")
            raise
    
    def add_listener(self, lb_name, protocol, port):
        """Add listener to load balancer"""
        try:
            lb = self.neutron.list_loadbalancers(name=lb_name)['loadbalancers'][0]
            
            listener = self.neutron.create_listener({
                'listener': {
                    'name': f"{lb_name}-listener",
                    'loadbalancer_id': lb['id'],
                    'protocol': protocol,
                    'protocol_port': port,
                    'admin_state_up': True
                }
            })
            
            return listener
        except Exception as e:
            print(f"Failed to add listener: {str(e)}")
            raise
```

### Auto Scaling
```python
class AutoScalingManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.heat = heat_client.Client('1', session=sess)
    
    def create_scaling_group(self, name, min_size, max_size, template):
        """Create auto scaling group"""
        try:
            stack = self.heat.stacks.create(
                stack_name=name,
                template=template,
                parameters={
                    'min_size': min_size,
                    'max_size': max_size
                }
            )
            
            self._wait_for_stack(stack.id)
            return stack
        except Exception as e:
            print(f"Failed to create scaling group: {str(e)}")
            raise
    
    def update_scaling_policy(self, stack_name, adjustment):
        """Update scaling policy"""
        try:
            stack = self.heat.stacks.get(stack_name)
            
            self.heat.stacks.update(
                stack.id,
                parameters={'adjustment': adjustment}
            )
            
            return True
        except Exception as e:
            print(f"Failed to update scaling policy: {str(e)}")
            raise
```

## Security Considerations

1. Network Security:
```python
class SecurityManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.neutron = clients['network']
    
    def create_security_group(self, name, description):
        """Create security group"""
        try:
            secgroup = self.neutron.create_security_group({
                'security_group': {
                    'name': name,
                    'description': description
                }
            })
            return secgroup
        except Exception as e:
            print(f"Failed to create security group: {str(e)}")
            raise
    
    def add_security_rule(self, group_name, protocol, port_range):
        """Add security rule to group"""
        try:
            group = self.neutron.list_security_groups(
                name=group_name
            )['security_groups'][0]
            
            rule = self.neutron.create_security_group_rule({
                'security_group_rule': {
                    'security_group_id': group['id'],
                    'protocol': protocol,
                    'port_range_min': port_range[0],
                    'port_range_max': port_range[1],
                    'direction': 'ingress'
                }
            })
            
            return rule
        except Exception as e:
            print(f"Failed to add security rule: {str(e)}")
            raise
```

2. Access Control:
```python
class RoleManager:
    def __init__(self):
        clients = get_openstack_clients()
        self.keystone = keystone_client.Client(session=sess)
    
    def create_role(self, name):
        """Create new role"""
        try:
            role = self.keystone.roles.create(name=name)
            return role
        except Exception as e:
            print(f"Failed to create role: {str(e)}")
            raise
    
    def assign_role(self, role_name, user_name, project_name):
        """Assign role to user in project"""
        try:
            role = self.keystone.roles.find(name=role_name)
            user = self.keystone.users.find(name=user_name)
            project = self.keystone.projects.find(name=project_name)
            
            self.keystone.roles.grant(
                role.id,
                user=user.id,
                project=project.id
            )
            return True
        except Exception as e:
            print(f"Failed to assign role: {str(e)}")
            raise
```

## Performance Optimization

1. Resource Management:
```python
class ResourceOptimizer:
    def __init__(self):
        clients = get_openstack_clients()
        self.nova = clients['compute']
    
    def optimize_flavor(self, instance_name):
        """Optimize instance flavor based on usage"""
        try:
            instance = self.nova.servers.find(name=instance_name)
            stats = self.get_instance_stats(instance)
            
            if stats['cpu_util'] < 20 and stats['memory_util'] < 30:
                # Downsize instance
                smaller_flavor = self._find_smaller_flavor(instance.flavor)
                if smaller_flavor:
                    instance.resize(smaller_flavor)
                    return True
            
            return False
        except Exception as e:
            print(f"Failed to optimize flavor: {str(e)}")
            raise
```

2. Monitoring:
```python
class PerformanceMonitor:
    def __init__(self):
        clients = get_openstack_clients()
        self.ceilometer = ceilometer_client.Client('2', session=sess)
    
    def get_instance_metrics(self, instance_name, metric_name, period=3600):
        """Get instance performance metrics"""
        try:
            instance = self.nova.servers.find(name=instance_name)
            
            samples = self.ceilometer.samples.list(
                meter_name=metric_name,
                q=[{'field': 'resource_id', 'op': 'eq', 'value': instance.id}],
                limit=100
            )
            
            return [
                {
                    'timestamp': s.timestamp,
                    'value': s.volume
                }
                for s in samples
            ]
        except Exception as e:
            print(f"Failed to get metrics: {str(e)}")
            raise
```

## Testing

1. Unit Tests:
```python
import unittest
from unittest.mock import patch

class OpenStackTests(unittest.TestCase):
    def setUp(self):
        self.clients = get_openstack_clients()
    
    def test_instance_creation(self):
        manager = InstanceManager()
        instance = manager.create_instance(
            'test-instance',
            'm1.small',
            'ubuntu-20.04',
            'private-net'
        )
        self.assertIsNotNone(instance)
        self.assertEqual(instance.status, 'ACTIVE')
    
    def test_volume_operations(self):
        manager = VolumeManager()
        
        # Create volume
        volume = manager.create_volume('test-volume', 10)
        
        # Attach to instance
        result = manager.attach_volume(
            'test-volume',
            'test-instance'
        )
        
        self.assertTrue(result)
        self.assertEqual(volume.status, 'in-use')
```

2. Integration Tests:
```python
class OpenStackIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.instance_manager = InstanceManager()
        self.volume_manager = VolumeManager()
        self.network_manager = NetworkManager()
    
    def test_full_deployment(self):
        # Create network
        network = self.network_manager.create_network(
            'test-net',
            'test-subnet',
            '192.168.1.0/24'
        )
        
        # Create instance
        instance = self.instance_manager.create_instance(
            'test-instance',
            'm1.small',
            'ubuntu-20.04',
            'test-net'
        )
        
        # Create and attach volume
        volume = self.volume_manager.create_volume(
            'test-volume',
            10
        )
        self.volume_manager.attach_volume(
            'test-volume',
            'test-instance'
        )
        
        # Verify setup
        self.assertEqual(instance.status, 'ACTIVE')
        self.assertEqual(volume.status, 'in-use')
        
        # Clean up
        self.volume_manager.detach_volume('test-volume')
        self.instance_manager.delete_instance('test-instance')
        self.network_manager.delete_network('test-net')
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
