# F5 API Integration Guide for OpenStack

This guide covers how to use the F5 API to manage F5 GTM (Global Traffic Manager) and LTM (Local Traffic Manager) instances in an OpenStack environment.

## Table of Contents
- [F5 API Integration Guide for OpenStack](#f5-api-integration-guide-for-openstack)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Quick Start](#quick-start)
  - [Basic Connection Example](#basic-connection-example)
- [Connect to F5 device](#connect-to-f5-device)
- [Verify connection](#verify-connection)

1. [Installation and Setup](installation.md)
2. [Authentication](authentication.md)
3. [GTM Management](gtm_management.md)
4. [LTM Management](ltm_management.md)
5. [Data Center Operations](datacenter_operations.md)
6. [DNS and A Records](dns_records.md)
7. [Monitoring and Health Checks](monitoring.md)

## Prerequisites

- Python 3.6+
- F5 SDK (`f5-sdk`)
- OpenStack credentials
- F5 device credentials
- Network access to F5 devices

## Quick Start

```python
pip install f5-sdk requests
```

## Basic Connection Example

```python
from f5.bigip import ManagementRoot

# Connect to F5 device
mgmt = ManagementRoot("f5-device.example.com", 
                     "admin", 
                     "your-password",
                     port=443)

# Verify connection
version = mgmt.tmos_version
print(f"Connected to F5 version: {version}")
