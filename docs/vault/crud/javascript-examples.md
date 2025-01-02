# HashiCorp Vault JavaScript Examples

## Table of Contents
- [HashiCorp Vault JavaScript Examples](#hashicorp-vault-javascript-examples)
  - [Setup and Installation](#setup-and-installation)
- [Install required packages](#install-required-packages)
  - [Environment Configuration](#environment-configuration)
  - [Using node-vault Client](#using-node-vault-client)
    - [Basic Client Setup](#basic-client-setup)
    - [Basic CRUD Operations](#basic-crud-operations)
    - [Advanced Operations](#advanced-operations)
    - [Dynamic Secrets](#dynamic-secrets)
  - [Direct HTTP API Integration](#direct-http-api-integration)
    - [API Client](#api-client)
  - [Error Handling and Retries](#error-handling-and-retries)
  - [Browser Integration](#browser-integration)
  - [Usage Examples](#usage-examples)
    - [Basic Operations](#basic-operations)
    - [Advanced Usage](#advanced-usage)
    - [Dynamic Secrets](#dynamic-secrets)
    - [Direct API Usage](#direct-api-usage)



This guide provides examples of interacting with HashiCorp Vault using JavaScript, both with the node-vault client and direct HTTP API calls.

## Setup and Installation

```bash
# Install required packages
npm install node-vault axios dotenv
```

## Environment Configuration

```javascript
// config.js
require('dotenv').config();

const config = {
  vaultUrl: process.env.VAULT_ADDR || 'http://127.0.0.1:8200',
  vaultToken: process.env.VAULT_TOKEN
};

module.exports = config;
```

## Using node-vault Client

### Basic Client Setup

```javascript
// vaultClient.js
const vault = require('node-vault');
const config = require('./config');

function createClient() {
  try {
    const client = vault({
      apiVersion: 'v1',
      endpoint: config.vaultUrl,
      token: config.vaultToken
    });
    return client;
  } catch (error) {
    throw new Error(`Failed to create Vault client: ${error.message}`);
  }
}

module.exports = createClient;
```

### Basic CRUD Operations

```javascript
// vaultOperations.js
const createClient = require('./vaultClient');

class VaultOperations {
  constructor() {
    this.client = createClient();
    this.mountPoint = 'secret';
  }

  async createSecret(path, data) {
    try {
      await this.client.write(
        `${this.mountPoint}/data/${path}`,
        { data }
      );
      return true;
    } catch (error) {
      console.error(`Failed to create secret: ${error.message}`);
      return false;
    }
  }

  async readSecret(path) {
    try {
      const { data } = await this.client.read(
        `${this.mountPoint}/data/${path}`
      );
      return data.data;
    } catch (error) {
      console.error(`Failed to read secret: ${error.message}`);
      return null;
    }
  }

  async updateSecret(path, data) {
    try {
      const current = await this.readSecret(path);
      if (current) {
        const updated = { ...current, ...data };
        return await this.createSecret(path, updated);
      }
      return false;
    } catch (error) {
      console.error(`Failed to update secret: ${error.message}`);
      return false;
    }
  }

  async deleteSecret(path) {
    try {
      await this.client.delete(`${this.mountPoint}/metadata/${path}`);
      return true;
    } catch (error) {
      console.error(`Failed to delete secret: ${error.message}`);
      return false;
    }
  }

  async listSecrets(path) {
    try {
      const { data } = await this.client.list(
        `${this.mountPoint}/metadata/${path}`
      );
      return data.keys;
    } catch (error) {
      console.error(`Failed to list secrets: ${error.message}`);
      return null;
    }
  }
}

module.exports = VaultOperations;
```

### Advanced Operations

```javascript
// advancedOperations.js
const createClient = require('./vaultClient');

class AdvancedVaultOperations {
  constructor() {
    this.client = createClient();
    this.mountPoint = 'secret';
  }

  async createWithMetadata(path, data, metadata) {
    try {
      // Create secret
      await this.client.write(
        `${this.mountPoint}/data/${path}`,
        { data }
      );

      // Update metadata
      await this.client.write(
        `${this.mountPoint}/metadata/${path}`,
        { custom_metadata: metadata }
      );
      return true;
    } catch (error) {
      console.error(`Failed to create secret with metadata: ${error.message}`);
      return false;
    }
  }

  async readSecretVersion(path, version) {
    try {
      const { data } = await this.client.read(
        `${this.mountPoint}/data/${path}`,
        { version }
      );
      return data.data;
    } catch (error) {
      console.error(`Failed to read secret version: ${error.message}`);
      return null;
    }
  }

  async softDelete(path, versions) {
    try {
      await this.client.write(
        `${this.mountPoint}/delete/${path}`,
        { versions }
      );
      return true;
    } catch (error) {
      console.error(`Failed to soft delete versions: ${error.message}`);
      return false;
    }
  }

  async destroyVersions(path, versions) {
    try {
      await this.client.write(
        `${this.mountPoint}/destroy/${path}`,
        { versions }
      );
      return true;
    } catch (error) {
      console.error(`Failed to destroy versions: ${error.message}`);
      return false;
    }
  }
}

module.exports = AdvancedVaultOperations;
```

### Dynamic Secrets

```javascript
// dynamicSecrets.js
const createClient = require('./vaultClient');

class DynamicSecrets {
  constructor() {
    this.client = createClient();
  }

  async generateDatabaseCreds(roleName) {
    try {
      const { data } = await this.client.read(
        `database/creds/${roleName}`
      );
      return {
        username: data.username,
        password: data.password
      };
    } catch (error) {
      console.error(`Failed to generate database credentials: ${error.message}`);
      return null;
    }
  }

  async generateAwsCreds(roleName) {
    try {
      const { data } = await this.client.read(
        `aws/creds/${roleName}`
      );
      return {
        accessKey: data.access_key,
        secretKey: data.secret_key
      };
    } catch (error) {
      console.error(`Failed to generate AWS credentials: ${error.message}`);
      return null;
    }
  }
}

module.exports = DynamicSecrets;
```

## Direct HTTP API Integration

### API Client

```javascript
// vaultApi.js
const axios = require('axios');
const config = require('./config');

class VaultAPI {
  constructor(url = config.vaultUrl, token = config.vaultToken) {
    this.url = url;
    this.token = token;
    this.client = axios.create({
      baseURL: `${url}/v1`,
      headers: {
        'X-Vault-Token': token
      }
    });
  }

  async request(method, endpoint, data = null) {
    try {
      const response = await this.client({
        method,
        url: endpoint,
        data
      });
      return response.data;
    } catch (error) {
      console.error(`API request failed: ${error.message}`);
      return null;
    }
  }

  async createSecret(path, data) {
    return this.request(
      'POST',
      `secret/data/${path}`,
      { data }
    );
  }

  async readSecret(path) {
    return this.request('GET', `secret/data/${path}`);
  }

  async listSecrets(path) {
    return this.request('LIST', `secret/metadata/${path}`);
  }

  async deleteSecret(path) {
    return this.request('DELETE', `secret/data/${path}`);
  }
}

module.exports = VaultAPI;
```

## Error Handling and Retries

```javascript
// utils.js
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function retryOperation(operation, maxAttempts = 3, delay = 1000) {
  let attempts = 0;
  while (attempts < maxAttempts) {
    try {
      return await operation();
    } catch (error) {
      attempts++;
      if (attempts === maxAttempts) throw error;
      const wait = delay * Math.pow(2, attempts - 1);
      console.log(`Attempt ${attempts} failed, retrying in ${wait}ms...`);
      await sleep(wait);
    }
  }
}

module.exports = {
  retryOperation
};
```

## Browser Integration

```javascript
// browser.js
class VaultBrowser {
  constructor(vaultUrl) {
    this.vaultUrl = vaultUrl;
  }

  async login(username, password) {
    try {
      const response = await fetch(
        `${this.vaultUrl}/v1/auth/userpass/login/${username}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ password })
        }
      );
      const data = await response.json();
      return data.auth.client_token;
    } catch (error) {
      console.error(`Login failed: ${error.message}`);
      return null;
    }
  }

  async readSecret(path, token) {
    try {
      const response = await fetch(
        `${this.vaultUrl}/v1/secret/data/${path}`,
        {
          headers: {
            'X-Vault-Token': token
          }
        }
      );
      const data = await response.json();
      return data.data.data;
    } catch (error) {
      console.error(`Failed to read secret: ${error.message}`);
      return null;
    }
  }
}
```

## Usage Examples

### Basic Operations

```javascript
const VaultOperations = require('./vaultOperations');

async function basicExample() {
  const vault = new VaultOperations();

  // Create secret
  const secretData = {
    username: 'admin',
    password: 'secret123'
  };
  await vault.createSecret('my-app/config', secretData);

  // Read secret
  const secret = await vault.readSecret('my-app/config');
  console.log(secret);

  // Update secret
  const updateData = {
    password: 'newpassword'
  };
  await vault.updateSecret('my-app/config', updateData);

  // List secrets
  const secrets = await vault.listSecrets('my-app');
  console.log(secrets);

  // Delete secret
  await vault.deleteSecret('my-app/config');
}
```

### Advanced Usage

```javascript
const AdvancedVaultOperations = require('./advancedOperations');

async function advancedExample() {
  const vault = new AdvancedVaultOperations();

  // Create secret with metadata
  const secretData = { api_key: '12345' };
  const metadata = {
    owner: 'team-a',
    environment: 'prod'
  };
  await vault.createWithMetadata('my-app/api', secretData, metadata);

  // Read specific version
  const secretV2 = await vault.readSecretVersion('my-app/api', 2);
  console.log(secretV2);

  // Soft delete versions
  await vault.softDelete('my-app/api', [1, 2]);

  // Destroy versions
  await vault.destroyVersions('my-app/api', [1, 2]);
}
```

### Dynamic Secrets

```javascript
const DynamicSecrets = require('./dynamicSecrets');

async function dynamicExample() {
  const dynamic = new DynamicSecrets();

  // Generate database credentials
  const dbCreds = await dynamic.generateDatabaseCreds('readonly');
  console.log('Database credentials:', dbCreds);

  // Generate AWS credentials
  const awsCreds = await dynamic.generateAwsCreds('s3-role');
  console.log('AWS credentials:', awsCreds);
}
```

### Direct API Usage

```javascript
const VaultAPI = require('./vaultApi');

async function apiExample() {
  const api = new VaultAPI();

  // Create secret
  await api.createSecret('my-app/api', { key: 'value' });

  // Read secret
  const secret = await api.readSecret('my-app/api');
  console.log(secret);

  // List secrets
  const secrets = await api.listSecrets('my-app');
  console.log(secrets);

  // Delete secret
  await api.deleteSecret('my-app/api');
}
```

For more information on related topics, see:
- [Authentication Methods](../authentication.md)
- [Policy Management](../policies.md)
- [Secret Engines](../secret-engines.md)
