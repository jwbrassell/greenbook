# Timeline Charts with Chart.js and Flask

## Table of Contents
- [Timeline Charts with Chart.js and Flask](#timeline-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Project Gantt Chart](#example-1:-project-gantt-chart)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
    - [Database Model](#database-model)
  - [Example 2: Event Timeline](#example-2:-event-timeline)
    - [Flask Implementation](#flask-implementation)
    - [Interactive Features Configuration](#interactive-features-configuration)
  - [Example 3: Progress Timeline](#example-3:-progress-timeline)
    - [Flask Implementation](#flask-implementation)
    - [Progress Visualization Configuration](#progress-visualization-configuration)
  - [Working with Database Data](#working-with-database-data)



Timeline charts are specialized visualizations for displaying temporal data. While Chart.js doesn't have a specific timeline chart type, we can create effective timeline visualizations using bar or line charts with time-based configurations.

## Basic Implementation

### Flask Route
```python
@app.route('/timeline-chart')
def timeline_chart():
    return render_template('timeline_chart.html')

@app.route('/api/timeline-data')
def timeline_data():
    # Example: Project milestones data
    data = {
        'datasets': [{
            'label': 'Project Timeline',
            'data': [
                {
                    'x': '2023-01-15',
                    'y': 'Planning'
                },
                {
                    'x': '2023-03-01',
                    'y': 'Development'
                },
                {
                    'x': '2023-06-15',
                    'y': 'Testing'
                },
                {
                    'x': '2023-08-01',
                    'y': 'Deployment'
                }
            ],
            'backgroundColor': [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)',
                'rgba(75, 192, 192, 0.5)'
            ],
            'borderColor': [
                'rgb(255, 99, 132)',
                'rgb(54, 162, 235)',
                'rgb(255, 206, 86)',
                'rgb(75, 192, 192)'
            ],
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="timelineChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/timeline-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('timelineChart').getContext('2d');
            new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    indexAxis: 'y',  // Horizontal bars
                    plugins: {
                        title: {
                            display: true,
                            text: 'Project Timeline'
                        }
                    },
                    scales: {
                        x: {
                            type: 'time',
                            time: {
                                unit: 'month',
                                displayFormats: {
                                    month: 'MMM YYYY'
                                }
                            },
                            title: {
                                display: true,
                                text: 'Date'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Project Phase'
                            }
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Project Gantt Chart

This example shows how to create a Gantt-style chart for project management.

### Flask Implementation
```python
@app.route('/api/gantt-data')
def gantt_data():
    data = {
        'datasets': [
            {
                'label': 'Tasks',
                'data': [
                    {
                        'x': ['2023-01-01', '2023-02-15'],
                        'y': 'Research'
                    },
                    {
                        'x': ['2023-02-01', '2023-04-30'],
                        'y': 'Design'
                    },
                    {
                        'x': ['2023-04-15', '2023-08-30'],
                        'y': 'Development'
                    },
                    {
                        'x': ['2023-08-15', '2023-09-30'],
                        'y': 'Testing'
                    }
                ],
                'backgroundColor': [
                    'rgba(255, 99, 132, 0.5)',
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 206, 86, 0.5)',
                    'rgba(75, 192, 192, 0.5)'
                ],
                'borderColor': 'rgba(0, 0, 0, 0.1)',
                'borderWidth': 1,
                'borderSkipped': false,
                'barPercentage': 0.8
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        indexAxis: 'y',
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const dates = context.raw.x;
                        const start = new Date(dates[0]);
                        const end = new Date(dates[1]);
                        const duration = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
                        return `Duration: ${duration} days`;
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'month',
                    displayFormats: {
                        month: 'MMM YYYY'
                    }
                },
                min: '2023-01-01',
                max: '2023-12-31'
            },
            y: {
                reverse: true
            }
        },
        parsing: {
            xAxisKey: 'x.0',
            yAxisKey: 'y'
        }
    }
};
```

### Database Model
```python
class ProjectTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(100))
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20))
    
    @staticmethod
    def get_project_timeline():
        tasks = ProjectTask.query\
            .order_by(ProjectTask.start_date)\
            .all()
            
        return {
            'datasets': [{
                'label': 'Project Tasks',
                'data': [{
                    'x': [task.start_date.isoformat(), 
                         task.end_date.isoformat()],
                    'y': task.task_name
                } for task in tasks],
                'backgroundColor': generate_colors(len(tasks), 0.5),
                'borderWidth': 1
            }]
        }
```

## Example 2: Event Timeline

This example demonstrates how to create an interactive event timeline with tooltips.

### Flask Implementation
```python
@app.route('/api/event-timeline')
def event_timeline():
    data = {
        'datasets': [{
            'label': 'Events',
            'data': [
                {
                    'x': '2023-03-15T10:00:00',
                    'y': 'Meeting',
                    'description': 'Project kickoff meeting',
                    'duration': 60
                },
                {
                    'x': '2023-03-15T14:30:00',
                    'y': 'Review',
                    'description': 'Design review session',
                    'duration': 90
                },
                {
                    'x': '2023-03-16T09:00:00',
                    'y': 'Workshop',
                    'description': 'Team workshop',
                    'duration': 180
                }
            ],
            'backgroundColor': 'rgba(75, 192, 192, 0.5)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1,
            'pointStyle': 'circle',
            'pointRadius': 6,
            'pointHoverRadius': 8
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
                    const event = context.raw;
                    const time = new Date(event.x).toLocaleTimeString();
                    return [
                        `Time: ${time}`,
                        `Event: ${event.y}`,
                        `Duration: ${event.duration} minutes`,
                        `Details: ${event.description}`
                    ];
                }
            }
        }
    },
    scales: {
        x: {
            type: 'time',
            time: {
                unit: 'hour',
                displayFormats: {
                    hour: 'HH:mm'
                }
            },
            title: {
                display: true,
                text: 'Time'
            }
        },
        y: {
            title: {
                display: true,
                text: 'Event Type'
            }
        }
    },
    onClick: (event, elements) => {
        if (elements.length > 0) {
            const element = elements[0];
            const eventData = data.datasets[element.datasetIndex].data[element.index];
            showEventDetails(eventData);
        }
    }
};

function showEventDetails(event) {
    // Custom modal or popup implementation
    console.log('Event Details:', event);
}
```

## Example 3: Progress Timeline

This example shows how to create a timeline that displays progress and completion status.

### Flask Implementation
```python
@app.route('/api/progress-timeline')
def progress_timeline():
    data = {
        'datasets': [{
            'label': 'Project Progress',
            'data': [
                {
                    'x': '2023-Q1',
                    'y': 'Phase 1',
                    'progress': 100,
                    'status': 'completed'
                },
                {
                    'x': '2023-Q2',
                    'y': 'Phase 2',
                    'progress': 75,
                    'status': 'in-progress'
                },
                {
                    'x': '2023-Q3',
                    'y': 'Phase 3',
                    'progress': 25,
                    'status': 'in-progress'
                },
                {
                    'x': '2023-Q4',
                    'y': 'Phase 4',
                    'progress': 0,
                    'status': 'pending'
                }
            ],
            'backgroundColor': function(context) {
                const progress = context.raw.progress;
                return progress === 100 ? 'rgba(75, 192, 192, 0.5)' :
                       progress > 0 ? 'rgba(255, 206, 86, 0.5)' :
                       'rgba(255, 99, 132, 0.5)';
            }
        }]
    }
    return jsonify(data)
```

### Progress Visualization Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        indexAxis: 'y',
        responsive: true,
        plugins: {
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const item = context.raw;
                        return [
                            `Progress: ${item.progress}%`,
                            `Status: ${item.status}`
                        ];
                    }
                }
            }
        },
        scales: {
            x: {
                type: 'category',
                title: {
                    display: true,
                    text: 'Quarter'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Project Phase'
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic timeline charts:

```python
class ProjectMilestone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.String(100))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    progress = db.Column(db.Float)
    status = db.Column(db.String(20))
    description = db.Column(db.Text)

    @staticmethod
    def get_project_progress():
        milestones = ProjectMilestone.query\
            .order_by(ProjectMilestone.start_date)\
            .all()
            
        return {
            'datasets': [{
                'label': 'Project Progress',
                'data': [{
                    'x': milestone.start_date.strftime('%Y-%m'),
                    'y': milestone.phase,
                    'progress': milestone.progress,
                    'status': milestone.status,
                    'description': milestone.description,
                    'end_date': milestone.end_date.strftime('%Y-%m-%d')
                } for milestone in milestones],
                'backgroundColor': generate_status_colors(),
                'borderWidth': 1
            }]
        }

def generate_status_colors():
    return {
        'completed': 'rgba(75, 192, 192, 0.5)',
        'in-progress': 'rgba(255, 206, 86, 0.5)',
        'pending': 'rgba(255, 99, 132, 0.5)'
    }
```

This documentation provides three distinct examples of timeline charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like interactive timelines and progress tracking.
