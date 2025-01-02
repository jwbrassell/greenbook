# HashiCorp Vault Python Examples

## Table of Contents
- [HashiCorp Vault Python Examples](#hashicorp-vault-python-examples)
  - [Setup and Installation](#setup-and-installation)
- [Install required packages](#install-required-packages)
  - [Environment Configuration](#environment-configuration)
- [config.py](#configpy)
  - [Using hvac Client](#using-hvac-client)
    - [Basic Client Setup](#basic-client-setup)
    - [Basic CRUD Operations](#basic-crud-operations)
    - [Advanced Operations](#advanced-operations)
    - [Dynamic Secrets](#dynamic-secrets)
  - [Direct HTTP API Integration](#direct-http-api-integration)
    - [API Client](#api-client)
  - [Error Handling and Retries](#error-handling-and-retries)
  - [Usage Examples](#usage-examples)
    - [Basic Operations](#basic-operations)
- [Initialize operations](#initialize-operations)
- [Create secret](#create-secret)
- [Read secret](#read-secret)
- [Update secret](#update-secret)
- [List secrets](#list-secrets)
- [Delete secret](#delete-secret)
    - [Advanced Usage](#advanced-usage)
- [Initialize advanced operations](#initialize-advanced-operations)
- [Create secret with metadata](#create-secret-with-metadata)
- [Read specific version](#read-specific-version)
- [Soft delete versions](#soft-delete-versions)
- [Destroy versions](#destroy-versions)
    - [Dynamic Secrets](#dynamic-secrets)
- [Initialize dynamic secrets](#initialize-dynamic-secrets)
- [Generate database credentials](#generate-database-credentials)
- [Generate AWS credentials](#generate-aws-credentials)
    - [Direct API Usage](#direct-api-usage)
- [Initialize API client](#initialize-api-client)
- [Create secret](#create-secret)
- [Read secret](#read-secret)
- [List secrets](#list-secrets)
- [Delete secret](#delete-secret)



This guide provides examples of interacting with HashiCorp Vault using Python, both with the hvac client and direct HTTP API calls.

## Setup and Installation

```bash
# Install required packages
pip install hvac requests python-dotenv
```

## Environment Configuration

```python
# config.py
import os
from dotenv import load_dotenv

load_dotenv()

VAULT_URL = os.getenv('VAULT_ADDR', 'http://127.0.0.1:8200')
VAULT_TOKEN = os.getenv('VAULT_TOKEN')
```

## Using hvac Client

### Basic Client Setup

```python
import hvac
import json

def create_client():
    """Create and configure Vault client"""
    try:
        client = hvac.Client(
            url=VAULT_URL,
            token=VAULT_TOKEN
        )
        # Verify client is authenticated
        if client.is_authenticated():
            return client
        raise Exception("Client authentication failed")
    except Exception as e:
        raise Exception(f"Failed to create Vault client: {str(e)}")
```

### Basic CRUD Operations

```python
class VaultOperations:
    def __init__(self):
        self.client = create_client()
        self.mount_point = 'secret'  # KV version 2 secrets engine

    def create_secret(self, path, data):
        """Create or update a secret"""
        try:
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=self.mount_point
            )
            return True
        except Exception as e:
            print(f"Failed to create secret: {str(e)}")
            return False

    def read_secret(self, path):
        """Read a secret"""
        try:
            secret = self.client.secrets.kv.v2.read_secret_version(
                path=path,
                mount_point=self.mount_point
            )
            return secret['data']['data']
        except Exception as e:
            print(f"Failed to read secret: {str(e)}")
            return None

    def update_secret(self, path, data):
        """Update an existing secret"""
        try:
            current = self.read_secret(path)
            if current:
                updated = {**current, **data}
                return self.create_secret(path, updated)
            return False
        except Exception as e:
            print(f"Failed to update secret: {str(e)}")
            return False

    def delete_secret(self, path):
        """Delete a secret"""
        try:
            self.client.secrets.kv.v2.delete_metadata_and_all_versions(
                path=path,
                mount_point=self.mount_point
            )
            return True
        except Exception as e:
            print(f"Failed to delete secret: {str(e)}")
            return False

    def list_secrets(self, path):
        """List secrets at path"""
        try:
            return self.client.secrets.kv.v2.list_secrets(
                path=path,
                mount_point=self.mount_point
            )
        except Exception as e:
            print(f"Failed to list secrets: {str(e)}")
            return None
```

### Advanced Operations

```python
class AdvancedVaultOperations:
    def __init__(self):
        self.client = create_client()
        self.mount_point = 'secret'

    def create_with_metadata(self, path, data, metadata):
        """Create secret with custom metadata"""
        try:
            # Create secret
            self.client.secrets.kv.v2.create_or_update_secret(
                path=path,
                secret=data,
                mount_point=self.mount_point
            )
            
            # Update metadata
            self.client.secrets.kv.v2.update_metadata(
                path=path,
                mount_point=self.mount_point,
                custom_metadata=metadata
            )
            return True
        except Exception as e:
            print(f"Failed to create secret with metadata: {str(e)}")
            return False

    def read_secret_version(self, path, version):
        """Read specific version of a secret"""
        try:
            return self.client.secrets.kv.v2.read_secret_version(
                path=path,
                version=version,
                mount_point=self.mount_point
            )
        except Exception as e:
            print(f"Failed to read secret version: {str(e)}")
            return None

    def soft_delete(self, path, versions):
        """Soft delete specific versions of a secret"""
        try:
            self.client.secrets.kv.v2.delete_secret_versions(
                path=path,
                versions=versions,
                mount_point=self.mount_point
            )
            return True
        except Exception as e:
            print(f"Failed to soft delete versions: {str(e)}")
            return False

    def destroy_versions(self, path, versions):
        """Permanently destroy specific versions of a secret"""
        try:
            self.client.secrets.kv.v2.destroy_secret_versions(
                path=path,
                versions=versions,
                mount_point=self.mount_point
            )
            return True
        except Exception as e:
            print(f"Failed to destroy versions: {str(e)}")
            return False
```

### Dynamic Secrets

```python
class DynamicSecrets:
    def __init__(self):
        self.client = create_client()

    def generate_database_creds(self, role_name):
        """Generate dynamic database credentials"""
        try:
            response = self.client.secrets.database.generate_credentials(
                name=role_name
            )
            return {
                'username': response['data']['username'],
                'password': response['data']['password']
            }
        except Exception as e:
            print(f"Failed to generate database credentials: {str(e)}")
            return None

    def generate_aws_creds(self, role_name):
        """Generate dynamic AWS credentials"""
        try:
            response = self.client.secrets.aws.generate_credentials(
                name=role_name
            )
            return {
                'access_key': response['data']['access_key'],
                'secret_key': response['data']['secret_key']
            }
        except Exception as e:
            print(f"Failed to generate AWS credentials: {str(e)}")
            return None
```

## Direct HTTP API Integration

### API Client

```python
import requests
from urllib.parse import urljoin

class VaultAPI:
    def __init__(self, url=VAULT_URL, token=VAULT_TOKEN):
        self.url = url
        self.token = token
        self.headers = {'X-Vault-Token': token}

    def _request(self, method, endpoint, data=None):
        """Make HTTP request to Vault API"""
        try:
            url = urljoin(self.url, f'/v1/{endpoint}')
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return response.json() if response.text else None
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {str(e)}")
            return None

    def create_secret(self, path, data):
        """Create secret using direct API call"""
        endpoint = f'secret/data/{path}'
        payload = {'data': data}
        return self._request('POST', endpoint, payload)

    def read_secret(self, path):
        """Read secret using direct API call"""
        endpoint = f'secret/data/{path}'
        return self._request('GET', endpoint)

    def list_secrets(self, path):
        """List secrets using direct API call"""
        endpoint = f'secret/metadata/{path}'
        return self._request('LIST', endpoint)

    def delete_secret(self, path):
        """Delete secret using direct API call"""
        endpoint = f'secret/data/{path}'
        return self._request('DELETE', endpoint)
```

## Error Handling and Retries

```python
import time
from functools import wraps

def retry_operation(max_attempts=3, delay=1):
    """Retry decorator with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise e
                    wait = delay * (2 ** (attempts - 1))
                    print(f"Attempt {attempts} failed, retrying in {wait}s...")
                    time.sleep(wait)
            return None
        return wrapper
    return decorator

class ResilientVaultClient:
    def __init__(self):
        self.client = create_client()

    @retry_operation(max_attempts=3)
    def safe_read_secret(self, path):
        """Read secret with retry mechanism"""
        return self.client.secrets.kv.v2.read_secret_version(
            path=path,
            mount_point='secret'
        )
```

## Usage Examples

### Basic Operations

```python
# Initialize operations
vault_ops = VaultOperations()

# Create secret
secret_data = {
    'username': 'admin',
    'password': 'secret123'
}
vault_ops.create_secret('my-app/config', secret_data)

# Read secret
secret = vault_ops.read_secret('my-app/config')
print(secret)

# Update secret
update_data = {
    'password': 'newpassword'
}
vault_ops.update_secret('my-app/config', update_data)

# List secrets
secrets = vault_ops.list_secrets('my-app')
print(secrets)

# Delete secret
vault_ops.delete_secret('my-app/config')
```

### Advanced Usage

```python
# Initialize advanced operations
advanced_ops = AdvancedVaultOperations()

# Create secret with metadata
secret_data = {'api_key': '12345'}
metadata = {'owner': 'team-a', 'environment': 'prod'}
advanced_ops.create_with_metadata('my-app/api', secret_data, metadata)

# Read specific version
secret_v2 = advanced_ops.read_secret_version('my-app/api', 2)
print(secret_v2)

# Soft delete versions
advanced_ops.soft_delete('my-app/api', [1, 2])

# Destroy versions
advanced_ops.destroy_versions('my-app/api', [1, 2])
```

### Dynamic Secrets

```python
# Initialize dynamic secrets
dynamic = DynamicSecrets()

# Generate database credentials
db_creds = dynamic.generate_database_creds('readonly')
print(f"Database credentials: {db_creds}")

# Generate AWS credentials
aws_creds = dynamic.generate_aws_creds('s3-role')
print(f"AWS credentials: {aws_creds}")
```

### Direct API Usage

```python
# Initialize API client
api = VaultAPI()

# Create secret
api.create_secret('my-app/api', {'key': 'value'})

# Read secret
secret = api.read_secret('my-app/api')
print(secret)

# List secrets
secrets = api.list_secrets('my-app')
print(secrets)

# Delete secret
api.delete_secret('my-app/api')
```

For more information on related topics, see:
- [Authentication Methods](../authentication.md)
- [Policy Management](../policies.md)
- [Secret Engines](../secret-engines.md)
