# Python Data Handling Guide

## Table of Contents
- [Python Data Handling Guide](#python-data-handling-guide)
  - [Table of Contents](#table-of-contents)
  - [Table of Contents](#table-of-contents)
  - [JSON Data](#json-data)
    - [Reading JSON](#reading-json)
- [Reading JSON from a string](#reading-json-from-a-string)
- [Reading JSON from a file](#reading-json-from-a-file)
    - [Writing JSON](#writing-json)
- [Writing JSON to a string](#writing-json-to-a-string)
- [Writing JSON to a file](#writing-json-to-a-file)
    - [Pretty Printing JSON](#pretty-printing-json)
- [Pretty print with custom formatting](#pretty-print-with-custom-formatting)
  - [XML Data](#xml-data)
    - [Reading XML](#reading-xml)
- [Parse XML file](#parse-xml-file)
- [Parse XML string](#parse-xml-string)
- [Accessing elements](#accessing-elements)
    - [Writing XML](#writing-xml)
- [Create XML structure](#create-xml-structure)
- [Create XML tree](#create-xml-tree)
- [Write to file](#write-to-file)
  - [CSV Data](#csv-data)
    - [Reading CSV](#reading-csv)
- [Reading CSV file](#reading-csv-file)
    - [Writing CSV](#writing-csv)
- [Writing dictionary data](#writing-dictionary-data)
- [Writing list data](#writing-list-data)
  - [Pandas DataFrames](#pandas-dataframes)
    - [Creating DataFrames](#creating-dataframes)
- [Create from dictionary](#create-from-dictionary)
- [Create from CSV](#create-from-csv)
- [Create from JSON](#create-from-json)
    - [Basic Operations](#basic-operations)
- [View first few rows](#view-first-few-rows)
- [Get basic information](#get-basic-information)
- [Get statistical summary](#get-statistical-summary)
- [Select columns](#select-columns)
- [Filter rows](#filter-rows)
- [Sort values](#sort-values)
- [Group by and aggregate](#group-by-and-aggregate)
    - [Data Export](#data-export)
- [Export to CSV](#export-to-csv)
- [Export to JSON](#export-to-json)
- [Export to Excel](#export-to-excel)
    - [Data Cleaning](#data-cleaning)
- [Handle missing values](#handle-missing-values)
- [Remove duplicates](#remove-duplicates)
- [Rename columns](#rename-columns)
- [Change data types](#change-data-types)
    - [Data Analysis](#data-analysis)
- [Basic statistics](#basic-statistics)
- [Correlation](#correlation)
- [Custom calculations](#custom-calculations)
- [Apply custom function](#apply-custom-function)
  - [Best Practices](#best-practices)
  - [Common Patterns](#common-patterns)
    - [Reading Large Files](#reading-large-files)
- [CSV - using chunks](#csv---using-chunks)
- [JSON - using iterative parser](#json---using-iterative-parser)
    - [Data Transformation Pipeline](#data-transformation-pipeline)
    - [Combining Multiple Data Sources](#combining-multiple-data-sources)
- [Merge DataFrames](#merge-dataframes)
- [Concatenate DataFrames](#concatenate-dataframes)



This guide demonstrates how to work with various data formats in Python, including JSON, XML, CSV, and pandas DataFrames.

## Table of Contents
1. [JSON Data](#json-data)
2. [XML Data](#xml-data)
3. [CSV Data](#csv-data)
4. [Pandas DataFrames](#pandas-dataframes)

## JSON Data

### Reading JSON
```python
import json

# Reading JSON from a string
json_string = '{"name": "John", "age": 30}'
data = json.loads(json_string)

# Reading JSON from a file
with open('data.json', 'r') as file:
    data = json.load(file)
```

### Writing JSON
```python
# Writing JSON to a string
data = {"name": "John", "age": 30}
json_string = json.dumps(data, indent=4)

# Writing JSON to a file
with open('output.json', 'w') as file:
    json.dump(data, file, indent=4)
```

### Pretty Printing JSON
```python
# Pretty print with custom formatting
json_string = json.dumps(data, indent=4, sort_keys=True)
```

## XML Data

### Reading XML
```python
import xml.etree.ElementTree as ET

# Parse XML file
tree = ET.parse('data.xml')
root = tree.getroot()

# Parse XML string
xml_string = '''
<root>
    <person>
        <name>John</name>
        <age>30</age>
    </person>
</root>
'''
root = ET.fromstring(xml_string)

# Accessing elements
for person in root.findall('person'):
    name = person.find('name').text
    age = person.find('age').text
```

### Writing XML
```python
# Create XML structure
root = ET.Element('root')
person = ET.SubElement(root, 'person')
name = ET.SubElement(person, 'name')
name.text = 'John'
age = ET.SubElement(person, 'age')
age.text = '30'

# Create XML tree
tree = ET.ElementTree(root)

# Write to file
tree.write('output.xml', encoding='utf-8', xml_declaration=True)
```

## CSV Data

### Reading CSV
```python
import csv

# Reading CSV file
with open('data.csv', 'r') as file:
    # Read as dictionary
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        print(row)  # Each row is a dictionary

    # Read as list
    csv_reader = csv.reader(file)
    for row in csv_reader:
        print(row)  # Each row is a list
```

### Writing CSV
```python
# Writing dictionary data
data = [
    {'name': 'John', 'age': 30},
    {'name': 'Jane', 'age': 25}
]

with open('output.csv', 'w', newline='') as file:
    fieldnames = ['name', 'age']
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()  # Write header row
    writer.writerows(data)  # Write data rows

# Writing list data
data = [
    ['name', 'age'],
    ['John', 30],
    ['Jane', 25]
]

with open('output.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)
```

## Pandas DataFrames

### Creating DataFrames
```python
import pandas as pd

# Create from dictionary
data = {
    'name': ['John', 'Jane'],
    'age': [30, 25]
}
df = pd.DataFrame(data)

# Create from CSV
df = pd.read_csv('data.csv')

# Create from JSON
df = pd.read_json('data.json')
```

### Basic Operations
```python
# View first few rows
print(df.head())

# Get basic information
print(df.info())

# Get statistical summary
print(df.describe())

# Select columns
names = df['name']
subset = df[['name', 'age']]

# Filter rows
adults = df[df['age'] >= 18]

# Sort values
sorted_df = df.sort_values('age', ascending=False)

# Group by and aggregate
grouped = df.groupby('category').mean()
```

### Data Export
```python
# Export to CSV
df.to_csv('output.csv', index=False)

# Export to JSON
df.to_json('output.json', orient='records')

# Export to Excel
df.to_excel('output.xlsx', sheet_name='Sheet1')
```

### Data Cleaning
```python
# Handle missing values
df.fillna(0)  # Fill with zero
df.dropna()   # Remove rows with missing values

# Remove duplicates
df.drop_duplicates()

# Rename columns
df.rename(columns={'old_name': 'new_name'})

# Change data types
df['age'] = df['age'].astype(int)
```

### Data Analysis
```python
# Basic statistics
mean_age = df['age'].mean()
median_age = df['age'].median()
age_counts = df['age'].value_counts()

# Correlation
correlation = df.corr()

# Custom calculations
df['age_squared'] = df['age'] ** 2

# Apply custom function
def adult_status(age):
    return 'Adult' if age >= 18 else 'Minor'
df['status'] = df['age'].apply(adult_status)
```

## Best Practices

1. **Error Handling**: Always wrap file operations in try-except blocks
2. **File Closing**: Use context managers (with statements) for file operations
3. **Data Validation**: Validate data before processing
4. **Memory Management**: Use iterators for large files
5. **Encoding**: Specify encoding when dealing with text files
6. **Backup**: Create backups before modifying data files
7. **Documentation**: Document data structure and processing steps

## Common Patterns

### Reading Large Files
```python
# CSV - using chunks
for chunk in pd.read_csv('large_file.csv', chunksize=1000):
    process_chunk(chunk)

# JSON - using iterative parser
with open('large_file.json', 'r') as file:
    parser = ijson.parse(file)
    for prefix, event, value in parser:
        process_value(value)
```

### Data Transformation Pipeline
```python
def transform_data(df):
    return (df
            .pipe(clean_data)
            .pipe(transform_columns)
            .pipe(calculate_metrics)
            .pipe(validate_results))
```

### Combining Multiple Data Sources
```python
# Merge DataFrames
merged_df = pd.merge(df1, df2, on='id', how='left')

# Concatenate DataFrames
combined_df = pd.concat([df1, df2], axis=0)
