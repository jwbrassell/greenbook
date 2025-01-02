"""
Python Data Handling Examples
This script demonstrates practical examples of working with different data formats.
"""

import json
import csv
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path

def json_examples():
    """Demonstrate JSON data handling"""
    # Sample data
    data = {
        'employees': [
            {'name': 'John Doe', 'age': 30, 'department': 'IT'},
            {'name': 'Jane Smith', 'age': 25, 'department': 'HR'}
        ]
    }

    # Writing JSON to file
    with open('sample_data.json', 'w') as f:
        json.dump(data, f, indent=4)

    # Reading JSON from file
    with open('sample_data.json', 'r') as f:
        loaded_data = json.load(f)

    # Manipulating JSON data
    for employee in loaded_data['employees']:
        employee['salary'] = 50000 + (employee['age'] * 1000)

    return loaded_data

def xml_examples():
    """Demonstrate XML data handling"""
    # Create XML structure
    root = ET.Element('company')
    
    departments = {
        'IT': ['John Doe', 'Alice Johnson'],
        'HR': ['Jane Smith', 'Bob Wilson']
    }
    
    for dept_name, employees in departments.items():
        dept = ET.SubElement(root, 'department')
        dept.set('name', dept_name)
        
        for emp_name in employees:
            emp = ET.SubElement(dept, 'employee')
            emp.text = emp_name
    
    # Write to file
    tree = ET.ElementTree(root)
    tree.write('sample_data.xml')
    
    # Read and parse XML
    parsed_tree = ET.parse('sample_data.xml')
    parsed_root = parsed_tree.getroot()
    
    # Extract data
    departments_data = {}
    for department in parsed_root.findall('department'):
        dept_name = department.get('name')
        employees = [emp.text for emp in department.findall('employee')]
        departments_data[dept_name] = employees
    
    return departments_data

def csv_examples():
    """Demonstrate CSV data handling"""
    # Sample data
    data = [
        ['Name', 'Age', 'Department', 'Salary'],
        ['John Doe', 30, 'IT', 80000],
        ['Jane Smith', 25, 'HR', 75000],
        ['Bob Wilson', 35, 'IT', 85000]
    ]
    
    # Writing CSV
    with open('sample_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)
    
    # Reading CSV as lists
    rows = []
    with open('sample_data.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            rows.append(row)
    
    # Reading CSV as dictionaries
    dict_rows = []
    with open('sample_data.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_rows.append(row)
    
    return {'list_data': rows, 'dict_data': dict_rows}

def pandas_examples():
    """Demonstrate pandas DataFrame operations"""
    # Create DataFrame from dictionary
    data = {
        'Name': ['John Doe', 'Jane Smith', 'Bob Wilson'],
        'Age': [30, 25, 35],
        'Department': ['IT', 'HR', 'IT'],
        'Salary': [80000, 75000, 85000]
    }
    df = pd.DataFrame(data)
    
    # Basic operations
    avg_salary = df['Salary'].mean()
    dept_stats = df.groupby('Department').agg({
        'Salary': ['mean', 'min', 'max'],
        'Age': 'mean'
    })
    
    # Save to different formats
    df.to_csv('pandas_output.csv', index=False)
    df.to_json('pandas_output.json', orient='records')
    
    # Read from different formats
    csv_df = pd.read_csv('pandas_output.csv')
    json_df = pd.read_json('pandas_output.json')
    
    # Data manipulation
    df['Bonus'] = df['Salary'] * 0.1
    df['Total'] = df['Salary'] + df['Bonus']
    
    return {
        'original_df': df,
        'department_stats': dept_stats,
        'average_salary': avg_salary
    }

def main():
    """Run all examples"""
    # Create output directory if it doesn't exist
    Path('output').mkdir(exist_ok=True)
    
    # Run examples
    json_result = json_examples()
    xml_result = xml_examples()
    csv_result = csv_examples()
    pandas_result = pandas_examples()
    
    # Print results
    print("\nJSON Results:")
    print(json.dumps(json_result, indent=2))
    
    print("\nXML Results:")
    print(json.dumps(xml_result, indent=2))
    
    print("\nCSV Results:")
    print(json.dumps(csv_result, indent=2))
    
    print("\nPandas Results:")
    print("\nDepartment Statistics:")
    print(pandas_result['department_stats'])
    print(f"\nAverage Salary: ${pandas_result['average_salary']:,.2f}")

if __name__ == '__main__':
    main()
