# HashiCorp Vault Guide

## Table of Contents
- [HashiCorp Vault Guide](#hashicorp-vault-guide)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing Strategies](#testing-strategies)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
This comprehensive guide covers HashiCorp Vault, a tool for managing secrets and protecting sensitive data. Learn how to securely store and access secrets, manage encryption, and integrate Vault with your applications.

## Prerequisites
- Basic understanding of:
  - Security concepts
  - PKI and encryption
  - RESTful APIs
  - Command line interface
- Required software:
  - Vault binary
  - OpenSSL
  - jq (for JSON processing)

## Installation and Setup
1. Install Vault:
```bash
# Download and install Vault
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt update && sudo apt install vault

# Verify installation
vault --version
```

2. Server Configuration:
```hcl
# config.hcl
storage "file" {
  path = "/opt/vault/data"
}

listener "tcp" {
  address     = "0.0.0.0:8200"
  tls_disable = 1  # Enable TLS in production
}

api_addr = "http://127.0.0.1:8200"
```

3. Initialize Vault:
```bash
# Start Vault server
vault server -config=config.hcl

# Initialize Vault
vault operator init

# Unseal Vault
vault operator unseal
```

## Basic Operations
1. Secret Management:
```bash
# Enable KV secrets engine
vault secrets enable -path=secret kv-v2

# Store a secret
vault kv put secret/myapp/config \
    db_user="app_user" \
    db_password="super-secret"

# Retrieve a secret
vault kv get secret/myapp/config
```

2. Authentication:
```bash
# Enable AppRole auth
vault auth enable approle

# Create policy
vault policy write myapp-policy - << EOF
path "secret/data/myapp/*" {
  capabilities = ["read", "list"]
}
EOF

# Create AppRole
vault write auth/approle/role/myapp \
    token_policies="myapp-policy" \
    token_ttl=1h
```

## Advanced Features
1. Dynamic Secrets:
```bash
# Enable database secrets engine
vault secrets enable database

# Configure MySQL connection
vault write database/config/mysql \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(localhost:3306)/" \
    allowed_roles="readonly" \
    username="root" \
    password="root-password"

# Create role
vault write database/roles/readonly \
    db_name=mysql \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; \
        GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"
```

2. Encryption as a Service:
```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/myapp-key

# Encrypt data
vault write transit/encrypt/myapp-key \
    plaintext=$(echo "secret-data" | base64)

# Decrypt data
vault write transit/decrypt/myapp-key \
    ciphertext="vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX"
```

## Security Considerations
1. Access Control:
```bash
# Create fine-grained policy
vault policy write app-policy - << EOF
path "secret/data/app/*" {
  capabilities = ["read"]
  
  # Add conditions
  required_parameters = ["version"]
  allowed_parameters = {
    "version" = []
  }
}
EOF

# Audit logging
vault audit enable file file_path=/var/log/vault/audit.log
```

2. TLS Configuration:
```bash
# Generate certificates
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout vault.key -out vault.crt

# Configure TLS
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/path/to/vault.crt"
  tls_key_file  = "/path/to/vault.key"
}
```

## Performance Optimization
1. Storage Tuning:
```hcl
storage "raft" {
  path = "/opt/vault/data"
  node_id = "node-1"
  
  performance_multiplier = 1
  retry_join {
    leader_api_addr = "https://vault-0:8200"
  }
}
```

2. Cache Configuration:
```hcl
cache {
  use_auto_auth_token = true
}

listener "tcp" {
  address = "127.0.0.1:8200"
  tls_disable = true
}
```

## Testing Strategies
1. Integration Testing:
```bash
#!/bin/bash
# test_vault.sh

# Start Vault in dev mode
vault server -dev &
export VAULT_ADDR='http://127.0.0.1:8200'

# Test secret operations
vault kv put secret/test value=test
result=$(vault kv get -field=value secret/test)
[ "$result" = "test" ] || exit 1

# Test policy enforcement
vault policy write test-policy test-policy.hcl
vault token create -policy=test-policy
```

2. Health Checks:
```bash
# Check seal status
vault status

# Verify auth methods
vault auth list

# Test HA status
vault operator raft list-peers
```

## Troubleshooting
1. Common Issues:
```bash
# Check server logs
journalctl -u vault

# Verify connectivity
curl -s http://127.0.0.1:8200/v1/sys/health | jq

# Debug mode
vault server -dev -log-level=debug
```

2. Recovery Procedures:
```bash
# Recover from sealed state
vault operator unseal

# Reset root token
vault operator generate-root -init
vault operator generate-root
vault operator generate-root -decode=
```

## Best Practices
1. Secret Management:
```bash
# Rotate credentials
vault write -force auth/token/roles/myapp-role \
    allowed_policies="myapp-policy" \
    period="24h"

# Version secrets
vault kv put -cas=0 secret/myapp/config @config.json
```

2. High Availability:
```hcl
storage "raft" {
  path = "/opt/vault/data"
  node_id = "node-1"
  
  retry_join {
    leader_api_addr = "https://vault-0:8200"
    leader_ca_cert_file = "/path/to/ca.crt"
  }
}
```

## Integration Points
1. Application Integration:
```python
import hvac

def get_vault_client():
    return hvac.Client(
        url='http://localhost:8200',
        token='your-token'
    )

def get_secret(path):
    client = get_vault_client()
    try:
        secret = client.secrets.kv.v2.read_secret_version(path)
        return secret['data']['data']
    except hvac.exceptions.VaultError as e:
        logging.error(f"Vault error: {e}")
        raise
```

2. CI/CD Integration:
```yaml
# GitLab CI example
variables:
  VAULT_ADDR: "https://vault.example.com"

before_script:
  - vault login -method=jwt role=ci-role

deploy:
  script:
    - secrets=$(vault kv get -format=json secret/myapp/deploy)
    - deploy_app "$secrets"
```

## Next Steps
1. Advanced Topics
   - Auto-unseal
   - Disaster recovery
   - Custom secret engines
   - Advanced policies

2. Further Learning
   - [Vault Documentation](https://www.vaultproject.io/docs)
   - [Learn HashiCorp Vault](https://learn.hashicorp.com/vault)
   - [API Documentation](https://www.vaultproject.io/api-docs)
   - Community resources

## Contributing
Feel free to contribute to this documentation by submitting pull requests or opening issues for improvements. Please ensure your contributions follow security best practices and include practical examples.
