# Chart.js Events and Interactions with Flask

## Table of Contents
- [Chart.js Events and Interactions with Flask](#chartjs-events-and-interactions-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Event Implementation](#basic-event-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template with Events](#html-template-with-events)
  - [Example 1: Advanced Selection and Filtering](#example-1:-advanced-selection-and-filtering)
    - [Flask Implementation](#flask-implementation)
    - [Selection Configuration](#selection-configuration)
  - [Example 2: Drill-Down Interactions](#example-2:-drill-down-interactions)
    - [Flask Implementation](#flask-implementation)
    - [Drill-Down Configuration](#drill-down-configuration)
  - [Example 3: Custom Interaction Modes](#example-3:-custom-interaction-modes)
    - [Flask Implementation](#flask-implementation)
    - [Custom Interaction Configuration](#custom-interaction-configuration)
  - [Working with Database Data](#working-with-database-data)



Chart.js provides various events and interaction capabilities that allow users to interact with charts in meaningful ways. This guide demonstrates how to implement event handling and custom interactions when using Chart.js with Flask.

## Basic Event Implementation

### Flask Route
```python
@app.route('/interactive-chart')
def interactive_chart():
    return render_template('interactive_chart.html')

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

@app.route('/api/data-point/<int:index>')
def get_data_details(index):
    # Example: Return detailed information for a specific data point
    details = {
        'month': ['January', 'February', 'March', 'April', 'May', 'June'][index],
        'value': [65, 59, 80, 81, 56, 55][index],
        'transactions': [120, 110, 150, 142, 98, 95][index],
        'average': [542, 536, 533, 570, 571, 579][index]
    }
    return jsonify(details)
```

### HTML Template with Events
```html
<div class="chart-container" style="width: 800px;">
    <canvas id="interactiveChart"></canvas>
    <div id="tooltip" style="display: none; position: absolute; background: white; padding: 10px; border: 1px solid #ddd; border-radius: 4px;"></div>
    <div id="details" style="margin-top: 20px;"></div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('interactiveChart').getContext('2d');
            const chart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    onHover: (event, elements) => {
                        const tooltip = document.getElementById('tooltip');
                        if (elements.length > 0) {
                            const element = elements[0];
                            const value = data.datasets[0].data[element.index];
                            const label = data.labels[element.index];
                            
                            tooltip.style.display = 'block';
                            tooltip.style.left = event.x + 10 + 'px';
                            tooltip.style.top = event.y + 10 + 'px';
                            tooltip.innerHTML = `${label}: ${value}`;
                        } else {
                            tooltip.style.display = 'none';
                        }
                    },
                    onClick: (event, elements) => {
                        if (elements.length > 0) {
                            const element = elements[0];
                            showDetails(element.index);
                        }
                    }
                }
            });
        });
});

function showDetails(index) {
    fetch(`/api/data-point/${index}`)
        .then(response => response.json())
        .then(details => {
            document.getElementById('details').innerHTML = `
                <h3>${details.month} Details</h3>
                <p>Value: $${details.value}</p>
                <p>Transactions: ${details.transactions}</p>
                <p>Average Transaction: $${details.average}</p>
            `;
        });
}
</script>
```

## Example 1: Advanced Selection and Filtering

This example demonstrates how to implement multi-select and filtering capabilities.

### Flask Implementation
```python
@app.route('/api/filtered-data')
def filtered_data():
    category = request.args.get('category', 'all')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    # Example: Filter data based on parameters
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Category A',
            'data': [65, 59, 80, 81, 56, 55]
        }, {
            'label': 'Category B',
            'data': [28, 48, 40, 19, 86, 27]
        }]
    }
    return jsonify(data)
```

### Selection Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                onClick: function(e, legendItem, legend) {
                    const index = legendItem.datasetIndex;
                    const ci = legend.chart;
                    
                    if (e.shiftKey) {
                        // Multi-select with shift key
                        ci.setDatasetVisibility(
                            index,
                            !ci.isDatasetVisible(index)
                        );
                    } else {
                        // Single select without shift key
                        ci.data.datasets.forEach((dataset, i) => {
                            ci.setDatasetVisibility(
                                i,
                                i === index
                            );
                        });
                    }
                    ci.update();
                }
            }
        },
        onClick: function(event, elements) {
            if (elements.length > 0) {
                const element = elements[0];
                selectDataPoint(element);
            }
        }
    }
};

function selectDataPoint(element) {
    const selectedPoints = chart.getSelectedPoints() || [];
    const index = selectedPoints.findIndex(p => 
        p.datasetIndex === element.datasetIndex && 
        p.index === element.index
    );
    
    if (index === -1) {
        selectedPoints.push(element);
    } else {
        selectedPoints.splice(index, 1);
    }
    
    chart.setSelectedPoints(selectedPoints);
    updateSelectionUI(selectedPoints);
}

function updateSelectionUI(selectedPoints) {
    const summary = selectedPoints.reduce((acc, point) => {
        const value = chart.data.datasets[point.datasetIndex].data[point.index];
        acc.total += value;
        acc.count++;
        return acc;
    }, { total: 0, count: 0 });
    
    document.getElementById('selectionSummary').innerHTML = `
        Selected Points: ${summary.count}
        Total Value: ${summary.total}
        Average: ${(summary.total / summary.count).toFixed(2)}
    `;
}
```

## Example 2: Drill-Down Interactions

This example shows how to implement drill-down functionality for detailed data exploration.

### Flask Implementation
```python
@app.route('/api/drill-down/<category>/<period>')
def drill_down_data(category, period):
    # Example: Return detailed data for a specific category and period
    if period == 'monthly':
        data = {
            'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
            'datasets': [{
                'label': f'{category} - Weekly Breakdown',
                'data': generate_weekly_data()
            }]
        }
    elif period == 'weekly':
        data = {
            'labels': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'datasets': [{
                'label': f'{category} - Daily Breakdown',
                'data': generate_daily_data()
            }]
        }
    return jsonify(data)
```

### Drill-Down Configuration
```javascript
const drillDownConfig = {
    type: 'bar',
    data: initialData,
    options: {
        responsive: true,
        onClick: async function(event, elements) {
            if (elements.length > 0) {
                const element = elements[0];
                const category = this.data.datasets[element.datasetIndex].label;
                const period = this.drillDownLevel || 'monthly';
                
                // Get detailed data
                const response = await fetch(
                    `/api/drill-down/${category}/${period}`
                );
                const detailedData = await response.json();
                
                // Update chart with new data
                this.data.labels = detailedData.labels;
                this.data.datasets = detailedData.datasets;
                this.drillDownLevel = period === 'monthly' ? 'weekly' : 'daily';
                this.update();
                
                // Add breadcrumb
                updateBreadcrumb(category, period);
            }
        }
    }
};

function updateBreadcrumb(category, period) {
    const breadcrumb = document.getElementById('breadcrumb');
    breadcrumb.innerHTML += ` > ${category} (${period})`;
}

function resetDrillDown() {
    chart.data = initialData;
    chart.drillDownLevel = 'monthly';
    chart.update();
    document.getElementById('breadcrumb').innerHTML = 'Overview';
}
```

## Example 3: Custom Interaction Modes

This example demonstrates how to implement custom interaction modes for different user behaviors.

### Flask Implementation
```python
@app.route('/api/interaction-data')
def interaction_data():
    data = {
        'labels': ['A', 'B', 'C', 'D', 'E'],
        'datasets': [{
            'label': 'Dataset 1',
            'data': [65, 59, 80, 81, 56]
        }],
        'annotations': [
            {'point': 2, 'text': 'Peak'},
            {'point': 4, 'text': 'Low'}
        ]
    }
    return jsonify(data)
```

### Custom Interaction Configuration
```javascript
const interactionModes = {
    select: {
        id: 'select',
        beforeEvent: function(chart, event) {
            // Handle selection logic
            if (event.type === 'click') {
                handleSelection(chart, event);
                return false;  // Prevent default handling
            }
            return true;
        }
    },
    annotate: {
        id: 'annotate',
        beforeEvent: function(chart, event) {
            // Handle annotation logic
            if (event.type === 'click') {
                handleAnnotation(chart, event);
                return false;
            }
            return true;
        }
    },
    zoom: {
        id: 'zoom',
        beforeEvent: function(chart, event) {
            // Handle zoom logic
            if (event.type === 'wheel') {
                handleZoom(chart, event);
                return false;
            }
            return true;
        }
    }
};

function setInteractionMode(mode) {
    chart.options.plugins.interaction = interactionModes[mode];
    chart.update();
}

function handleSelection(chart, event) {
    const elements = chart.getElementsAtEventForMode(
        event,
        'nearest',
        { intersect: true },
        false
    );
    
    if (elements.length > 0) {
        const element = elements[0];
        element.selected = !element.selected;
        
        // Update visual state
        chart.data.datasets[element.datasetIndex].backgroundColor = 
            chart.data.datasets[element.datasetIndex].data.map((_, i) => 
                i === element.index && element.selected ?
                'rgba(255, 99, 132, 0.2)' :
                'rgba(75, 192, 192, 0.2)'
            );
        
        chart.update();
    }
}

function handleAnnotation(chart, event) {
    const elements = chart.getElementsAtEventForMode(
        event,
        'nearest',
        { intersect: true },
        false
    );
    
    if (elements.length > 0) {
        const element = elements[0];
        const text = prompt('Enter annotation text:');
        
        if (text) {
            chart.data.annotations = chart.data.annotations || [];
            chart.data.annotations.push({
                point: element.index,
                text: text
            });
            
            chart.update();
        }
    }
}

function handleZoom(chart, event) {
    const delta = event.deltaY;
    const currentMin = chart.scales.x.min;
    const currentMax = chart.scales.x.max;
    const range = currentMax - currentMin;
    
    // Zoom in/out by 10%
    const zoomFactor = delta > 0 ? 1.1 : 0.9;
    const newRange = range * zoomFactor;
    
    chart.options.scales.x.min = currentMin - (newRange - range) / 2;
    chart.options.scales.x.max = currentMax + (newRange - range) / 2;
    
    chart.update();
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for interactive data exploration:

```python
class ChartInteraction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chart_id = db.Column(db.String(50))
    interaction_type = db.Column(db.String(50))
    data_point = db.Column(db.Integer)
    value = db.Column(db.Float)
    annotation = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    @staticmethod
    def log_interaction(chart_id, interaction_type, data_point, value, annotation=None):
        interaction = ChartInteraction(
            chart_id=chart_id,
            interaction_type=interaction_type,
            data_point=data_point,
            value=value,
            annotation=annotation
        )
        db.session.add(interaction)
        db.session.commit()
        return interaction

@app.route('/api/log-interaction', methods=['POST'])
def log_interaction():
    data = request.json
    interaction = ChartInteraction.log_interaction(
        chart_id=data['chartId'],
        interaction_type=data['type'],
        data_point=data['dataPoint'],
        value=data['value'],
        annotation=data.get('annotation')
    )
    return jsonify({'status': 'success', 'id': interaction.id})
```

This documentation provides three distinct examples of Chart.js events and interactions with varying complexity and features. Each example demonstrates different aspects of interaction handling when integrated with Flask, from basic click events to complex custom interaction modes.
