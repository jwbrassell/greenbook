# Scatter Charts with Highcharts and Flask

## Table of Contents
- [Scatter Charts with Highcharts and Flask](#scatter-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Student Performance Analysis](#example-1:-student-performance-analysis)
  - [Example 2: Population Demographics](#example-2:-population-demographics)
  - [Example 3: Clustering Analysis](#example-3:-clustering-analysis)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Scatter Charts](#tips-for-working-with-scatter-charts)



## Overview

Scatter charts are ideal for visualizing relationships between two variables, showing patterns, correlations, and outliers in data points. They are particularly useful for analyzing trends, clustering, and distributions in datasets where each point represents two related values.

## Basic Configuration

Here's how to create a basic scatter chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/scatter-chart')
def scatter_chart():
    return render_template('scatter-chart.html')

@app.route('/scatter-data')
def scatter_data():
    # Generate sample data points
    n_points = 50
    x = np.random.normal(0, 2, n_points)
    y = x + np.random.normal(0, 1, n_points)
    
    data = [[float(x[i]), float(y[i])] for i in range(n_points)]
    
    return jsonify(data)
```

```html
<!-- templates/scatter-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="scatter-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/scatter-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('scatter-container', {
                chart: {
                    type: 'scatter'
                },
                title: {
                    text: 'Sample Correlation'
                },
                xAxis: {
                    title: {
                        text: 'X Value'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Y Value'
                    }
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5,
                            states: {
                                hover: {
                                    enabled: true,
                                    lineColor: 'rgb(100,100,100)'
                                }
                            }
                        },
                        states: {
                            hover: {
                                marker: {
                                    enabled: false
                                }
                            }
                        },
                        tooltip: {
                            headerFormat: '<b>{series.name}</b><br>',
                            pointFormat: 'x: {point.x:.2f}, y: {point.y:.2f}'
                        }
                    }
                },
                series: [{
                    name: 'Data Points',
                    color: 'rgba(124, 181, 236, 0.5)',
                    data: data
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Scatter charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        scatter: {
            marker: {
                radius: 5,           // Point size
                symbol: 'circle',    // Point shape
                fillColor: '#ff0000', // Point color
                lineWidth: 2,        // Point border width
                lineColor: '#000000' // Point border color
            },
            jitter: {
                x: 0.24             // Add random noise to prevent overlap
            },
            enableMouseTracking: true, // Enable hover effects
            stickyTracking: false,    // Keep tooltip visible
            animation: {
                duration: 1000      // Animation duration
            },
            states: {
                hover: {
                    enabled: true,   // Enable hover state
                    lineWidth: 2    // Hover border width
                }
            }
        }
    }
});
```

## Example 1: Student Performance Analysis

This example shows the relationship between study hours and test scores:

```python
@app.route('/student-performance')
def student_performance():
    # Sample student performance data
    n_students = 50
    np.random.seed(42)  # For reproducible results
    
    study_hours = np.random.uniform(1, 8, n_students)
    base_score = study_hours * 10  # Base correlation
    noise = np.random.normal(0, 5, n_students)  # Random variation
    test_scores = base_score + noise
    
    # Ensure scores are between 0 and 100
    test_scores = np.clip(test_scores, 0, 100)
    
    data = [{
        'x': float(study_hours[i]),
        'y': float(test_scores[i]),
        'student': f'Student {i+1}',
        'grade': 'A' if test_scores[i] >= 90 else
                 'B' if test_scores[i] >= 80 else
                 'C' if test_scores[i] >= 70 else
                 'D' if test_scores[i] >= 60 else 'F'
    } for i in range(n_students)]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="performance-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/student-performance')
        .then(response => response.json())
        .then(data => {
            const gradeColors = {
                'A': '#28a745',
                'B': '#17a2b8',
                'C': '#ffc107',
                'D': '#fd7e14',
                'F': '#dc3545'
            };
            
            Highcharts.chart('performance-chart', {
                chart: {
                    type: 'scatter'
                },
                title: {
                    text: 'Study Hours vs. Test Scores'
                },
                xAxis: {
                    title: {
                        text: 'Study Hours'
                    },
                    min: 0
                },
                yAxis: {
                    title: {
                        text: 'Test Score'
                    },
                    min: 0,
                    max: 100
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 6,
                            symbol: 'circle'
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.student + '</b><br>' +
                               'Study Hours: ' + this.x + '<br>' +
                               'Score: ' + this.y.toFixed(1) + '<br>' +
                               'Grade: ' + this.point.grade;
                    }
                },
                series: [{
                    name: 'Students',
                    data: data.map(point => ({
                        x: point.x,
                        y: point.y,
                        student: point.student,
                        grade: point.grade,
                        color: gradeColors[point.grade]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Population Demographics

This example shows age vs. income distribution with additional demographic information:

```python
@app.route('/demographics')
def demographics():
    # Sample demographic data
    n_people = 100
    np.random.seed(42)
    
    # Generate age and income with some correlation
    age = np.random.normal(40, 10, n_people)
    base_income = age * 1000  # Base correlation with age
    noise = np.random.normal(0, 10000, n_people)
    income = base_income + noise
    
    # Additional demographic factors
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD']
    industries = ['Technology', 'Healthcare', 'Finance', 'Education', 'Other']
    
    data = [{
        'x': float(age[i]),
        'y': float(income[i]),
        'education': np.random.choice(education_levels),
        'industry': np.random.choice(industries),
        'gender': np.random.choice(['Male', 'Female']),
        'experience': max(0, int(age[i] - 22))  # Assuming career starts at 22
    } for i in range(n_people)]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="demographics-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/demographics')
        .then(response => response.json())
        .then(data => {
            const industryColors = {
                'Technology': '#007bff',
                'Healthcare': '#28a745',
                'Finance': '#ffc107',
                'Education': '#17a2b8',
                'Other': '#6c757d'
            };
            
            Highcharts.chart('demographics-chart', {
                chart: {
                    type: 'scatter'
                },
                title: {
                    text: 'Age vs. Income Distribution'
                },
                xAxis: {
                    title: {
                        text: 'Age'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Income ($)'
                    },
                    labels: {
                        formatter: function() {
                            return this.value.toLocaleString();
                        }
                    }
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 6
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>Demographics</b><br>' +
                               'Age: ' + Math.round(this.x) + '<br>' +
                               'Income: $' + this.y.toLocaleString() + '<br>' +
                               'Education: ' + this.point.education + '<br>' +
                               'Industry: ' + this.point.industry + '<br>' +
                               'Gender: ' + this.point.gender + '<br>' +
                               'Experience: ' + this.point.experience + ' years';
                    }
                },
                series: [{
                    name: 'Population',
                    data: data.map(point => ({
                        x: point.x,
                        y: point.y,
                        education: point.education,
                        industry: point.industry,
                        gender: point.gender,
                        experience: point.experience,
                        color: industryColors[point.industry]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Clustering Analysis

This example shows data points with cluster assignments:

```python
@app.route('/cluster-data')
def cluster_data():
    # Generate clustered data
    n_clusters = 3
    n_points = 150
    np.random.seed(42)
    
    clusters = []
    for i in range(n_clusters):
        center_x = np.random.uniform(-5, 5)
        center_y = np.random.uniform(-5, 5)
        
        cluster_x = np.random.normal(center_x, 0.5, n_points // n_clusters)
        cluster_y = np.random.normal(center_y, 0.5, n_points // n_clusters)
        
        for j in range(len(cluster_x)):
            clusters.append({
                'x': float(cluster_x[j]),
                'y': float(cluster_y[j]),
                'cluster': i,
                'distance': float(np.sqrt((cluster_x[j] - center_x)**2 + 
                                       (cluster_y[j] - center_y)**2))
            })
    
    return jsonify(clusters)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="cluster-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/cluster-data')
        .then(response => response.json())
        .then(data => {
            const clusterColors = ['#007bff', '#28a745', '#dc3545'];
            
            // Group data by cluster
            const clusters = data.reduce((acc, point) => {
                if (!acc[point.cluster]) {
                    acc[point.cluster] = [];
                }
                acc[point.cluster].push(point);
                return acc;
            }, {});
            
            Highcharts.chart('cluster-chart', {
                chart: {
                    type: 'scatter'
                },
                title: {
                    text: 'Cluster Analysis'
                },
                xAxis: {
                    title: {
                        text: 'X Value'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Y Value'
                    }
                },
                plotOptions: {
                    scatter: {
                        marker: {
                            radius: 5
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>Cluster ' + this.point.cluster + '</b><br>' +
                               'X: ' + this.x.toFixed(2) + '<br>' +
                               'Y: ' + this.y.toFixed(2) + '<br>' +
                               'Distance from center: ' + 
                               this.point.distance.toFixed(2);
                    }
                },
                series: Object.entries(clusters).map(([cluster, points]) => ({
                    name: 'Cluster ' + cluster,
                    color: clusterColors[cluster],
                    data: points.map(point => ({
                        x: point.x,
                        y: point.y,
                        cluster: point.cluster,
                        distance: point.distance
                    }))
                }))
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate scatter charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_value = db.Column(db.Float, nullable=False)
    y_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)

@app.route('/scatter-data')
def get_scatter_data():
    points = DataPoint.query.all()
    
    data = [{
        'x': point.x_value,
        'y': point.y_value,
        'category': point.category,
        'metadata': point.metadata
    } for point in points]
    
    return jsonify(data)
```

## Tips for Working with Scatter Charts

1. Choose appropriate scales
2. Consider point size and opacity
3. Use meaningful colors
4. Implement proper tooltips
5. Handle overlapping points
6. Add trend lines if relevant
7. Consider data grouping
8. Optimize for large datasets
