# Error Bars Charts with Chart.js and Flask

## Table of Contents
- [Error Bars Charts with Chart.js and Flask](#error-bars-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Scientific Data with Error Ranges](#example-1:-scientific-data-with-error-ranges)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Error Bars Configuration](#advanced-error-bars-configuration)
  - [Example 2: Line Chart with Error Bands](#example-2:-line-chart-with-error-bands)
    - [Flask Implementation](#flask-implementation)
    - [Error Bands Configuration](#error-bands-configuration)
  - [Example 3: Box Plot with Error Bars](#example-3:-box-plot-with-error-bars)
    - [Flask Implementation](#flask-implementation)
    - [Box Plot with Error Bars Configuration](#box-plot-with-error-bars-configuration)
  - [Working with Database Data](#working-with-database-data)



Error bars are important visual elements that indicate the variability of data or measurement uncertainty. While Chart.js doesn't have built-in error bars, we can implement them using custom plugins and configurations.

## Basic Implementation

### Flask Route
```python
@app.route('/error-bars-chart')
def error_bars_chart():
    return render_template('error_bars_chart.html')

@app.route('/api/error-bars-data')
def error_bars_data():
    # Example: Experimental measurements with uncertainties
    data = {
        'labels': ['Sample A', 'Sample B', 'Sample C', 'Sample D', 'Sample E'],
        'datasets': [{
            'label': 'Measurements',
            'data': [45, 59, 75, 62, 48],
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'errorBars': {
                'plus': [5, 4, 6, 5, 4],      # Upper error margins
                'minus': [4, 5, 5, 4, 3]      # Lower error margins
            }
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="errorBarsChart"></canvas>
</div>

<script>
// Error bars plugin
const errorBarsPlugin = {
    id: 'errorBars',
    afterDatasetsDraw: (chart, args, options) => {
        const {ctx} = chart;
        
        chart.data.datasets.forEach((dataset, i) => {
            const meta = chart.getDatasetMeta(i);
            if (!meta.visible || !dataset.errorBars) return;
            
            meta.data.forEach((element, index) => {
                const {x, y} = element.tooltipPosition();
                const plus = dataset.errorBars.plus[index];
                const minus = dataset.errorBars.minus[index];
                
                ctx.save();
                ctx.beginPath();
                ctx.strokeStyle = dataset.borderColor;
                ctx.lineWidth = 2;
                
                // Draw vertical error bar line
                ctx.moveTo(x, y - plus);
                ctx.lineTo(x, y + minus);
                
                // Draw horizontal caps
                ctx.moveTo(x - 5, y - plus);
                ctx.lineTo(x + 5, y - plus);
                ctx.moveTo(x - 5, y + minus);
                ctx.lineTo(x + 5, y + minus);
                
                ctx.stroke();
                ctx.restore();
            });
        });
    }
};

document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/error-bars-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('errorBarsChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Measurements with Error Bars'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const value = context.raw;
                                    const plus = context.dataset.errorBars.plus[context.dataIndex];
                                    const minus = context.dataset.errorBars.minus[context.dataIndex];
                                    return [
                                        `Value: ${value}`,
                                        `Error: +${plus}/-${minus}`
                                    ];
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                },
                plugins: [errorBarsPlugin]
            });
        });
});
</script>
```

## Example 1: Scientific Data with Error Ranges

This example shows how to display scientific measurements with asymmetric error ranges.

### Flask Implementation
```python
@app.route('/api/scientific-data')
def scientific_data():
    import numpy as np
    
    # Simulated experimental data
    measurements = np.array([120, 135, 145, 130, 140])
    uncertainties = {
        'systematic': np.array([5, 5, 5, 5, 5]),
        'statistical': np.array([3, 4, 2, 3, 4]),
        'total': None
    }
    
    # Calculate total uncertainty (root sum square)
    uncertainties['total'] = np.sqrt(
        uncertainties['systematic']**2 + 
        uncertainties['statistical']**2
    )
    
    data = {
        'labels': ['Exp 1', 'Exp 2', 'Exp 3', 'Exp 4', 'Exp 5'],
        'datasets': [{
            'type': 'bar',
            'label': 'Measurements',
            'data': measurements.tolist(),
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'errorBars': {
                'plus': uncertainties['total'].tolist(),
                'minus': uncertainties['total'].tolist(),
                'systematic': uncertainties['systematic'].tolist(),
                'statistical': uncertainties['statistical'].tolist()
            }
        }]
    }
    return jsonify(data)
```

### Advanced Error Bars Configuration
```javascript
const advancedErrorBarsPlugin = {
    id: 'advancedErrorBars',
    afterDatasetsDraw: (chart, args, options) => {
        const {ctx} = chart;
        
        chart.data.datasets.forEach((dataset, i) => {
            const meta = chart.getDatasetMeta(i);
            if (!meta.visible || !dataset.errorBars) return;
            
            meta.data.forEach((element, index) => {
                const {x, y} = element.tooltipPosition();
                const errorBars = dataset.errorBars;
                
                // Draw total error bars
                drawErrorBar(ctx, x, y, 
                    errorBars.plus[index], 
                    errorBars.minus[index],
                    dataset.borderColor,
                    10  // Cap width
                );
                
                // Draw systematic error bars (thinner)
                drawErrorBar(ctx, x, y,
                    errorBars.systematic[index],
                    errorBars.systematic[index],
                    'rgba(255, 99, 132, 1)',
                    5   // Smaller cap width
                );
            });
        });
    }
};

function drawErrorBar(ctx, x, y, plus, minus, color, capWidth) {
    ctx.save();
    ctx.beginPath();
    ctx.strokeStyle = color;
    ctx.lineWidth = 2;
    
    ctx.moveTo(x, y - plus);
    ctx.lineTo(x, y + minus);
    ctx.moveTo(x - capWidth/2, y - plus);
    ctx.lineTo(x + capWidth/2, y - plus);
    ctx.moveTo(x - capWidth/2, y + minus);
    ctx.lineTo(x + capWidth/2, y + minus);
    
    ctx.stroke();
    ctx.restore();
}
```

## Example 2: Line Chart with Error Bands

This example demonstrates how to create a line chart with error bands (continuous error ranges).

### Flask Implementation
```python
@app.route('/api/error-bands')
def error_bands():
    import numpy as np
    
    x = np.linspace(0, 10, 50)
    y = 5 * np.sin(x) + 20
    uncertainty = 2 * np.ones_like(x)
    
    data = {
        'labels': x.tolist(),
        'datasets': [
            {
                'type': 'line',
                'label': 'Measurement',
                'data': y.tolist(),
                'borderColor': 'rgba(75, 192, 192, 1)',
                'fill': false
            },
            {
                'type': 'line',
                'label': 'Upper Bound',
                'data': (y + uncertainty).tolist(),
                'borderColor': 'rgba(75, 192, 192, 0.2)',
                'fill': '+1'  # Fill to next dataset
            },
            {
                'type': 'line',
                'label': 'Lower Bound',
                'data': (y - uncertainty).tolist(),
                'borderColor': 'rgba(75, 192, 192, 0.2)',
                'fill': false
            }
        ]
    }
    return jsonify(data)
```

### Error Bands Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            filler: {
                propagate: true
            },
            legend: {
                labels: {
                    filter: function(legendItem, data) {
                        return legendItem.text === 'Measurement';
                    }
                }
            }
        },
        interaction: {
            intersect: false,
            mode: 'index'
        }
    }
};
```

## Example 3: Box Plot with Error Bars

This example shows how to combine box plots with error bars for comprehensive statistical visualization.

### Flask Implementation
```python
@app.route('/api/box-plot-with-errors')
def box_plot_with_errors():
    import numpy as np
    
    def generate_sample_data():
        base = np.random.normal(100, 15, 50)
        return {
            'min': np.min(base),
            'q1': np.percentile(base, 25),
            'median': np.median(base),
            'q3': np.percentile(base, 75),
            'max': np.max(base),
            'mean': np.mean(base),
            'std': np.std(base)
        }
    
    samples = [generate_sample_data() for _ in range(5)]
    
    data = {
        'labels': ['Group A', 'Group B', 'Group C', 'Group D', 'Group E'],
        'datasets': [{
            'type': 'boxplot',
            'data': [{
                'min': s['min'],
                'q1': s['q1'],
                'median': s['median'],
                'q3': s['q3'],
                'max': s['max']
            } for s in samples],
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'errorBars': {
                'mean': [s['mean'] for s in samples],
                'std': [s['std'] for s in samples]
            }
        }]
    }
    return jsonify(data)
```

### Box Plot with Error Bars Configuration
```javascript
const boxPlotErrorBarsPlugin = {
    id: 'boxPlotErrorBars',
    afterDatasetsDraw: (chart, args, options) => {
        const {ctx} = chart;
        
        chart.data.datasets.forEach((dataset, i) => {
            const meta = chart.getDatasetMeta(i);
            if (!meta.visible || !dataset.errorBars) return;
            
            meta.data.forEach((element, index) => {
                const {x} = element.tooltipPosition();
                const mean = dataset.errorBars.mean[index];
                const std = dataset.errorBars.std[index];
                
                const meanY = chart.scales.y.getPixelForValue(mean);
                
                // Draw mean marker
                ctx.save();
                ctx.beginPath();
                ctx.strokeStyle = 'rgba(255, 99, 132, 1)';
                ctx.fillStyle = 'rgba(255, 99, 132, 1)';
                ctx.arc(x, meanY, 3, 0, 2 * Math.PI);
                ctx.fill();
                
                // Draw standard deviation bars
                const upperY = chart.scales.y.getPixelForValue(mean + std);
                const lowerY = chart.scales.y.getPixelForValue(mean - std);
                
                ctx.beginPath();
                ctx.moveTo(x, upperY);
                ctx.lineTo(x, lowerY);
                ctx.moveTo(x - 5, upperY);
                ctx.lineTo(x + 5, upperY);
                ctx.moveTo(x - 5, lowerY);
                ctx.lineTo(x + 5, lowerY);
                ctx.stroke();
                
                ctx.restore();
            });
        });
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic error bars charts:

```python
class ExperimentalData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment_id = db.Column(db.String(50))
    value = db.Column(db.Float)
    uncertainty = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def get_experiment_data(experiment_id):
        measurements = ExperimentalData.query\
            .filter_by(experiment_id=experiment_id)\
            .order_by(ExperimentalData.timestamp)\
            .all()
            
        return {
            'labels': [m.timestamp.strftime('%Y-%m-%d %H:%M') for m in measurements],
            'datasets': [{
                'label': 'Measurements',
                'data': [m.value for m in measurements],
                'backgroundColor': 'rgba(75, 192, 192, 0.5)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'errorBars': {
                    'plus': [m.uncertainty for m in measurements],
                    'minus': [m.uncertainty for m in measurements]
                }
            }]
        }
```

This documentation provides three distinct examples of error bars charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like error bands and statistical visualizations.
