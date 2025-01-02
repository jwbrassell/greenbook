# Network Charts with Highcharts and Flask

## Table of Contents
- [Network Charts with Highcharts and Flask](#network-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
- [app.py](#apppy)
  - [Database Integration Example](#database-integration-example)
  - [Tips for Working with Network Charts](#tips-for-working-with-network-charts)



## Overview

Network charts (also known as network graphs or force-directed graphs) visualize relationships between entities represented as nodes and connections represented as links. They are particularly useful for showing social networks, organizational relationships, system architectures, or any data where connections between elements are important.

## Basic Configuration

Here's how to create a basic network chart with Highcharts and Flask:

```python
# app.py
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/network-chart')
def network_chart():
    return render_template('network-chart.html')

@app.route('/network-data')
def network_data():
    # Sample data: team collaboration network
    data = {
        'nodes': [
            {'id': '1', 'name': 'Project Manager', 'color': '#7cb5ec'},
            {'id': '2', 'name': 'Developer 1', 'color': '#434348'},
            {'id': '3', 'name': 'Developer 2', 'color': '#90ed7d'},
            {'id': '4', 'name': 'Designer', 'color': '#f7a35c'},
            {'id': '5', 'name': 'QA Engineer', 'color': '#8085e9'}
        ],
        'links': [
            {'from': '1', 'to': '2', 'weight': 5},
            {'from': '1', 'to': '3', 'weight': 5},
            {'from': '1', 'to': '4', 'weight': 3},
            {'from': '1', 'to': '5', 'weight': 3},
            {'from': '2', 'to': '3', 'weight': 4},
            {'from': '2', 'to': '4', 'weight': 2},
            {'from': '3', 'to': '4', 'weight': 2},
            {'from': '4', 'to': '5', 'weight': 1}
        ]
    }
    
    return jsonify(data)
```

```html
<!-- templates/network-chart.html -->
{% extends "base.html" %}

{% block content %}
<div id="network-container" style="min-width: 310px; height: 600px; margin: 0 auto"></div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/network-data')
        .then(response => response.json())
        .then(data => {
            Highcharts.chart('network-container', {
                chart: {
                    type: 'networkgraph',
                    marginTop: 80
                },
                title: {
                    text: 'Team Collaboration Network'
                },
                plotOptions: {
                    networkgraph: {
                        keys: ['from', 'to'],
                        layoutAlgorithm: {
                            enableSimulation: true,
                            friction: -0.9
                        }
                    }
                },
                series: [{
                    dataLabels: {
                        enabled: true,
                        linkFormat: '',
                        allowOverlap: false
                    },
                    data: data.links,
                    nodes: data.nodes,
                    marker: {
                        radius: 20
                    }
                }]
            });
        });
});
</script>
{% endblock %}
```

## Database Integration Example

Here's how to integrate network charts with a SQLAlchemy database:

```python
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///network.db'
db = SQLAlchemy(app)

class Node(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(20))
    category = db.Column(db.String(50))

class Connection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.String(50), db.ForeignKey('node.id'), nullable=False)
    target_id = db.Column(db.String(50), db.ForeignKey('node.id'), nullable=False)
    weight = db.Column(db.Float, default=1.0)
    type = db.Column(db.String(50))

@app.route('/network-data')
def get_network_data():
    nodes = Node.query.all()
    connections = Connection.query.all()
    
    data = {
        'nodes': [{
            'id': node.id,
            'name': node.name,
            'color': node.color,
            'category': node.category
        } for node in nodes],
        'links': [{
            'from': conn.source_id,
            'to': conn.target_id,
            'weight': conn.weight,
            'type': conn.type
        } for conn in connections]
    }
    
    return jsonify(data)
```

## Tips for Working with Network Charts

1. Optimize layout algorithm
2. Handle node sizing
3. Use meaningful colors
4. Implement proper tooltips
5. Consider interactivity
6. Manage data density
7. Add clear labels
8. Handle performance
