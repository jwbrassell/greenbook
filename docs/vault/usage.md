# HashiCorp Vault Usage Guide

## Table of Contents
- [HashiCorp Vault Usage Guide](#hashicorp-vault-usage-guide)
  - [Basic Operations](#basic-operations)
    - [Environment Setup](#environment-setup)
- [Set Vault address](#set-vault-address)
- [Set Vault token (if not using other auth methods)](#set-vault-token-if-not-using-other-auth-methods)
    - [Key-Value Secrets](#key-value-secrets)
- [Enable KV secrets engine version 2](#enable-kv-secrets-engine-version-2)
- [Store a secret](#store-a-secret)
- [Read a secret](#read-a-secret)
- [List secrets](#list-secrets)
- [Delete a secret](#delete-a-secret)
- [Enable versioning](#enable-versioning)
- [Read specific version](#read-specific-version)
    - [Secret Engines](#secret-engines)
- [List enabled secret engines](#list-enabled-secret-engines)
- [Enable a new secrets engine](#enable-a-new-secrets-engine)
- [Disable a secrets engine](#disable-a-secrets-engine)
- [Move a secrets engine](#move-a-secrets-engine)
- [Tune a secrets engine](#tune-a-secrets-engine)
  - [Working with Different Secret Types](#working-with-different-secret-types)
    - [Database Credentials](#database-credentials)
- [Enable database secrets engine](#enable-database-secrets-engine)
- [Configure PostgreSQL connection](#configure-postgresql-connection)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
    - [AWS Credentials](#aws-credentials)
- [Enable AWS secrets engine](#enable-aws-secrets-engine)
- [Configure AWS credentials](#configure-aws-credentials)
- [Create role](#create-role)
- [Generate credentials](#generate-credentials)
    - [SSH Keys](#ssh-keys)
- [Enable SSH secrets engine](#enable-ssh-secrets-engine)
- [Create a role for signing SSH keys](#create-a-role-for-signing-ssh-keys)
- [Sign a key](#sign-a-key)
  - [Token Management](#token-management)
    - [Token Creation](#token-creation)
- [Create a token](#create-a-token)
- [Create a token with specific properties](#create-a-token-with-specific-properties)
- [Create an orphan token](#create-an-orphan-token)
    - [Token Operations](#token-operations)
- [Look up token information](#look-up-token-information)
- [Renew a token](#renew-a-token)
- [Revoke a token](#revoke-a-token)
- [Revoke all tokens](#revoke-all-tokens)
  - [Response Wrapping](#response-wrapping)
- [Wrap a secret](#wrap-a-secret)
- [Unwrap a secret](#unwrap-a-secret)
- [Look up wrap info](#look-up-wrap-info)
  - [Lease Management](#lease-management)
- [List leases](#list-leases)
- [Renew a lease](#renew-a-lease)
- [Revoke a lease](#revoke-a-lease)
- [Revoke all leases under a prefix](#revoke-all-leases-under-a-prefix)
  - [Dynamic Secrets](#dynamic-secrets)
    - [Database Example](#database-example)
- [Generate dynamic credentials](#generate-dynamic-credentials)
- [Renew database credentials](#renew-database-credentials)
- [Revoke database credentials](#revoke-database-credentials)
    - [Cloud Credentials Example](#cloud-credentials-example)
- [Generate AWS credentials](#generate-aws-credentials)
- [Generate Azure credentials](#generate-azure-credentials)
- [Generate GCP credentials](#generate-gcp-credentials)
  - [Encryption as a Service](#encryption-as-a-service)
- [Enable transit engine](#enable-transit-engine)
- [Create encryption key](#create-encryption-key)
- [Encrypt data](#encrypt-data)
- [Decrypt data](#decrypt-data)
- [Rotate encryption key](#rotate-encryption-key)
- [Re-encrypt data with latest key version](#re-encrypt-data-with-latest-key-version)
  - [Best Practices](#best-practices)
  - [Common Patterns](#common-patterns)
- [Initial setup](#initial-setup)
- [Fetch secrets](#fetch-secrets)
- [Rotate database credentials](#rotate-database-credentials)
- [Rotate encryption key](#rotate-encryption-key)
- [Snapshot backup](#snapshot-backup)
- [Restore from snapshot](#restore-from-snapshot)
  - [Troubleshooting](#troubleshooting)
- [Check token validity](#check-token-validity)
- [Check auth methods](#check-auth-methods)
- [Check policy](#check-policy)
- [Test capabilities](#test-capabilities)
- [Check seal status](#check-seal-status)
- [Unseal if needed](#unseal-if-needed)



This guide covers the basic usage patterns and common operations in HashiCorp Vault.

## Basic Operations

### Environment Setup

```bash
# Set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Set Vault token (if not using other auth methods)
export VAULT_TOKEN='your-token'
```

### Key-Value Secrets

```bash
# Enable KV secrets engine version 2
vault secrets enable -version=2 kv

# Store a secret
vault kv put kv/my-secret username=admin password=secret

# Read a secret
vault kv get kv/my-secret

# List secrets
vault kv list kv/

# Delete a secret
vault kv delete kv/my-secret

# Enable versioning
vault kv enable-versioning kv/

# Read specific version
vault kv get -version=1 kv/my-secret
```

### Secret Engines

```bash
# List enabled secret engines
vault secrets list

# Enable a new secrets engine
vault secrets enable -path=aws aws

# Disable a secrets engine
vault secrets disable aws/

# Move a secrets engine
vault secrets move aws/ aws-prod/

# Tune a secrets engine
vault secrets tune -max-lease-ttl=12h aws/
```

## Working with Different Secret Types

### Database Credentials

```bash
# Enable database secrets engine
vault secrets enable database

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

### AWS Credentials

```bash
# Enable AWS secrets engine
vault secrets enable aws

# Configure AWS credentials
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

### SSH Keys

```bash
# Enable SSH secrets engine
vault secrets enable ssh

# Create a role for signing SSH keys
vault write ssh/roles/my-role \
    key_type=ca \
    allowed_users="ubuntu,admin" \
    ttl=1h

# Sign a key
vault write ssh/sign/my-role \
    public_key=@$HOME/.ssh/id_rsa.pub
```

## Token Management

### Token Creation

```bash
# Create a token
vault token create -policy=my-policy

# Create a token with specific properties
vault token create \
    -policy="my-policy" \
    -period=24h \
    -explicit-max-ttl=48h \
    -display-name="app-token"

# Create an orphan token
vault token create -orphan
```

### Token Operations

```bash
# Look up token information
vault token lookup

# Renew a token
vault token renew

# Revoke a token
vault token revoke <token>

# Revoke all tokens
vault token revoke -prefix auth/token/
```

## Response Wrapping

```bash
# Wrap a secret
vault kv get -wrap-ttl=30m kv/my-secret

# Unwrap a secret
vault unwrap <wrapping-token>

# Look up wrap info
vault unwrap -lookup <wrapping-token>
```

## Lease Management

```bash
# List leases
vault list sys/leases/lookup/

# Renew a lease
vault lease renew <lease-id>

# Revoke a lease
vault lease revoke <lease-id>

# Revoke all leases under a prefix
vault lease revoke -prefix auth/token/
```

## Dynamic Secrets

### Database Example

```bash
# Generate dynamic credentials
vault read database/creds/readonly

# Renew database credentials
vault lease renew database/creds/readonly/<lease-id>

# Revoke database credentials
vault lease revoke database/creds/readonly/<lease-id>
```

### Cloud Credentials Example

```bash
# Generate AWS credentials
vault read aws/creds/my-role

# Generate Azure credentials
vault read azure/creds/my-role

# Generate GCP credentials
vault read gcp/token/my-role
```

## Encryption as a Service

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

# Rotate encryption key
vault write -f transit/keys/my-key/rotate

# Re-encrypt data with latest key version
vault write transit/rewrap/my-key \
    ciphertext="vault:v1:8SDd3WHDOjf7mq69CyCqYjBXAiQQAVZRkFM13ok481zoCmHnSeDX9vyf7w=="
```

## Best Practices

1. **Token Management**
   - Use short-lived tokens
   - Implement token renewal
   - Use appropriate policies
   - Regularly rotate tokens

2. **Secret Management**
   - Use versioned KV store
   - Implement secret rotation
   - Use dynamic secrets where possible
   - Implement proper backup procedures

3. **Access Control**
   - Follow principle of least privilege
   - Use fine-grained policies
   - Implement proper authentication methods
   - Regular access review

4. **Monitoring**
   - Enable audit logging
   - Monitor token usage
   - Track failed operations
   - Set up alerts for anomalies

## Common Patterns

1. **Application Integration**
```bash
# Initial setup
export VAULT_ADDR='https://vault.example.com'
export VAULT_TOKEN=$(vault write -field=token auth/approle/login \
    role_id="$ROLE_ID" \
    secret_id="$SECRET_ID")

# Fetch secrets
DB_CREDS=$(vault read -format=json database/creds/readonly)
export DB_USER=$(echo $DB_CREDS | jq -r .data.username)
export DB_PASS=$(echo $DB_CREDS | jq -r .data.password)
```

2. **Secret Rotation**
```bash
# Rotate database credentials
vault write database/rotate-root/postgresql

# Rotate encryption key
vault write -f transit/keys/my-key/rotate
```

3. **Backup and Recovery**
```bash
# Snapshot backup
vault operator raft snapshot save backup.snap

# Restore from snapshot
vault operator raft snapshot restore backup.snap
```

## Troubleshooting

1. **Authentication Issues**
```bash
# Check token validity
vault token lookup

# Check auth methods
vault auth list
```

2. **Permission Issues**
```bash
# Check policy
vault policy read my-policy

# Test capabilities
vault token capabilities <token> path/to/secret
```

3. **Seal Status**
```bash
# Check seal status
vault status

# Unseal if needed
vault operator unseal
```

For more detailed information on specific topics, refer to:
- [Authentication Methods](authentication.md)
- [Policy Management](policies.md)
- [Secret Engines](secret-engines.md)
- [CRUD Operations](crud/index.md)
