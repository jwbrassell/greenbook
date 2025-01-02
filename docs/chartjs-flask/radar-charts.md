# Radar Charts with Chart.js and Flask

## Table of Contents
- [Radar Charts with Chart.js and Flask](#radar-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template](#html-template)
  - [Example 1: Team Performance Comparison](#example-1:-team-performance-comparison)
    - [Flask Implementation](#flask-implementation)
    - [Database Model](#database-model)
  - [Example 2: Product Feature Analysis](#example-2:-product-feature-analysis)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Configuration](#advanced-configuration)
  - [Example 3: Student Performance Tracking](#example-3:-student-performance-tracking)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Animation Configuration](#advanced-animation-configuration)
  - [Working with Database Data](#working-with-database-data)



Radar charts (also known as spider or web charts) are perfect for displaying multivariate data in a two-dimensional chart. They're excellent for comparing multiple variables and identifying patterns or outliers.

## Basic Implementation

### Flask Route
```python
@app.route('/radar-chart')
def radar_chart():
    return render_template('radar_chart.html')

@app.route('/api/radar-data')
def radar_data():
    # Example: Skills assessment data
    data = {
        'labels': ['Python', 'JavaScript', 'SQL', 'DevOps', 'Testing', 'Documentation'],
        'datasets': [{
            'label': 'Developer Skills',
            'data': [90, 85, 75, 80, 70, 85],
            'fill': True,
            'backgroundColor': 'rgba(54, 162, 235, 0.2)',
            'borderColor': 'rgb(54, 162, 235)',
            'pointBackgroundColor': 'rgb(54, 162, 235)',
            'pointBorderColor': '#fff',
            'pointHoverBackgroundColor': '#fff',
            'pointHoverBorderColor': 'rgb(54, 162, 235)'
        }]
    }
    return jsonify(data)
```

### HTML Template
```html
<div style="width: 800px;">
    <canvas id="radarChart"></canvas>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/radar-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('radarChart').getContext('2d');
            new Chart(ctx, {
                type: 'radar',
                data: data,
                options: {
                    responsive: true,
                    elements: {
                        line: {
                            borderWidth: 3
                        }
                    },
                    plugins: {
                        title: {
                            display: true,
                            text: 'Developer Skills Assessment'
                        }
                    }
                }
            });
        });
});
</script>
```

## Example 1: Team Performance Comparison

This example compares performance metrics across multiple teams.

### Flask Implementation
```python
@app.route('/api/team-performance')
def team_performance():
    data = {
        'labels': ['Communication', 'Technical Skills', 'Productivity', 
                  'Innovation', 'Collaboration', 'Leadership'],
        'datasets': [
            {
                'label': 'Team A',
                'data': [95, 89, 90, 85, 88, 92],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgb(255, 99, 132)',
                'pointBackgroundColor': 'rgb(255, 99, 132)'
            },
            {
                'label': 'Team B',
                'data': [88, 92, 85, 90, 85, 88],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgb(54, 162, 235)',
                'pointBackgroundColor': 'rgb(54, 162, 235)'
            }
        ]
    }
    return jsonify(data)
```

### Database Model
```python
class TeamMetrics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(50))
    metric_name = db.Column(db.String(50))
    score = db.Column(db.Float)
    quarter = db.Column(db.String(2))
    year = db.Column(db.Integer)
    
    @staticmethod
    def get_team_comparison(year, quarter):
        metrics = ['Communication', 'Technical Skills', 'Productivity',
                  'Innovation', 'Collaboration', 'Leadership']
        teams = TeamMetrics.query\
            .filter_by(year=year, quarter=quarter)\
            .order_by(TeamMetrics.team_name)\
            .all()
        
        # Group by team
        team_data = {}
        for team in teams:
            if team.team_name not in team_data:
                team_data[team.team_name] = []
            team_data[team.team_name].append(team.score)
            
        return {
            'labels': metrics,
            'datasets': [
                {
                    'label': team_name,
                    'data': scores,
                    'backgroundColor': get_team_color(team_name, 0.2),
                    'borderColor': get_team_color(team_name, 1)
                }
                for team_name, scores in team_data.items()
            ]
        }
```

## Example 2: Product Feature Analysis

This example demonstrates how to analyze product features across different dimensions.

### Flask Implementation
```python
@app.route('/api/product-analysis')
def product_analysis():
    data = {
        'labels': ['Usability', 'Performance', 'Reliability', 
                  'Security', 'Maintainability', 'Cost-Efficiency'],
        'datasets': [
            {
                'label': 'Current Version',
                'data': [85, 80, 90, 95, 75, 85],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgb(75, 192, 192)'
            },
            {
                'label': 'Target Metrics',
                'data': [90, 85, 95, 95, 80, 90],
                'backgroundColor': 'rgba(255, 205, 86, 0.2)',
                'borderColor': 'rgb(255, 205, 86)',
                'borderDash': [5, 5]  # Creates dashed line for target
            }
        ]
    }
    return jsonify(data)
```

### Advanced Configuration
```javascript
const options = {
    responsive: true,
    scales: {
        r: {
            angleLines: {
                display: true
            },
            suggestedMin: 50,
            suggestedMax: 100,
            ticks: {
                stepSize: 10,
                callback: function(value) {
                    return value + '%';
                }
            }
        }
    },
    plugins: {
        tooltip: {
            callbacks: {
                label: function(context) {
                    return context.dataset.label + ': ' + context.parsed.r + '%';
                }
            }
        },
        legend: {
            position: 'top',
        }
    }
};
```

## Example 3: Student Performance Tracking

This example shows how to track and compare student performance across subjects over time.

### Flask Implementation
```python
@app.route('/api/student-performance')
def student_performance():
    data = {
        'labels': ['Mathematics', 'Science', 'Language', 
                  'History', 'Arts', 'Physical Education'],
        'datasets': [
            {
                'label': 'First Semester',
                'data': [75, 82, 90, 85, 88, 92],
                'backgroundColor': 'rgba(153, 102, 255, 0.2)',
                'borderColor': 'rgb(153, 102, 255)'
            },
            {
                'label': 'Second Semester',
                'data': [85, 88, 92, 88, 90, 95],
                'backgroundColor': 'rgba(255, 159, 64, 0.2)',
                'borderColor': 'rgb(255, 159, 64)'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Animation Configuration
```javascript
const config = {
    type: 'radar',
    data: chartData,
    options: {
        animation: {
            duration: 2000,
            easing: 'easeInOutQuart',
            delay: function(context) {
                return context.dataIndex * 100 + context.datasetIndex * 500;
            }
        },
        scales: {
            r: {
                pointLabels: {
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                animation: {
                    numbers: {
                        type: 'number',
                        properties: ['r', 'x', 'y']
                    }
                }
            }
        },
        transitions: {
            show: {
                animations: {
                    r: {
                        duration: 1000,
                        easing: 'easeInOutQuad',
                        from: 0
                    }
                }
            }
        }
    }
};
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for dynamic radar charts:

```python
class StudentPerformance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(50))
    subject = db.Column(db.String(50))
    score = db.Column(db.Float)
    semester = db.Column(db.String(20))
    year = db.Column(db.Integer)

    @staticmethod
    def get_student_progress(student_id, year):
        semesters = ['First Semester', 'Second Semester']
        subjects = ['Mathematics', 'Science', 'Language', 
                   'History', 'Arts', 'Physical Education']
        
        datasets = []
        for semester in semesters:
            scores = StudentPerformance.query\
                .filter_by(
                    student_id=student_id,
                    year=year,
                    semester=semester
                )\
                .order_by(StudentPerformance.subject)\
                .all()
                
            datasets.append({
                'label': semester,
                'data': [s.score for s in scores],
                'backgroundColor': get_semester_color(semester, 0.2),
                'borderColor': get_semester_color(semester, 1)
            })
            
        return {
            'labels': subjects,
            'datasets': datasets
        }
```

This documentation provides three distinct examples of radar charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic implementation to advanced features like animations and comparative analysis.
