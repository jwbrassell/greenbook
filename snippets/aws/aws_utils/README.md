# AWS Utilities Package

## Table of Contents
- [AWS Utilities Package](#aws-utilities-package)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Available Modules](#available-modules)
    - [EC2 Utilities (ec2_utils)](#ec2-utilities-ec2_utils)
- [List running instances](#list-running-instances)
- [Create a new instance](#create-a-new-instance)
- [Get instance status](#get-instance-status)
    - [IAM Utilities (iam_utils)](#iam-utilities-iam_utils)
- [Create a new IAM user](#create-a-new-iam-user)
- [Create access keys](#create-access-keys)
- [Create role with policy](#create-role-with-policy)
    - [Route53 Utilities (route53_utils)](#route53-utilities-route53_utils)
- [Create hosted zone](#create-hosted-zone)
- [Add DNS record](#add-dns-record)
- [Create health check](#create-health-check)
    - [Health Utilities (health_utils)](#health-utilities-health_utils)
- [Get service status](#get-service-status)
- [Get open events](#get-open-events)
- [Get resource health](#get-resource-health)
    - [Cost Utilities (cost_utils)](#cost-utilities-cost_utils)
- [Get cost and usage data](#get-cost-and-usage-data)
- [Get cost forecast](#get-cost-forecast)
- [Create budget](#create-budget)
    - [Security Utilities (security_utils)](#security-utilities-security_utils)
- [Create security group](#create-security-group)
- [Add security group rule](#add-security-group-rule)
- [Create network ACL](#create-network-acl)
- [Add network ACL rule](#add-network-acl-rule)
  - [Error Handling](#error-handling)
  - [Best Practices](#best-practices)
  - [Contributing](#contributing)
  - [License](#license)



A comprehensive collection of Python utility functions for working with AWS services using boto3. This package provides high-level abstractions and helper functions to simplify common AWS operations.

## Installation

1. Ensure you have Python 3.6+ and boto3 installed:
```bash
pip install boto3
```

2. Configure your AWS credentials:
```bash
aws configure
```

3. Install the package:
```bash
pip install -e .
```

## Available Modules

### EC2 Utilities (`ec2_utils`)
Functions for managing EC2 instances and AMIs:
```python
from aws_utils import ec2_utils

# List running instances
instances = ec2_utils.list_instances([
    {'Name': 'instance-state-name', 'Values': ['running']}
])

# Create a new instance
instance = ec2_utils.create_instance(
    name="web-server",
    instance_type="t2.micro",
    ami_id="ami-12345678",
    security_group_ids=["sg-12345678"],
    key_name="my-key-pair"
)

# Get instance status
status = ec2_utils.get_instance_status('i-1234567890abcdef0')
```

### IAM Utilities (`iam_utils`)
Functions for managing IAM users, roles, and policies:
```python
from aws_utils import iam_utils

# Create a new IAM user
user = iam_utils.create_user(
    username="service-account-1",
    tags=[
        {"Key": "Department", "Value": "Engineering"},
        {"Key": "Environment", "Value": "Production"}
    ]
)

# Create access keys
keys = iam_utils.create_access_key("service-account-1")

# Create role with policy
trust_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"Service": "ec2.amazonaws.com"},
        "Action": "sts:AssumeRole"
    }]
}

role = iam_utils.create_role(
    "EC2ServiceRole",
    trust_policy,
    description="Role for EC2 instances"
)
```

### Route53 Utilities (`route53_utils`)
Functions for managing DNS records and health checks:
```python
from aws_utils import route53_utils

# Create hosted zone
zone = route53_utils.create_hosted_zone(
    "example.com",
    comment="Main company domain"
)

# Add DNS record
record = route53_utils.create_record_set(
    zone['Id'],
    "www.example.com",
    "A",
    "203.0.113.1"
)

# Create health check
check = route53_utils.create_health_check(
    domain_name="www.example.com",
    port=443,
    type="HTTPS",
    resource_path="/health"
)
```

### Health Utilities (`health_utils`)
Functions for monitoring AWS service health:
```python
from aws_utils import health_utils
from datetime import datetime, timedelta

# Get service status
events = health_utils.get_service_status(
    services=['EC2', 'RDS'],
    regions=['us-east-1'],
    start_time=datetime.utcnow() - timedelta(days=1)
)

# Get open events
open_events = health_utils.get_open_events(
    services=['EC2']
)

# Get resource health
health = health_utils.get_resource_health(
    'AWS::EC2::Instance',
    ['i-1234567890abcdef0']
)
```

### Cost Utilities (`cost_utils`)
Functions for monitoring and analyzing costs:
```python
from aws_utils import cost_utils

# Get cost and usage data
costs = cost_utils.get_cost_and_usage(
    '2023-01-01',
    '2023-12-31',
    granularity='MONTHLY',
    metrics=['BlendedCost'],
    group_by=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
)

# Get cost forecast
forecast = cost_utils.get_cost_forecast(
    '2023-07-01',
    '2023-12-31',
    metric='UNBLENDED_COST',
    granularity='MONTHLY'
)

# Create budget
budget = cost_utils.create_budget(
    "MonthlyBudget",
    1000.0,
    "MONTHLY",
    datetime.now(),
    notifications=[{
        'NotificationType': 'ACTUAL',
        'ComparisonOperator': 'GREATER_THAN',
        'Threshold': 80.0,
        'ThresholdType': 'PERCENTAGE',
        'NotificationState': 'ALARM'
    }]
)
```

### Security Utilities (`security_utils`)
Functions for managing security groups and network ACLs:
```python
from aws_utils import security_utils

# Create security group
sg = security_utils.create_security_group(
    "web-servers",
    "Security group for web servers",
    vpc_id="vpc-1234567890abcdef0"
)

# Add security group rule
rule = security_utils.add_security_group_rule(
    sg['GroupId'],
    "tcp",
    80,
    80,
    cidr_ip="0.0.0.0/0",
    description="Allow HTTP from anywhere"
)

# Create network ACL
acl = security_utils.create_network_acl(
    "vpc-1234567890abcdef0",
    tags=[{"Key": "Name", "Value": "Web-Tier-ACL"}]
)

# Add network ACL rule
entry = security_utils.add_network_acl_entry(
    acl['NetworkAclId'],
    100,
    "6",  # TCP
    "allow",
    "0.0.0.0/0",
    port_range={'From': 80, 'To': 80}
)
```

## Error Handling

All functions include proper error handling and will raise exceptions with descriptive error messages when operations fail. It's recommended to wrap API calls in try-except blocks:

```python
from botocore.exceptions import ClientError

try:
    instance = ec2_utils.create_instance(...)
except ClientError as e:
    print(f"Failed to create instance: {e}")
    raise
```

## Best Practices

1. Always use the most specific function for your needs to ensure proper error handling and validation.
2. Use tags consistently to help with resource organization and cost tracking.
3. Follow the principle of least privilege when creating IAM roles and policies.
4. Regularly monitor costs using the cost utilities to avoid unexpected charges.
5. Use health checks and monitoring to ensure high availability of your resources.
6. Keep security group and network ACL rules as restrictive as possible.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
