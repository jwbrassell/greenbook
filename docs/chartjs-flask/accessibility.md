# Chart.js Accessibility with Flask

## Table of Contents
- [Chart.js Accessibility with Flask](#chartjs-accessibility-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Accessibility Implementation](#basic-accessibility-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template with Accessibility Features](#html-template-with-accessibility-features)
  - [Monthly Sales Data](#monthly-sales-data)



Making data visualizations accessible is crucial for ensuring all users can understand and interact with your charts. This guide demonstrates how to implement accessibility features in Chart.js when using it with Flask.

## Basic Accessibility Implementation

### Flask Route
```python
@app.route('/accessible-chart')
def accessible_chart():
    return render_template('accessible_chart.html')

@app.route('/api/chart-data')
def chart_data():
    data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'datasets': [{
            'label': 'Monthly Sales',
            'data': [65, 59, 80, 81, 56, 55],
            'backgroundColor': 'rgba(75, 192, 192, 0.2)',
            'borderColor': 'rgba(75, 192, 192, 1)',
            'borderWidth': 1
        }]
    }
    return jsonify(data)
```

### HTML Template with Accessibility Features
```html
<div class="chart-container" role="region" aria-label="Monthly Sales Chart">
    <h2 id="chartTitle" class="visually-hidden">Monthly Sales Data</h2>
    <canvas id="accessibleChart" role="img" aria-labelledby="chartTitle chartDescription"></canvas>
    <div id="chartDescription" class="visually-hidden">
        Bar chart showing monthly sales data from January to June
    </div>
    
    <!-- Accessible data table -->
    <div class="visually-hidden">
        <table id="chartData" role="table" aria-label="Monthly Sales Data Table">
            <thead>
                <tr>
                    <th scope="col">Month</th>
                    <th scope="col">Sales</th>
                </tr>
            </thead>
            <tbody>
                <!-- Will be populated with JavaScript -->
            </tbody>
        </table>
    </div>
    
    <!-- Keyboard controls description -->
    <div class="keyboard-instructions" aria-live="polite">
        Press arrow keys to navigate between data points. 
        Press Enter to get detailed information.
    </div>
</div>

<style>
.visually-hidden {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    border: 0;
}

.keyboard-instructions {
    margin-top: 10px;
    padding: 10px;
    background: #f8f9fa;
    border-radius: 4px;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/chart-data')
        .then(response => response.json())
        .then(data => {
            const ctx = document.getElementById('accessibleChart').getContext('2d');
            
            // Populate accessible data table
            const tbody = document.querySelector('#chartData tbody');
            data.labels.forEach((label, index) => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${label}</td>
                    <td>${data.datasets[0].data[index]}</td>
                `;
                tbody.appendChild(row);
            });
            
            // Initialize chart with accessibility features
            const chart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    responsive: true,
                    plugins: {
                        title: {
                            display: true,
                            text: 'Monthly Sales Data'
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `Sales for ${context.label}: $${context.raw}`;
                                }
                            }
                        }
                    },
                    interaction: {
                        mode: 'nearest',
                        axis: 'x',
                        intersect: false
                    }
                }
            });
            
            // Add keyboard navigation
            setupKeyboardNavigation(chart);
        });
});

function setupKeyboardNavigation(chart) {
    let currentIndex = -1;
    
    document.addEventListener('keydown', function(e) {
        switch(e.key) {
            case 'ArrowLeft':
                e.preventDefault();
                currentIndex = Math.max(0, currentIndex - 1);
                highlightDataPoint(chart, currentIndex);
                break;
            case 'ArrowRight':
                e.preventDefault();
                currentIndex = Math.min(
                    chart.data.labels.length - 1,
                    currentIndex + 1
                );
                highlightDataPoint(chart, currentIndex);
                break;
            case 'Enter':
                e.preventDefault();
                if (currentIndex >= 0) {
                    announceDataPoint(chart, currentIndex);
                }
                break;
        }
    });
}

function highlightDataPoint(chart, index) {
    // Clear previous highlights
    chart.data.datasets[0].backgroundColor = chart.data.labels.map(() =>
        'rgba(75, 192, 192, 0.2)'
    );
    
    // Highlight current point
    if (index >= 0) {
        chart.data.datasets[0].backgroundColor[index] = 'rgba(255, 99, 132, 0.2)';
    }
    
    chart.update();
    announceDataPoint(chart, index);
}

function announceDataPoint(chart, index) {
    const announcement = `
        ${chart.data.labels[index]}: 
        ${chart.data.datasets[0].data[index]} in sales
    `;
    
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.classList.add('visually-hidden');
    document.body.appendChild(liveRegion);
    
    setTimeout(() => {
        liveRegion.textContent = announcement;
        setTimeout(() => liveRegion.remove(), 1000);
    }, 100);
}
```

## Example 1: Enhanced Screen Reader Support

This example demonstrates how to provide detailed screen reader descriptions and announcements.

### Flask Implementation
```python
@app.route('/api/enhanced-accessibility-data')
def enhanced_accessibility_data():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [{
            'label': 'Quarterly Revenue',
            'data': [12000, 19000, 15000, 22000],
            'descriptions': [
                'First quarter showed steady growth',
                'Strong performance in Q2 with 58% increase',
                'Slight decline in Q3 due to seasonal factors',
                'Record-breaking fourth quarter'
            ]
        }]
    }
    return jsonify(data)
```

### Enhanced Screen Reader Configuration
```javascript
const accessibilityPlugin = {
    id: 'accessibilityPlugin',
    afterInit: (chart) => {
        // Add detailed descriptions to chart container
        const descriptions = chart.data.datasets[0].descriptions;
        const descriptionList = document.createElement('ul');
        descriptionList.setAttribute('aria-label', 'Data Point Descriptions');
        descriptionList.classList.add('visually-hidden');
        
        descriptions.forEach((desc, i) => {
            const li = document.createElement('li');
            li.textContent = `${chart.data.labels[i]}: ${desc}`;
            descriptionList.appendChild(li);
        });
        
        chart.canvas.parentNode.appendChild(descriptionList);
    },
    afterDatasetsDraw: (chart) => {
        // Add ARIA labels to individual data points
        chart.data.datasets.forEach((dataset, datasetIndex) => {
            const meta = chart.getDatasetMeta(datasetIndex);
            meta.data.forEach((element, index) => {
                element.options.ariaLabel = 
                    `${dataset.label} for ${chart.data.labels[index]}: ` +
                    `${dataset.data[index]}. ${dataset.descriptions[index]}`;
            });
        });
    }
};
```

## Example 2: Interactive Focus Management

This example shows how to implement proper focus management for interactive chart elements.

### Flask Implementation
```python
@app.route('/api/interactive-accessibility-data')
def interactive_accessibility_data():
    data = {
        'labels': ['A', 'B', 'C', 'D', 'E'],
        'datasets': [{
            'label': 'Interactive Dataset',
            'data': [65, 59, 80, 81, 56]
        }]
    }
    return jsonify(data)
```

### Focus Management Configuration
```javascript
const focusManagementPlugin = {
    id: 'focusManagement',
    afterInit: (chart) => {
        // Create focus trap container
        const container = chart.canvas.parentNode;
        container.setAttribute('tabindex', '0');
        container.setAttribute('role', 'application');
        container.setAttribute('aria-label', chart.options.plugins.title.text);
        
        // Add focusable data points
        chart.data.datasets.forEach((dataset, datasetIndex) => {
            const meta = chart.getDatasetMeta(datasetIndex);
            meta.data.forEach((element, index) => {
                const point = document.createElement('button');
                point.classList.add('visually-hidden', 'focus-point');
                point.setAttribute('aria-label', 
                    `${dataset.label} ${chart.data.labels[index]}: ${dataset.data[index]}`
                );
                point.dataset.index = index;
                container.appendChild(point);
            });
        });
        
        // Setup focus management
        setupFocusManagement(chart);
    }
};

function setupFocusManagement(chart) {
    const container = chart.canvas.parentNode;
    const focusPoints = container.querySelectorAll('.focus-point');
    
    container.addEventListener('keydown', (e) => {
        const currentFocus = document.activeElement;
        let nextFocus;
        
        switch(e.key) {
            case 'ArrowRight':
            case 'ArrowDown':
                e.preventDefault();
                nextFocus = getNextFocusablePoint(currentFocus, focusPoints);
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                e.preventDefault();
                nextFocus = getPreviousFocusablePoint(currentFocus, focusPoints);
                break;
            case 'Home':
                e.preventDefault();
                nextFocus = focusPoints[0];
                break;
            case 'End':
                e.preventDefault();
                nextFocus = focusPoints[focusPoints.length - 1];
                break;
        }
        
        if (nextFocus) {
            nextFocus.focus();
            highlightDataPoint(chart, parseInt(nextFocus.dataset.index));
        }
    });
}
```

## Example 3: Color Contrast and High Contrast Mode

This example demonstrates how to implement proper color contrast and support high contrast mode.

### Flask Implementation
```python
@app.route('/api/contrast-aware-data')
def contrast_aware_data():
    data = {
        'labels': ['Category A', 'Category B', 'Category C'],
        'datasets': [{
            'label': 'High Contrast Dataset',
            'data': [300, 450, 280],
            'colorSchemes': {
                'default': {
                    'backgroundColor': [
                        'rgba(0, 123, 255, 0.5)',
                        'rgba(40, 167, 69, 0.5)',
                        'rgba(220, 53, 69, 0.5)'
                    ],
                    'borderColor': [
                        'rgb(0, 123, 255)',
                        'rgb(40, 167, 69)',
                        'rgb(220, 53, 69)'
                    ]
                },
                'highContrast': {
                    'backgroundColor': [
                        'rgba(0, 0, 0, 0.8)',
                        'rgba(255, 255, 255, 0.8)',
                        'rgba(128, 128, 128, 0.8)'
                    ],
                    'borderColor': [
                        'rgb(0, 0, 0)',
                        'rgb(255, 255, 255)',
                        'rgb(128, 128, 128)'
                    ]
                }
            }
        }]
    }
    return jsonify(data)
```

### High Contrast Configuration
```javascript
const contrastPlugin = {
    id: 'contrastPlugin',
    beforeInit: (chart) => {
        // Check for high contrast mode
        const isHighContrast = window.matchMedia('(forced-colors: active)').matches;
        
        // Apply appropriate color scheme
        chart.data.datasets.forEach(dataset => {
            const scheme = isHighContrast ? 
                dataset.colorSchemes.highContrast : 
                dataset.colorSchemes.default;
            
            dataset.backgroundColor = scheme.backgroundColor;
            dataset.borderColor = scheme.borderColor;
        });
    }
};

// Add color contrast checker
function hasGoodContrast(foreground, background) {
    // Calculate relative luminance
    function getLuminance(r, g, b) {
        let [rs, gs, bs] = [r, g, b].map(c => {
            c = c / 255;
            return c <= 0.03928 ? 
                c / 12.92 : 
                Math.pow((c + 0.055) / 1.055, 2.4);
        });
        return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
    }
    
    // Parse colors and calculate contrast ratio
    const fg = foreground.match(/\d+/g).map(Number);
    const bg = background.match(/\d+/g).map(Number);
    
    const l1 = getLuminance(fg[0], fg[1], fg[2]);
    const l2 = getLuminance(bg[0], bg[1], bg[2]);
    
    const ratio = (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
    return ratio >= 4.5;  // WCAG AA standard for normal text
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database while maintaining accessibility:

```python
class AccessibleChartData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100))
    value = db.Column(db.Float)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    
    @staticmethod
    def get_accessible_data(category):
        data = AccessibleChartData.query\
            .filter_by(category=category)\
            .order_by(AccessibleChartData.label)\
            .all()
            
        return {
            'labels': [d.label for d in data],
            'datasets': [{
                'label': category,
                'data': [d.value for d in data],
                'descriptions': [d.description for d in data]
            }]
        }

@app.route('/api/accessible-data/<category>')
def get_accessible_data(category):
    data = AccessibleChartData.get_accessible_data(category)
    
    # Add ARIA descriptions
    for i, description in enumerate(data['datasets'][0]['descriptions']):
        data['datasets'][0]['aria-descriptions'] = f"""
            {data['labels'][i]}: {data['datasets'][0]['data'][i]}.
            {description}
        """
    
    return jsonify(data)
```

This documentation provides three distinct examples of Chart.js accessibility features with varying complexity. Each example demonstrates different aspects of accessibility implementation when integrated with Flask, from basic screen reader support to advanced features like high contrast mode and proper focus management.
