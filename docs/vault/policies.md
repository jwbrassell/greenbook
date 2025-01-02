# HashiCorp Vault Policy Management

## Table of Contents
- [HashiCorp Vault Policy Management](#hashicorp-vault-policy-management)
  - [Policy Basics](#policy-basics)
    - [Policy Structure](#policy-structure)
- [Basic policy structure](#basic-policy-structure)
  - [Creating and Managing Policies](#creating-and-managing-policies)
    - [Basic Policy Operations](#basic-policy-operations)
- [Write a policy](#write-a-policy)
- [Read a policy](#read-a-policy)
- [List policies](#list-policies)
- [Delete a policy](#delete-a-policy)
  - [Common Policy Examples](#common-policy-examples)
    - [Read-Only Policy](#read-only-policy)
- [read-only.hcl](#read-onlyhcl)
    - [Developer Policy](#developer-policy)
- [developer.hcl](#developerhcl)
- [Allow full access to dev/ path](#allow-full-access-to-dev/-path)
- [Allow listing of secret mounts](#allow-listing-of-secret-mounts)
- [Allow reading specific application configs](#allow-reading-specific-application-configs)
    - [Admin Policy](#admin-policy)
- [admin.hcl](#adminhcl)
- [Full access to all secret paths](#full-access-to-all-secret-paths)
- [System management capabilities](#system-management-capabilities)
- [Auth method management](#auth-method-management)
    - [Application Policy](#application-policy)
- [app-policy.hcl](#app-policyhcl)
- [Allow access to application-specific secrets](#allow-access-to-application-specific-secrets)
- [Allow database credential generation](#allow-database-credential-generation)
- [Allow token renewal](#allow-token-renewal)
  - [Advanced Policy Features](#advanced-policy-features)
    - [Parameter Templating](#parameter-templating)
- [Use templating for dynamic paths](#use-templating-for-dynamic-paths)
- [Use metadata in paths](#use-metadata-in-paths)
    - [Required Parameters](#required-parameters)
- [Require specific parameters in requests](#require-specific-parameters-in-requests)
    - [Denied Parameters](#denied-parameters)
- [Deny specific parameters](#deny-specific-parameters)
    - [Response Wrapping](#response-wrapping)
- [Enforce response wrapping](#enforce-response-wrapping)
  - [Policy Best Practices](#policy-best-practices)
    - [1. Principle of Least Privilege](#1-principle-of-least-privilege)
- [Instead of broad access](#instead-of-broad-access)
- [Use specific paths](#use-specific-paths)
    - [2. Path Segmentation](#2-path-segmentation)
- [Segment by environment](#segment-by-environment)
    - [3. Token Binding](#3-token-binding)
- [Bind policy to specific auth method](#bind-policy-to-specific-auth-method)
  - [Common Policy Patterns](#common-policy-patterns)
    - [1. Service Account Pattern](#1-service-account-pattern)
- [service-account.hcl](#service-accounthcl)
- [Allow service to read its own config](#allow-service-to-read-its-own-config)
- [Allow service to generate database credentials](#allow-service-to-generate-database-credentials)
- [Allow service to renew its token](#allow-service-to-renew-its-token)
- [Allow service to renew its database credentials](#allow-service-to-renew-its-database-credentials)
    - [2. Team Access Pattern](#2-team-access-pattern)
- [team-policy.hcl](#team-policyhcl)
- [Allow team members to access team secrets](#allow-team-members-to-access-team-secrets)
- [Allow team members to generate credentials](#allow-team-members-to-generate-credentials)
- [Allow team members to manage their own service accounts](#allow-team-members-to-manage-their-own-service-accounts)
    - [3. Environment-Based Pattern](#3-environment-based-pattern)
- [environment.hcl](#environmenthcl)
- [Production access](#production-access)
- [Development access](#development-access)
  - [Troubleshooting](#troubleshooting)
    - [1. Policy Testing](#1-policy-testing)
- [Test token capabilities](#test-token-capabilities)
- [Create token with policy](#create-token-with-policy)
- [Test policy with different paths](#test-policy-with-different-paths)
    - [2. Common Issues](#2-common-issues)
- [Check effective policies](#check-effective-policies)
- [View policy details](#view-policy-details)
- [Test path access](#test-path-access)
    - [3. Audit Logging](#3-audit-logging)
- [Enable audit logging](#enable-audit-logging)
- [Review access denials](#review-access-denials)
  - [Integration Examples](#integration-examples)
    - [1. CI/CD Pipeline](#1-ci/cd-pipeline)
- [ci-cd-policy.hcl](#ci-cd-policyhcl)
    - [2. Kubernetes Integration](#2-kubernetes-integration)
- [kubernetes-policy.hcl](#kubernetes-policyhcl)



This guide covers how to create and manage policies in HashiCorp Vault. Policies define permissions and access control for tokens and authentication methods.

## Policy Basics

Policies in Vault are written in HashiCorp Configuration Language (HCL) and specify access rules for paths in Vault.

### Policy Structure

```hcl
# Basic policy structure
path "secret/data/foo" {
  capabilities = ["read", "list"]
}
```

Available capabilities:
- `create` - Create new data
- `read` - Read data
- `update` - Update existing data
- `delete` - Delete data
- `list` - List data
- `sudo` - Privileged operations
- `deny` - Explicitly deny access

## Creating and Managing Policies

### Basic Policy Operations

```bash
# Write a policy
vault policy write my-policy -<<EOF
path "secret/data/foo" {
  capabilities = ["read", "list"]
}
EOF

# Read a policy
vault policy read my-policy

# List policies
vault policy list

# Delete a policy
vault policy delete my-policy
```

## Common Policy Examples

### Read-Only Policy

```hcl
# read-only.hcl
path "secret/data/*" {
  capabilities = ["read", "list"]
}

path "secret/metadata/*" {
  capabilities = ["list"]
}
```

### Developer Policy

```hcl
# developer.hcl
# Allow full access to dev/ path
path "secret/data/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow listing of secret mounts
path "secret/metadata/*" {
  capabilities = ["list"]
}

# Allow reading specific application configs
path "secret/data/apps/config" {
  capabilities = ["read"]
}
```

### Admin Policy

```hcl
# admin.hcl
# Full access to all secret paths
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# System management capabilities
path "sys/*" {
  capabilities = ["create", "read", "update", "delete", "sudo"]
}

# Auth method management
path "auth/*" {
  capabilities = ["create", "read", "update", "delete", "list", "sudo"]
}
```

### Application Policy

```hcl
# app-policy.hcl
# Allow access to application-specific secrets
path "secret/data/apps/${app_name}/*" {
  capabilities = ["read"]
}

# Allow database credential generation
path "database/creds/${app_name}" {
  capabilities = ["read"]
}

# Allow token renewal
path "auth/token/renew-self" {
  capabilities = ["update"]
}
```

## Advanced Policy Features

### Parameter Templating

```hcl
# Use templating for dynamic paths
path "secret/data/{{identity.entity.name}}/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Use metadata in paths
path "secret/data/{{identity.entity.metadata.team}}/*" {
  capabilities = ["read", "list"]
}
```

### Required Parameters

```hcl
# Require specific parameters in requests
path "secret/data/foo" {
  capabilities = ["create", "update"]
  required_parameters = ["username", "password"]
}
```

### Denied Parameters

```hcl
# Deny specific parameters
path "secret/data/foo" {
  capabilities = ["create", "update"]
  denied_parameters = {
    "password" = []
  }
}
```

### Response Wrapping

```hcl
# Enforce response wrapping
path "secret/data/foo" {
  capabilities = ["read"]
  min_wrapping_ttl = "1h"
  max_wrapping_ttl = "24h"
}
```

## Policy Best Practices

### 1. Principle of Least Privilege

```hcl
# Instead of broad access
path "secret/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Use specific paths
path "secret/data/apps/${app_name}/*" {
  capabilities = ["read"]
}
```

### 2. Path Segmentation

```hcl
# Segment by environment
path "secret/data/prod/*" {
  capabilities = ["read"]
  condition {
    env = ["prod"]
  }
}

path "secret/data/dev/*" {
  capabilities = ["create", "read", "update", "delete"]
  condition {
    env = ["dev"]
  }
}
```

### 3. Token Binding

```hcl
# Bind policy to specific auth method
path "auth/approle/role/app1/secret-id" {
  capabilities = ["create", "update"]
  bound_cidr_list = ["10.0.0.0/16"]
}
```

## Common Policy Patterns

### 1. Service Account Pattern

```hcl
# service-account.hcl
# Allow service to read its own config
path "secret/data/services/${service_name}/config" {
  capabilities = ["read"]
}

# Allow service to generate database credentials
path "database/creds/${service_name}" {
  capabilities = ["read"]
}

# Allow service to renew its token
path "auth/token/renew-self" {
  capabilities = ["update"]
}

# Allow service to renew its database credentials
path "sys/leases/renew" {
  capabilities = ["update"]
}
```

### 2. Team Access Pattern

```hcl
# team-policy.hcl
# Allow team members to access team secrets
path "secret/data/teams/${team_name}/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}

# Allow team members to generate credentials
path "database/creds/${team_name}-*" {
  capabilities = ["read"]
}

# Allow team members to manage their own service accounts
path "auth/approle/role/${team_name}-*" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

### 3. Environment-Based Pattern

```hcl
# environment.hcl
# Production access
path "secret/data/prod/*" {
  capabilities = ["read"]
  allowed_parameters = {
    "*" = []
  }
}

# Development access
path "secret/data/dev/*" {
  capabilities = ["create", "read", "update", "delete", "list"]
  denied_parameters = {
    "restricted_*" = []
  }
}
```

## Troubleshooting

### 1. Policy Testing

```bash
# Test token capabilities
vault token capabilities <token> path/to/secret

# Create token with policy
vault token create -policy=my-policy

# Test policy with different paths
vault token capabilities <token> secret/data/foo
vault token capabilities <token> secret/data/bar
```

### 2. Common Issues

```bash
# Check effective policies
vault token lookup | grep policies

# View policy details
vault policy read my-policy

# Test path access
vault auth token/lookup-self
```

### 3. Audit Logging

```bash
# Enable audit logging
vault audit enable file file_path=/var/log/vault/audit.log

# Review access denials
grep "permission denied" /var/log/vault/audit.log
```

## Integration Examples

### 1. CI/CD Pipeline

```hcl
# ci-cd-policy.hcl
path "secret/data/ci/*" {
  capabilities = ["read"]
}

path "auth/approle/role/ci-role/*" {
  capabilities = ["read"]
}
```

### 2. Kubernetes Integration

```hcl
# kubernetes-policy.hcl
path "auth/kubernetes/role/*" {
  capabilities = ["create", "read", "update", "delete"]
}

path "secret/data/k8s/*" {
  capabilities = ["read"]
}
```

For more information on related topics, see:
- [Authentication Methods](authentication.md)
- [Secret Engines](secret-engines.md)
- [Audit Logging](audit-logging.md)
