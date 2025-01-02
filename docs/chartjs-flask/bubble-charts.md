# Bubble Charts with Chart.js and Flask

## Table of Contents
- [Bubble Charts with Chart.js and Flask](#bubble-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Population Demographics Analysis](#example-1:-population-demographics-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Research Impact Analysis](#example-2:-research-impact-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Example 3: Project Resource Allocation](#example-3:-project-resource-allocation)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Working with Database Data](#working-with-database-data)



Bubble charts are powerful visualizations that can display three dimensions of data simultaneously: x-axis position, y-axis position, and bubble size. They're particularly useful for showing relationships between different variables while incorporating a third dimension through the bubble size.

## Basic Implementation

### Flask Route
```python
@app.route('/bubble-chart')
def bubble_chart():
    return render_template('bubble_chart.html')

@app.route('/api/bubble-data')
def bubble_data():
    # Example: Product data (x: price, y: sales, r: market size)
    data = {
        'datasets': [{
            'label': 'Product Performance',
            'data': [
                {'x': 20, 'y': 150, 'r': 15},  # Low price, high sales, medium market
                {'x': 35, 'y': 90, 'r': 10},   # Mid price, mid sales, small market
                {'x': 50, 'y': 45, 'r': 20},   # High price, low sales, large market
                {'x': 15, 'y': 195, 'r': 25},  # Lowest price, highest sales, largest market
                {'x': 40, 'y': 75, 'r': 12}    # Mid-high price, lower sales, medium market
            ],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)',
                'rgba(153, 102, 255, 0.5)'
            ],
            'borderColor': [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)',
                'rgb(153, 102, 255)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="bubbleChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/bubble-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('bubbleChart').getContext('2d');
            new Chart(ctx, {
                type: 'bubble',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Product Performance Analysis'
                        },
                        legend: {
                            position: 'top',
                        }
                    },
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Price ($)'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Sales Volume'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Population Demographics Analysis

This example shows how to visualize population demographics with age, income, and population size.

### Flask Implementation
```python
@app.route('/api/demographics-data')
def demographics_data():
    data = {
        'datasets': [
            {
                'label': 'Urban Demographics',
                'data': [
                    {'x': 25, 'y': 45000, 'r': 30},  # Young adults, medium income, large population
                    {'x': 35, 'y': 65000, 'r': 25},  # Mid-age, higher income, medium population
                    {'x': 45, 'y': 85000, 'r': 20},  # Older, highest income, smaller population
                    {'x': 55, 'y': 75000, 'r': 15}   # Senior, high income, smallest population
                ],
                'backgroundColor': 'rgba(255, 99, 132, 0.5)'
            },
            {
                'label': 'Suburban Demographics',
                'data': [
                    {'x': 30, 'y': 55000, 'r': 25},
                    {'x': 40, 'y': 75000, 'r': 30},
                    {'x': 50, 'y': 95000, 'r': 20},
                    {'x': 60, 'y': 85000, 'r': 15}
                ],
                'backgroundColor': 'rgba(54, 162, 235, 0.5)'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'bubble',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return [
                            `${context.dataset.label}`,
                            `Age: ${context.raw.x} years`,
                            `Income: $${context.raw.y.toLocaleString()}`,
                            `Population: ${(context.raw.r * 1000).toLocaleString()}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Average Age'
                },
                min: 20,
                max: 65
            },
            y: {
                title: {
                    display: true,
                    text: 'Average Income ($)'
                },
                ticks: {
                    callback: function(value) {
                        return '$' + value.toLocaleString();
                    }
                }
            }
        }
    }
};
```

### Database Model
```python
class DemographicData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region_type = db.Column(db.String(50))  # Urban/Suburban
    avg_age = db.Column(db.Float)
    avg_income = db.Column(db.Float)
    population = db.Column(db.Integer)
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_demographics(year):
        demographics = DemographicData.query\
            .filter_by(year=year)\
            .order_by(DemographicData.region_type)\
            .all()
            
        datasets = {}
        for demo in demographics:
            if demo.region_type not in datasets:
                datasets[demo.region_type] = {
                    'label': f'{demo.region_type} Demographics',
                    'data': [],
                    'backgroundColor': get_color_for_region(demo.region_type)
                }
            datasets[demo.region_type]['data'].append({
                'x': demo.avg_age,
                'y': demo.avg_income,
                'r': demo.population / 1000  # Scale population to reasonable bubble size
            })
            
        return {'datasets': list(datasets.values())}
```

## Example 2: Research Impact Analysis

This example demonstrates how to visualize research papers' impact using citations, publication year, and influence score.

### Flask Implementation
```python
@app.route('/api/research-impact')
def research_impact():
    data = {
        'datasets': [{
            'label': 'Research Papers',
            'data': [
                {'x': 2019, 'y': 150, 'r': 25},  # Year, citations, influence
                {'x': 2020, 'y': 89, 'r': 15},
                {'x': 2021, 'y': 45, 'r': 10},
                {'x': 2022, 'y': 25, 'r': 8},
                {'x': 2023, 'y': 10, 'r': 5}
            ],
            'backgroundColor': generate_color_gradient(5, 'rgba(75, 192, 192, 0.5)')
        }]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'bubble',
    data: chartData,
    options: {
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
            delay: function(context) {
                return context.dataIndex * 100;
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'year'
                },
                title: {
                    display: true,
                    text: 'Publication Year'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Citation Count'
                }
            }
        },
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return [
                            `Citations: ${context.raw.y}`,
                            `Impact Factor: ${context.raw.r}`,
                            `Year: ${context.raw.x}`
                        ];
                    }
                }
            }
        }
    }
};
```

## Example 3: Project Resource Allocation

This example shows how to visualize project resource allocation with budget, team size, and project duration.

### Flask Implementation
```python
@app.route('/api/project-resources')
def project_resources():
    data = {
        'datasets': [{
            'label': 'Projects',
            'data': [
                {'x': 100000, 'y': 8, 'r': 12},   # Budget, team size, duration
                {'x': 250000, 'y': 15, 'r': 18},
                {'x': 500000, 'y': 25, 'r': 24},
                {'x': 150000, 'y': 12, 'r': 15}
            ],
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

### Interactive Features Configuration
```javascript
const options = {
    responsive: true,
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    return [
                        `Budget: $${context.raw.x.toLocaleString()}`,
                        `Team Size: ${context.raw.y} members`,
                        `Duration: ${context.raw.r} months`
                    ];
                }
            }
        }
    },
    scales: {
        x: {
            type: 'logarithmic',
            title: {
                display: true,
                text: 'Budget ($)'
            },
            ticks: {
                callback: function(value) {
                    return '$' + value.toLocaleString();
                }
            }
        },
        y: {
            title: {
                display: true,
                text: 'Team Size'
            }
        }
    },
    onClick: (event, elements) => {
        if (elements.length > 0) {
            const element = elements[0];
            const datapoint = data.datasets[element.datasetIndex].data[element.index];
            // Handle click event
            console.log(`Project Details:`, datapoint);
            // Could trigger a modal with detailed project information
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic bubble charts:

```python
class ProjectMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(100))
    budget = db.Column(db.Float)
    team_size = db.Column(db.Integer)
    duration_months = db.Column(db.Integer)
    status = db.Column(db.String(20))

    @staticmethod
    def get_project_metrics(status='active'):
        projects = ProjectMetrics.query\
            .filter_by(status=status)\
            .order_by(ProjectMetrics.budget)\
            .all()
            
        return {
            'datasets': [{
                'label': 'Project Resources',
                'data': [{
                    'x': p.budget,
                    'y': p.team_size,
                    'r': p.duration_months
                } for p in projects],
                'backgroundColor': generate_colors(len(projects), 0.5)
            }]
        }
```

This documentation provides three distinct examples of bubble charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and interactive elements.
