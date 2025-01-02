# HashiCorp Vault Guide

## Table of Contents
- [HashiCorp Vault Guide](#hashicorp-vault-guide)
  - [What is HashiCorp Vault?](#what-is-hashicorp-vault?)
  - [Core Features](#core-features)
  - [Guide Contents](#guide-contents)
  - [Quick Start](#quick-start)
- [Start Vault in development mode](#start-vault-in-development-mode)
- [Set environment variable for Vault address](#set-environment-variable-for-vault-address)
- [Initialize Vault](#initialize-vault)
- [Unseal Vault (required in production, not in dev mode)](#unseal-vault-required-in-production,-not-in-dev-mode)
  - [Key Concepts](#key-concepts)
  - [Use Cases](#use-cases)



HashiCorp Vault is a secrets management tool that provides a secure, centralized solution for managing sensitive data such as API keys, passwords, certificates, and encryption keys. This comprehensive guide covers everything from basic concepts to advanced implementations.

## What is HashiCorp Vault?

Vault is designed to address several key challenges in modern infrastructure:

- **Secrets Management**: Securely store and control access to tokens, passwords, certificates, and encryption keys
- **Data Encryption**: Encrypt and decrypt data in transit and at rest
- **Identity-based Access**: Provide authentication and authorization through multiple providers
- **Key Management**: Generate, distribute, and revoke encryption keys
- **Audit Logging**: Track all secrets access with detailed audit logs

## Core Features

- **Dynamic Secrets**: Generate on-demand secrets for various services
- **Data Encryption**: Encrypt/decrypt data without storing it
- **Leasing and Renewal**: Automatically revoke secrets after a specified time
- **Secure Storage**: Multiple storage backends with encryption
- **Access Control**: Fine-grained policies for access management
- **Multiple Auth Methods**: Support for various authentication mechanisms
- **API-driven**: RESTful API for all operations

## Guide Contents

1. [Setup and Installation](setup.md)
2. [Basic Usage Guide](usage.md)
3. [Authentication Methods](authentication.md)
4. [Policy Management](policies.md)
5. [Secret Engines](secret-engines.md)
6. [CRUD Operations](crud/index.md)
   - [Bash Examples](crud/bash-examples.md)
   - [Python Examples](crud/python-examples.md)
   - [JavaScript Examples](crud/javascript-examples.md)

## Quick Start

```bash
# Start Vault in development mode
vault server -dev

# Set environment variable for Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Initialize Vault
vault operator init

# Unseal Vault (required in production, not in dev mode)
vault operator unseal
```

## Key Concepts

1. **Secrets**: Any sensitive information that needs to be tightly controlled
2. **Secret Engines**: Components managing different types of secrets
3. **Authentication**: Methods to verify identity
4. **Policies**: Rules defining access permissions
5. **Tokens**: Core authentication method used by clients
6. **Leases**: Time-limited access to secrets

## Use Cases

- Storing database credentials
- Managing API keys
- Storing SSL/TLS certificates
- Encrypting application data
- Managing SSH access
- Protecting sensitive configuration

For detailed information on each topic, please refer to the respective sections in this guide.
