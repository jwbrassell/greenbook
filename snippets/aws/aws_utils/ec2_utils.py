"""
EC2 Utilities Module

This module provides utility functions for working with AWS EC2 instances.
"""

import boto3
from typing import List, Dict, Optional, Union
from botocore.exceptions import ClientError

# Initialize boto3 clients
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def list_instances(filters: Optional[List[Dict]] = None) -> List[Dict]:
    """
    List EC2 instances with optional filtering.
    
    Args:
        filters: Optional list of filters to apply. Example:
            [{'Name': 'instance-state-name', 'Values': ['running']}]
    
    Returns:
        List of instance dictionaries containing details about each instance.
    
    Example:
        # List all running instances
        running_instances = list_instances([
            {'Name': 'instance-state-name', 'Values': ['running']}
        ])
        
        # List instances with specific tag
        tagged_instances = list_instances([
            {'Name': 'tag:Environment', 'Values': ['Production']}
        ])
    """
    try:
        if filters:
            instances = ec2_client.describe_instances(Filters=filters)
        else:
            instances = ec2_client.describe_instances()
        
        instance_list = []
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_list.append(instance)
        return instance_list
    
    except ClientError as e:
        print(f"Error listing instances: {e}")
        raise

def create_instance(
    name: str,
    instance_type: str,
    ami_id: str,
    subnet_id: Optional[str] = None,
    security_group_ids: Optional[List[str]] = None,
    key_name: Optional[str] = None,
    user_data: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create a new EC2 instance with specified configuration.
    
    Args:
        name: Name tag for the instance
        instance_type: EC2 instance type (e.g., 't2.micro')
        ami_id: ID of the AMI to use
        subnet_id: Optional subnet ID for VPC
        security_group_ids: Optional list of security group IDs
        key_name: Optional name of the key pair for SSH access
        user_data: Optional user data script
        tags: Optional list of additional tags
    
    Returns:
        Dictionary containing details about the created instance.
    
    Example:
        instance = create_instance(
            name="web-server",
            instance_type="t2.micro",
            ami_id="ami-12345678",
            security_group_ids=["sg-12345678"],
            key_name="my-key-pair",
            tags=[
                {"Key": "Environment", "Value": "Production"},
                {"Key": "Project", "Value": "WebApp"}
            ]
        )
    """
    try:
        # Prepare instance parameters
        params = {
            'ImageId': ami_id,
            'InstanceType': instance_type,
            'MaxCount': 1,
            'MinCount': 1,
            'TagSpecifications': [{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'Name', 'Value': name}]
            }]
        }

        # Add optional parameters if provided
        if subnet_id:
            params['SubnetId'] = subnet_id
        if security_group_ids:
            params['SecurityGroupIds'] = security_group_ids
        if key_name:
            params['KeyName'] = key_name
        if user_data:
            params['UserData'] = user_data
        if tags:
            params['TagSpecifications'][0]['Tags'].extend(tags)

        # Create the instance
        response = ec2_client.run_instances(**params)
        return response['Instances'][0]

    except ClientError as e:
        print(f"Error creating instance: {e}")
        raise

def get_instance_status(instance_id: str) -> Dict:
    """
    Get detailed status information about an EC2 instance.
    
    Args:
        instance_id: ID of the EC2 instance
    
    Returns:
        Dictionary containing instance status information
    
    Example:
        status = get_instance_status('i-1234567890abcdef0')
        print(f"Instance state: {status['InstanceState']['Name']}")
        print(f"System status: {status['SystemStatus']['Status']}")
    """
    try:
        response = ec2_client.describe_instance_status(
            InstanceIds=[instance_id],
            IncludeAllInstances=True
        )
        if response['InstanceStatuses']:
            return response['InstanceStatuses'][0]
        return {}
    
    except ClientError as e:
        print(f"Error getting instance status: {e}")
        raise

def stop_instances(instance_ids: List[str], force: bool = False) -> List[Dict]:
    """
    Stop one or more EC2 instances.
    
    Args:
        instance_ids: List of instance IDs to stop
        force: Whether to force stop the instances
    
    Returns:
        List of dictionaries containing the stopping status of each instance
    
    Example:
        # Stop multiple instances
        result = stop_instances(['i-1234567890abcdef0', 'i-0987654321fedcba0'])
        
        # Force stop an instance
        result = stop_instances(['i-1234567890abcdef0'], force=True)
    """
    try:
        response = ec2_client.stop_instances(
            InstanceIds=instance_ids,
            Force=force
        )
        return response['StoppingInstances']
    
    except ClientError as e:
        print(f"Error stopping instances: {e}")
        raise

def start_instances(instance_ids: List[str]) -> List[Dict]:
    """
    Start one or more stopped EC2 instances.
    
    Args:
        instance_ids: List of instance IDs to start
    
    Returns:
        List of dictionaries containing the starting status of each instance
    
    Example:
        result = start_instances(['i-1234567890abcdef0', 'i-0987654321fedcba0'])
    """
    try:
        response = ec2_client.start_instances(InstanceIds=instance_ids)
        return response['StartingInstances']
    
    except ClientError as e:
        print(f"Error starting instances: {e}")
        raise

def terminate_instances(instance_ids: List[str]) -> List[Dict]:
    """
    Terminate one or more EC2 instances.
    
    Args:
        instance_ids: List of instance IDs to terminate
    
    Returns:
        List of dictionaries containing the termination status of each instance
    
    Example:
        result = terminate_instances(['i-1234567890abcdef0'])
    """
    try:
        response = ec2_client.terminate_instances(InstanceIds=instance_ids)
        return response['TerminatingInstances']
    
    except ClientError as e:
        print(f"Error terminating instances: {e}")
        raise

def get_instance_metrics(
    instance_id: str,
    metric_name: str,
    period: int = 300,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None
) -> Dict:
    """
    Get CloudWatch metrics for an EC2 instance.
    
    Args:
        instance_id: ID of the EC2 instance
        metric_name: Name of the metric (e.g., 'CPUUtilization')
        period: Time period in seconds (default: 300)
        start_time: Start time for metrics (default: 1 hour ago)
        end_time: End time for metrics (default: now)
    
    Returns:
        Dictionary containing the metric data
    
    Example:
        # Get CPU utilization
        metrics = get_instance_metrics(
            'i-1234567890abcdef0',
            'CPUUtilization',
            period=300
        )
    """
    try:
        cloudwatch = boto3.client('cloudwatch')
        
        if not start_time:
            start_time = (
                datetime.datetime.utcnow() - 
                datetime.timedelta(hours=1)
            ).isoformat()
        if not end_time:
            end_time = datetime.datetime.utcnow().isoformat()

        response = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[
                {
                    'Name': 'InstanceId',
                    'Value': instance_id
                }
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=['Average']
        )
        return response
    
    except ClientError as e:
        print(f"Error getting instance metrics: {e}")
        raise

def create_ami(
    instance_id: str,
    name: str,
    description: Optional[str] = None,
    no_reboot: bool = False
) -> str:
    """
    Create an AMI from an EC2 instance.
    
    Args:
        instance_id: ID of the EC2 instance
        name: Name for the new AMI
        description: Optional description for the AMI
        no_reboot: If True, the instance will not be rebooted during AMI creation
    
    Returns:
        ID of the created AMI
    
    Example:
        ami_id = create_ami(
            'i-1234567890abcdef0',
            'web-server-backup-2023-06-01',
            description='Backup of production web server',
            no_reboot=True
        )
    """
    try:
        params = {
            'InstanceId': instance_id,
            'Name': name,
            'NoReboot': no_reboot
        }
        if description:
            params['Description'] = description

        response = ec2_client.create_image(**params)
        return response['ImageId']
    
    except ClientError as e:
        print(f"Error creating AMI: {e}")
        raise

def wait_for_instance_state(
    instance_id: str,
    desired_state: str,
    timeout: int = 300
) -> bool:
    """
    Wait for an EC2 instance to reach a desired state.
    
    Args:
        instance_id: ID of the EC2 instance
        desired_state: Target state to wait for (e.g., 'running', 'stopped')
        timeout: Maximum time to wait in seconds
    
    Returns:
        True if the desired state was reached, False if timeout occurred
    
    Example:
        # Wait for instance to be running
        success = wait_for_instance_state('i-1234567890abcdef0', 'running')
        if success:
            print("Instance is now running")
    """
    try:
        waiter = ec2_client.get_waiter(f'instance_{desired_state}')
        waiter.wait(
            InstanceIds=[instance_id],
            WaiterConfig={'Timeout': timeout}
        )
        return True
    
    except WaiterError as e:
        print(f"Timeout waiting for instance state: {e}")
        return False
    except ClientError as e:
        print(f"Error waiting for instance state: {e}")
        raise
