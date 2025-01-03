# Python Data Handling Guide

## Table of Contents
- [Python Data Handling Guide](#python-data-handling-guide)
  - [Overview](#overview)
  - [Prerequisites](#prerequisites)
  - [Installation and Setup](#installation-and-setup)
  - [Data Formats](#data-formats)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing Strategies](#testing-strategies)
  - [Troubleshooting](#troubleshooting)
  - [Best Practices](#best-practices)
  - [Integration Points](#integration-points)
  - [Next Steps](#next-steps)

## Overview
This comprehensive guide demonstrates how to work with various data formats in Python, including JSON, XML, CSV, and pandas DataFrames. Learn best practices for data handling, transformation, and analysis in Python applications.

## Prerequisites
- Python 3.7+
- Basic understanding of:
  - Python programming
  - Data structures
  - File operations
  - Memory management
- Required packages:
  - pandas
  - numpy
  - json
  - xml
  - csv

## Installation and Setup
1. Environment Setup:
```bash
# Create virtual environment
python -m venv data-env
source data-env/bin/activate  # Linux/Mac
# or
.\data-env\Scripts\activate   # Windows

# Install required packages
pip install pandas numpy requests lxml openpyxl
```

2. Basic Configuration:
```python
import pandas as pd
import numpy as np
import json
import xml.etree.ElementTree as ET
import csv

# Configure pandas display options
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.width', 1000)
```

## Data Formats
1. JSON Handling:
```python
def read_json_safely(file_path):
    """Safe JSON reading with error handling"""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        logging.error(f"JSON decode error: {e}")
        raise
    except IOError as e:
        logging.error(f"File error: {e}")
        raise

def write_json_safely(data, file_path):
    """Safe JSON writing with backup"""
    backup_path = f"{file_path}.bak"
    if os.path.exists(file_path):
        shutil.copy2(file_path, backup_path)
    
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
```

2. XML Processing:
```python
def parse_xml_safely(file_path):
    """Safe XML parsing with validation"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        validate_xml_structure(root)
        return root
    except ET.ParseError as e:
        logging.error(f"XML parse error: {e}")
        raise

def validate_xml_structure(root):
    """Validate XML structure against schema"""
    required_elements = ['id', 'name', 'value']
    for element in root:
        missing = [req for req in required_elements 
                  if element.find(req) is None]
        if missing:
            raise ValueError(f"Missing required elements: {missing}")
```

## Advanced Features
1. Data Transformation Pipeline:
```python
class DataPipeline:
    def __init__(self):
        self.steps = []
    
    def add_step(self, func):
        self.steps.append(func)
        return self
    
    def process(self, data):
        result = data
        for step in self.steps:
            result = step(result)
        return result

# Usage
pipeline = DataPipeline()
pipeline.add_step(clean_data)
       .add_step(transform_columns)
       .add_step(validate_results)
```

2. Custom Data Types:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataRecord:
    id: int
    name: str
    value: float
    timestamp: datetime
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'timestamp': self.timestamp.isoformat()
        }
```

## Security Considerations
1. Input Validation:
```python
def validate_dataframe(df, schema):
    """Validate DataFrame against schema"""
    for column, dtype in schema.items():
        if column not in df.columns:
            raise ValueError(f"Missing column: {column}")
        if df[column].dtype != dtype:
            raise ValueError(f"Invalid dtype for {column}")
```

2. File Operations:
```python
def safe_file_operation(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PermissionError:
            logging.error("Permission denied")
            raise
        except IOError as e:
            logging.error(f"IO Error: {e}")
            raise
    return wrapper
```

## Performance Optimization
1. Chunked Processing:
```python
def process_large_csv(file_path, chunk_size=10000):
    """Process large CSV files in chunks"""
    chunks = pd.read_csv(file_path, chunksize=chunk_size)
    results = []
    
    for chunk in chunks:
        processed = process_chunk(chunk)
        results.append(processed)
    
    return pd.concat(results)
```

2. Memory Management:
```python
def optimize_dataframe(df):
    """Optimize DataFrame memory usage"""
    for col in df.columns:
        if df[col].dtype == 'object':
            if len(df[col].unique()) / len(df) < 0.5:
                df[col] = df[col].astype('category')
        elif df[col].dtype == 'float64':
            df[col] = df[col].astype('float32')
    return df
```

## Testing Strategies
1. Unit Testing:
```python
import unittest

class TestDataHandling(unittest.TestCase):
    def setUp(self):
        self.test_data = pd.DataFrame({
            'id': range(1000),
            'value': np.random.randn(1000)
        })
    
    def test_data_cleaning(self):
        cleaned = clean_data(self.test_data)
        self.assertFalse(cleaned.isnull().any().any())
        self.assertTrue((cleaned['id'] >= 0).all())
```

2. Integration Testing:
```python
def test_data_pipeline():
    # Prepare test data
    input_data = load_test_data()
    
    # Process through pipeline
    pipeline = DataPipeline()
    result = pipeline.process(input_data)
    
    # Verify results
    assert_data_quality(result)
    verify_business_rules(result)
```

## Troubleshooting
1. Common Issues:
```python
def diagnose_dataframe(df):
    """Diagnose common DataFrame issues"""
    issues = []
    
    # Check for missing values
    missing = df.isnull().sum()
    if missing.any():
        issues.append(f"Missing values found: {missing}")
    
    # Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates:
        issues.append(f"Found {duplicates} duplicate rows")
    
    return issues
```

2. Error Handling:
```python
class DataHandlingError(Exception):
    """Custom error for data handling issues"""
    pass

def handle_data_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise DataHandlingError(f"Error in {func.__name__}: {str(e)}")
    return wrapper
```

## Best Practices
1. Data Validation:
```python
def validate_data_quality(df):
    """Validate data quality metrics"""
    assert df.shape[0] > 0, "DataFrame is empty"
    assert df.isnull().sum().sum() == 0, "Contains missing values"
    assert len(df.columns) == len(set(df.columns)), "Duplicate columns"
```

2. Documentation:
```python
def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Process DataFrame according to business rules.
    
    Args:
        df: Input DataFrame with required columns [id, value]
    
    Returns:
        Processed DataFrame with additional columns [result]
    
    Raises:
        ValueError: If required columns are missing
    """
    pass
```

## Integration Points
1. Database Integration:
```python
from sqlalchemy import create_engine

def save_to_database(df, table_name, connection_string):
    """Save DataFrame to database"""
    engine = create_engine(connection_string)
    df.to_sql(table_name, engine, if_exists='replace')
```

2. API Integration:
```python
import requests

def fetch_data_from_api(url, params=None):
    """Fetch data from REST API"""
    response = requests.get(url, params=params)
    response.raise_for_status()
    return pd.DataFrame(response.json())
```

## Next Steps
1. Advanced Topics
   - Machine learning integration
   - Real-time data processing
   - Big data frameworks
   - Data visualization

2. Further Learning
   - [Pandas Documentation](https://pandas.pydata.org/docs/)
   - [NumPy Documentation](https://numpy.org/doc/)
   - [Python Data Science Handbook](https://jakevdp.github.io/PythonDataScienceHandbook/)
   - Community resources
