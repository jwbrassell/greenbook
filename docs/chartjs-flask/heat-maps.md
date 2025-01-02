# Heat Maps with Chart.js and Flask

## Table of Contents
- [Heat Maps with Chart.js and Flask](#heat-maps-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Activity Density Map](#example-1:-activity-density-map)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Performance Analysis Heat Map](#example-2:-performance-analysis-heat-map)
    - [Flask Implementation](#flask-implementation)
    - [Performance Visualization Configuration](#performance-visualization-configuration)
  - [Example 3: Geographic Heat Map](#example-3:-geographic-heat-map)
    - [Flask Implementation](#flask-implementation)
    - [Geographic Visualization Configuration](#geographic-visualization-configuration)
  - [Working with Database Data](#working-with-database-data)



Heat maps are effective for visualizing data density and patterns across two dimensions using color intensity. While Chart.js doesn't have a built-in heat map type, we can create them using scatter plots with custom configurations and plugins.

## Basic Implementation

### Flask Route
```python
@app.route('/heat-map')
def heat_map():
    return render_template('heat_map.html')

@app.route('/api/heat-map-data')
def heat_map_data():
    # Example: Temperature readings across a grid
    import numpy as np
    
    # Generate sample data
    x_points = np.linspace(0, 10, 20)
    y_points = np.linspace(0, 10, 20)
    data_points = []
    
    for x in x_points:
        for y in y_points:
            # Generate temperature value with some random variation
            temperature = 20 + 5 * np.sin(x/2) + 3 * np.cos(y/2) + np.random.normal(0, 1)
            data_points.append({
                'x': float(x),
                'y': float(y),
                'value': float(temperature)
            })
    
    data = {
        'datasets': [{
            'label': 'Temperature Distribution',
            'data': data_points,
            'backgroundColor': 'function',  # Will be set in JavaScript
            'borderColor': 'white',
            'borderWidth': 1,
            'radius': 20,
            'hoverRadius': 22
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="heatMap"></canvas>
</div>

<script>
// Color scale function
function getColor(value, min, max) {
    const normalized = (value - min) / (max - min);
    // Use a color scale from blue (cold) to red (hot)
    const hue = ((1 - normalized) * 240).toString(10);
    return `hsla(${hue}, 100%, 50%, 0.5)`;
}

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/heat-map-data')
        .then(response => response.json())
        .then(data => {
            // Calculate min and max values
            const values = data.datasets[0].data.map(d => d.value);
            const min = Math.min(...values);
            const max = Math.max(...values);
            
            // Set color function
            data.datasets[0].backgroundColor = function(context) {
                if (context.raw) {
                    return getColor(context.raw.value, min, max);
                }
                return 'rgba(0, 0, 0, 0.1)';
            };
            
            const ctx = document.getElementById('heatMap').getContext('2d');
            new Chart(ctx, {
                type: 'scatter',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Temperature Distribution'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Temperature: ${context.raw.value.toFixed(1)}°C`;
                                }
                            }
                        },
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'X Position'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Y Position'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Activity Density Map

This example shows how to create a heat map of user activity across different times and days.

### Flask Implementation
```python
@app.route('/api/activity-heatmap')
def activity_heatmap():
    import numpy as np
    
    # Generate 7 days x 24 hours activity data
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    hours = list(range(24))
    data_points = []
    
    for day_idx, day in enumerate(days):
        for hour in hours:
            # Simulate higher activity during work hours on weekdays
            is_weekend = day_idx >= 5
            is_work_hours = 8 <= hour <= 17
            base_activity = 10 if (is_work_hours and not is_weekend) else 5
            activity = base_activity + np.random.normal(0, 2)
            
            data_points.append({
                'x': hour,
                'y': day_idx,
                'value': float(max(0, activity))
            })
    
    data = {
        'datasets': [{
            'data': data_points,
            'backgroundColor': 'function',
            'borderColor': 'white',
            'borderWidth': 1,
            'radius': 15,
            'hoverRadius': 17
        }],
        'labels': {
            'y': days
        }
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'scatter',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const hour = context.raw.x;
                        const day = chartData.labels.y[context.raw.y];
                        return [
                            `${day}, ${hour}:00`,
                            `Activity Level: ${context.raw.value.toFixed(1)}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                min: -0.5,
                max: 23.5,
                ticks: {
                    callback: function(value) {
                        return `${value}:00`;
                    }
                }
            },
            y: {
                min: -0.5,
                max: 6.5,
                ticks: {
                    callback: function(value) {
                        return chartData.labels.y[value];
                    }
                }
            }
        }
    }
};
```

## Example 2: Performance Analysis Heat Map

This example demonstrates how to analyze system performance metrics using a heat map.

### Flask Implementation
```python
@app.route('/api/performance-heatmap')
def performance_heatmap():
    data_points = []
    metrics = ['CPU', 'Memory', 'Disk', 'Network', 'Cache']
    servers = ['Server A', 'Server B', 'Server C', 'Server D', 'Server E']
    
    for i, metric in enumerate(metrics):
        for j, server in enumerate(servers):
            # Simulate performance score (0-100)
            score = generate_performance_score(metric, server)
            data_points.append({
                'x': j,
                'y': i,
                'value': score
            })
    
    data = {
        'datasets': [{
            'data': data_points,
            'backgroundColor': 'function',
            'borderColor': 'white',
            'borderWidth': 1,
            'radius': 25
        }],
        'labels': {
            'x': servers,
            'y': metrics
        }
    }
    return jsonify(data)

def generate_performance_score(metric, server):
    import random
    base_score = 80  # Generally good performance
    variation = random.uniform(-20, 10)  # Some variation
    return max(0, min(100, base_score + variation))
```

### Performance Visualization Configuration
```javascript
const config = {
    type: 'scatter',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const server = chartData.labels.x[context.raw.x];
                        const metric = chartData.labels.y[context.raw.y];
                        const score = context.raw.value.toFixed(1);
                        return [
                            `${server} - ${metric}`,
                            `Performance Score: ${score}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    callback: function(value) {
                        return chartData.labels.x[value];
                    }
                }
            },
            y: {
                ticks: {
                    callback: function(value) {
                        return chartData.labels.y[value];
                    }
                }
            }
        }
    }
};
```

## Example 3: Geographic Heat Map

This example shows how to create a simplified geographic heat map for regional data analysis.

### Flask Implementation
```python
@app.route('/api/geographic-heatmap')
def geographic_heatmap():
    # Example: Regional sales data
    regions = [
        {'name': 'North', 'x': 5, 'y': 8},
        {'name': 'South', 'x': 5, 'y': 2},
        {'name': 'East', 'x': 8, 'y': 5},
        {'name': 'West', 'x': 2, 'y': 5},
        {'name': 'Central', 'x': 5, 'y': 5}
    ]
    
    data_points = []
    for region in regions:
        # Generate sales data for each region
        sales = generate_regional_sales(region['name'])
        data_points.append({
            'x': region['x'],
            'y': region['y'],
            'value': sales,
            'region': region['name']
        })
    
    data = {
        'datasets': [{
            'data': data_points,
            'backgroundColor': 'function',
            'borderColor': 'white',
            'borderWidth': 1,
            'radius': 30,
            'hoverRadius': 35
        }]
    }
    return jsonify(data)

def generate_regional_sales(region):
    import random
    # Simulate different sales patterns for different regions
    base_sales = {
        'North': 800,
        'South': 600,
        'East': 750,
        'West': 700,
        'Central': 900
    }
    variation = random.uniform(-100, 100)
    return base_sales.get(region, 700) + variation
```

### Geographic Visualization Configuration
```javascript
const config = {
    type: 'scatter',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const data = context.raw;
                        return [
                            `Region: ${data.region}`,
                            `Sales: $${data.value.toFixed(0)}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                min: 0,
                max: 10,
                display: false
            },
            y: {
                min: 0,
                max: 10,
                display: false
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic heat maps:

```python
class MetricData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x_value = db.Column(db.Float)
    y_value = db.Column(db.Float)
    metric_value = db.Column(db.Float)
    category = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_heatmap_data(category, start_date, end_date):
        metrics = MetricData.query\
            .filter(
                MetricData.category == category,
                MetricData.timestamp.between(start_date, end_date)
            )\
            .all()
            
        return {
            'datasets': [{
                'data': [{
                    'x': m.x_value,
                    'y': m.y_value,
                    'value': m.metric_value
                } for m in metrics],
                'backgroundColor': 'function',
                'borderColor': 'white',
                'borderWidth': 1,
                'radius': 20
            }]
        }
```

This documentation provides three distinct examples of heat maps with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like geographic visualization and performance analysis.
