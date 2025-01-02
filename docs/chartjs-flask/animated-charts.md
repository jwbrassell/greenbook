# Animated Charts with Chart.js and Flask

## Table of Contents
- [Animated Charts with Chart.js and Flask](#animated-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Progressive Data Loading](#example-1:-progressive-data-loading)
    - [Flask Implementation](#flask-implementation)
    - [Progressive Animation Configuration](#progressive-animation-configuration)
  - [Example 2: Animated Data Updates](#example-2:-animated-data-updates)
    - [Flask Implementation](#flask-implementation)
    - [Dynamic Update Configuration](#dynamic-update-configuration)
  - [Example 3: Complex Animation Sequences](#example-3:-complex-animation-sequences)
    - [Flask Implementation](#flask-implementation)
    - [Sequence Animation Configuration](#sequence-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Animations can enhance data visualization by making charts more engaging and helping users understand data changes. This guide demonstrates how to implement various animation techniques using Chart.js with Flask.

## Basic Implementation

### Flask Route
```python
@app.route('/animated-chart')
def animated_chart():
    return render_template('animated_chart.html')

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

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="animatedChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('animatedChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    animation: {
                        duration: 2000,  // Animation duration in milliseconds
                        easing: 'easeInOutQuart',  // Animation easing function
                        from: 1,  // Start scale
                        to: 0,    // End scale
                        loop: false  // Whether to loop the animation
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Animated Sales Chart'
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Progressive Data Loading

This example shows how to animate data points appearing progressively.

### Flask Implementation
```python
@app.route('/api/progressive-data')
def progressive_data():
    data = {
        'labels': list(range(1, 13)),  # 12 months
        'datasets': [{
            'label': 'Monthly Performance',
            'data': [65, 59, 80, 81, 56, 55, 40, 45, 70, 85, 90, 95],
            'borderColor': 'rgb(75, 192, 192)',
            'tension': 0.4,
            'fill': false
        }]
    }
    return jsonify(data)
```

### Progressive Animation Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart'
        },
        plugins: {
            title: {
                display: true,
                text: 'Progressive Data Loading'
            }
        }
    },
    plugins: [{
        id: 'progressiveLoad',
        beforeInit: (chart) => {
            chart.data.datasets.forEach(dataset => {
                const originalData = [...dataset.data];
                dataset.data = [];
                
                // Progressively add data points
                let currentIndex = 0;
                const addDataPoint = () => {
                    if (currentIndex < originalData.length) {
                        dataset.data.push(originalData[currentIndex]);
                        currentIndex++;
                        chart.update('none');  // Update without animation
                        
                        if (currentIndex < originalData.length) {
                            setTimeout(addDataPoint, 200);
                        }
                    }
                };
                
                setTimeout(addDataPoint, 500);  // Start after initial render
            });
        }
    }]
};
```

## Example 2: Animated Data Updates

This example demonstrates how to animate data changes with smooth transitions.

### Flask Implementation
```python
@app.route('/api/update-data/<int:iteration>')
def update_data(iteration):
    import numpy as np
    
    # Generate different data for each iteration
    base = 50 + 10 * np.sin(iteration / 5)
    noise = np.random.normal(0, 5, 6)
    
    data = {
        'labels': ['A', 'B', 'C', 'D', 'E', 'F'],
        'datasets': [{
            'label': 'Dynamic Data',
            'data': [base + n for n in noise],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### Dynamic Update Configuration
```javascript
const chart = new Chart(ctx, {
    type: 'bar',
    data: initialData,
    options: {
        responsive: true,
        animation: {
            duration: 750,
            easing: 'easeInOutCubic',
            mode: 'active'
        },
        transitions: {
            active: {
                animation: {
                    duration: 750
                }
            }
        },
        plugins: {
            title: {
                display: true,
                text: 'Live Data Updates'
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grace: '10%'  // Add space for animations
            }
        }
    }
});

// Update data periodically
let iteration = 0;
setInterval(() => {
    fetch(`/api/update-data/${iteration}`)
        .then(response => response.json())
        .then(newData => {
            chart.data.datasets[0].data = newData.datasets[0].data;
            chart.update();
            iteration++;
        });
}, 2000);
```

## Example 3: Complex Animation Sequences

This example shows how to create complex animation sequences with multiple stages.

### Flask Implementation
```python
@app.route('/api/sequence-data')
def sequence_data():
    data = {
        'labels': ['Stage 1', 'Stage 2', 'Stage 3', 'Stage 4'],
        'datasets': [
            {
                'label': 'Process Flow',
                'data': [100, 80, 60, 40],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                'borderColor': [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                'borderWidth': 1
            }
        ]
    }
    return jsonify(data)
```

### Sequence Animation Configuration
```javascript
const animationSequence = {
    currentStage: 0,
    stages: [
        {
            duration: 1000,
            easing: 'easeInQuad',
            scale: {
                x: 1.2,
                y: 1
            }
        },
        {
            duration: 1000,
            easing: 'easeOutQuad',
            scale: {
                x: 1,
                y: 1.2
            }
        },
        {
            duration: 1000,
            easing: 'easeInOutQuad',
            scale: {
                x: 1,
                y: 1
            }
        }
    ]
};

const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        animation: false,  // Disable default animations
        plugins: {
            title: {
                display: true,
                text: 'Animation Sequence'
            }
        }
    },
    plugins: [{
        id: 'customAnimation',
        afterDraw: (chart) => {
            const stage = animationSequence.stages[animationSequence.currentStage];
            
            if (stage) {
                const {currentStage, stages} = animationSequence;
                const progress = chart.animator.getProgress();
                
                // Apply current stage transformations
                chart.ctx.save();
                chart.ctx.scale(
                    stage.scale.x,
                    stage.scale.y
                );
                
                // Move to next stage when current is complete
                if (progress === 1) {
                    animationSequence.currentStage = 
                        (currentStage + 1) % stages.length;
                    chart.draw();
                }
                
                chart.ctx.restore();
            }
        }
    }]
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for animated data visualization:

```python
class TimeSeriesData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime)
    value = db.Column(db.Float)
    category = db.Column(db.String(50))

    @staticmethod
    def get_animated_series(category, limit=50):
        """
        Get time series data with animation metadata
        """
        data = TimeSeriesData.query\
            .filter_by(category=category)\
            .order_by(TimeSeriesData.timestamp.desc())\
            .limit(limit)\
            .all()
            
        return {
            'labels': [d.timestamp.strftime('%Y-%m-%d %H:%M') for d in data],
            'datasets': [{
                'label': category,
                'data': [d.value for d in data],
                'borderColor': 'rgb(75, 192, 192)',
                'tension': 0.4,
                'animation': {
                    'duration': 2000,
                    'easing': 'easeInOutQuart',
                    'from': 0,
                    'to': 1,
                    'loop': false
                }
            }]
        }

@app.route('/api/animated-series/<category>')
def get_animated_series(category):
    return jsonify(TimeSeriesData.get_animated_series(category))
```

This documentation provides three distinct examples of animated charts with varying complexity and features. Each example demonstrates different aspects of Chart.js animation capabilities when integrated with Flask, from basic animations to complex sequences and dynamic updates.
