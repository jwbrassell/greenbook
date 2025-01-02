"""
AWS Utilities Package

This package provides a collection of utility functions for working with AWS services via boto3.
Each module focuses on a specific AWS service and provides high-level functions for common operations.

Available modules:
- ec2_utils: EC2 instance and AMI management
- iam_utils: IAM user, role, and policy management
- route53_utils: DNS and domain management
- health_utils: AWS health monitoring
- cost_utils: Cost and billing management
- security_utils: Security group management

Example usage:
    from aws_utils import ec2_utils
    
    # List all running instances
    instances = ec2_utils.list_running_instances()
    
    # Create a new instance
    instance = ec2_utils.create_instance(
        name="web-server",
        instance_type="t2.micro",
        ami_id="ami-12345678"
    )
"""

from . import ec2_utils
from . import iam_utils
from . import route53_utils
from . import health_utils
from . import cost_utils
from . import security_utils

__all__ = [
    'ec2_utils',
    'iam_utils', 
    'route53_utils',
    'health_utils',
    'cost_utils',
    'security_utils'
]
