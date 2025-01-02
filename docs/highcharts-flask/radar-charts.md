# Radar Charts with Highcharts and Flask

## Table of Contents
- [Radar Charts with Highcharts and Flask](#radar-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
  - [Common Options](#common-options)
  - [Database Integration Examples](#database-integration-examples)
    - [Example 1: Student Performance Analysis](#example-1:-student-performance-analysis)
    - [Example 2: Product Feature Comparison](#example-2:-product-feature-comparison)
    - [Example 3: Team Skills Assessment](#example-3:-team-skills-assessment)
  - [Flask Integration Tips](#flask-integration-tips)



## Overview
Radar charts, also known as spider or star charts, display multivariate data on a two-dimensional chart with three or more variables represented on axes starting from the same point. They're particularly useful for comparing multiple entities across various attributes or showing performance metrics.

## Basic Configuration
```python
@app.route('/radar-chart')
def radar_chart():
    chart_data = {
        'chart': {
            'type': 'radar'
        },
        'title': {
            'text': 'Skills Assessment'
        },
        'xAxis': {
            'categories': ['Coding', 'Communication', 'Problem Solving', 
                          'Teamwork', 'Leadership', 'Technical Knowledge']
        },
        'series': [{
            'name': 'Employee A',
            'data': [90, 85, 95, 80, 75, 88]
        }, {
            'name': 'Employee B',
            'data': [85, 90, 80, 88, 82, 85]
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Common Options
- **plotOptions.radar**: Customize radar-specific options
  - `pointPlacement`: Control point placement on the radial axis
  - `lineWidth`: Set the width of radar lines
  - `marker`: Configure data point markers
- **xAxis.labels**: Format category labels
- **yAxis**: Configure value axis properties
- **tooltip**: Customize hover tooltips

## Database Integration Examples

### Example 1: Student Performance Analysis
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class StudentPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100))
    math = db.Column(db.Integer)
    science = db.Column(db.Integer)
    literature = db.Column(db.Integer)
    history = db.Column(db.Integer)
    arts = db.Column(db.Integer)
    sports = db.Column(db.Integer)

@app.route('/student-performance')
def student_performance():
    students = StudentPerformance.query.limit(3).all()
    
    series_data = [{
        'name': student.student_name,
        'data': [student.math, student.science, student.literature,
                student.history, student.arts, student.sports]
    } for student in students]
    
    chart_data = {
        'chart': {'type': 'radar'},
        'title': {'text': 'Student Performance Comparison'},
        'xAxis': {
            'categories': ['Math', 'Science', 'Literature', 
                          'History', 'Arts', 'Sports']
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 2: Product Feature Comparison
```python
@app.route('/product-comparison')
def product_comparison():
    products = Product.query.filter(
        Product.category == 'Smartphone'
    ).limit(3).all()
    
    series_data = [{
        'name': product.name,
        'data': [
            product.performance_score,
            product.camera_score,
            product.battery_score,
            product.display_score,
            product.build_quality_score
        ]
    } for product in products]
    
    chart_data = {
        'chart': {'type': 'radar'},
        'title': {'text': 'Smartphone Comparison'},
        'xAxis': {
            'categories': ['Performance', 'Camera', 'Battery', 
                          'Display', 'Build Quality']
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 3: Team Skills Assessment
```python
@app.route('/team-skills')
def team_skills():
    team_members = Employee.query.filter_by(department='Engineering').all()
    
    series_data = [{
        'name': employee.name,
        'data': [
            employee.technical_skills,
            employee.communication_skills,
            employee.problem_solving,
            employee.teamwork,
            employee.leadership,
            employee.innovation
        ]
    } for employee in team_members]
    
    chart_data = {
        'chart': {'type': 'radar'},
        'title': {'text': 'Team Skills Assessment'},
        'xAxis': {
            'categories': ['Technical Skills', 'Communication', 
                          'Problem Solving', 'Teamwork', 
                          'Leadership', 'Innovation']
        },
        'yAxis': {
            'min': 0,
            'max': 100
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Flask Integration Tips
1. Use SQLAlchemy models to structure your data
2. Implement proper error handling for database queries
3. Consider caching for frequently accessed data
4. Use database indexes for better performance
5. Implement data validation before rendering
