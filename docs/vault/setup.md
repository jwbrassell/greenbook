# HashiCorp Vault Setup Guide

## Table of Contents
- [HashiCorp Vault Setup Guide](#hashicorp-vault-setup-guide)
  - [Installation Methods](#installation-methods)
    - [Package Manager Installation](#package-manager-installation)
      - [Ubuntu/Debian](#ubuntu/debian)
      - [RHEL/CentOS](#rhel/centos)
      - [macOS](#macos)
    - [Binary Installation](#binary-installation)
- [Download latest version](#download-latest-version)
- [Unzip the downloaded file](#unzip-the-downloaded-file)
- [Move the binary to a directory in your PATH](#move-the-binary-to-a-directory-in-your-path)
- [Verify installation](#verify-installation)
  - [Initial Configuration](#initial-configuration)
    - [Development Mode](#development-mode)
- [Start vault in development mode](#start-vault-in-development-mode)
- [In another terminal, set environment variables](#in-another-terminal,-set-environment-variables)
    - [Production Configuration](#production-configuration)
- [Create vault user and group](#create-vault-user-and-group)
- [Create necessary directories](#create-necessary-directories)
- [Start vault service](#start-vault-service)
  - [Initialization and Unsealing](#initialization-and-unsealing)
- [Initialize vault](#initialize-vault)
- [This will output 5 unseal keys and an initial root token](#this-will-output-5-unseal-keys-and-an-initial-root-token)
- [SAVE THESE SECURELY](#save-these-securely)
- [Unseal vault (needs 3 of 5 keys by default)](#unseal-vault-needs-3-of-5-keys-by-default)
- [Login with root token](#login-with-root-token)
  - [Storage Backend Options](#storage-backend-options)
  - [High Availability Setup](#high-availability-setup)
  - [Security Considerations](#security-considerations)
- [Enable file audit device](#enable-file-audit-device)
- [Enable syslog audit device](#enable-syslog-audit-device)
- [Allow Vault API traffic](#allow-vault-api-traffic)
- [Allow Vault cluster traffic](#allow-vault-cluster-traffic)
  - [Troubleshooting](#troubleshooting)
- [Check seal status](#check-seal-status)
- [Unseal if needed](#unseal-if-needed)
- [Check ownership and permissions](#check-ownership-and-permissions)
- [Check service status](#check-service-status)
- [Check logs](#check-logs)
  - [Next Steps](#next-steps)



This guide covers the installation and initial setup of HashiCorp Vault across different platforms and environments.

## Installation Methods

### Package Manager Installation

#### Ubuntu/Debian
```bash
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install vault
```

#### RHEL/CentOS
```bash
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo
sudo yum -y install vault
```

#### macOS
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/vault
```

### Binary Installation

```bash
# Download latest version
VAULT_VERSION="1.13.0"  # Replace with desired version
wget "https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip"

# Unzip the downloaded file
unzip "vault_${VAULT_VERSION}_linux_amd64.zip"

# Move the binary to a directory in your PATH
sudo mv vault /usr/local/bin/

# Verify installation
vault --version
```

## Initial Configuration

### Development Mode
For testing and development:

```bash
# Start vault in development mode
vault server -dev

# In another terminal, set environment variables
export VAULT_ADDR='http://127.0.0.1:8200'
export VAULT_TOKEN='root'  # Only in dev mode
```

### Production Configuration

1. Create configuration file `/etc/vault.d/config.hcl`:

```hcl
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = "true"  # Enable TLS in production
}

api_addr = "http://0.0.0.0:8200"
cluster_addr = "https://0.0.0.0:8201"
```

2. Create systemd service file `/etc/systemd/system/vault.service`:

```ini
[Unit]
Description=HashiCorp Vault Service
Documentation=https://www.vaultproject.io/docs/
Requires=network-online.target
After=network-online.target

[Service]
Type=simple
User=vault
Group=vault
ExecStart=/usr/local/bin/vault server -config=/etc/vault.d/config.hcl
ExecReload=/bin/kill -HUP $MAINPID
CapabilityBoundingSet=CAP_SYSLOG CAP_IPC_LOCK
Capabilities=CAP_IPC_LOCK+ep
SecureBits=keep-caps
NoNewPrivileges=yes
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
```

3. Setup directories and permissions:

```bash
# Create vault user and group
sudo useradd --system --home /etc/vault.d --shell /bin/false vault

# Create necessary directories
sudo mkdir -p /opt/vault/data
sudo chown -R vault:vault /opt/vault
sudo chmod 750 /opt/vault/data

# Start vault service
sudo systemctl enable vault
sudo systemctl start vault
```

## Initialization and Unsealing

In production mode, Vault needs to be initialized and unsealed:

```bash
# Initialize vault
vault operator init

# This will output 5 unseal keys and an initial root token
# SAVE THESE SECURELY

# Unseal vault (needs 3 of 5 keys by default)
vault operator unseal # Enter first unseal key
vault operator unseal # Enter second unseal key
vault operator unseal # Enter third unseal key

# Login with root token
vault login
```

## Storage Backend Options

Vault supports various storage backends:

1. **File** (shown above)
2. **Consul**:
```hcl
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}
```

3. **PostgreSQL**:
```hcl
storage "postgresql" {
  connection_url = "postgres://user:password@localhost:5432/vault?sslmode=disable"
}
```

4. **AWS DynamoDB**:
```hcl
storage "dynamodb" {
  region = "us-west-2"
  table  = "vault-data"
}
```

## High Availability Setup

For production environments, consider these HA configurations:

1. **Consul Backend**:
```hcl
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
  ha_enabled = "true"
}

api_addr = "https://vault-1.example.com:8200"
cluster_addr = "https://vault-1.example.com:8201"
```

2. **Load Balancer Configuration**:
```nginx
upstream vault {
    server vault-1.example.com:8200;
    server vault-2.example.com:8200;
    server vault-3.example.com:8200;
}

server {
    listen 443 ssl;
    server_name vault.example.com;

    location / {
        proxy_pass http://vault;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## Security Considerations

1. **TLS Configuration**:
```hcl
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/path/to/fullchain.pem"
  tls_key_file  = "/path/to/privkey.pem"
}
```

2. **Audit Logging**:
```bash
# Enable file audit device
vault audit enable file file_path=/var/log/vault/audit.log

# Enable syslog audit device
vault audit enable syslog
```

3. **Firewall Rules**:
```bash
# Allow Vault API traffic
sudo ufw allow 8200/tcp

# Allow Vault cluster traffic
sudo ufw allow 8201/tcp
```

## Troubleshooting

Common issues and solutions:

1. **Vault Sealed**:
```bash
# Check seal status
vault status

# Unseal if needed
vault operator unseal
```

2. **Permission Issues**:
```bash
# Check ownership and permissions
sudo chown -R vault:vault /opt/vault
sudo chmod 750 /opt/vault/data
```

3. **Service Not Starting**:
```bash
# Check service status
sudo systemctl status vault

# Check logs
sudo journalctl -u vault
```

## Next Steps

After installation:

1. [Configure Authentication Methods](authentication.md)
2. [Set up Policies](policies.md)
3. [Enable Secret Engines](secret-engines.md)
4. [Configure Audit Devices](audit-logging.md)

For production deployments, ensure you have:

- [ ] Configured TLS certificates
- [ ] Set up proper backup procedures
- [ ] Implemented monitoring and alerting
- [ ] Documented key management procedures
- [ ] Tested disaster recovery procedures
