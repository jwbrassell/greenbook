# Boxplot Charts with Highcharts and Flask

## Table of Contents
- [Boxplot Charts with Highcharts and Flask](#boxplot-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
  - [Common Options](#common-options)
  - [Database Integration Examples](#database-integration-examples)
    - [Example 1: Student Test Scores Analysis](#example-1:-student-test-scores-analysis)
    - [Example 2: Sales Performance Analysis](#example-2:-sales-performance-analysis)
    - [Example 3: Response Time Analysis](#example-3:-response-time-analysis)
  - [Flask Integration Tips](#flask-integration-tips)



## Overview
Boxplot charts, also known as box-and-whisker plots, display statistical data through quartiles. They're excellent for showing the distribution of datasets and identifying outliers. Each box shows the median, quartiles, and potential outlier values.

## Basic Configuration
```python
@app.route('/boxplot-chart')
def boxplot_chart():
    chart_data = {
        'chart': {
            'type': 'boxplot'
        },
        'title': {
            'text': 'Monthly Temperature Distribution'
        },
        'legend': {
            'enabled': False
        },
        'xAxis': {
            'categories': ['Jan', 'Feb', 'Mar', 'Apr', 'May']
        },
        'series': [{
            'name': 'Temperature',
            'data': [
                [1, 2, 3, 4, 5],  # Min, Q1, Median, Q3, Max
                [2, 3, 4, 5, 6],
                [3, 4, 5, 6, 7],
                [4, 5, 6, 7, 8],
                [5, 6, 7, 8, 9]
            ]
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Common Options
- **plotOptions.boxplot**: Customize boxplot-specific options
  - `fillColor`: Set box fill color
  - `lineWidth`: Set line width
  - `medianWidth`: Set median line width
  - `whiskerLength`: Set whisker length
- **tooltip**: Configure hover information
- **outliers**: Handle outlier points display

## Database Integration Examples

### Example 1: Student Test Scores Analysis
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import numpy as np

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
db = SQLAlchemy(app)

class TestScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(50))
    score = db.Column(db.Float)
    class_name = db.Column(db.String(50))

@app.route('/test-scores')
def test_scores():
    subjects = ['Math', 'Science', 'English', 'History']
    series_data = []
    
    for subject in subjects:
        scores = [s.score for s in TestScore.query.filter_by(subject=subject).all()]
        if scores:
            stats = [
                np.min(scores),
                np.percentile(scores, 25),
                np.median(scores),
                np.percentile(scores, 75),
                np.max(scores)
            ]
            series_data.append(stats)
    
    chart_data = {
        'chart': {'type': 'boxplot'},
        'title': {'text': 'Test Score Distribution by Subject'},
        'xAxis': {'categories': subjects},
        'series': [{
            'name': 'Scores',
            'data': series_data
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 2: Sales Performance Analysis
```python
@app.route('/sales-distribution')
def sales_distribution():
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    series_data = []
    
    for month in months:
        sales = SalesRecord.query.filter(
            extract('month', SalesRecord.date) == months.index(month) + 1
        ).with_entities(SalesRecord.amount).all()
        
        sales_values = [sale.amount for sale in sales]
        stats = [
            min(sales_values),
            np.percentile(sales_values, 25),
            np.percentile(sales_values, 50),
            np.percentile(sales_values, 75),
            max(sales_values)
        ]
        series_data.append(stats)
    
    chart_data = {
        'chart': {'type': 'boxplot'},
        'title': {'text': 'Monthly Sales Distribution'},
        'xAxis': {'categories': months},
        'yAxis': {'title': {'text': 'Sales Amount ($)'}},
        'series': [{
            'name': 'Sales',
            'data': series_data
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 3: Response Time Analysis
```python
@app.route('/response-times')
def response_times():
    services = Service.query.all()
    series_data = []
    categories = []
    
    for service in services:
        response_times = [
            r.duration for r in ResponseTime.query.filter_by(service_id=service.id).all()
        ]
        
        if response_times:
            categories.append(service.name)
            stats = [
                min(response_times),
                np.percentile(response_times, 25),
                np.median(response_times),
                np.percentile(response_times, 75),
                max(response_times)
            ]
            series_data.append(stats)
    
    chart_data = {
        'chart': {'type': 'boxplot'},
        'title': {'text': 'Service Response Time Distribution'},
        'xAxis': {'categories': categories},
        'yAxis': {
            'title': {'text': 'Response Time (ms)'},
            'min': 0
        },
        'series': [{
            'name': 'Response Times',
            'data': series_data
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Flask Integration Tips
1. Use numpy for statistical calculations
2. Implement proper error handling for empty datasets
3. Consider caching for large datasets
4. Use database indexes for better query performance
5. Validate data before statistical calculations
6. Handle outliers appropriately based on business rules
