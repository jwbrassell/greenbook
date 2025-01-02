# Organization Charts with Highcharts and Flask

## Table of Contents
- [Organization Charts with Highcharts and Flask](#organization-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Common Options](#common-options)
  - [Example 1: Department Structure](#example-1:-department-structure)
  - [Example 2: Company Divisions](#example-2:-company-divisions)
  - [Example 3: Project Teams](#example-3:-project-teams)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Organization Charts](#tips-for-working-with-organization-charts)



## Overview

Organization charts (also known as org charts) are specialized hierarchical diagrams designed to show the structure of organizations and relationships between different positions or departments. They are particularly useful for visualizing reporting relationships, team structures, and company hierarchies.

## Basic Configuration

Here's how to create a basic organization chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/org-chart')
def org_chart():
    return render_template('org-chart.html')

@app.route('/org-data')
def org_data():
    # Sample organization structure
    data = [{
        'id': 'CEO',
        'title': 'Chief Executive Officer',
        'name': 'John Smith',
        'color': '#007ad0'
    }, {
        'id': 'CTO',
        'title': 'Chief Technology Officer',
        'name': 'Sarah Johnson',
        'reportsTo': 'CEO',
        'color': '#00a28a'
    }, {
        'id': 'CFO',
        'title': 'Chief Financial Officer',
        'name': 'Michael Brown',
        'reportsTo': 'CEO',
        'color': '#00a28a'
    }, {
        'id': 'COO',
        'title': 'Chief Operating Officer',
        'name': 'Emily Davis',
        'reportsTo': 'CEO',
        'color': '#00a28a'
    }]
    
    return jsonify(data)
```

```html
<!-- templates/org-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="org-container" style="min-width: 310px; height: 600px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/org-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('org-container', {
                chart: {
                    height: '100%',
                    inverted: true
                },
                title: {
                    text: 'Organization Chart'
                },
                series: [{
                    type: 'organization',
                    name: 'Organization',
                    keys: ['from', 'to'],
                    data: data.filter(item => item.reportsTo)
                        .map(item => [item.reportsTo, item.id]),
                    levels: [{
                        level: 0,
                        color: '#007ad0',
                        dataLabels: {
                            color: '#FFFFFF'
                        },
                        height: 25
                    }, {
                        level: 1,
                        color: '#00a28a',
                        dataLabels: {
                            color: '#FFFFFF'
                        },
                        height: 25
                    }],
                    nodes: data.map(item => ({
                        id: item.id,
                        title: item.title,
                        name: item.name,
                        color: item.color
                    })),
                    colorByPoint: false,
                    color: '#007ad0',
                    dataLabels: {
                        nodeFormatter: function() {
                            return this.point.name + '<br/>' + this.point.title;
                        }
                    },
                    borderColor: '#666',
                    nodeWidth: 65
                }],
                tooltip: {
                    outside: true
                },
                exporting: {
                    allowHTML: true,
                    sourceWidth: 800,
                    sourceHeight: 600
                }
            });
        });
});
</script>
{% endblock %}
```

## Common Options

Organization charts in Highcharts offer various customization options:

```javascript
Highcharts.chart('container', {
    series: [{
        type: 'organization',
        levels: [{
            level: 0,                 // Hierarchy level
            color: '#007ad0',         // Node color
            dataLabels: {
                color: '#FFFFFF'      // Label color
            },
            height: 25               // Level height
        }],
        nodes: [{
            id: 'id',                // Unique identifier
            title: 'Title',          // Position title
            name: 'Name',            // Person name
            color: '#007ad0',        // Individual node color
            column: 2,               // Force column position
            offset: '50%'           // Vertical offset
        }],
        dataLabels: {
            nodeFormatter: function() {
                return customFormat;  // Custom label format
            }
        },
        nodeWidth: 65,              // Node width
        nodePadding: 10,            // Space between nodes
        borderColor: '#666666',      // Node border color
        borderRadius: 3,            // Node corner radius
        linkColor: '#666666',       // Connection line color
        linkLineWidth: 1           // Connection line width
    }]
});
```

## Example 1: Department Structure

This example shows a detailed department structure with multiple levels:

```python
@app.route('/department-structure')
def department_structure():
    data = [{
        'id': 'head',
        'title': 'Department Head',
        'name': 'Alice White',
        'level': 0
    }, {
        'id': 'team1',
        'title': 'Team Lead',
        'name': 'Bob Wilson',
        'reportsTo': 'head',
        'level': 1
    }, {
        'id': 'team2',
        'title': 'Team Lead',
        'name': 'Carol Martin',
        'reportsTo': 'head',
        'level': 1
    }, {
        'id': 'dev1',
        'title': 'Developer',
        'name': 'David Lee',
        'reportsTo': 'team1',
        'level': 2
    }, {
        'id': 'dev2',
        'title': 'Developer',
        'name': 'Eva Chen',
        'reportsTo': 'team1',
        'level': 2
    }, {
        'id': 'qa1',
        'title': 'QA Engineer',
        'name': 'Frank Lopez',
        'reportsTo': 'team2',
        'level': 2
    }, {
        'id': 'qa2',
        'title': 'QA Engineer',
        'name': 'Grace Kim',
        'reportsTo': 'team2',
        'level': 2
    }]
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="department-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/department-structure')
        .then(response => response.json())
        .then(data => {
            const levelColors = ['#007ad0', '#00a28a', '#ffa000'];
            
            Highcharts.chart('department-chart', {
                chart: {
                    height: '100%',
                    inverted: true
                },
                title: {
                    text: 'Department Structure'
                },
                series: [{
                    type: 'organization',
                    name: 'Department',
                    keys: ['from', 'to'],
                    data: data.filter(item => item.reportsTo)
                        .map(item => [item.reportsTo, item.id]),
                    levels: levelColors.map((color, index) => ({
                        level: index,
                        color: color,
                        dataLabels: {
                            color: '#FFFFFF'
                        },
                        height: 25
                    })),
                    nodes: data.map(item => ({
                        id: item.id,
                        title: item.title,
                        name: item.name,
                        color: levelColors[item.level]
                    })),
                    colorByPoint: false,
                    dataLabels: {
                        nodeFormatter: function() {
                            return '<b>' + this.point.name + '</b><br/>' +
                                   this.point.title;
                        }
                    },
                    borderColor: '#666',
                    nodeWidth: 65,
                    nodePadding: 10
                }],
                tooltip: {
                    outside: true,
                    formatter: function() {
                        return '<b>' + this.point.name + '</b><br/>' +
                               this.point.title;
                    }
                }
            });
        });
});
</script>
{% endblock %}
```

## Example 2: Company Divisions

This example shows company divisions with employee counts:

```python
@app.route('/company-divisions')
def company_divisions():
    data = [{
        'id': 'company',
        'title': 'CEO',
        'name': 'Global Operations',
        'employees': 1000,
        'level': 0
    }]
    
    divisions = {
        'tech': {
            'name': 'Technology',
            'head': 'CTO',
            'employees': 400,
            'departments': {
                'dev': {'name': 'Development', 'employees': 200},
                'infra': {'name': 'Infrastructure', 'employees': 100},
                'qa': {'name': 'Quality Assurance', 'employees': 100}
            }
        },
        'sales': {
            'name': 'Sales',
            'head': 'Sales Director',
            'employees': 300,
            'departments': {
                'direct': {'name': 'Direct Sales', 'employees': 150},
                'channel': {'name': 'Channel Sales', 'employees': 150}
            }
        },
        'ops': {
            'name': 'Operations',
            'head': 'COO',
            'employees': 300,
            'departments': {
                'support': {'name': 'Support', 'employees': 150},
                'hr': {'name': 'Human Resources', 'employees': 50},
                'admin': {'name': 'Administration', 'employees': 100}
            }
        }
    }
    
    # Build hierarchical data
    for div_id, div in divisions.items():
        data.append({
            'id': div_id,
            'title': div['head'],
            'name': div['name'],
            'employees': div['employees'],
            'reportsTo': 'company',
            'level': 1
        })
        
        for dept_id, dept in div['departments'].items():
            data.append({
                'id': f"{div_id}_{dept_id}",
                'title': 'Manager',
                'name': dept['name'],
                'employees': dept['employees'],
                'reportsTo': div_id,
                'level': 2
            })
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="divisions-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/company-divisions')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('divisions-chart', {
                chart: {
                    height: '100%',
                    inverted: true
                },
                title: {
                    text: 'Company Divisions'
                },
                series: [{
                    type: 'organization',
                    name: 'Company',
                    keys: ['from', 'to'],
                    data: data.filter(item => item.reportsTo)
                        .map(item => [item.reportsTo, item.id]),
                    levels: [{
                        level: 0,
                        color: '#007ad0'
                    }, {
                        level: 1,
                        color: '#00a28a'
                    }, {
                        level: 2,
                        color: '#ffa000'
                    }],
                    nodes: data.map(item => ({
                        id: item.id,
                        title: item.title,
                        name: item.name,
                        description: item.employees + ' employees',
                        column: item.level
                    })),
                    colorByPoint: false,
                    dataLabels: {
                        nodeFormatter: function() {
                            return '<b>' + this.point.name + '</b><br/>' +
                                   this.point.title + '<br/>' +
                                   this.point.description;
                        }
                    },
                    borderColor: '#666',
                    nodeWidth: 65,
                    nodePadding: 10
                }]
            });
        });
});
</script>
{% endblock %}
```

## Example 3: Project Teams

This example shows project team structures with roles and responsibilities:

```python
@app.route('/project-teams')
def project_teams():
    data = [{
        'id': 'pm',
        'title': 'Project Manager',
        'name': 'Project Alpha',
        'description': 'Overall project management',
        'level': 0
    }]
    
    teams = {
        'dev': {
            'name': 'Development',
            'lead': 'Tech Lead',
            'description': 'Core development',
            'members': [
                {'role': 'Frontend Dev', 'focus': 'UI/UX'},
                {'role': 'Backend Dev', 'focus': 'API'},
                {'role': 'DevOps', 'focus': 'Infrastructure'}
            ]
        },
        'design': {
            'name': 'Design',
            'lead': 'Design Lead',
            'description': 'UX/UI design',
            'members': [
                {'role': 'UI Designer', 'focus': 'Interface'},
                {'role': 'UX Designer', 'focus': 'User Experience'}
            ]
        },
        'qa': {
            'name': 'Quality Assurance',
            'lead': 'QA Lead',
            'description': 'Testing and quality',
            'members': [
                {'role': 'Test Engineer', 'focus': 'Automation'},
                {'role': 'QA Analyst', 'focus': 'Manual Testing'}
            ]
        }
    }
    
    # Build team structure
    for team_id, team in teams.items():
        data.append({
            'id': team_id,
            'title': team['lead'],
            'name': team['name'],
            'description': team['description'],
            'reportsTo': 'pm',
            'level': 1
        })
        
        for i, member in enumerate(team['members']):
            data.append({
                'id': f"{team_id}_m{i}",
                'title': member['role'],
                'name': member['focus'],
                'description': '',
                'reportsTo': team_id,
                'level': 2
            })
    
    return jsonify(data)
```

```html
{% extends "base.html" %}

{% block content %}
<div id="teams-chart"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/project-teams')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('teams-chart', {
                chart: {
                    height: '100%',
                    inverted: true
                },
                title: {
                    text: 'Project Team Structure'
                },
                series: [{
                    type: 'organization',
                    name: 'Project',
                    keys: ['from', 'to'],
                    data: data.filter(item => item.reportsTo)
                        .map(item => [item.reportsTo, item.id]),
                    levels: [{
                        level: 0,
                        color: '#007ad0'
                    }, {
                        level: 1,
                        color: '#00a28a'
                    }, {
                        level: 2,
                        color: '#ffa000'
                    }],
                    nodes: data.map(item => ({
                        id: item.id,
                        title: item.title,
                        name: item.name,
                        description: item.description,
                        column: item.level
                    })),
                    colorByPoint: false,
                    dataLabels: {
                        nodeFormatter: function() {
                            let label = '<b>' + this.point.title + '</b><br/>' +
                                      this.point.name;
                            if (this.point.description) {
                                label += '<br/><i>' + this.point.description + '</i>';
                            }
                            return label;
                        }
                    },
                    borderColor: '#666',
                    nodeWidth: 65,
                    nodePadding: 10
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate organization charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///organization.db'
db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    reports_to_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    level = db.Column(db.Integer, nullable=False)
    
    reports_to = db.relationship('Employee', remote_side=[id],
                               backref='direct_reports')

@app.route('/org-structure')
def get_org_structure():
    employees = Employee.query.all()
    
    data = [{
        'id': str(emp.id),
        'name': emp.name,
        'title': emp.title,
        'reportsTo': str(emp.reports_to_id) if emp.reports_to_id else None,
        'level': emp.level
    } for emp in employees]
    
    return jsonify(data)
```

## Tips for Working with Organization Charts

1. Plan the hierarchy carefully
2. Use consistent level styling
3. Consider node spacing
4. Implement proper data labels
5. Use meaningful colors
6. Handle large organizations
7. Consider export options
8. Optimize layout direction
