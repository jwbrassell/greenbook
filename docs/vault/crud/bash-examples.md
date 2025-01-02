# HashiCorp Vault Bash Examples

## Table of Contents
- [HashiCorp Vault Bash Examples](#hashicorp-vault-bash-examples)
  - [Environment Setup](#environment-setup)
- [Set Vault address](#set-vault-address)
- [Set Vault token](#set-vault-token)
- [Optional: Disable SSL verification for testing](#optional:-disable-ssl-verification-for-testing)
  - [Basic CRUD Operations](#basic-crud-operations)
    - [Using Vault CLI](#using-vault-cli)
      - [Create (Write) Operations](#create-write-operations)
- [Write a simple secret](#write-a-simple-secret)
- [Write JSON data](#write-json-data)
- [Write with metadata](#write-with-metadata)
      - [Read Operations](#read-operations)
- [Read a secret](#read-a-secret)
- [Read specific version](#read-specific-version)
- [Read as JSON](#read-as-json)
- [List secrets](#list-secrets)
- [Read metadata](#read-metadata)
      - [Update Operations](#update-operations)
- [Update existing secret](#update-existing-secret)
- [Update metadata](#update-metadata)
      - [Delete Operations](#delete-operations)
- [Soft delete latest version](#soft-delete-latest-version)
- [Delete specific version](#delete-specific-version)
- [Permanently delete versions](#permanently-delete-versions)
- [Delete all versions and metadata](#delete-all-versions-and-metadata)
    - [Using Curl Commands](#using-curl-commands)
      - [Authentication](#authentication)
- [Login with userpass](#login-with-userpass)
- [Set token for subsequent requests](#set-token-for-subsequent-requests)
      - [Create Operations](#create-operations)
- [Write a secret](#write-a-secret)
- [Write with custom metadata](#write-with-custom-metadata)
      - [Read Operations](#read-operations)
- [Read a secret](#read-a-secret)
- [Read specific version](#read-specific-version)
- [List secrets](#list-secrets)
      - [Update Operations](#update-operations)
- [Update a secret](#update-a-secret)
- [Update metadata](#update-metadata)
      - [Delete Operations](#delete-operations)
- [Delete latest version](#delete-latest-version)
- [Delete specific versions](#delete-specific-versions)
- [Permanently delete versions](#permanently-delete-versions)
  - [Advanced Operations](#advanced-operations)
    - [Batch Operations](#batch-operations)
- [!/bin/bash](#!/bin/bash)
- [Batch write secrets](#batch-write-secrets)
- [Usage](#usage)
    - [Secret Rotation](#secret-rotation)
- [!/bin/bash](#!/bin/bash)
- [Usage](#usage)
    - [Error Handling](#error-handling)
- [!/bin/bash](#!/bin/bash)
- [Usage](#usage)
    - [Token Management](#token-management)
- [!/bin/bash](#!/bin/bash)
- [Create token with specific policy](#create-token-with-specific-policy)
- [Renew token](#renew-token)
- [Revoke token](#revoke-token)
  - [Best Practices](#best-practices)
    - [1. Environment Variables](#1-environment-variables)
- [!/bin/bash](#!/bin/bash)
- [Check required environment variables](#check-required-environment-variables)
    - [2. Secure Token Handling](#2-secure-token-handling)
- [!/bin/bash](#!/bin/bash)
- [Securely read token](#securely-read-token)
    - [3. Logging](#3-logging)
- [!/bin/bash](#!/bin/bash)
- [Usage](#usage)



This guide provides practical examples of interacting with HashiCorp Vault using Bash scripts and curl commands.

## Environment Setup

```bash
# Set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Set Vault token
export VAULT_TOKEN='your-token'

# Optional: Disable SSL verification for testing
export VAULT_SKIP_VERIFY=true
```

## Basic CRUD Operations

### Using Vault CLI

#### Create (Write) Operations

```bash
# Write a simple secret
vault kv put secret/my-app/config \
    username="admin" \
    password="secret123"

# Write JSON data
vault kv put secret/my-app/json @data.json

# Write with metadata
vault kv metadata put secret/my-app/config \
    custom_metadata=value \
    max_versions=5
```

#### Read Operations

```bash
# Read a secret
vault kv get secret/my-app/config

# Read specific version
vault kv get -version=2 secret/my-app/config

# Read as JSON
vault kv get -format=json secret/my-app/config

# List secrets
vault kv list secret/my-app/

# Read metadata
vault kv metadata get secret/my-app/config
```

#### Update Operations

```bash
# Update existing secret
vault kv patch secret/my-app/config \
    password="newpassword"

# Update metadata
vault kv metadata put secret/my-app/config \
    max_versions=10 \
    delete_version_after="30d"
```

#### Delete Operations

```bash
# Soft delete latest version
vault kv delete secret/my-app/config

# Delete specific version
vault kv delete -versions=2 secret/my-app/config

# Permanently delete versions
vault kv destroy -versions=1,2 secret/my-app/config

# Delete all versions and metadata
vault kv metadata delete secret/my-app/config
```

### Using Curl Commands

#### Authentication

```bash
# Login with userpass
TOKEN=$(curl \
    --request POST \
    --data '{"password": "password"}' \
    $VAULT_ADDR/v1/auth/userpass/login/username \
    | jq -r .auth.client_token)

# Set token for subsequent requests
export VAULT_TOKEN=$TOKEN
```

#### Create Operations

```bash
# Write a secret
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"data": {"username": "admin", "password": "secret123"}}' \
    $VAULT_ADDR/v1/secret/data/my-app/config

# Write with custom metadata
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"max_versions": 5, "custom_metadata": {"owner": "team-a"}}' \
    $VAULT_ADDR/v1/secret/metadata/my-app/config
```

#### Read Operations

```bash
# Read a secret
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    $VAULT_ADDR/v1/secret/data/my-app/config

# Read specific version
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    $VAULT_ADDR/v1/secret/data/my-app/config?version=2

# List secrets
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request LIST \
    $VAULT_ADDR/v1/secret/metadata/my-app/
```

#### Update Operations

```bash
# Update a secret
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"data": {"password": "newpassword"}}' \
    $VAULT_ADDR/v1/secret/data/my-app/config

# Update metadata
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"max_versions": 10}' \
    $VAULT_ADDR/v1/secret/metadata/my-app/config
```

#### Delete Operations

```bash
# Delete latest version
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request DELETE \
    $VAULT_ADDR/v1/secret/data/my-app/config

# Delete specific versions
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"versions": [1,2]}' \
    $VAULT_ADDR/v1/secret/delete/my-app/config

# Permanently delete versions
curl \
    --header "X-Vault-Token: $VAULT_TOKEN" \
    --request POST \
    --data '{"versions": [1,2]}' \
    $VAULT_ADDR/v1/secret/destroy/my-app/config
```

## Advanced Operations

### Batch Operations

```bash
#!/bin/bash

# Batch write secrets
batch_write() {
    local path=$1
    shift
    local data="{\"data\":{"
    while (( "$#" )); do
        data="$data\"$1\":\"$2\","
        shift 2
    done
    data="${data%,}}"
    
    curl \
        --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        --data "$data" \
        "$VAULT_ADDR/v1/secret/data/$path"
}

# Usage
batch_write "my-app/config" \
    "db_user" "admin" \
    "db_pass" "secret" \
    "api_key" "12345"
```

### Secret Rotation

```bash
#!/bin/bash

rotate_secret() {
    local path=$1
    local key=$2
    
    # Read current secret
    local current=$(curl -s \
        --header "X-Vault-Token: $VAULT_TOKEN" \
        "$VAULT_ADDR/v1/secret/data/$path" \
        | jq -r ".data.data.$key")
    
    # Generate new secret
    local new=$(openssl rand -base64 32)
    
    # Update secret
    curl \
        --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        --data "{\"data\":{\"$key\":\"$new\"}}" \
        "$VAULT_ADDR/v1/secret/data/$path"
    
    echo "Old: $current"
    echo "New: $new"
}

# Usage
rotate_secret "my-app/config" "api_key"
```

### Error Handling

```bash
#!/bin/bash

vault_operation() {
    local operation=$1
    local path=$2
    local data=$3
    local max_retries=3
    local retry_count=0
    
    while [ $retry_count -lt $max_retries ]; do
        response=$(curl -s -w "%{http_code}" \
            --header "X-Vault-Token: $VAULT_TOKEN" \
            --request $operation \
            ${data:+--data "$data"} \
            "$VAULT_ADDR/v1/secret/data/$path")
        
        status_code=${response: -3}
        body=${response:0:${#response}-3}
        
        case $status_code in
            200|204)
                echo "Success: $body"
                return 0
                ;;
            403)
                echo "Permission denied"
                return 1
                ;;
            404)
                echo "Secret not found"
                return 1
                ;;
            5*)
                if [ $retry_count -lt $((max_retries-1)) ]; then
                    echo "Server error, retrying..."
                    sleep $((2**retry_count))
                    ((retry_count++))
                    continue
                else
                    echo "Max retries reached"
                    return 1
                fi
                ;;
            *)
                echo "Unknown error: $status_code"
                return 1
                ;;
        esac
    done
}

# Usage
vault_operation "GET" "my-app/config"
vault_operation "POST" "my-app/config" '{"data":{"key":"value"}}'
```

### Token Management

```bash
#!/bin/bash

# Create token with specific policy
create_token() {
    local policy=$1
    local ttl=${2:-"1h"}
    
    curl \
        --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        --data "{
            \"policies\": [\"$policy\"],
            \"ttl\": \"$ttl\"
        }" \
        "$VAULT_ADDR/v1/auth/token/create"
}

# Renew token
renew_token() {
    local token=${1:-$VAULT_TOKEN}
    
    curl \
        --header "X-Vault-Token: $token" \
        --request POST \
        "$VAULT_ADDR/v1/auth/token/renew-self"
}

# Revoke token
revoke_token() {
    local token=${1:-$VAULT_TOKEN}
    
    curl \
        --header "X-Vault-Token: $VAULT_TOKEN" \
        --request POST \
        "$VAULT_ADDR/v1/auth/token/revoke" \
        --data "{\"token\": \"$token\"}"
}
```

## Best Practices

### 1. Environment Variables

```bash
#!/bin/bash

# Check required environment variables
check_env() {
    local required_vars=("VAULT_ADDR" "VAULT_TOKEN")
    local missing=()
    
    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing+=("$var")
        fi
    done
    
    if [ ${#missing[@]} -ne 0 ]; then
        echo "Missing required environment variables: ${missing[*]}"
        exit 1
    fi
}
```

### 2. Secure Token Handling

```bash
#!/bin/bash

# Securely read token
read_token() {
    local token_file=$1
    
    if [ -f "$token_file" ]; then
        VAULT_TOKEN=$(cat "$token_file")
    else
        read -s -p "Enter Vault token: " VAULT_TOKEN
        echo
    fi
    
    export VAULT_TOKEN
}
```

### 3. Logging

```bash
#!/bin/bash

log() {
    local level=$1
    shift
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] [$level] $*"
}

# Usage
log "INFO" "Starting secret rotation"
log "ERROR" "Failed to connect to Vault"
```

For more information on related topics, see:
- [Authentication Methods](../authentication.md)
- [Policy Management](../policies.md)
- [Secret Engines](../secret-engines.md)
