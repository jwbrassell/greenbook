"""
IAM Utilities Module

This module provides utility functions for working with AWS IAM (Identity and Access Management).
"""

import boto3
from typing import List, Dict, Optional, Union
from botocore.exceptions import ClientError

# Initialize boto3 client
iam_client = boto3.client('iam')

def create_user(
    username: str,
    path: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create a new IAM user.
    
    Args:
        username: Name of the IAM user
        path: Optional path for the user
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created user's details
    
    Example:
        user = create_user(
            username="service-account-1",
            tags=[
                {"Key": "Department", "Value": "Engineering"},
                {"Key": "Environment", "Value": "Production"}
            ]
        )
    """
    try:
        params = {'UserName': username}
        if path:
            params['Path'] = path
        if tags:
            params['Tags'] = tags
            
        response = iam_client.create_user(**params)
        return response['User']
    
    except ClientError as e:
        print(f"Error creating IAM user: {e}")
        raise

def create_access_key(username: str) -> Dict:
    """
    Create an access key pair for an IAM user.
    
    Args:
        username: Name of the IAM user
    
    Returns:
        Dictionary containing the access key details
    
    Example:
        key_pair = create_access_key("service-account-1")
        print(f"Access Key ID: {key_pair['AccessKeyId']}")
        print(f"Secret Key: {key_pair['SecretAccessKey']}")
    """
    try:
        response = iam_client.create_access_key(UserName=username)
        return response['AccessKey']
    
    except ClientError as e:
        print(f"Error creating access key: {e}")
        raise

def list_users(path_prefix: Optional[str] = None) -> List[Dict]:
    """
    List IAM users with optional path prefix filtering.
    
    Args:
        path_prefix: Optional path prefix to filter users
    
    Returns:
        List of dictionaries containing user details
    
    Example:
        # List all users
        users = list_users()
        
        # List users in specific path
        service_users = list_users('/service-accounts/')
    """
    try:
        params = {}
        if path_prefix:
            params['PathPrefix'] = path_prefix
            
        response = iam_client.list_users(**params)
        return response['Users']
    
    except ClientError as e:
        print(f"Error listing IAM users: {e}")
        raise

def create_role(
    role_name: str,
    trust_policy: Dict,
    description: Optional[str] = None,
    path: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create an IAM role with specified trust policy.
    
    Args:
        role_name: Name of the role
        trust_policy: Trust policy document
        description: Optional role description
        path: Optional path for the role
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created role's details
    
    Example:
        # Create role that trusts EC2 service
        trust_policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": {"Service": "ec2.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }]
        }
        role = create_role(
            role_name="EC2ServiceRole",
            trust_policy=trust_policy,
            description="Role for EC2 instances"
        )
    """
    try:
        params = {
            'RoleName': role_name,
            'AssumeRolePolicyDocument': json.dumps(trust_policy)
        }
        if description:
            params['Description'] = description
        if path:
            params['Path'] = path
        if tags:
            params['Tags'] = tags
            
        response = iam_client.create_role(**params)
        return response['Role']
    
    except ClientError as e:
        print(f"Error creating IAM role: {e}")
        raise

def attach_role_policy(
    role_name: str,
    policy_arn: str
) -> None:
    """
    Attach a managed policy to an IAM role.
    
    Args:
        role_name: Name of the IAM role
        policy_arn: ARN of the policy to attach
    
    Example:
        # Attach S3 read-only policy to role
        attach_role_policy(
            "EC2ServiceRole",
            "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
        )
    """
    try:
        iam_client.attach_role_policy(
            RoleName=role_name,
            PolicyArn=policy_arn
        )
    
    except ClientError as e:
        print(f"Error attaching policy to role: {e}")
        raise

def create_policy(
    policy_name: str,
    policy_document: Dict,
    description: Optional[str] = None,
    path: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create a custom IAM policy.
    
    Args:
        policy_name: Name of the policy
        policy_document: Policy document
        description: Optional policy description
        path: Optional path for the policy
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created policy's details
    
    Example:
        # Create S3 bucket access policy
        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Action": [
                    "s3:GetObject",
                    "s3:PutObject"
                ],
                "Resource": "arn:aws:s3:::my-bucket/*"
            }]
        }
        policy = create_policy(
            policy_name="S3BucketAccess",
            policy_document=policy_doc,
            description="Allow access to specific S3 bucket"
        )
    """
    try:
        params = {
            'PolicyName': policy_name,
            'PolicyDocument': json.dumps(policy_document)
        }
        if description:
            params['Description'] = description
        if path:
            params['Path'] = path
        if tags:
            params['Tags'] = tags
            
        response = iam_client.create_policy(**params)
        return response['Policy']
    
    except ClientError as e:
        print(f"Error creating IAM policy: {e}")
        raise

def get_policy_version(
    policy_arn: str,
    version_id: str
) -> Dict:
    """
    Get the specified version of an IAM policy.
    
    Args:
        policy_arn: ARN of the policy
        version_id: Version ID to retrieve
    
    Returns:
        Dictionary containing the policy version document
    
    Example:
        policy_version = get_policy_version(
            "arn:aws:iam::123456789012:policy/MyPolicy",
            "v1"
        )
    """
    try:
        response = iam_client.get_policy_version(
            PolicyArn=policy_arn,
            VersionId=version_id
        )
        return response['PolicyVersion']
    
    except ClientError as e:
        print(f"Error getting policy version: {e}")
        raise

def list_attached_user_policies(username: str) -> List[Dict]:
    """
    List all managed policies attached to an IAM user.
    
    Args:
        username: Name of the IAM user
    
    Returns:
        List of dictionaries containing attached policy details
    
    Example:
        policies = list_attached_user_policies("service-account-1")
        for policy in policies:
            print(f"Policy: {policy['PolicyName']}")
    """
    try:
        response = iam_client.list_attached_user_policies(
            UserName=username
        )
        return response['AttachedPolicies']
    
    except ClientError as e:
        print(f"Error listing attached policies: {e}")
        raise

def create_instance_profile(
    profile_name: str,
    path: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create an instance profile for EC2 instances.
    
    Args:
        profile_name: Name of the instance profile
        path: Optional path for the profile
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created instance profile details
    
    Example:
        profile = create_instance_profile(
            "WebServerProfile",
            tags=[{"Key": "Environment", "Value": "Production"}]
        )
    """
    try:
        params = {'InstanceProfileName': profile_name}
        if path:
            params['Path'] = path
        if tags:
            params['Tags'] = tags
            
        response = iam_client.create_instance_profile(**params)
        return response['InstanceProfile']
    
    except ClientError as e:
        print(f"Error creating instance profile: {e}")
        raise

def add_role_to_instance_profile(
    instance_profile_name: str,
    role_name: str
) -> None:
    """
    Add an IAM role to an instance profile.
    
    Args:
        instance_profile_name: Name of the instance profile
        role_name: Name of the IAM role to add
    
    Example:
        add_role_to_instance_profile(
            "WebServerProfile",
            "EC2ServiceRole"
        )
    """
    try:
        iam_client.add_role_to_instance_profile(
            InstanceProfileName=instance_profile_name,
            RoleName=role_name
        )
    
    except ClientError as e:
        print(f"Error adding role to instance profile: {e}")
        raise
