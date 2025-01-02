# Chart.js Plugins with Flask

## Table of Contents
- [Chart.js Plugins with Flask](#chartjs-plugins-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Plugin Implementation](#basic-plugin-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template with Plugin](#html-template-with-plugin)
  - [Example 1: Data Label Plugin](#example-1:-data-label-plugin)
    - [Flask Implementation](#flask-implementation)
    - [Data Label Plugin Configuration](#data-label-plugin-configuration)
  - [Example 2: Interactive Annotation Plugin](#example-2:-interactive-annotation-plugin)
    - [Flask Implementation](#flask-implementation)
    - [Annotation Plugin Configuration](#annotation-plugin-configuration)
  - [Example 3: Advanced Analytics Plugin](#example-3:-advanced-analytics-plugin)
    - [Flask Implementation](#flask-implementation)
    - [Analytics Plugin Configuration](#analytics-plugin-configuration)
  - [Working with Database Data](#working-with-database-data)



Plugins extend Chart.js functionality by adding new features or modifying existing behavior. This guide demonstrates how to use built-in plugins and create custom plugins when integrating Chart.js with Flask.

## Basic Plugin Implementation

### Flask Route
```python
@app.route('/plugin-chart')
def plugin_chart():
    return render_template('plugin_chart.html')

@app.route('/api/chart-data')
def chart_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Sales',
            'data': [65, 59, 80, 81, 56, 55],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template with Plugin
```html
<div style="width: 800px;">
    <canvas id="pluginChart"></canvas>
</div>

<script>
// Custom plugin definition
const customPlugin = {
    id: 'customPlugin',
    beforeDraw: (chart, args, options) => {
        const {ctx, chartArea: {top, bottom, left, right, width, height}} = chart;
        
        ctx.save();
        
        // Add custom background
        ctx.fillStyle = options.backgroundColor || 'rgba(255, 255, 255, 0.5)';
        ctx.fillRect(left, top, width, height);
        
        // Add watermark
        if (options.watermark) {
            ctx.font = '20px Arial';
            ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(options.watermark, left + width/2, top + height/2);
        }
        
        ctx.restore();
    }
};

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('pluginChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        customPlugin: {
                            backgroundColor: 'rgba(230, 230, 230, 0.2)',
                            watermark: 'Company Data'
                        }
                    }
                },
                plugins: [customPlugin]
            });
        });
});
</script>
```

## Example 1: Data Label Plugin

This example shows how to implement a plugin for displaying data labels on chart elements.

### Flask Implementation
```python
@app.route('/api/labeled-data')
def labeled_data():
    data = {
        'labels': ['Product A', 'Product B', 'Product C', 'Product D'],
        'datasets': [{
            'label': 'Sales Distribution',
            'data': [4500, 3200, 6800, 2100],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)'
            ]
        }]
    }
    return jsonify(data)
```

### Data Label Plugin Configuration
```javascript
const dataLabelsPlugin = {
    id: 'dataLabels',
    afterDatasetsDraw: (chart, args, options) => {
        const {ctx, data, chartArea: {top, bottom}, scales: {x, y}} = chart;
        
        ctx.save();
        ctx.font = options.font || '12px Arial';
        ctx.fillStyle = options.color || 'black';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'bottom';
        
        data.datasets.forEach((dataset, datasetIndex) => {
            chart.getDatasetMeta(datasetIndex).data.forEach((datapoint, index) => {
                const value = dataset.data[index];
                const formattedValue = options.formatter ? 
                    options.formatter(value) : 
                    value.toString();
                
                // Position label above bar/point
                const x = datapoint.x;
                const y = datapoint.y - 5;  // 5px above
                
                ctx.fillText(formattedValue, x, y);
            });
        });
        
        ctx.restore();
    }
};

const config = {
    type: 'bar',
    data: chartData,
    options: {
        plugins: {
            dataLabels: {
                font: '14px Arial',
                color: '#666',
                formatter: (value) => `$${value.toLocaleString()}`
            }
        }
    },
    plugins: [dataLabelsPlugin]
};
```

## Example 2: Interactive Annotation Plugin

This example demonstrates how to create a plugin for adding interactive annotations to charts.

### Flask Implementation
```python
@app.route('/api/annotated-data')
def annotated_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Performance',
            'data': [65, 59, 80, 81, 56, 55],
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.4,
            'fill': false
        }],
        'annotations': [
            {
                'point': 2,  # March
                'text': 'Peak Performance',
                'color': 'rgba(255, 99, 132, 0.8)'
            },
            {
                'point': 4,  # May
                'text': 'Strategy Change',
                'color': 'rgba(54, 162, 235, 0.8)'
            }
        ]
    }
    return jsonify(data)
```

### Annotation Plugin Configuration
```javascript
const annotationPlugin = {
    id: 'annotations',
    afterDraw: (chart, args, options) => {
        const {ctx, data, chartArea: {top, bottom}, scales: {x, y}} = chart;
        
        if (!data.annotations) return;
        
        ctx.save();
        
        data.annotations.forEach(annotation => {
            const meta = chart.getDatasetMeta(0);
            const datapoint = meta.data[annotation.point];
            
            // Draw connector line
            ctx.beginPath();
            ctx.moveTo(datapoint.x, datapoint.y);
            ctx.lineTo(datapoint.x, top);
            ctx.strokeStyle = annotation.color;
            ctx.stroke();
            
            // Draw annotation box
            const boxWidth = ctx.measureText(annotation.text).width + 20;
            const boxHeight = 30;
            const boxX = datapoint.x - boxWidth/2;
            const boxY = top - boxHeight - 5;
            
            ctx.fillStyle = annotation.color;
            ctx.fillRect(boxX, boxY, boxWidth, boxHeight);
            
            // Draw annotation text
            ctx.fillStyle = 'white';
            ctx.font = '12px Arial';
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(
                annotation.text,
                datapoint.x,
                boxY + boxHeight/2
            );
        });
        
        ctx.restore();
    }
};
```

## Example 3: Advanced Analytics Plugin

This example shows how to create a plugin that adds statistical analysis overlays to charts.

### Flask Implementation
```python
@app.route('/api/analytics-data')
def analytics_data():
    import numpy as np
    
    # Generate sample data
    data = np.random.normal(100, 15, 50).tolist()
    
    return jsonify({
        'labels': list(range(len(data))),
        'datasets': [{
            'label': 'Measurements',
            'data': data,
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.4,
            'fill': false
        }]
    })
```

### Analytics Plugin Configuration
```javascript
const analyticsPlugin = {
    id: 'analytics',
    beforeDraw: (chart, args, options) => {
        const {ctx, data, chartArea: {top, bottom, left, right}, scales: {x, y}} = chart;
        
        // Calculate statistics
        const values = data.datasets[0].data;
        const mean = values.reduce((a, b) => a + b) / values.length;
        const stdDev = Math.sqrt(
            values.reduce((a, b) => a + Math.pow(b - mean, 2), 0) / values.length
        );
        
        ctx.save();
        
        // Draw mean line
        const meanY = y.getPixelForValue(mean);
        ctx.beginPath();
        ctx.moveTo(left, meanY);
        ctx.lineTo(right, meanY);
        ctx.strokeStyle = 'rgba(255, 99, 132, 0.8)';
        ctx.setLineDash([5, 5]);
        ctx.stroke();
        
        // Draw standard deviation band
        const upperY = y.getPixelForValue(mean + stdDev);
        const lowerY = y.getPixelForValue(mean - stdDev);
        
        ctx.fillStyle = 'rgba(255, 99, 132, 0.1)';
        ctx.fillRect(left, upperY, right - left, lowerY - upperY);
        
        // Add labels
        ctx.font = '12px Arial';
        ctx.fillStyle = 'rgba(255, 99, 132, 0.8)';
        ctx.textAlign = 'left';
        ctx.fillText(`Mean: ${mean.toFixed(2)}`, left + 10, meanY - 5);
        ctx.fillText(`σ: ${stdDev.toFixed(2)}`, left + 10, upperY - 5);
        
        ctx.restore();
    }
};

const config = {
    type: 'line',
    data: chartData,
    options: {
        plugins: {
            analytics: {
                enabled: true
            }
        }
    },
    plugins: [analyticsPlugin]
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database and use plugins for enhanced visualization:

```python
class AnalyticsData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Float)
    category = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime)
    
    @staticmethod
    def get_data_with_analytics(category):
        data = AnalyticsData.query\
            .filter_by(category=category)\
            .order_by(AnalyticsData.timestamp)\
            .all()
            
        values = [d.value for d in data]
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        std_dev = variance ** 0.5
        
        return {
            'labels': [d.timestamp.strftime('%Y-%m-%d') for d in data],
            'datasets': [{
                'label': category,
                'data': values,
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.4
            }],
            'analytics': {
                'mean': mean,
                'standardDeviation': std_dev,
                'outliers': [
                    i for i, v in enumerate(values)
                    if abs(v - mean) > 2 * std_dev
                ]
            }
        }

@app.route('/api/analytics/<category>')
def get_analytics(category):
    return jsonify(AnalyticsData.get_data_with_analytics(category))
```

This documentation provides three distinct examples of Chart.js plugins with varying complexity and features. Each example demonstrates different aspects of plugin development when integrated with Flask, from basic customizations to advanced analytics overlays.
