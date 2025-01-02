# Gauge Charts with Chart.js and Flask

## Table of Contents
- [Gauge Charts with Chart.js and Flask](#gauge-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Multi-Level Gauge](#example-1:-multi-level-gauge)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 2: Animated Gauge with Gradient](#example-2:-animated-gauge-with-gradient)
    - [Flask Implementation](#flask-implementation)
    - [Gradient and Animation Configuration](#gradient-and-animation-configuration)
  - [Example 3: Multiple Metrics Gauge](#example-3:-multiple-metrics-gauge)
    - [Flask Implementation](#flask-implementation)
    - [Multi-Metrics Configuration](#multi-metrics-configuration)
  - [Working with Database Data](#working-with-database-data)



Gauge charts are effective for displaying single values in a circular or semi-circular format. While Chart.js doesn't have a built-in gauge chart type, we can create them using doughnut charts with custom configurations.

## Basic Implementation

### Flask Route
```python
@app.route('/gauge-chart')
def gauge_chart():
    return render_template('gauge_chart.html')

@app.route('/api/gauge-data')
def gauge_data():
    # Example: System CPU usage percentage
    value = 65  # Example value between 0 and 100
    data = {
        'datasets': [{
            'data': [value, 100 - value],  # Value and remaining
            'backgroundColor': [
                'rgba(75, 192, 192, 0.8)',  # Active color
                'rgba(200, 200, 200, 0.2)'  # Background color
            ],
            'borderWidth': 0,
            'circumference': 180,  # Semi-circle
            'rotation': 270  # Start from bottom
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 300px;">
    <canvas id="gaugeChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/gauge-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('gaugeChart').getContext('2d');
            new Chart(ctx, {
                type: 'doughnut',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'CPU Usage'
                        },
                        tooltip: {
                            enabled: false
                        },
                        legend: {
                            display: false
                        }
                    },
                    cutout: '75%',
                    maintainAspectRatio: true
                },
                plugins: [{
                    id: 'gaugeText',
                    afterDraw: (chart) => {
                        const {ctx, data} = chart;
                        const value = data.datasets[0].data[0];
                        ctx.save();
                        ctx.textAlign = 'center';
                        ctx.textBaseline = 'middle';
                        ctx.font = '30px Arial';
                        ctx.fillStyle = '#666';
                        ctx.fillText(
                            `${value}%`,
                            chart.getDatasetMeta(0).data[0].x,
                            chart.getDatasetMeta(0).data[0].y + 30
                        );
                        ctx.restore();
                    }
                }]
            });
        });
});
</script>
```

## Example 1: Multi-Level Gauge

This example shows how to create a gauge with multiple color levels based on value ranges.

### Flask Implementation
```python
@app.route('/api/multi-level-gauge')
def multi_level_gauge():
    value = 75  # Example value
    
    def get_colors(value):
        if value < 30:
            return 'rgba(75, 192, 192, 0.8)'  # Green
        elif value < 70:
            return 'rgba(255, 206, 86, 0.8)'  # Yellow
        else:
            return 'rgba(255, 99, 132, 0.8)'  # Red
    
    data = {
        'datasets': [{
            'data': [value, 100 - value],
            'backgroundColor': [
                get_colors(value),
                'rgba(200, 200, 200, 0.2)'
            ],
            'borderWidth': 0,
            'circumference': 180,
            'rotation': 270
        }]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'doughnut',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                enabled: false
            },
            legend: {
                display: false
            }
        },
        cutout: '75%',
        rotation: -90,
        circumference: 180,
        maintainAspectRatio: true
    },
    plugins: [{
        id: 'gaugeText',
        afterDraw: (chart) => {
            const {ctx, data} = chart;
            const value = data.datasets[0].data[0];
            const centerX = chart.getDatasetMeta(0).data[0].x;
            const centerY = chart.getDatasetMeta(0).data[0].y;
            
            // Draw value
            ctx.save();
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = 'bold 30px Arial';
            ctx.fillStyle = '#666';
            ctx.fillText(`${value}%`, centerX, centerY + 30);
            
            // Draw status text
            ctx.font = '20px Arial';
            let status = value < 30 ? 'Low' :
                        value < 70 ? 'Medium' : 'High';
            ctx.fillText(status, centerX, centerY + 60);
            
            ctx.restore();
        }
    }]
};
```

## Example 2: Animated Gauge with Gradient

This example demonstrates how to create an animated gauge with gradient coloring.

### Flask Implementation
```python
@app.route('/api/animated-gauge')
def animated_gauge():
    value = 85  # Example value
    data = {
        'datasets': [{
            'data': [value, 100 - value],
            'backgroundColor': [
                'gradient',  # Will be replaced with gradient in JS
                'rgba(200, 200, 200, 0.2)'
            ],
            'borderWidth': 0,
            'circumference': 180,
            'rotation': 270
        }]
    }
    return jsonify(data)
```

### Gradient and Animation Configuration
```javascript
const config = {
    type: 'doughnut',
    data: chartData,
    options: {
        responsive: true,
        animation: {
            duration: 1500,
            easing: 'easeInOutQuart'
        },
        plugins: {
            tooltip: {
                enabled: false
            },
            legend: {
                display: false
            }
        },
        cutout: '75%'
    },
    plugins: [{
        id: 'gaugeGradient',
        beforeDraw: (chart) => {
            const {ctx, width, height} = chart.canvas;
            const gradient = ctx.createLinearGradient(0, 0, width, 0);
            gradient.addColorStop(0, 'rgba(75, 192, 192, 1)');
            gradient.addColorStop(0.5, 'rgba(255, 206, 86, 1)');
            gradient.addColorStop(1, 'rgba(255, 99, 132, 1)');
            chart.data.datasets[0].backgroundColor[0] = gradient;
        }
    }, {
        id: 'gaugeText',
        afterDraw: (chart) => {
            const {ctx, data} = chart;
            const value = data.datasets[0].data[0];
            const centerX = chart.getDatasetMeta(0).data[0].x;
            const centerY = chart.getDatasetMeta(0).data[0].y;
            
            ctx.save();
            
            // Animate value
            const currentValue = Math.round(chart.currentValue || 0);
            const targetValue = value;
            const speed = (targetValue - currentValue) / 20;
            chart.currentValue = currentValue + speed;
            
            // Draw value
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.font = 'bold 30px Arial';
            ctx.fillStyle = '#666';
            ctx.fillText(
                `${Math.round(chart.currentValue)}%`,
                centerX,
                centerY + 30
            );
            
            if (Math.abs(targetValue - currentValue) > 0.1) {
                requestAnimationFrame(() => chart.draw());
            }
            
            ctx.restore();
        }
    }]
};
```

## Example 3: Multiple Metrics Gauge

This example shows how to display multiple metrics in a single gauge chart.

### Flask Implementation
```python
@app.route('/api/multi-metrics-gauge')
def multi_metrics_gauge():
    data = {
        'cpu': 75,
        'memory': 60,
        'disk': 45,
        'datasets': [
            {
                'data': [75, 25],  # CPU
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(200, 200, 200, 0.2)'
                ],
                'circumference': 120,
                'rotation': 300
            },
            {
                'data': [60, 40],  # Memory
                'backgroundColor': [
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(200, 200, 200, 0.2)'
                ],
                'circumference': 120,
                'rotation': 180
            },
            {
                'data': [45, 55],  # Disk
                'backgroundColor': [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(200, 200, 200, 0.2)'
                ],
                'circumference': 120,
                'rotation': 60
            }
        ]
    }
    return jsonify(data)
```

### Multi-Metrics Configuration
```javascript
const config = {
    type: 'doughnut',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                enabled: false
            },
            legend: {
                display: false
            }
        },
        cutout: '75%'
    },
    plugins: [{
        id: 'gaugeText',
        afterDraw: (chart) => {
            const {ctx} = chart;
            const centerX = chart.width / 2;
            const centerY = chart.height / 2;
            const radius = Math.min(centerX, centerY) * 0.6;
            
            const metrics = [
                { name: 'CPU', color: 'rgb(255, 99, 132)' },
                { name: 'Memory', color: 'rgb(54, 162, 235)' },
                { name: 'Disk', color: 'rgb(75, 192, 192)' }
            ];
            
            metrics.forEach((metric, i) => {
                const angle = (i * 120 - 90) * Math.PI / 180;
                const x = centerX + radius * Math.cos(angle);
                const y = centerY + radius * Math.sin(angle);
                
                ctx.save();
                ctx.translate(x, y);
                
                // Draw metric name
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.font = '16px Arial';
                ctx.fillStyle = metric.color;
                ctx.fillText(metric.name, 0, -15);
                
                // Draw value
                ctx.font = 'bold 20px Arial';
                ctx.fillText(
                    `${chart.data.datasets[i].data[0]}%`,
                    0,
                    10
                );
                
                ctx.restore();
            });
        }
    }]
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic gauge charts:

```python
class SystemMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric_name = db.Column(db.String(50))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def get_latest_metrics():
        metrics = {}
        for metric in ['cpu', 'memory', 'disk']:
            latest = SystemMetrics.query\
                .filter_by(metric_name=metric)\
                .order_by(SystemMetrics.timestamp.desc())\
                .first()
            if latest:
                metrics[metric] = latest.value
                
        return {
            'datasets': [{
                'data': [
                    metrics.get('cpu', 0),
                    100 - metrics.get('cpu', 0)
                ],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(200, 200, 200, 0.2)'
                ],
                'borderWidth': 0,
                'circumference': 180,
                'rotation': 270
            }]
        }
```

This documentation provides three distinct examples of gauge charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and multiple metrics visualization.
