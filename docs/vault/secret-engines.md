# HashiCorp Vault Secret Engines

## Table of Contents
- [HashiCorp Vault Secret Engines](#hashicorp-vault-secret-engines)
  - [Overview](#overview)
  - [Key-Value Secret Engine](#key-value-secret-engine)
- [Enable KV version 2 engine](#enable-kv-version-2-engine)
- [Store a secret](#store-a-secret)
- [Read a secret](#read-a-secret)
- [List secrets](#list-secrets)
- [Delete a secret](#delete-a-secret)
- [Enable versioning](#enable-versioning)
- [Read specific version](#read-specific-version)
  - [Database Secret Engine](#database-secret-engine)
- [Enable database engine](#enable-database-engine)
    - [PostgreSQL Configuration](#postgresql-configuration)
- [Configure PostgreSQL connection](#configure-postgresql-connection)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
    - [MySQL Configuration](#mysql-configuration)
- [Configure MySQL connection](#configure-mysql-connection)
- [Create role](#create-role)
  - [AWS Secret Engine](#aws-secret-engine)
- [Enable AWS engine](#enable-aws-engine)
- [Configure root credentials](#configure-root-credentials)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
  - [Azure Secret Engine](#azure-secret-engine)
- [Enable Azure engine](#enable-azure-engine)
- [Configure](#configure)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
  - [GCP Secret Engine](#gcp-secret-engine)
- [Enable GCP engine](#enable-gcp-engine)
- [Configure](#configure)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
  - [PKI Secret Engine](#pki-secret-engine)
- [Enable PKI engine](#enable-pki-engine)
- [Configure CA](#configure-ca)
- [Create role](#create-role)
- [Generate certificate](#generate-certificate)
  - [SSH Secret Engine](#ssh-secret-engine)
- [Enable SSH engine](#enable-ssh-engine)
- [Create CA](#create-ca)
- [Create role](#create-role)
- [Sign key](#sign-key)
  - [Transit Secret Engine](#transit-secret-engine)
- [Enable transit engine](#enable-transit-engine)
- [Create encryption key](#create-encryption-key)
- [Encrypt data](#encrypt-data)
- [Decrypt data](#decrypt-data)
- [Rotate key](#rotate-key)
- [Re-encrypt data](#re-encrypt-data)
  - [TOTP Secret Engine](#totp-secret-engine)
- [Enable TOTP engine](#enable-totp-engine)
- [Create key](#create-key)
- [Generate code](#generate-code)
- [Validate code](#validate-code)
  - [Best Practices](#best-practices)
    - [1. Secret Engine Management](#1-secret-engine-management)
- [List enabled engines](#list-enabled-engines)
- [Move secret engine](#move-secret-engine)
- [Tune engine settings](#tune-engine-settings)
    - [2. Backup and Recovery](#2-backup-and-recovery)
- [Take snapshot](#take-snapshot)
- [Restore snapshot](#restore-snapshot)
    - [3. Monitoring and Maintenance](#3-monitoring-and-maintenance)
- [Enable audit logging](#enable-audit-logging)
- [Monitor secret access](#monitor-secret-access)
  - [Common Integration Patterns](#common-integration-patterns)
    - [1. Application Integration](#1-application-integration)
- [Store application secrets](#store-application-secrets)
- [Generate dynamic credentials](#generate-dynamic-credentials)
    - [2. CI/CD Integration](#2-ci/cd-integration)
- [Store deployment credentials](#store-deployment-credentials)
- [Generate AWS deployment credentials](#generate-aws-deployment-credentials)
    - [3. Certificate Management](#3-certificate-management)
- [Generate TLS certificate](#generate-tls-certificate)
  - [Troubleshooting](#troubleshooting)
    - [1. Secret Engine Issues](#1-secret-engine-issues)
- [Check engine status](#check-engine-status)
- [View mount configuration](#view-mount-configuration)
- [Check lease status](#check-lease-status)
    - [2. Performance Issues](#2-performance-issues)
- [Tune engine performance](#tune-engine-performance)
- [Monitor metrics](#monitor-metrics)
    - [3. Access Issues](#3-access-issues)
- [Check policies](#check-policies)
- [Test capabilities](#test-capabilities)



This guide covers the various secret engines available in HashiCorp Vault and how to configure and use them effectively.

## Overview

Secret engines are plugins that store, generate, or encrypt data. Vault supports various types of secret engines, each designed for specific use cases.

## Key-Value Secret Engine

The most basic secret engine for storing static secrets.

```bash
# Enable KV version 2 engine
vault secrets enable -version=2 kv

# Store a secret
vault kv put kv/my-app/config \
    api_key="abc123" \
    password="secret"

# Read a secret
vault kv get kv/my-app/config

# List secrets
vault kv list kv/my-app

# Delete a secret
vault kv delete kv/my-app/config

# Enable versioning
vault kv enable-versioning kv/

# Read specific version
vault kv get -version=1 kv/my-app/config
```

## Database Secret Engine

Generates dynamic credentials for databases.

```bash
# Enable database engine
vault secrets enable database

### PostgreSQL Configuration
```bash
# Configure PostgreSQL connection
vault write database/config/postgresql \
    plugin_name=postgresql-database-plugin \
    connection_url="postgresql://{{username}}:{{password}}@localhost:5432/mydb?sslmode=disable" \
    allowed_roles="readonly" \
    username="vault" \
    password="vaultpass"

# Create role
vault write database/roles/readonly \
    db_name=postgresql \
    creation_statements="CREATE ROLE \"{{name}}\" WITH LOGIN PASSWORD '{{password}}' VALID UNTIL '{{expiration}}'; \
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO \"{{name}}\";" \
    default_ttl="1h" \
    max_ttl="24h"

# Generate credentials
vault read database/creds/readonly
```

### MySQL Configuration
```bash
# Configure MySQL connection
vault write database/config/mysql \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(localhost:3306)/" \
    allowed_roles="readonly" \
    username="vault" \
    password="vaultpass"

# Create role
vault write database/roles/readonly \
    db_name=mysql \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}'; \
        GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"
```

## AWS Secret Engine

Generates dynamic AWS credentials.

```bash
# Enable AWS engine
vault secrets enable aws

# Configure root credentials
vault write aws/config/root \
    access_key=AKIAXXXXXXXXXXXXXXXX \
    secret_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    region=us-east-1

# Create role
vault write aws/roles/my-role \
    credential_type=iam_user \
    policy_document=@aws-policy.json

# Generate credentials
vault read aws/creds/my-role
```

## Azure Secret Engine

Generates dynamic Azure credentials.

```bash
# Enable Azure engine
vault secrets enable azure

# Configure
vault write azure/config \
    subscription_id=$AZURE_SUBSCRIPTION_ID \
    tenant_id=$AZURE_TENANT_ID \
    client_id=$AZURE_CLIENT_ID \
    client_secret=$AZURE_CLIENT_SECRET

# Create role
vault write azure/roles/my-role \
    application_object_id=$APP_OBJECT_ID \
    ttl=1h

# Generate credentials
vault read azure/creds/my-role
```

## GCP Secret Engine

Generates dynamic Google Cloud credentials.

```bash
# Enable GCP engine
vault secrets enable gcp

# Configure
vault write gcp/config \
    credentials=@/path/to/credentials.json

# Create role
vault write gcp/roleset/my-role \
    project="my-project" \
    secret_type="service_account_key" \
    bindings='resource "//cloudresourcemanager.googleapis.com/projects/my-project" {
      roles = ["roles/viewer"]
    }'

# Generate credentials
vault read gcp/roleset/my-role/key
```

## PKI Secret Engine

Generates X.509 certificates.

```bash
# Enable PKI engine
vault secrets enable pki

# Configure CA
vault write pki/root/generate/internal \
    common_name="example.com" \
    ttl=8760h

# Create role
vault write pki/roles/my-role \
    allowed_domains="example.com" \
    allow_subdomains=true \
    max_ttl="72h"

# Generate certificate
vault write pki/issue/my-role \
    common_name="app.example.com"
```

## SSH Secret Engine

Manages SSH access.

```bash
# Enable SSH engine
vault secrets enable ssh

# Create CA
vault write ssh/config/ca \
    generate_signing_key=true

# Create role
vault write ssh/roles/my-role \
    key_type=ca \
    allowed_users="ubuntu,admin" \
    ttl=1h

# Sign key
vault write ssh/sign/my-role \
    public_key=@$HOME/.ssh/id_rsa.pub
```

## Transit Secret Engine

Provides encryption as a service.

```bash
# Enable transit engine
vault secrets enable transit

# Create encryption key
vault write -f transit/keys/my-key

# Encrypt data
vault write transit/encrypt/my-key \
    plaintext=$(base64 <<< "my secret data")

# Decrypt data
vault write transit/decrypt/my-key \
    ciphertext="vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX9vyf7w=="

# Rotate key
vault write -f transit/keys/my-key/rotate

# Re-encrypt data
vault write transit/rewrap/my-key \
    ciphertext="vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX9vyf7w=="
```

## TOTP Secret Engine

Generates Time-Based One-Time Passwords.

```bash
# Enable TOTP engine
vault secrets enable totp

# Create key
vault write totp/keys/my-key \
    generate=true \
    issuer="Vault" \
    account_name="user@example.com"

# Generate code
vault read totp/code/my-key

# Validate code
vault write totp/code/my-key code="123456"
```

## Best Practices

### 1. Secret Engine Management

```bash
# List enabled engines
vault secrets list

# Move secret engine
vault secrets move kv/ new-kv/

# Tune engine settings
vault secrets tune -max-lease-ttl=12h kv/
```

### 2. Backup and Recovery

```bash
# Take snapshot
vault operator raft snapshot save backup.snap

# Restore snapshot
vault operator raft snapshot restore backup.snap
```

### 3. Monitoring and Maintenance

```bash
# Enable audit logging
vault audit enable file file_path=/var/log/vault/audit.log

# Monitor secret access
vault audit list
```

## Common Integration Patterns

### 1. Application Integration

```bash
# Store application secrets
vault kv put kv/my-app/config \
    db_user="app" \
    db_password="secret" \
    api_key="abc123"

# Generate dynamic credentials
vault read database/creds/my-app-role
```

### 2. CI/CD Integration

```bash
# Store deployment credentials
vault kv put kv/ci/deploy-keys \
    ssh_key="..." \
    api_token="..."

# Generate AWS deployment credentials
vault read aws/creds/deploy-role
```

### 3. Certificate Management

```bash
# Generate TLS certificate
vault write pki/issue/my-role \
    common_name="app.example.com" \
    alt_names="app1.example.com,app2.example.com" \
    ttl="720h"
```

## Troubleshooting

### 1. Secret Engine Issues

```bash
# Check engine status
vault secrets list -detailed

# View mount configuration
vault read sys/mounts/kv/tune

# Check lease status
vault list sys/leases/lookup/
```

### 2. Performance Issues

```bash
# Tune engine performance
vault secrets tune -default-lease-ttl=1h -max-lease-ttl=24h kv/

# Monitor metrics
vault read sys/metrics
```

### 3. Access Issues

```bash
# Check policies
vault token lookup | grep policies

# Test capabilities
vault token capabilities <token> kv/my-app/config
```

For more information on related topics, see:
- [Authentication Methods](authentication.md)
- [Policy Management](policies.md)
- [Audit Logging](audit-logging.md)
