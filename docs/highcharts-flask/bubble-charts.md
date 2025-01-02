# Bubble Charts with Highcharts and Flask

## Table of Contents
- [Bubble Charts with Highcharts and Flask](#bubble-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Population Demographics](#example-1:-population-demographics)
  - [Example 2: Product Analysis](#example-2:-product-analysis)
  - [Example 3: Research Data](#example-3:-research-data)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Bubble Charts](#tips-for-working-with-bubble-charts)



## Overview

Bubble charts extend scatter plots by adding a third dimension represented by the size of each bubble. They are particularly useful for visualizing data with three numerical variables, where two dimensions are plotted on the X and Y axes, and the third dimension is represented by the bubble size.

## Basic Configuration

Here's how to create a basic bubble chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify
import numpy as np

app = Flask(__name__)

@app.route('/bubble-chart')
def bubble_chart():
    return render_template('bubble-chart.html')

@app.route('/bubble-data')
def bubble_data():
    # Generate sample data points
    n_points = 20
    np.random.seed(42)
    
    data = [{
        'x': float(np.random.normal(100, 20)),  # X value
        'y': float(np.random.normal(100, 20)),  # Y value
        'z': float(np.random.uniform(5, 25)),   # Bubble size
        'name': f'Point {i+1}'                  # Point name
    } for i in range(n_points)]
    
    return jsonify(data)
```

```html
<!-- templates/bubble-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="bubble-container" style="min-width: 310px; height: 400px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/bubble-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('bubble-container', {
                chart: {
                    type: 'bubble'
                },
                title: {
                    text: 'Sample Bubble Chart'
                },
                xAxis: {
                    title: {
                        text: 'X Axis'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Y Axis'
                    }
                },
                plotOptions: {
                    bubble: {
                        minSize: 5,
                        maxSize: 25,
                        zMin: 0,
                        zMax: 25
                    }
                },
                tooltip: {
                    pointFormat: 'X: {point.x}<br>Y: {point.y}<br>Size: {point.z}'
                },
                series: [{
                    name: 'Bubbles',
                    data: data.map(point => ({
                        x: point.x,
                        y: point.y,
                        z: point.z,
                        name: point.name
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Bubble charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    plotOptions: {
        bubble: {
            minSize: 5,          // Minimum bubble size in pixels
            maxSize: 25,         // Maximum bubble size in pixels
            zMin: 0,            // Minimum z value
            zMax: 100,          // Maximum z value
            sizeBy: 'area',     // 'area' or 'width'
            zThreshold: 0,      // Z value below which bubbles are colored differently
            displayNegative: true, // Show negative z values
            marker: {
                fillOpacity: 0.5, // Bubble opacity
                lineWidth: 1,    // Bubble border width
                lineColor: null  // Bubble border color
            }
        }
    }
});
```

## Example 1: Population Demographics

This example shows cities with population, GDP per capita, and total GDP:

```python
@app.route('/city-demographics')
def city_demographics():
    # Sample city data
    cities = [
        {
            'name': 'Tokyo',
            'population': 37.4,  # millions
            'gdpPerCapita': 42000,
            'region': 'Asia'
        },
        {
            'name': 'New York',
            'population': 18.8,
            'gdpPerCapita': 75000,
            'region': 'Americas'
        },
        {
            'name': 'London',
            'population': 9.0,
            'gdpPerCapita': 66000,
            'region': 'Europe'
        },
        {
            'name': 'Shanghai',
            'population': 27.0,
            'gdpPerCapita': 35000,
            'region': 'Asia'
        },
        {
            'name': 'Paris',
            'population': 11.0,
            'gdpPerCapita': 62000,
            'region': 'Europe'
        }
    ]
    
    # Calculate total GDP (bubble size)
    for city in cities:
        city['gdp'] = city['population'] * city['gdpPerCapita']
    
    return jsonify(cities)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="demographics-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/city-demographics')
        .then(response => response.json())
        .then(data => {
            const regionColors = {
                'Asia': '#ff7f0e',
                'Americas': '#2ca02c',
                'Europe': '#1f77b4'
            };
            
            Highcharts.chart('demographics-chart', {
                chart: {
                    type: 'bubble'
                },
                title: {
                    text: 'City Demographics and Economic Indicators'
                },
                xAxis: {
                    title: {
                        text: 'Population (millions)'
                    }
                },
                yAxis: {
                    title: {
                        text: 'GDP per Capita ($)'
                    },
                    labels: {
                        formatter: function() {
                            return this.value.toLocaleString();
                        }
                    }
                },
                plotOptions: {
                    bubble: {
                        minSize: 20,
                        maxSize: 60
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'Population: ' + this.x + ' million<br>' +
                               'GDP per Capita: $' + this.y.toLocaleString() + '<br>' +
                               'Total GDP: $' + (this.z/1e9).toFixed(1) + ' billion';
                    }
                },
                series: [{
                    name: 'Cities',
                    data: data.map(city => ({
                        x: city.population,
                        y: city.gdpPerCapita,
                        z: city.gdp,
                        name: city.name,
                        color: regionColors[city.region]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Product Analysis

This example shows products with price, sales volume, and profit margin:

```python
@app.route('/product-analysis')
def product_analysis():
    # Sample product data
    products = [
        {
            'name': 'Product A',
            'price': 199.99,
            'sales': 1500,
            'margin': 0.35,
            'category': 'Electronics'
        },
        {
            'name': 'Product B',
            'price': 49.99,
            'sales': 5000,
            'margin': 0.25,
            'category': 'Accessories'
        },
        {
            'name': 'Product C',
            'price': 299.99,
            'sales': 800,
            'margin': 0.40,
            'category': 'Electronics'
        },
        {
            'name': 'Product D',
            'price': 79.99,
            'sales': 3000,
            'margin': 0.30,
            'category': 'Accessories'
        },
        {
            'name': 'Product E',
            'price': 149.99,
            'sales': 2000,
            'margin': 0.45,
            'category': 'Electronics'
        }
    ]
    
    # Calculate total profit (bubble size)
    for product in products:
        product['profit'] = product['price'] * product['sales'] * product['margin']
    
    return jsonify(products)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="product-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/product-analysis')
        .then(response => response.json())
        .then(data => {
            const categoryColors = {
                'Electronics': '#1f77b4',
                'Accessories': '#ff7f0e'
            };
            
            Highcharts.chart('product-chart', {
                chart: {
                    type: 'bubble'
                },
                title: {
                    text: 'Product Performance Analysis'
                },
                xAxis: {
                    title: {
                        text: 'Price ($)'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Sales Volume'
                    }
                },
                plotOptions: {
                    bubble: {
                        minSize: 20,
                        maxSize: 50,
                        opacity: 0.7
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'Price: $' + this.x.toFixed(2) + '<br>' +
                               'Sales: ' + this.y + ' units<br>' +
                               'Margin: ' + (this.point.margin * 100).toFixed(1) + '%<br>' +
                               'Total Profit: $' + this.z.toLocaleString();
                    }
                },
                series: [{
                    name: 'Products',
                    data: data.map(product => ({
                        x: product.price,
                        y: product.sales,
                        z: product.profit,
                        name: product.name,
                        margin: product.margin,
                        color: categoryColors[product.category]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Research Data

This example shows research data with multiple variables and confidence levels:

```python
@app.route('/research-data')
def research_data():
    # Sample research data
    np.random.seed(42)
    n_samples = 15
    
    data = []
    for i in range(n_samples):
        confidence = np.random.uniform(0.7, 0.99)
        data.append({
            'x_value': float(np.random.normal(50, 10)),
            'y_value': float(np.random.normal(50, 10)),
            'sample_size': int(np.random.uniform(100, 1000)),
            'confidence': confidence,
            'group': np.random.choice(['A', 'B', 'C']),
            'name': f'Sample {i+1}'
        })
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="research-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/research-data')
        .then(response => response.json())
        .then(data => {
            const groupColors = {
                'A': '#1f77b4',
                'B': '#ff7f0e',
                'C': '#2ca02c'
            };
            
            Highcharts.chart('research-chart', {
                chart: {
                    type: 'bubble'
                },
                title: {
                    text: 'Research Data Analysis'
                },
                xAxis: {
                    title: {
                        text: 'Variable X'
                    }
                },
                yAxis: {
                    title: {
                        text: 'Variable Y'
                    }
                },
                plotOptions: {
                    bubble: {
                        minSize: 15,
                        maxSize: 45,
                        opacity: function(point) {
                            return point.confidence;
                        }
                    }
                },
                tooltip: {
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br>' +
                               'X Value: ' + this.x.toFixed(2) + '<br>' +
                               'Y Value: ' + this.y.toFixed(2) + '<br>' +
                               'Sample Size: ' + this.z + '<br>' +
                               'Confidence: ' + (this.point.confidence * 100).toFixed(1) + '%<br>' +
                               'Group: ' + this.point.group;
                    }
                },
                series: [{
                    name: 'Samples',
                    data: data.map(point => ({
                        x: point.x_value,
                        y: point.y_value,
                        z: point.sample_size,
                        name: point.name,
                        group: point.group,
                        confidence: point.confidence,
                        color: groupColors[point.group]
                    }))
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate bubble charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///research.db'
db = SQLAlchemy(app)

class DataPoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_value = db.Column(db.Float, nullable=False)
    y_value = db.Column(db.Float, nullable=False)
    size_value = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50))
    confidence = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    metadata = db.Column(db.JSON)

@app.route('/bubble-data')
def get_bubble_data():
    points = DataPoint.query.all()
    
    data = [{
        'x': point.x_value,
        'y': point.y_value,
        'z': point.size_value,
        'category': point.category,
        'confidence': point.confidence,
        'metadata': point.metadata
    } for point in points]
    
    return jsonify(data)
```

## Tips for Working with Bubble Charts

1. Choose appropriate scales
2. Size bubbles meaningfully
3. Use opacity effectively
4. Implement clear tooltips
5. Consider data grouping
6. Use meaningful colors
7. Handle overlapping
8. Optimize for readability
