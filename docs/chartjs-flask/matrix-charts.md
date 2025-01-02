# Matrix Charts with Chart.js and Flask

## Table of Contents
- [Matrix Charts with Chart.js and Flask](#matrix-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Heatmap Analysis](#example-1:-heatmap-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Activity Correlation Matrix](#example-2:-activity-correlation-matrix)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Example 3: Time-Based Usage Pattern](#example-3:-time-based-usage-pattern)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Visualization Configuration](#advanced-visualization-configuration)
  - [Working with Database Data](#working-with-database-data)



Matrix charts display data in a grid format, making them ideal for correlation analysis, heatmaps, and other grid-based visualizations. While Chart.js doesn't have a built-in matrix chart type, we can create them using a combination of scatter plots and custom plugins.

## Basic Implementation

### Flask Route
```python
@app.route('/matrix-chart')
def matrix_chart():
    return render_template('matrix_chart.html')

@app.route('/api/matrix-data')
def matrix_data():
    # Example: Correlation matrix data
    data = {
        'labels': ['A', 'B', 'C', 'D', 'E'],
        'datasets': [{
            'data': [
                {'x': 0, 'y': 0, 'v': 1.0},
                {'x': 0, 'y': 1, 'v': 0.8},
                {'x': 0, 'y': 2, 'v': 0.6},
                {'x': 0, 'y': 3, 'v': 0.4},
                {'x': 0, 'y': 4, 'v': 0.2},
                {'x': 1, 'y': 0, 'v': 0.8},
                {'x': 1, 'y': 1, 'v': 1.0},
                {'x': 1, 'y': 2, 'v': 0.7},
                {'x': 1, 'y': 3, 'v': 0.5},
                {'x': 1, 'y': 4, 'v': 0.3},
                # ... more data points
            ],
            'backgroundColor': function(context) {
                const value = context.raw.v;
                const alpha = value;
                return `rgba(75, 192, 192, ${alpha})`;
            },
            'borderColor': 'white',
            'borderWidth': 1,
            'hoverBackgroundColor': 'rgba(75, 192, 192, 1)',
            'width': 1,
            'height': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 600px;">
    <canvas id="matrixChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/matrix-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('matrixChart').getContext('2d');
            new Chart(ctx, {
                type: 'matrix',
                data: data,
                options: {
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Correlation Matrix'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw.v;
                                    return `Value: ${value.toFixed(2)}`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            type: 'linear',
                            offset: true,
                            min: -0.5,
                            max: data.labels.length - 0.5,
                            ticks: {
                                callback: function(value) {
                                    return data.labels[value];
                                }
                            }
                        },
                        y: {
                            type: 'linear',
                            offset: true,
                            min: -0.5,
                            max: data.labels.length - 0.5,
                            ticks: {
                                callback: function(value) {
                                    return data.labels[value];
                                }
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Heatmap Analysis

This example shows how to create a heatmap for temperature data across different times and locations.

### Flask Implementation
```python
@app.route('/api/heatmap-data')
def heatmap_data():
    # Example: Temperature data across hours and locations
    hours = list(range(24))
    locations = ['North', 'South', 'East', 'West', 'Center']
    
    import random
    data = {
        'labels': {
            'x': hours,
            'y': locations
        },
        'datasets': [{
            'data': [
                {
                    'x': hour,
                    'y': loc_idx,
                    'v': random.uniform(15, 35)  # Temperature between 15-35°C
                }
                for hour in hours
                for loc_idx, _ in enumerate(locations)
            ],
            'backgroundColor': function(context) {
                const value = context.raw.v;
                const normalized = (value - 15) / 20;  # Scale to 0-1
                return getTemperatureColor(normalized);
            },
            'borderColor': 'white',
            'borderWidth': 1,
            'width': 1,
            'height': 1
        }]
    }
    return jsonify(data)

def getTemperatureColor(value):
    # Convert value to color (blue to red gradient)
    return f'rgba({int(255 * value)}, 0, {int(255 * (1-value))}, 0.8)'
```

### Advanced Configuration
```javascript
const config = {
    type: 'matrix',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const hour = context.raw.x;
                        const location = data.labels.y[context.raw.y];
                        const temp = context.raw.v.toFixed(1);
                        return [
                            `Location: ${location}`,
                            `Time: ${hour}:00`,
                            `Temperature: ${temp}°C`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Hour of Day'
                },
                ticks: {
                    callback: function(value) {
                        return `${value}:00`;
                    }
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Location'
                }
            }
        }
    }
};
```

## Example 2: Activity Correlation Matrix

This example demonstrates how to create an interactive correlation matrix for user activities.

### Flask Implementation
```python
@app.route('/api/correlation-matrix')
def correlation_matrix():
    activities = ['Login', 'Search', 'Purchase', 'Review', 'Share']
    
    def generate_correlation(i, j):
        if i == j:
            return 1.0
        # Simulate correlation values
        import random
        return round(random.uniform(0.1, 0.9), 2)
    
    data = {
        'labels': activities,
        'datasets': [{
            'data': [
                {
                    'x': i,
                    'y': j,
                    'v': generate_correlation(i, j)
                }
                for i in range(len(activities))
                for j in range(len(activities))
            ],
            'backgroundColor': function(context) {
                const value = context.raw.v;
                return `rgba(75, 192, 192, ${value})`;
            },
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### Interactive Features Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    const value = context.raw.v;
                    const xLabel = data.labels[context.raw.x];
                    const yLabel = data.labels[context.raw.y];
                    return [
                        `${xLabel} vs ${yLabel}`,
                        `Correlation: ${value.toFixed(2)}`
                    ];
                }
            }
        }
    },
    onClick: (event, elements) => {
        if (elements.length > 0) {
            const element = elements[0];
            const datapoint = data.datasets[0].data[element.index];
            showCorrelationDetails(datapoint);
        }
    }
};

function showCorrelationDetails(datapoint) {
    const xActivity = data.labels[datapoint.x];
    const yActivity = data.labels[datapoint.y];
    console.log(`Detailed analysis of ${xActivity} vs ${yActivity}`);
    // Implement modal or detailed view
}
```

## Example 3: Time-Based Usage Pattern

This example shows how to create a matrix chart for analyzing usage patterns over time.

### Flask Implementation
```python
@app.route('/api/usage-pattern')
def usage_pattern():
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    hours = list(range(24))
    
    def generate_usage(day_idx, hour):
        # Simulate higher usage during work hours on weekdays
        is_weekend = day_idx >= 5
        is_work_hours = 9 <= hour <= 17
        base_usage = 0.2 if is_weekend else 0.4
        work_boost = 0.4 if is_work_hours and not is_weekend else 0
        return round(base_usage + work_boost + random.uniform(0, 0.2), 2)
    
    data = {
        'labels': {
            'x': hours,
            'y': days
        },
        'datasets': [{
            'data': [
                {
                    'x': hour,
                    'y': day_idx,
                    'v': generate_usage(day_idx, hour)
                }
                for day_idx in range(len(days))
                for hour in hours
            ],
            'backgroundColor': function(context) {
                return `rgba(54, 162, 235, ${context.raw.v})`;
            }
        }]
    }
    return jsonify(data)
```

### Advanced Visualization Configuration
```javascript
const config = {
    type: 'matrix',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: 'Weekly Usage Pattern'
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const value = context.raw.v;
                        const hour = context.raw.x;
                        const day = data.labels.y[context.raw.y];
                        const percentage = (value * 100).toFixed(1);
                        return [
                            `${day} at ${hour}:00`,
                            `Usage: ${percentage}%`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Hour of Day'
                },
                ticks: {
                    callback: function(value) {
                        return `${value}:00`;
                    }
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Day of Week'
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic matrix charts:

```python
class ActivityData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    day_of_week = db.Column(db.Integer)  # 0-6
    hour = db.Column(db.Integer)  # 0-23
    usage_level = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_weekly_pattern():
        activities = ActivityData.query\
            .order_by(ActivityData.day_of_week, ActivityData.hour)\
            .all()
            
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        hours = list(range(24))
        
        return {
            'labels': {
                'x': hours,
                'y': days
            },
            'datasets': [{
                'data': [
                    {
                        'x': activity.hour,
                        'y': activity.day_of_week,
                        'v': activity.usage_level
                    }
                    for activity in activities
                ],
                'backgroundColor': function(context) {
                    return `rgba(54, 162, 235, ${context.raw.v})`;
                }
            }]
        }
```

This documentation provides three distinct examples of matrix charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like interactive heatmaps and usage pattern analysis.
