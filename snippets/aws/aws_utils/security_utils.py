"""
AWS Security Utilities Module

This module provides utility functions for working with AWS security groups,
network ACLs, and other security-related resources.
"""

import boto3
from typing import List, Dict, Optional, Union
from botocore.exceptions import ClientError

# Initialize boto3 clients
ec2_client = boto3.client('ec2')
ec2_resource = boto3.resource('ec2')

def create_security_group(
    name: str,
    description: str,
    vpc_id: Optional[str] = None,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create a new security group.
    
    Args:
        name: Name of the security group
        description: Description of the security group
        vpc_id: Optional VPC ID (required for VPC security groups)
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created security group details
    
    Example:
        # Create VPC security group
        sg = create_security_group(
            "web-servers",
            "Security group for web servers",
            vpc_id="vpc-1234567890abcdef0",
            tags=[{"Key": "Environment", "Value": "Production"}]
        )
    """
    try:
        params = {
            'GroupName': name,
            'Description': description
        }
        
        if vpc_id:
            params['VpcId'] = vpc_id
            
        response = ec2_client.create_security_group(**params)
        group_id = response['GroupId']
        
        if tags:
            ec2_client.create_tags(
                Resources=[group_id],
                Tags=tags
            )
            
        return ec2_client.describe_security_groups(
            GroupIds=[group_id]
        )['SecurityGroups'][0]
    
    except ClientError as e:
        print(f"Error creating security group: {e}")
        raise

def add_security_group_rule(
    group_id: str,
    ip_protocol: str,
    from_port: int,
    to_port: int,
    cidr_ip: Optional[str] = None,
    source_group_id: Optional[str] = None,
    description: Optional[str] = None,
    is_egress: bool = False
) -> Dict:
    """
    Add an ingress or egress rule to a security group.
    
    Args:
        group_id: ID of the security group
        ip_protocol: IP protocol (tcp, udp, icmp, etc.)
        from_port: Start of port range
        to_port: End of port range
        cidr_ip: Optional CIDR IP range
        source_group_id: Optional source security group ID
        description: Optional rule description
        is_egress: Whether this is an egress rule
    
    Returns:
        Dictionary containing the rule details
    
    Example:
        # Allow inbound HTTP
        rule = add_security_group_rule(
            "sg-1234567890abcdef0",
            "tcp",
            80,
            80,
            cidr_ip="0.0.0.0/0",
            description="Allow HTTP from anywhere"
        )
        
        # Allow outbound to specific security group
        rule = add_security_group_rule(
            "sg-1234567890abcdef0",
            "tcp",
            3306,
            3306,
            source_group_id="sg-0987654321fedcba0",
            description="Allow MySQL to DB servers",
            is_egress=True
        )
    """
    try:
        ip_permission = {
            'IpProtocol': ip_protocol,
            'FromPort': from_port,
            'ToPort': to_port
        }
        
        if cidr_ip:
            ip_permission['IpRanges'] = [{
                'CidrIp': cidr_ip
            }]
            if description:
                ip_permission['IpRanges'][0]['Description'] = description
                
        if source_group_id:
            ip_permission['UserIdGroupPairs'] = [{
                'GroupId': source_group_id
            }]
            if description:
                ip_permission['UserIdGroupPairs'][0]['Description'] = description
        
        if is_egress:
            response = ec2_client.authorize_security_group_egress(
                GroupId=group_id,
                IpPermissions=[ip_permission]
            )
        else:
            response = ec2_client.authorize_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[ip_permission]
            )
            
        return response
    
    except ClientError as e:
        print(f"Error adding security group rule: {e}")
        raise

def revoke_security_group_rule(
    group_id: str,
    ip_protocol: str,
    from_port: int,
    to_port: int,
    cidr_ip: Optional[str] = None,
    source_group_id: Optional[str] = None,
    is_egress: bool = False
) -> Dict:
    """
    Remove an ingress or egress rule from a security group.
    
    Args:
        group_id: ID of the security group
        ip_protocol: IP protocol
        from_port: Start of port range
        to_port: End of port range
        cidr_ip: Optional CIDR IP range
        source_group_id: Optional source security group ID
        is_egress: Whether this is an egress rule
    
    Returns:
        Dictionary containing the response
    
    Example:
        # Remove inbound HTTP rule
        response = revoke_security_group_rule(
            "sg-1234567890abcdef0",
            "tcp",
            80,
            80,
            cidr_ip="0.0.0.0/0"
        )
    """
    try:
        ip_permission = {
            'IpProtocol': ip_protocol,
            'FromPort': from_port,
            'ToPort': to_port
        }
        
        if cidr_ip:
            ip_permission['IpRanges'] = [{'CidrIp': cidr_ip}]
        if source_group_id:
            ip_permission['UserIdGroupPairs'] = [{
                'GroupId': source_group_id
            }]
        
        if is_egress:
            response = ec2_client.revoke_security_group_egress(
                GroupId=group_id,
                IpPermissions=[ip_permission]
            )
        else:
            response = ec2_client.revoke_security_group_ingress(
                GroupId=group_id,
                IpPermissions=[ip_permission]
            )
            
        return response
    
    except ClientError as e:
        print(f"Error revoking security group rule: {e}")
        raise

def get_security_group_rules(
    group_id: str,
    rule_type: str = 'all'
) -> Dict[str, List[Dict]]:
    """
    Get all rules for a security group.
    
    Args:
        group_id: ID of the security group
        rule_type: Type of rules to get ('all', 'ingress', or 'egress')
    
    Returns:
        Dictionary containing ingress and/or egress rules
    
    Example:
        # Get all rules
        rules = get_security_group_rules("sg-1234567890abcdef0")
        
        # Get only ingress rules
        ingress_rules = get_security_group_rules(
            "sg-1234567890abcdef0",
            rule_type="ingress"
        )
    """
    try:
        group = ec2_client.describe_security_groups(
            GroupIds=[group_id]
        )['SecurityGroups'][0]
        
        result = {}
        if rule_type in ('all', 'ingress'):
            result['ingress'] = group['IpPermissions']
        if rule_type in ('all', 'egress'):
            result['egress'] = group['IpPermissionsEgress']
            
        return result
    
    except ClientError as e:
        print(f"Error getting security group rules: {e}")
        raise

def create_network_acl(
    vpc_id: str,
    tags: Optional[List[Dict]] = None
) -> Dict:
    """
    Create a new network ACL in a VPC.
    
    Args:
        vpc_id: ID of the VPC
        tags: Optional list of tags
    
    Returns:
        Dictionary containing the created network ACL details
    
    Example:
        acl = create_network_acl(
            "vpc-1234567890abcdef0",
            tags=[{"Key": "Name", "Value": "Web-Tier-ACL"}]
        )
    """
    try:
        response = ec2_client.create_network_acl(VpcId=vpc_id)
        acl_id = response['NetworkAcl']['NetworkAclId']
        
        if tags:
            ec2_client.create_tags(
                Resources=[acl_id],
                Tags=tags
            )
            
        return response['NetworkAcl']
    
    except ClientError as e:
        print(f"Error creating network ACL: {e}")
        raise

def add_network_acl_entry(
    acl_id: str,
    rule_number: int,
    protocol: str,
    rule_action: str,
    cidr_block: str,
    egress: bool = False,
    port_range: Optional[Dict[str, int]] = None,
    icmp_type: Optional[Dict[str, int]] = None
) -> Dict:
    """
    Add an entry to a network ACL.
    
    Args:
        acl_id: ID of the network ACL
        rule_number: Rule number (1-32766)
        protocol: Protocol number (-1 for all)
        rule_action: Action (allow|deny)
        cidr_block: CIDR block
        egress: Whether this is an egress rule
        port_range: Optional port range dict with 'From' and 'To'
        icmp_type: Optional ICMP type dict with 'Type' and 'Code'
    
    Returns:
        Dictionary containing the response
    
    Example:
        # Allow inbound HTTP
        response = add_network_acl_entry(
            "acl-1234567890abcdef0",
            100,
            "6",  # TCP
            "allow",
            "0.0.0.0/0",
            port_range={'From': 80, 'To': 80}
        )
        
        # Deny outbound ICMP
        response = add_network_acl_entry(
            "acl-1234567890abcdef0",
            200,
            "1",  # ICMP
            "deny",
            "0.0.0.0/0",
            egress=True,
            icmp_type={'Type': -1, 'Code': -1}
        )
    """
    try:
        params = {
            'NetworkAclId': acl_id,
            'RuleNumber': rule_number,
            'Protocol': protocol,
            'RuleAction': rule_action,
            'CidrBlock': cidr_block,
            'Egress': egress
        }
        
        if port_range:
            params['PortRange'] = port_range
        if icmp_type:
            params['IcmpTypeCode'] = icmp_type
            
        response = ec2_client.create_network_acl_entry(**params)
        return response
    
    except ClientError as e:
        print(f"Error adding network ACL entry: {e}")
        raise

def get_network_acl_entries(acl_id: str) -> Dict[str, List[Dict]]:
    """
    Get all entries in a network ACL.
    
    Args:
        acl_id: ID of the network ACL
    
    Returns:
        Dictionary containing ingress and egress entries
    
    Example:
        entries = get_network_acl_entries("acl-1234567890abcdef0")
        print("Inbound rules:", entries['ingress'])
        print("Outbound rules:", entries['egress'])
    """
    try:
        response = ec2_client.describe_network_acls(
            NetworkAclIds=[acl_id]
        )
        acl = response['NetworkAcls'][0]
        
        return {
            'ingress': [entry for entry in acl['Entries'] if not entry['Egress']],
            'egress': [entry for entry in acl['Entries'] if entry['Egress']]
        }
    
    except ClientError as e:
        print(f"Error getting network ACL entries: {e}")
        raise

def delete_network_acl_entry(
    acl_id: str,
    rule_number: int,
    egress: bool = False
) -> Dict:
    """
    Delete an entry from a network ACL.
    
    Args:
        acl_id: ID of the network ACL
        rule_number: Rule number to delete
        egress: Whether this is an egress rule
    
    Returns:
        Dictionary containing the response
    
    Example:
        response = delete_network_acl_entry(
            "acl-1234567890abcdef0",
            100
        )
    """
    try:
        response = ec2_client.delete_network_acl_entry(
            NetworkAclId=acl_id,
            RuleNumber=rule_number,
            Egress=egress
        )
        return response
    
    except ClientError as e:
        print(f"Error deleting network ACL entry: {e}")
        raise
