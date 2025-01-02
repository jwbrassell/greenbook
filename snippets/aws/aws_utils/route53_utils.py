"""
Route53 Utilities Module

This module provides utility functions for working with AWS Route53 DNS service.
"""

import boto3
from typing import List, Dict, Optional, Union
from botocore.exceptions import ClientError

# Initialize boto3 client
route53_client = boto3.client('route53')

def create_hosted_zone(
    domain_name: str,
    comment: Optional[str] = None,
    private_zone: bool = False,
    vpc_id: Optional[str] = None,
    vpc_region: Optional[str] = None
) -> Dict:
    """
    Create a new Route53 hosted zone.
    
    Args:
        domain_name: Domain name for the hosted zone
        comment: Optional comment for the hosted zone
        private_zone: Whether this is a private hosted zone
        vpc_id: Required for private zones - VPC ID
        vpc_region: Required for private zones - VPC region
    
    Returns:
        Dictionary containing the created hosted zone details
    
    Example:
        # Create public hosted zone
        zone = create_hosted_zone(
            "example.com",
            comment="Main company domain"
        )
        
        # Create private hosted zone
        private_zone = create_hosted_zone(
            "internal.example.com",
            comment="Internal DNS",
            private_zone=True,
            vpc_id="vpc-1234567890abcdef0",
            vpc_region="us-west-2"
        )
    """
    try:
        params = {
            'Name': domain_name,
            'CallerReference': str(int(time.time()))
        }
        
        config = {'Comment': comment} if comment else {}
        if private_zone:
            if not vpc_id or not vpc_region:
                raise ValueError("vpc_id and vpc_region required for private zones")
            config['PrivateZone'] = True
            config['VPC'] = {
                'VPCId': vpc_id,
                'VPCRegion': vpc_region
            }
        
        if config:
            params['HostedZoneConfig'] = config
            
        response = route53_client.create_hosted_zone(**params)
        return response['HostedZone']
    
    except ClientError as e:
        print(f"Error creating hosted zone: {e}")
        raise

def list_hosted_zones() -> List[Dict]:
    """
    List all Route53 hosted zones.
    
    Returns:
        List of dictionaries containing hosted zone details
    
    Example:
        zones = list_hosted_zones()
        for zone in zones:
            print(f"Zone: {zone['Name']}, ID: {zone['Id']}")
    """
    try:
        response = route53_client.list_hosted_zones()
        return response['HostedZones']
    
    except ClientError as e:
        print(f"Error listing hosted zones: {e}")
        raise

def create_record_set(
    hosted_zone_id: str,
    record_name: str,
    record_type: str,
    record_value: Union[str, List[str]],
    ttl: int = 300,
    alias_target: Optional[Dict] = None
) -> Dict:
    """
    Create a new DNS record in a hosted zone.
    
    Args:
        hosted_zone_id: ID of the hosted zone
        record_name: DNS record name
        record_type: Record type (A, AAAA, CNAME, MX, etc.)
        record_value: Record value(s)
        ttl: Time to live in seconds
        alias_target: Optional alias target for alias records
    
    Returns:
        Dictionary containing the change info
    
    Example:
        # Create A record
        response = create_record_set(
            "Z1234567890ABC",
            "www.example.com",
            "A",
            "203.0.113.1"
        )
        
        # Create CNAME record
        response = create_record_set(
            "Z1234567890ABC",
            "mail.example.com",
            "CNAME",
            "mailserver.example.com"
        )
        
        # Create alias record for ELB
        response = create_record_set(
            "Z1234567890ABC",
            "app.example.com",
            "A",
            None,
            alias_target={
                'HostedZoneId': 'Z2P70J7EXAMPLE',
                'DNSName': 'lb-1234.us-east-1.elb.amazonaws.com',
                'EvaluateTargetHealth': True
            }
        )
    """
    try:
        change_batch = {
            'Changes': [{
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type
                }
            }]
        }
        
        record_set = change_batch['Changes'][0]['ResourceRecordSet']
        
        if alias_target:
            record_set['AliasTarget'] = alias_target
        else:
            record_set['TTL'] = ttl
            if isinstance(record_value, str):
                record_value = [record_value]
            record_set['ResourceRecords'] = [
                {'Value': value} for value in record_value
            ]
        
        response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        return response['ChangeInfo']
    
    except ClientError as e:
        print(f"Error creating record set: {e}")
        raise

def delete_record_set(
    hosted_zone_id: str,
    record_name: str,
    record_type: str,
    record_value: Optional[Union[str, List[str]]] = None,
    ttl: Optional[int] = None,
    alias_target: Optional[Dict] = None
) -> Dict:
    """
    Delete a DNS record from a hosted zone.
    
    Args:
        hosted_zone_id: ID of the hosted zone
        record_name: DNS record name
        record_type: Record type
        record_value: Record value(s) for non-alias records
        ttl: TTL for non-alias records
        alias_target: Alias target for alias records
    
    Returns:
        Dictionary containing the change info
    
    Example:
        # Delete A record
        response = delete_record_set(
            "Z1234567890ABC",
            "www.example.com",
            "A",
            "203.0.113.1",
            300
        )
    """
    try:
        change_batch = {
            'Changes': [{
                'Action': 'DELETE',
                'ResourceRecordSet': {
                    'Name': record_name,
                    'Type': record_type
                }
            }]
        }
        
        record_set = change_batch['Changes'][0]['ResourceRecordSet']
        
        if alias_target:
            record_set['AliasTarget'] = alias_target
        else:
            if not record_value or not ttl:
                raise ValueError("record_value and ttl required for non-alias records")
            record_set['TTL'] = ttl
            if isinstance(record_value, str):
                record_value = [record_value]
            record_set['ResourceRecords'] = [
                {'Value': value} for value in record_value
            ]
        
        response = route53_client.change_resource_record_sets(
            HostedZoneId=hosted_zone_id,
            ChangeBatch=change_batch
        )
        return response['ChangeInfo']
    
    except ClientError as e:
        print(f"Error deleting record set: {e}")
        raise

def list_resource_record_sets(
    hosted_zone_id: str,
    start_record_name: Optional[str] = None,
    start_record_type: Optional[str] = None
) -> List[Dict]:
    """
    List resource record sets in a hosted zone.
    
    Args:
        hosted_zone_id: ID of the hosted zone
        start_record_name: Optional name to start listing from
        start_record_type: Optional type to start listing from
    
    Returns:
        List of dictionaries containing record set details
    
    Example:
        records = list_resource_record_sets("Z1234567890ABC")
        for record in records:
            print(f"Record: {record['Name']} ({record['Type']})")
    """
    try:
        params = {'HostedZoneId': hosted_zone_id}
        if start_record_name:
            params['StartRecordName'] = start_record_name
        if start_record_type:
            params['StartRecordType'] = start_record_type
            
        response = route53_client.list_resource_record_sets(**params)
        return response['ResourceRecordSets']
    
    except ClientError as e:
        print(f"Error listing record sets: {e}")
        raise

def get_health_check_status(health_check_id: str) -> Dict:
    """
    Get the status of a Route53 health check.
    
    Args:
        health_check_id: ID of the health check
    
    Returns:
        Dictionary containing health check status
    
    Example:
        status = get_health_check_status("1234567890")
        print(f"Health check status: {status['HealthCheckStatus']}")
    """
    try:
        response = route53_client.get_health_check_status(
            HealthCheckId=health_check_id
        )
        return response['HealthCheckObservations'][0]
    
    except ClientError as e:
        print(f"Error getting health check status: {e}")
        raise

def create_health_check(
    ip_address: Optional[str] = None,
    domain_name: Optional[str] = None,
    port: int = 80,
    type: str = 'HTTP',
    resource_path: str = '/',
    request_interval: int = 30,
    failure_threshold: int = 3
) -> Dict:
    """
    Create a Route53 health check.
    
    Args:
        ip_address: IP address to check (mutually exclusive with domain_name)
        domain_name: Domain name to check (mutually exclusive with ip_address)
        port: Port number to check
        type: Type of health check (HTTP, HTTPS, TCP)
        resource_path: Path to check for HTTP(S) checks
        request_interval: Interval between checks in seconds
        failure_threshold: Number of consecutive failures before marking unhealthy
    
    Returns:
        Dictionary containing the created health check details
    
    Example:
        # Create HTTP health check for IP
        check = create_health_check(
            ip_address="203.0.113.1",
            port=80,
            type="HTTP",
            resource_path="/health"
        )
        
        # Create HTTPS health check for domain
        check = create_health_check(
            domain_name="example.com",
            port=443,
            type="HTTPS",
            resource_path="/status"
        )
    """
    try:
        if bool(ip_address) == bool(domain_name):
            raise ValueError("Exactly one of ip_address or domain_name required")
            
        config = {
            'Port': port,
            'Type': type,
            'RequestInterval': request_interval,
            'FailureThreshold': failure_threshold
        }
        
        if ip_address:
            config['IPAddress'] = ip_address
        else:
            config['FullyQualifiedDomainName'] = domain_name
            
        if type in ('HTTP', 'HTTPS'):
            config['ResourcePath'] = resource_path
            
        response = route53_client.create_health_check(
            CallerReference=str(int(time.time())),
            HealthCheckConfig=config
        )
        return response['HealthCheck']
    
    except ClientError as e:
        print(f"Error creating health check: {e}")
        raise
