# HashiCorp Vault Authentication Methods

## Table of Contents
- [HashiCorp Vault Authentication Methods](#hashicorp-vault-authentication-methods)
  - [Overview of Auth Methods](#overview-of-auth-methods)
  - [Token Authentication](#token-authentication)
- [Create a token](#create-a-token)
- [Login with token](#login-with-token)
- [Configure token auth settings](#configure-token-auth-settings)
- [Create token with specific parameters](#create-token-with-specific-parameters)
  - [AppRole Authentication](#approle-authentication)
- [Enable AppRole auth](#enable-approle-auth)
- [Create a role](#create-a-role)
- [Get RoleID](#get-roleid)
- [Generate SecretID](#generate-secretid)
- [Login with AppRole](#login-with-approle)
  - [Kubernetes Authentication](#kubernetes-authentication)
- [Enable Kubernetes auth](#enable-kubernetes-auth)
- [Configure Kubernetes auth](#configure-kubernetes-auth)
- [Create a role](#create-a-role)
  - [AWS Authentication](#aws-authentication)
- [Enable AWS auth](#enable-aws-auth)
- [Configure AWS auth](#configure-aws-auth)
- [Create role for EC2 auth](#create-role-for-ec2-auth)
- [Create role for IAM auth](#create-role-for-iam-auth)
  - [LDAP Authentication](#ldap-authentication)
- [Enable LDAP auth](#enable-ldap-auth)
- [Configure LDAP auth](#configure-ldap-auth)
- [Create group mapping](#create-group-mapping)
- [Test LDAP auth](#test-ldap-auth)
  - [GitHub Authentication](#github-authentication)
- [Enable GitHub auth](#enable-github-auth)
- [Configure GitHub auth](#configure-github-auth)
- [Map teams to policies](#map-teams-to-policies)
- [Login with GitHub](#login-with-github)
  - [TLS Certificate Authentication](#tls-certificate-authentication)
- [Enable TLS cert auth](#enable-tls-cert-auth)
- [Configure CA certificate](#configure-ca-certificate)
- [Login with cert](#login-with-cert)
  - [OIDC Authentication](#oidc-authentication)
- [Enable OIDC auth](#enable-oidc-auth)
- [Configure OIDC auth](#configure-oidc-auth)
- [Create role](#create-role)
  - [Userpass Authentication](#userpass-authentication)
- [Enable userpass auth](#enable-userpass-auth)
- [Create/update user](#create/update-user)
- [Login with userpass](#login-with-userpass)
  - [Best Practices](#best-practices)
  - [Common Configuration Patterns](#common-configuration-patterns)
    - [Application Authentication](#application-authentication)
- [AppRole setup for application](#approle-setup-for-application)
- [Get credentials](#get-credentials)
- [Application login](#application-login)
    - [CI/CD Integration](#ci/cd-integration)
- [Create specific role for CI/CD](#create-specific-role-for-ci/cd)
- [Jenkins credential rotation](#jenkins-credential-rotation)
    - [Kubernetes Integration](#kubernetes-integration)
- [Service account setup](#service-account-setup)
- [Vault configuration](#vault-configuration)
  - [Troubleshooting](#troubleshooting)
- [Check auth method status](#check-auth-method-status)
- [Test token capabilities](#test-token-capabilities)
- [View auth method configuration](#view-auth-method-configuration)
- [Check token details](#check-token-details)
- [View token accessor](#view-token-accessor)
- [Check token policies](#check-token-policies)
- [View auth tuning](#view-auth-tuning)
- [Check mount configuration](#check-mount-configuration)
- [List auth mounts](#list-auth-mounts)



This guide covers the various authentication methods available in HashiCorp Vault and how to configure them.

## Overview of Auth Methods

Vault supports multiple authentication methods, allowing users and applications to authenticate using the mechanism that best fits their use case.

## Token Authentication

The default authentication method built into Vault.

```bash
# Create a token
vault token create -policy=my-policy

# Login with token
vault login <token>

# Configure token auth settings
vault auth tune token/

# Create token with specific parameters
vault token create \
    -policy="my-policy" \
    -period=24h \
    -display-name="app-token"
```

## AppRole Authentication

Designed for application authentication.

```bash
# Enable AppRole auth
vault auth enable approle

# Create a role
vault write auth/approle/role/my-app \
    token_policies="my-policy" \
    token_ttl=1h \
    token_max_ttl=4h

# Get RoleID
vault read auth/approle/role/my-app/role-id

# Generate SecretID
vault write -f auth/approle/role/my-app/secret-id

# Login with AppRole
vault write auth/approle/login \
    role_id="<role_id>" \
    secret_id="<secret_id>"
```

## Kubernetes Authentication

For applications running in Kubernetes.

```bash
# Enable Kubernetes auth
vault auth enable kubernetes

# Configure Kubernetes auth
vault write auth/kubernetes/config \
    kubernetes_host="https://kubernetes.default.svc" \
    kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
    token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token

# Create a role
vault write auth/kubernetes/role/my-app \
    bound_service_account_names=my-app \
    bound_service_account_namespaces=default \
    policies=my-policy \
    ttl=1h
```

## AWS Authentication

For AWS EC2 instances and IAM principals.

```bash
# Enable AWS auth
vault auth enable aws

# Configure AWS auth
vault write auth/aws/config/client \
    access_key=AKIAXXXXXXXXXXXXXXXX \
    secret_key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX \
    region=us-east-1

# Create role for EC2 auth
vault write auth/aws/role/my-role \
    auth_type=ec2 \
    policies=my-policy \
    max_ttl=24h \
    bound_ami_id=ami-12345678

# Create role for IAM auth
vault write auth/aws/role/my-iam-role \
    auth_type=iam \
    policies=my-policy \
    bound_iam_principal_arn=arn:aws:iam::123456789012:role/my-role
```

## LDAP Authentication

For integrating with Active Directory or other LDAP servers.

```bash
# Enable LDAP auth
vault auth enable ldap

# Configure LDAP auth
vault write auth/ldap/config \
    url="ldaps://ldap.example.com" \
    userdn="ou=Users,dc=example,dc=com" \
    groupdn="ou=Groups,dc=example,dc=com" \
    groupattr="memberOf" \
    userattr="uid" \
    binddn="cn=vault,dc=example,dc=com" \
    bindpass="bindpass123"

# Create group mapping
vault write auth/ldap/groups/engineers \
    policies=engineering-policy

# Test LDAP auth
vault login -method=ldap username=john.doe
```

## GitHub Authentication

For development teams using GitHub.

```bash
# Enable GitHub auth
vault auth enable github

# Configure GitHub auth
vault write auth/github/config \
    organization=my-org

# Map teams to policies
vault write auth/github/map/teams/developers \
    value=developer-policy

# Login with GitHub
vault login -method=github token=<github-token>
```

## TLS Certificate Authentication

For clients with X.509 certificates.

```bash
# Enable TLS cert auth
vault auth enable cert

# Configure CA certificate
vault write auth/cert/certs/web \
    display_name=web \
    policies=web-policy \
    certificate=@ca.pem \
    ttl=3600

# Login with cert
vault login -method=cert \
    -client-cert=cert.pem \
    -client-key=key.pem
```

## OIDC Authentication

For integrating with OpenID Connect providers.

```bash
# Enable OIDC auth
vault auth enable oidc

# Configure OIDC auth
vault write auth/oidc/config \
    oidc_discovery_url="https://accounts.google.com" \
    oidc_client_id="your-client-id" \
    oidc_client_secret="your-client-secret" \
    default_role="default"

# Create role
vault write auth/oidc/role/default \
    user_claim="sub" \
    allowed_redirect_uris="http://localhost:8250/oidc/callback" \
    policies="default"
```

## Userpass Authentication

Simple username/password authentication.

```bash
# Enable userpass auth
vault auth enable userpass

# Create/update user
vault write auth/userpass/users/john \
    password="password123" \
    policies="user-policy"

# Login with userpass
vault login -method=userpass \
    username=john \
    password=password123
```

## Best Practices

1. **Method Selection**
   - Choose auth methods based on use case
   - Use AppRole for applications
   - Use OIDC/LDAP for human users
   - Consider multiple auth methods for different needs

2. **Security Considerations**
   - Regularly rotate credentials
   - Use short-lived tokens
   - Implement proper access controls
   - Enable audit logging

3. **Token Management**
   - Set appropriate TTLs
   - Use token roles
   - Implement token renewal
   - Regular token cleanup

4. **Integration Patterns**
   - Use response wrapping
   - Implement proper error handling
   - Monitor auth failures
   - Regular access review

## Common Configuration Patterns

### Application Authentication

```bash
# AppRole setup for application
vault write auth/approle/role/my-app \
    token_policies="app-policy" \
    token_ttl=1h \
    token_max_ttl=4h \
    secret_id_ttl=10m

# Get credentials
ROLE_ID=$(vault read -field=role_id auth/approle/role/my-app/role-id)
SECRET_ID=$(vault write -f -field=secret_id auth/approle/role/my-app/secret-id)

# Application login
vault write auth/approle/login \
    role_id="$ROLE_ID" \
    secret_id="$SECRET_ID"
```

### CI/CD Integration

```bash
# Create specific role for CI/CD
vault write auth/approle/role/ci-role \
    token_policies="ci-policy" \
    token_ttl=1h \
    secret_id_num_uses=1

# Jenkins credential rotation
vault write auth/approle/role/jenkins \
    token_policies="jenkins-policy" \
    secret_id_ttl=24h \
    token_period=24h
```

### Kubernetes Integration

```bash
# Service account setup
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: my-app
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: role-tokenreview-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: system:auth-delegator
subjects:
- kind: ServiceAccount
  name: my-app
  namespace: default
EOF

# Vault configuration
vault write auth/kubernetes/role/my-app \
    bound_service_account_names=my-app \
    bound_service_account_namespaces=default \
    policies=my-policy \
    ttl=1h
```

## Troubleshooting

1. **Authentication Failures**
```bash
# Check auth method status
vault auth list

# Test token capabilities
vault token capabilities <token> path/to/secret

# View auth method configuration
vault read auth/<method>/config
```

2. **Token Issues**
```bash
# Check token details
vault token lookup

# View token accessor
vault list auth/token/accessors

# Check token policies
vault token lookup -format=json | jq -r ".data.policies"
```

3. **Auth Method Configuration**
```bash
# View auth tuning
vault auth tune -listing

# Check mount configuration
vault read sys/auth/<path>/tune

# List auth mounts
vault auth list -detailed
```

For more information on related topics, see:
- [Policy Management](policies.md)
- [Audit Logging](audit-logging.md)
- [Secret Engines](secret-engines.md)
