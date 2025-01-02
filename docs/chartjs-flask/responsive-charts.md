# Responsive Charts with Chart.js and Flask

## Table of Contents
- [Responsive Charts with Chart.js and Flask](#responsive-charts-with-chartjs-and-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Implementation](#basic-implementation)
    - [Flask Route](#flask-route)
    - [HTML Template with Responsive Container](#html-template-with-responsive-container)
  - [Example 1: Dynamic Layout Adaptation](#example-1:-dynamic-layout-adaptation)
    - [Flask Implementation](#flask-implementation)
    - [Advanced Responsive Configuration](#advanced-responsive-configuration)
  - [Example 2: Responsive Dashboard Layout](#example-2:-responsive-dashboard-layout)
    - [Flask Implementation](#flask-implementation)
    - [Responsive Dashboard Template](#responsive-dashboard-template)
  - [Example 3: Touch-Friendly Mobile Charts](#example-3:-touch-friendly-mobile-charts)
    - [Flask Implementation](#flask-implementation)
    - [Mobile-Optimized Configuration](#mobile-optimized-configuration)
  - [Working with Database Data](#working-with-database-data)



Responsive charts automatically adapt to different screen sizes and device types, ensuring optimal visualization across desktop, tablet, and mobile devices. This guide demonstrates how to implement responsive charts using Chart.js with Flask.

## Basic Implementation

### Flask Route
```python
@app.route('/responsive-chart')
def responsive_chart():
    return render_template('responsive_chart.html')

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

### HTML Template with Responsive Container
```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .chart-container {
            position: relative;
            margin: auto;
            width: 100%;
            max-width: 800px;
        }

        @media (max-width: 600px) {
            .chart-container {
                min-height: 300px;
            }
        }

        @media (min-width: 601px) {
            .chart-container {
                min-height: 400px;
            }
        }
    </style>
</head>
<body>
    <div class="chart-container">
        <canvas id="responsiveChart"></canvas>
    </div>

    <script>
    document.addEventListener('DOMContentLoaded', function() {
        fetch('/api/chart-data')
            .then(response => response.json())
            .then(data => {
                const ctx = document.getElementById('responsiveChart').getContext('2d');
                new Chart(ctx, {
                    type: 'bar',
                    data: data,
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            title: {
                                display: true,
                                text: 'Sales Overview'
                            },
                            legend: {
                                position: window.innerWidth < 600 ? 'bottom' : 'top'
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                ticks: {
                                    // Adjust tick size for smaller screens
                                    font: {
                                        size: window.innerWidth < 600 ? 10 : 12
                                    }
                                }
                            },
                            x: {
                                ticks: {
                                    font: {
                                        size: window.innerWidth < 600 ? 10 : 12
                                    }
                                }
                            }
                        }
                    }
                });
            });
    });
    </script>
</body>
</html>
```

## Example 1: Dynamic Layout Adaptation

This example shows how to create charts that dynamically adjust their layout based on screen size.

### Flask Implementation
```python
@app.route('/api/dynamic-layout-data')
def dynamic_layout_data():
    data = {
        'labels': ['Q1', 'Q2', 'Q3', 'Q4'],
        'datasets': [
            {
                'label': 'Revenue',
                'data': [12000, 19000, 15000, 22000],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1,
                'yAxisID': 'revenue'
            },
            {
                'label': 'Profit',
                'data': [3000, 5000, 4000, 6000],
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'borderColor': 'rgba(255, 99, 132, 1)',
                'borderWidth': 1,
                'yAxisID': 'profit'
            }
        ]
    }
    return jsonify(data)
```

### Advanced Responsive Configuration
```javascript
const config = {
    type: 'bar',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: function() {
                    return window.innerWidth < 600 ? 'bottom' : 'top';
                }
            }
        },
        layout: {
            padding: {
                top: window.innerWidth < 600 ? 10 : 20,
                right: window.innerWidth < 600 ? 10 : 20,
                bottom: window.innerWidth < 600 ? 10 : 20,
                left: window.innerWidth < 600 ? 10 : 20
            }
        },
        scales: {
            revenue: {
                type: 'linear',
                position: window.innerWidth < 600 ? 'left' : 'right',
                grid: {
                    drawOnChartArea: window.innerWidth >= 600
                }
            },
            profit: {
                type: 'linear',
                position: 'left'
            }
        }
    }
};

// Handle resize events
window.addEventListener('resize', function() {
    const width = window.innerWidth;
    
    // Update legend position
    chart.options.plugins.legend.position = width < 600 ? 'bottom' : 'top';
    
    // Update scales layout
    chart.options.scales.revenue.position = width < 600 ? 'left' : 'right';
    chart.options.scales.revenue.grid.drawOnChartArea = width >= 600;
    
    // Update padding
    chart.options.layout.padding = {
        top: width < 600 ? 10 : 20,
        right: width < 600 ? 10 : 20,
        bottom: width < 600 ? 10 : 20,
        left: width < 600 ? 10 : 20
    };
    
    chart.update();
});
```

## Example 2: Responsive Dashboard Layout

This example demonstrates how to create a responsive dashboard with multiple charts.

### Flask Implementation
```python
@app.route('/dashboard')
def dashboard():
    return render_template('responsive_dashboard.html')

@app.route('/api/dashboard-data')
def dashboard_data():
    return jsonify({
        'sales': generate_sales_data(),
        'customers': generate_customer_data(),
        'products': generate_product_data()
    })
```

### Responsive Dashboard Template
```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        .dashboard-grid {
            display: grid;
            gap: 20px;
            padding: 20px;
        }

        .chart-wrapper {
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Desktop Layout */
        @media (min-width: 1024px) {
            .dashboard-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            .chart-wrapper.full-width {
                grid-column: 1 / -1;
            }
        }

        /* Tablet Layout */
        @media (min-width: 768px) and (max-width: 1023px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        /* Mobile Layout */
        @media (max-width: 767px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
                gap: 15px;
                padding: 10px;
            }
            .chart-wrapper {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="dashboard-grid">
        <div class="chart-wrapper full-width">
            <canvas id="salesChart"></canvas>
        </div>
        <div class="chart-wrapper">
            <canvas id="customersChart"></canvas>
        </div>
        <div class="chart-wrapper">
            <canvas id="productsChart"></canvas>
        </div>
    </div>

    <script>
    function createResponsiveChart(ctx, config) {
        const baseConfig = {
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: window.innerWidth < 768 ? 'bottom' : 'top'
                    }
                }
            }
        };
        return new Chart(ctx, {...baseConfig, ...config});
    }

    document.addEventListener('DOMContentLoaded', function() {
        fetch('/api/dashboard-data')
            .then(response => response.json())
            .then(data => {
                // Initialize charts with responsive configurations
                const charts = {
                    sales: createResponsiveChart(
                        document.getElementById('salesChart'),
                        createSalesChartConfig(data.sales)
                    ),
                    customers: createResponsiveChart(
                        document.getElementById('customersChart'),
                        createCustomersChartConfig(data.customers)
                    ),
                    products: createResponsiveChart(
                        document.getElementById('productsChart'),
                        createProductsChartConfig(data.products)
                    )
                };

                // Handle resize events
                window.addEventListener('resize', function() {
                    Object.values(charts).forEach(chart => {
                        chart.options.plugins.legend.position = 
                            window.innerWidth < 768 ? 'bottom' : 'top';
                        chart.update();
                    });
                });
            });
    });
    </script>
</body>
</html>
```

## Example 3: Touch-Friendly Mobile Charts

This example shows how to optimize charts for touch interactions on mobile devices.

### Flask Implementation
```python
@app.route('/api/touch-friendly-data')
def touch_friendly_data():
    data = {
        'labels': generate_monthly_labels(),
        'datasets': [{
            'label': 'Performance',
            'data': generate_performance_data(),
            'borderColor': 'rgb(75, 192, 192)',
            'pointRadius': 6,  # Larger points for touch
            'pointHoverRadius': 10
        }]
    }
    return jsonify(data)
```

### Mobile-Optimized Configuration
```javascript
const config = {
    type: 'line',
    data: chartData,
    options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            mode: 'nearest',
            axis: 'x',
            intersect: false
        },
        plugins: {
            tooltip: {
                enabled: true,
                position: 'nearest',
                external: function(context) {
                    // Custom tooltip for touch devices
                    if ('ontouchstart' in window) {
                        // Implement custom touch-friendly tooltip
                        showCustomTooltip(context);
                    }
                }
            }
        },
        scales: {
            x: {
                ticks: {
                    maxRotation: 45,
                    minRotation: 45,
                    font: {
                        size: 10
                    }
                }
            }
        }
    }
};

function showCustomTooltip(context) {
    // Create a custom tooltip element optimized for touch
    const tooltipEl = document.getElementById('chartTooltip') || 
        createTooltipElement();
    
    if (context.tooltip.opacity === 0) {
        tooltipEl.style.opacity = 0;
        return;
    }

    const position = context.chart.canvas.getBoundingClientRect();
    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = position.left + context.tooltip.caretX + 'px';
    tooltipEl.style.top = position.top + context.tooltip.caretY + 'px';
    tooltipEl.innerHTML = formatTooltipContent(context);
}

function createTooltipElement() {
    const el = document.createElement('div');
    el.id = 'chartTooltip';
    el.style.cssText = `
        position: absolute;
        padding: 10px;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        border-radius: 4px;
        font-size: 14px;
        touch-action: none;
        pointer-events: none;
        z-index: 1000;
    `;
    document.body.appendChild(el);
    return el;
}
```

## Working with Database Data

Here's how to integrate with a Flask-SQLAlchemy database for responsive charts:

```python
class ChartData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    value = db.Column(db.Float)
    timestamp = db.Column(db.DateTime)

    @staticmethod
    def get_aggregated_data(interval='day'):
        """
        Get data aggregated based on screen size/device
        For mobile, we might want less data points
        """
        if interval == 'day':
            # Detailed view for larger screens
            return db.session.query(
                func.date(ChartData.timestamp),
                func.sum(ChartData.value)
            ).group_by(
                func.date(ChartData.timestamp)
            ).all()
        else:
            # Aggregated view for smaller screens
            return db.session.query(
                func.date_trunc('month', ChartData.timestamp),
                func.sum(ChartData.value)
            ).group_by(
                func.date_trunc('month', ChartData.timestamp)
            ).all()

@app.route('/api/responsive-data')
def responsive_data():
    # Get device type from user agent or screen size
    is_mobile = request.user_agent.platform in ['iphone', 'android'] or \
                request.args.get('width', type=int, default=1024) < 768
    
    # Adjust data granularity based on device
    interval = 'month' if is_mobile else 'day'
    data = ChartData.get_aggregated_data(interval)
    
    return jsonify({
        'labels': [d[0].strftime('%Y-%m-%d') for d in data],
        'datasets': [{
            'data': [d[1] for d in data],
            'label': 'Value',
            # Adjust point size based on device
            'pointRadius': 6 if is_mobile else 3,
            'pointHoverRadius': 10 if is_mobile else 5
        }]
    })
```

This documentation provides three distinct examples of responsive charts with varying complexity and features. Each example demonstrates different aspects of Chart.js capabilities when integrated with Flask, from basic responsive layouts to advanced features like touch optimization and dynamic data aggregation.
