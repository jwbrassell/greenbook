"""
AWS Cost Utilities Module

This module provides utility functions for working with AWS Cost Explorer
and AWS Budgets to monitor and analyze costs.
"""

import boto3
from typing import List, Dict, Optional, Union
from botocore.exceptions import ClientError
from datetime import datetime, timedelta

# Initialize boto3 clients
ce_client = boto3.client('ce')
budgets_client = boto3.client('budgets')

def get_cost_and_usage(
    start_date: str,
    end_date: str,
    granularity: str = 'MONTHLY',
    metrics: Optional[List[str]] = None,
    group_by: Optional[List[Dict]] = None
) -> Dict:
    """
    Get cost and usage data from AWS Cost Explorer.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        granularity: Time granularity (DAILY|MONTHLY|HOURLY)
        metrics: List of metrics (e.g., ['BlendedCost', 'UnblendedCost'])
        group_by: Optional list of grouping dimensions
    
    Returns:
        Dictionary containing cost and usage data
    
    Example:
        # Get monthly costs grouped by service
        costs = get_cost_and_usage(
            '2023-01-01',
            '2023-12-31',
            granularity='MONTHLY',
            metrics=['BlendedCost'],
            group_by=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        
        # Get daily costs for specific time period
        daily_costs = get_cost_and_usage(
            '2023-06-01',
            '2023-06-30',
            granularity='DAILY',
            metrics=['UnblendedCost']
        )
    """
    try:
        if not metrics:
            metrics = ['UnblendedCost', 'UsageQuantity']
            
        params = {
            'TimePeriod': {
                'Start': start_date,
                'End': end_date
            },
            'Granularity': granularity,
            'Metrics': metrics
        }
        
        if group_by:
            params['GroupBy'] = group_by
            
        response = ce_client.get_cost_and_usage(**params)
        return response
    
    except ClientError as e:
        print(f"Error getting cost and usage: {e}")
        raise

def get_cost_forecast(
    start_date: str,
    end_date: str,
    metric: str = 'UNBLENDED_COST',
    granularity: str = 'MONTHLY',
    filter: Optional[Dict] = None
) -> Dict:
    """
    Get cost forecast from AWS Cost Explorer.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        metric: Cost metric to forecast
        granularity: Time granularity (DAILY|MONTHLY)
        filter: Optional cost filter
    
    Returns:
        Dictionary containing cost forecast data
    
    Example:
        # Get monthly cost forecast
        forecast = get_cost_forecast(
            '2023-07-01',
            '2023-12-31',
            metric='UNBLENDED_COST',
            granularity='MONTHLY'
        )
        
        # Get forecast for specific services
        forecast = get_cost_forecast(
            '2023-07-01',
            '2023-07-31',
            filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon EC2', 'Amazon RDS']
                }
            }
        )
    """
    try:
        params = {
            'TimePeriod': {
                'Start': start_date,
                'End': end_date
            },
            'Metric': metric,
            'Granularity': granularity
        }
        
        if filter:
            params['Filter'] = filter
            
        response = ce_client.get_cost_forecast(**params)
        return response
    
    except ClientError as e:
        print(f"Error getting cost forecast: {e}")
        raise

def create_budget(
    name: str,
    amount: float,
    time_unit: str,
    time_period_start: datetime,
    time_period_end: Optional[datetime] = None,
    notifications: Optional[List[Dict]] = None
) -> Dict:
    """
    Create an AWS Budget with optional notifications.
    
    Args:
        name: Name of the budget
        amount: Budget amount
        time_unit: Time unit (MONTHLY|QUARTERLY|ANNUALLY)
        time_period_start: Start time for the budget
        time_period_end: Optional end time for the budget
        notifications: Optional list of notification configurations
    
    Returns:
        Dictionary containing the created budget details
    
    Example:
        # Create monthly budget with notification
        budget = create_budget(
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
    """
    try:
        budget_data = {
            'BudgetName': name,
            'BudgetLimit': {
                'Amount': str(amount),
                'Unit': 'USD'
            },
            'TimeUnit': time_unit,
            'TimePeriod': {
                'Start': time_period_start
            },
            'BudgetType': 'COST'
        }
        
        if time_period_end:
            budget_data['TimePeriod']['End'] = time_period_end
            
        response = budgets_client.create_budget(
            AccountId=boto3.client('sts').get_caller_identity()['Account'],
            Budget=budget_data
        )
        
        if notifications:
            for notification in notifications:
                budgets_client.create_notification(
                    AccountId=boto3.client('sts').get_caller_identity()['Account'],
                    BudgetName=name,
                    Notification=notification,
                    Subscribers=[{
                        'SubscriptionType': 'EMAIL',
                        'Address': notification.get('EmailAddress')
                    }]
                )
                
        return response
    
    except ClientError as e:
        print(f"Error creating budget: {e}")
        raise

def get_cost_categories() -> List[Dict]:
    """
    Get list of defined cost categories.
    
    Returns:
        List of dictionaries containing cost category information
    
    Example:
        categories = get_cost_categories()
        for category in categories:
            print(f"Category: {category['Name']}")
    """
    try:
        response = ce_client.list_cost_categories()
        return response['CostCategories']
    
    except ClientError as e:
        print(f"Error getting cost categories: {e}")
        raise

def get_dimension_values(
    dimension: str,
    time_period_start: str,
    time_period_end: str
) -> List[Dict]:
    """
    Get values for a specific cost dimension.
    
    Args:
        dimension: Cost dimension (e.g., SERVICE, LINKED_ACCOUNT)
        time_period_start: Start date in YYYY-MM-DD format
        time_period_end: End date in YYYY-MM-DD format
    
    Returns:
        List of dictionaries containing dimension values
    
    Example:
        # Get all AWS services used in time period
        services = get_dimension_values(
            'SERVICE',
            '2023-01-01',
            '2023-12-31'
        )
        
        # Get linked accounts with costs
        accounts = get_dimension_values(
            'LINKED_ACCOUNT',
            '2023-01-01',
            '2023-12-31'
        )
    """
    try:
        response = ce_client.get_dimension_values(
            TimePeriod={
                'Start': time_period_start,
                'End': time_period_end
            },
            Dimension=dimension
        )
        return response['DimensionValues']
    
    except ClientError as e:
        print(f"Error getting dimension values: {e}")
        raise

def get_tags() -> List[Dict]:
    """
    Get all cost allocation tags.
    
    Returns:
        List of dictionaries containing tag information
    
    Example:
        tags = get_tags()
        for tag in tags:
            print(f"Tag key: {tag['Key']}")
    """
    try:
        response = ce_client.get_tags()
        return response['Tags']
    
    except ClientError as e:
        print(f"Error getting tags: {e}")
        raise

def get_cost_and_usage_with_resources(
    start_date: str,
    end_date: str,
    granularity: str = 'DAILY',
    filter: Optional[Dict] = None,
    group_by: Optional[List[Dict]] = None,
    metrics: Optional[List[str]] = None
) -> Dict:
    """
    Get detailed cost and usage data including resource IDs.
    
    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        granularity: Time granularity (DAILY|MONTHLY|HOURLY)
        filter: Optional cost filter
        group_by: Optional list of grouping dimensions
        metrics: Optional list of metrics
    
    Returns:
        Dictionary containing detailed cost and usage data
    
    Example:
        # Get daily costs by resource
        costs = get_cost_and_usage_with_resources(
            '2023-06-01',
            '2023-06-30',
            granularity='DAILY',
            group_by=[
                {'Type': 'DIMENSION', 'Key': 'SERVICE'},
                {'Type': 'DIMENSION', 'Key': 'RESOURCE'}
            ]
        )
        
        # Get costs for specific service
        service_costs = get_cost_and_usage_with_resources(
            '2023-06-01',
            '2023-06-30',
            filter={
                'Dimensions': {
                    'Key': 'SERVICE',
                    'Values': ['Amazon EC2']
                }
            }
        )
    """
    try:
        if not metrics:
            metrics = ['UnblendedCost', 'UsageQuantity']
            
        params = {
            'TimePeriod': {
                'Start': start_date,
                'End': end_date
            },
            'Granularity': granularity,
            'Metrics': metrics
        }
        
        if filter:
            params['Filter'] = filter
        if group_by:
            params['GroupBy'] = group_by
            
        response = ce_client.get_cost_and_usage_with_resources(**params)
        return response
    
    except ClientError as e:
        print(f"Error getting detailed cost and usage: {e}")
        raise
