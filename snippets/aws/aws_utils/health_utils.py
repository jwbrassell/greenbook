"""
AWS Health Utilities Module

This module provides utility functions for working with AWS Health to monitor 
the health of AWS services and resources.
"""

import boto3
from typing import List, Dict, Optional
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# Initialize boto3 client
health_client = boto3.client('health')

def get_service_status(
    services: Optional[List[str]] = None,
    regions: Optional[List[str]] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None
) -> List[Dict]:
    """
    Get AWS Health events for specified services and regions.
    
    Args:
        services: Optional list of AWS service names (e.g., ['EC2', 'RDS'])
        regions: Optional list of AWS regions
        start_time: Optional start time for events
        end_time: Optional end time for events
    
    Returns:
        List of dictionaries containing health events
    
    Example:
        # Get all EC2 and RDS events in us-east-1 for last 24 hours
        events = get_service_status(
            services=['EC2', 'RDS'],
            regions=['us-east-1'],
            start_time=datetime.utcnow() - timedelta(days=1)
        )
        
        # Get all recent health events
        events = get_service_status(
            start_time=datetime.utcnow() - timedelta(hours=1)
        )
    """
    try:
        filters = {}
        
        if services:
            filters['services'] = services
        if regions:
            filters['regions'] = regions
        if start_time:
            filters['startTimes'] = [{'from': start_time}]
        if end_time:
            if 'startTimes' in filters:
                filters['startTimes'][0]['to'] = end_time
            else:
                filters['startTimes'] = [{'to': end_time}]
        
        events = []
        paginator = health_client.get_paginator('describe_events')
        
        for page in paginator.paginate(filter=filters):
            events.extend(page['events'])
            
        return events
    
    except ClientError as e:
        print(f"Error getting service status: {e}")
        raise

def get_event_details(event_arn: str) -> Dict:
    """
    Get detailed information about a specific AWS Health event.
    
    Args:
        event_arn: ARN of the health event
    
    Returns:
        Dictionary containing detailed event information
    
    Example:
        details = get_event_details(
            "arn:aws:health:us-east-1::event/ABC123"
        )
        print(f"Event type: {details['event']['eventTypeCode']}")
    """
    try:
        response = health_client.describe_event_details(
            eventArns=[event_arn]
        )
        if response['successfulSet']:
            return response['successfulSet'][0]
        return {}
    
    except ClientError as e:
        print(f"Error getting event details: {e}")
        raise

def get_affected_entities(
    event_arn: str,
    max_results: int = 100
) -> List[Dict]:
    """
    Get entities affected by a specific AWS Health event.
    
    Args:
        event_arn: ARN of the health event
        max_results: Maximum number of results to return
    
    Returns:
        List of dictionaries containing affected entity details
    
    Example:
        entities = get_affected_entities(
            "arn:aws:health:us-east-1::event/ABC123"
        )
        for entity in entities:
            print(f"Affected entity: {entity['entityValue']}")
    """
    try:
        response = health_client.describe_affected_entities(
            filter={'eventArns': [event_arn]},
            maxResults=max_results
        )
        return response['entities']
    
    except ClientError as e:
        print(f"Error getting affected entities: {e}")
        raise

def get_resource_health(
    resource_type: str,
    resource_ids: List[str]
) -> List[Dict]:
    """
    Get health information for specific AWS resources.
    
    Args:
        resource_type: Type of AWS resource (e.g., 'AWS::EC2::Instance')
        resource_ids: List of resource IDs to check
    
    Returns:
        List of dictionaries containing resource health information
    
    Example:
        # Check EC2 instance health
        health = get_resource_health(
            'AWS::EC2::Instance',
            ['i-1234567890abcdef0', 'i-0987654321fedcba0']
        )
        
        # Check ELB health
        health = get_resource_health(
            'AWS::ElasticLoadBalancing::LoadBalancer',
            ['lb-1234567890']
        )
    """
    try:
        response = health_client.describe_entity_aggregates(
            filter={
                'entityArns': [
                    f"arn:aws:{resource_type}:{id}" 
                    for id in resource_ids
                ]
            }
        )
        return response['entityAggregates']
    
    except ClientError as e:
        print(f"Error getting resource health: {e}")
        raise

def get_event_types(
    services: Optional[List[str]] = None,
    regions: Optional[List[str]] = None
) -> List[Dict]:
    """
    Get available AWS Health event types.
    
    Args:
        services: Optional list of AWS service names to filter
        regions: Optional list of AWS regions to filter
    
    Returns:
        List of dictionaries containing event type information
    
    Example:
        # Get all EC2 event types
        types = get_event_types(services=['EC2'])
        
        # Get event types for specific region
        types = get_event_types(regions=['us-east-1'])
    """
    try:
        filters = {}
        if services:
            filters['services'] = services
        if regions:
            filters['regions'] = regions
            
        response = health_client.describe_event_types(filter=filters)
        return response['eventTypes']
    
    except ClientError as e:
        print(f"Error getting event types: {e}")
        raise

def get_open_events(
    services: Optional[List[str]] = None,
    regions: Optional[List[str]] = None
) -> List[Dict]:
    """
    Get all open (ongoing) AWS Health events.
    
    Args:
        services: Optional list of AWS service names to filter
        regions: Optional list of AWS regions to filter
    
    Returns:
        List of dictionaries containing open event information
    
    Example:
        # Get all open EC2 events
        events = get_open_events(services=['EC2'])
        
        # Get all open events in a region
        events = get_open_events(regions=['us-east-1'])
    """
    try:
        filters = {
            'eventStatusCodes': ['open', 'upcoming']
        }
        if services:
            filters['services'] = services
        if regions:
            filters['regions'] = regions
            
        events = []
        paginator = health_client.get_paginator('describe_events')
        
        for page in paginator.paginate(filter=filters):
            events.extend(page['events'])
            
        return events
    
    except ClientError as e:
        print(f"Error getting open events: {e}")
        raise

def get_event_aggregates(
    aggregation_field: str,
    max_results: int = 100,
    services: Optional[List[str]] = None,
    regions: Optional[List[str]] = None
) -> List[Dict]:
    """
    Get aggregated AWS Health event information.
    
    Args:
        aggregation_field: Field to aggregate by ('eventTypeCategory' or 'eventTypeCode')
        max_results: Maximum number of results to return
        services: Optional list of AWS service names to filter
        regions: Optional list of AWS regions to filter
    
    Returns:
        List of dictionaries containing aggregated event information
    
    Example:
        # Get event counts by category
        aggregates = get_event_aggregates('eventTypeCategory')
        
        # Get event counts by type for EC2
        aggregates = get_event_aggregates(
            'eventTypeCode',
            services=['EC2']
        )
    """
    try:
        filters = {}
        if services:
            filters['services'] = services
        if regions:
            filters['regions'] = regions
            
        response = health_client.describe_event_aggregates(
            aggregateField=aggregation_field,
            filter=filters,
            maxResults=max_results
        )
        return response['eventAggregates']
    
    except ClientError as e:
        print(f"Error getting event aggregates: {e}")
        raise
