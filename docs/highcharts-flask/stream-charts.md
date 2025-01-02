# Stream Charts with Highcharts and Flask

## Table of Contents
- [Stream Charts with Highcharts and Flask](#stream-charts-with-highcharts-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Basic Configuration](#basic-configuration)
  - [Common Options](#common-options)
  - [Database Integration Examples](#database-integration-examples)
    - [Example 1: Social Media Engagement Analysis](#example-1:-social-media-engagement-analysis)
    - [Example 2: Website Traffic Analysis](#example-2:-website-traffic-analysis)
    - [Example 3: Resource Usage Monitoring](#example-3:-resource-usage-monitoring)
  - [Flask Integration Tips](#flask-integration-tips)



## Overview
Stream charts, also known as streamgraphs, are a variation of stacked area charts that display the evolution of multiple variables over time. They're particularly useful for visualizing changing patterns, trends, and proportions across different categories over a continuous period.

## Basic Configuration
```python
@app.route('/stream-chart')
def stream_chart():
    chart_data = {
        'chart': {
            'type': 'streamgraph'
        },
        'title': {
            'text': 'Website Traffic Sources'
        },
        'xAxis': {
            'type': 'datetime',
            'labels': {
                'format': '{value:%Y-%m-%d}'
            }
        },
        'yAxis': {
            'visible': False
        },
        'plotOptions': {
            'streamgraph': {
                'fillOpacity': 0.8,
                'lineWidth': 1,
                'states': {
                    'hover': {
                        'lineWidth': 2
                    }
                }
            }
        },
        'series': [{
            'name': 'Direct',
            'data': [
                [1641024000000, 100],  # 2022-01-01
                [1643702400000, 150],  # 2022-02-01
                [1646092800000, 200]   # 2022-03-01
            ]
        }, {
            'name': 'Social Media',
            'data': [
                [1641024000000, 80],
                [1643702400000, 120],
                [1646092800000, 160]
            ]
        }, {
            'name': 'Search',
            'data': [
                [1641024000000, 200],
                [1643702400000, 250],
                [1646092800000, 300]
            ]
        }]
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Common Options
- **plotOptions.streamgraph**: Customize stream-specific options
  - `fillOpacity`: Set the opacity of the streams
  - `lineWidth`: Set the width of stream borders
  - `states.hover`: Configure hover effects
- **xAxis.type**: Usually 'datetime' for time-series data
- **colors**: Define custom color palette for streams
- **tooltip**: Configure hover information display

## Database Integration Examples

### Example 1: Social Media Engagement Analysis
```python
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///social_media.db'
db = SQLAlchemy(app)

class Engagement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(50))
    engagement_count = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime)

@app.route('/social-engagement')
def social_engagement():
    platforms = ['Facebook', 'Twitter', 'Instagram', 'LinkedIn']
    series_data = []
    
    for platform in platforms:
        engagements = Engagement.query.filter_by(
            platform=platform
        ).order_by(Engagement.timestamp).all()
        
        data = [[int(e.timestamp.timestamp() * 1000), e.engagement_count] 
                for e in engagements]
        
        series_data.append({
            'name': platform,
            'data': data
        })
    
    chart_data = {
        'chart': {'type': 'streamgraph'},
        'title': {'text': 'Social Media Engagement Over Time'},
        'xAxis': {
            'type': 'datetime',
            'labels': {'format': '{value:%Y-%m-%d}'}
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 2: Website Traffic Analysis
```python
@app.route('/traffic-sources')
def traffic_sources():
    sources = ['Direct', 'Organic Search', 'Paid Search', 
               'Social Media', 'Email', 'Referral']
    series_data = []
    
    for source in sources:
        traffic = TrafficData.query.filter_by(
            source=source
        ).order_by(TrafficData.date).all()
        
        data = [[int(t.date.timestamp() * 1000), t.visitors] 
                for t in traffic]
        
        series_data.append({
            'name': source,
            'data': data
        })
    
    chart_data = {
        'chart': {'type': 'streamgraph'},
        'title': {'text': 'Website Traffic Distribution'},
        'xAxis': {
            'type': 'datetime',
            'labels': {'format': '{value:%b %Y}'}
        },
        'plotOptions': {
            'streamgraph': {
                'fillOpacity': 0.8,
                'marker': {
                    'enabled': False
                }
            }
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

### Example 3: Resource Usage Monitoring
```python
@app.route('/resource-usage')
def resource_usage():
    resources = ['CPU', 'Memory', 'Disk IO', 'Network']
    end_time = datetime.now()
    start_time = end_time - timedelta(hours=24)
    series_data = []
    
    for resource in resources:
        usage = ResourceUsage.query.filter(
            ResourceUsage.resource_type == resource,
            ResourceUsage.timestamp.between(start_time, end_time)
        ).order_by(ResourceUsage.timestamp).all()
        
        data = [[int(u.timestamp.timestamp() * 1000), u.usage_percent] 
                for u in usage]
        
        series_data.append({
            'name': resource,
            'data': data
        })
    
    chart_data = {
        'chart': {'type': 'streamgraph'},
        'title': {'text': 'System Resource Usage'},
        'xAxis': {
            'type': 'datetime',
            'labels': {'format': '{value:%H:%M}'}
        },
        'yAxis': {
            'visible': False,
            'maxPadding': 0.2
        },
        'plotOptions': {
            'streamgraph': {
                'fillOpacity': 0.7,
                'lineWidth': 1,
                'states': {
                    'hover': {
                        'enabled': True,
                        'lineWidth': 2
                    }
                }
            }
        },
        'series': series_data
    }
    return render_template('chart.html', chart_data=chart_data)
```

## Flask Integration Tips
1. Use appropriate datetime handling for time-series data
2. Implement data aggregation for large datasets
3. Consider using caching for better performance
4. Handle timezone conversions properly
5. Validate and clean time-series data
6. Implement proper error handling for missing data points
