# OpenStack Installation Guide (Version 17.1)

## Table of Contents
- [OpenStack Installation Guide (Version 17.1)](#openstack-installation-guide-version-171)
  - [Development Environment Setup (DevStack)](#development-environment-setup-devstack)
    - [Prerequisites](#prerequisites)
- [Update system packages](#update-system-packages)
- [Install git](#install-git)
- [Create stack user](#create-stack-user)
    - [DevStack Installation](#devstack-installation)
- [Switch to stack user](#switch-to-stack-user)
- [Clone DevStack repository](#clone-devstack-repository)
- [Create local.conf configuration file](#create-localconf-configuration-file)
- [Start installation](#start-installation)
  - [Production Environment Setup](#production-environment-setup)
    - [1. Controller Node Setup](#1-controller-node-setup)
- [Install dependencies](#install-dependencies)
- [Install OpenStack client](#install-openstack-client)
- [Install MariaDB](#install-mariadb)
- [Configure MariaDB](#configure-mariadb)
- [Restart MariaDB](#restart-mariadb)
- [Secure MariaDB installation](#secure-mariadb-installation)
- [Install RabbitMQ](#install-rabbitmq)
- [Configure RabbitMQ](#configure-rabbitmq)
    - [2. Install Keystone (Identity Service)](#2-install-keystone-identity-service)
- [Create keystone database](#create-keystone-database)
- [Install Keystone packages](#install-keystone-packages)
- [Configure Keystone](#configure-keystone)
- [Initialize Keystone database](#initialize-keystone-database)
- [Initialize Fernet key repositories](#initialize-fernet-key-repositories)
- [Bootstrap Identity service](#bootstrap-identity-service)
    - [3. Install Nova (Compute Service)](#3-install-nova-compute-service)
- [Create Nova databases](#create-nova-databases)
- [Install Nova packages](#install-nova-packages)
- [Configure Nova](#configure-nova)
    - [4. Install Neutron (Networking Service)](#4-install-neutron-networking-service)
- [Create Neutron database](#create-neutron-database)
- [Install Neutron packages](#install-neutron-packages)
- [Configure Neutron](#configure-neutron)
  - [Post-Installation Verification](#post-installation-verification)
- [Source the admin credentials](#source-the-admin-credentials)
- [Verify Keystone installation](#verify-keystone-installation)
- [Verify Nova installation](#verify-nova-installation)
- [Verify Neutron installation](#verify-neutron-installation)
- [Create initial networks](#create-initial-networks)
  - [Security Considerations](#security-considerations)
  - [Troubleshooting](#troubleshooting)
  - [Next Steps](#next-steps)



This guide provides detailed instructions for installing OpenStack version 17.1 in both production and development environments.

## Development Environment Setup (DevStack)

DevStack is recommended for development and testing environments. It provides a quick way to set up a complete OpenStack environment.

### Prerequisites
```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install git
sudo apt install git -y

# Create stack user
sudo useradd -s /bin/bash -d /opt/stack -m stack
sudo chmod +x /opt/stack
echo "stack ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/stack
```

### DevStack Installation
```bash
# Switch to stack user
sudo su - stack

# Clone DevStack repository
git clone https://opendev.org/openstack/devstack
cd devstack

# Create local.conf configuration file
cat > local.conf << EOF
[[local|localrc]]
ADMIN_PASSWORD=secret
DATABASE_PASSWORD=\$ADMIN_PASSWORD
RABBIT_PASSWORD=\$ADMIN_PASSWORD
SERVICE_PASSWORD=\$ADMIN_PASSWORD
HOST_IP=127.0.0.1
EOF

# Start installation
./stack.sh
```

## Production Environment Setup

### 1. Controller Node Setup

```bash
# Install dependencies
sudo apt install -y python3-pip chrony

# Install OpenStack client
pip install python-openstackclient==6.2.0

# Install MariaDB
sudo apt install -y mariadb-server python3-pymysql

# Configure MariaDB
sudo tee /etc/mysql/mariadb.conf.d/99-openstack.cnf << EOF
[mysqld]
bind-address = 0.0.0.0
default-storage-engine = innodb
innodb_file_per_table = on
max_connections = 4096
collation-server = utf8_general_ci
character-set-server = utf8
EOF

# Restart MariaDB
sudo systemctl restart mariadb

# Secure MariaDB installation
sudo mysql_secure_installation

# Install RabbitMQ
sudo apt install -y rabbitmq-server

# Configure RabbitMQ
sudo rabbitmqctl add_user openstack RABBIT_PASS
sudo rabbitmqctl set_permissions openstack ".*" ".*" ".*"
```

### 2. Install Keystone (Identity Service)

```bash
# Create keystone database
mysql -u root -p << EOF
CREATE DATABASE keystone;
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'KEYSTONE_DBPASS';
GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'KEYSTONE_DBPASS';
EOF

# Install Keystone packages
sudo apt install -y keystone apache2 libapache2-mod-wsgi-py3

# Configure Keystone
sudo sed -i 's|#connection = sqlite:////var/lib/keystone/keystone.db|connection = mysql+pymysql://keystone:KEYSTONE_DBPASS@controller/keystone|' /etc/keystone/keystone.conf

# Initialize Keystone database
sudo keystone-manage db_sync

# Initialize Fernet key repositories
sudo keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
sudo keystone-manage credential_setup --keystone-user keystone --keystone-group keystone

# Bootstrap Identity service
sudo keystone-manage bootstrap --bootstrap-password ADMIN_PASS \
  --bootstrap-admin-url http://controller:5000/v3/ \
  --bootstrap-internal-url http://controller:5000/v3/ \
  --bootstrap-public-url http://controller:5000/v3/ \
  --bootstrap-region-id RegionOne
```

### 3. Install Nova (Compute Service)

```bash
# Create Nova databases
mysql -u root -p << EOF
CREATE DATABASE nova_api;
CREATE DATABASE nova;
CREATE DATABASE nova_cell0;

GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'NOVA_DBPASS';
GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'NOVA_DBPASS';
EOF

# Install Nova packages
sudo apt install -y nova-api nova-conductor nova-novncproxy nova-scheduler

# Configure Nova
sudo sed -i 's|#connection = sqlite:////var/lib/nova/nova.sqlite|connection = mysql+pymysql://nova:NOVA_DBPASS@controller/nova|' /etc/nova/nova.conf
```

### 4. Install Neutron (Networking Service)

```bash
# Create Neutron database
mysql -u root -p << EOF
CREATE DATABASE neutron;
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'localhost' IDENTIFIED BY 'NEUTRON_DBPASS';
GRANT ALL PRIVILEGES ON neutron.* TO 'neutron'@'%' IDENTIFIED BY 'NEUTRON_DBPASS';
EOF

# Install Neutron packages
sudo apt install -y neutron-server neutron-plugin-ml2 neutron-linuxbridge-agent neutron-l3-agent neutron-dhcp-agent neutron-metadata-agent

# Configure Neutron
sudo sed -i 's|connection = sqlite:////var/lib/neutron/neutron.sqlite|connection = mysql+pymysql://neutron:NEUTRON_DBPASS@controller/neutron|' /etc/neutron/neutron.conf
```

## Post-Installation Verification

```bash
# Source the admin credentials
source admin-openrc

# Verify Keystone installation
openstack token issue

# Verify Nova installation
openstack compute service list

# Verify Neutron installation
openstack network agent list

# Create initial networks
openstack network create --share --external --provider-physical-network provider --provider-network-type flat provider
openstack subnet create --network provider --subnet-range 203.0.113.0/24 --gateway 203.0.113.1 provider-subnet
```

## Security Considerations

1. Change all default passwords used in this guide
2. Configure firewall rules to restrict access
3. Use SSL/TLS for all service endpoints
4. Regularly update and patch all components
5. Monitor system logs for suspicious activities

## Troubleshooting

Common issues and their solutions:

1. **Service not starting**
   ```bash
   # Check service status
   sudo systemctl status <service-name>
   
   # Check logs
   sudo journalctl -u <service-name>
   ```

2. **Database connection issues**
   ```bash
   # Verify database connectivity
   mysql -u <username> -p -h controller
   ```

3. **Authentication failures**
   ```bash
   # Verify environment variables
   env | grep OS_
   
   # Test authentication
   openstack token issue
   ```

## Next Steps

1. Configure additional services (Cinder, Swift, etc.)
2. Set up monitoring and logging
3. Configure backup and recovery procedures
4. Implement high availability
5. Set up load balancing

For more detailed information, refer to the [official OpenStack documentation](https://docs.openstack.org/).
