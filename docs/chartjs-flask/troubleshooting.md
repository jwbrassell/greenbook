# Chart.js Troubleshooting with Flask

## Table of Contents
- [Chart.js Troubleshooting with Flask](#chartjs-troubleshooting-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Common Issues and Solutions](#common-issues-and-solutions)
    - [1. Chart Not Rendering](#1-chart-not-rendering)
      - [Symptoms](#symptoms)
      - [Solutions](#solutions)
    - [2. Data Loading Issues](#2-data-loading-issues)
      - [Symptoms](#symptoms)
      - [Solutions](#solutions)
- [Flask route with error handling](#flask-route-with-error-handling)
- [JavaScript error handling](#javascript-error-handling)
    - [3. Update and Animation Issues](#3-update-and-animation-issues)
      - [Symptoms](#symptoms)
      - [Solutions](#solutions)
  - [Debugging Techniques](#debugging-techniques)
    - [1. Chart State Inspection](#1-chart-state-inspection)
    - [2. Network Monitoring](#2-network-monitoring)
- [Flask debugging middleware](#flask-debugging-middleware)
- [Enable in development](#enable-in-development)
    - [3. Error Tracking](#3-error-tracking)
- [Usage in routes](#usage-in-routes)
  - [Working with Development Tools](#working-with-development-tools)
    - [Browser DevTools Integration](#browser-devtools-integration)



This guide covers common issues, debugging techniques, and solutions when working with Chart.js in Flask applications.

## Common Issues and Solutions

### 1. Chart Not Rendering

#### Symptoms
- Canvas remains empty
- No errors in console
- Data appears to be loaded correctly

#### Solutions
```javascript
// 1. Check Chart.js initialization
document.addEventListener('DOMContentLoaded', function() {
    // Verify canvas exists
    const canvas = document.getElementById('myChart');
    if (!canvas) {
        console.error('Canvas element not found');
        return;
    }
    
    // Verify context
    const ctx = canvas.getContext('2d');
    if (!ctx) {
        console.error('Could not get canvas context');
        return;
    }
    
    // Initialize with error handling
    try {
        const chart = new Chart(ctx, {
            type: 'line',
            data: chartData,
            options: chartOptions
        });
    } catch (error) {
        console.error('Chart initialization failed:', error);
    }
});

// 2. Check data structure
function validateChartData(data) {
    if (!data.datasets || !Array.isArray(data.datasets)) {
        console.error('Invalid datasets structure');
        return false;
    }
    
    if (!data.labels || !Array.isArray(data.labels)) {
        console.error('Invalid labels structure');
        return false;
    }
    
    return true;
}

// 3. Check container dimensions
function ensureChartDimensions() {
    const container = document.querySelector('.chart-container');
    if (container.offsetWidth === 0 || container.offsetHeight === 0) {
        console.error('Chart container has zero dimensions');
        container.style.width = '100%';
        container.style.height = '400px';
    }
}
```

### 2. Data Loading Issues

#### Symptoms
- Chart renders but no data appears
- Console shows API errors
- Data format mismatches

#### Solutions
```python
# Flask route with error handling
@app.route('/api/chart-data')
def get_chart_data():
    try:
        # Validate request parameters
        chart_id = request.args.get('id')
        if not chart_id:
            raise ValueError("Missing chart ID")
            
        # Get data with timeout
        data = fetch_chart_data(chart_id, timeout=5)
        
        # Validate data structure
        if not validate_data_structure(data):
            raise ValueError("Invalid data structure")
            
        return jsonify(data)
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except TimeoutError:
        return jsonify({'error': 'Data fetch timeout'}), 504
    except Exception as e:
        app.logger.error(f"Chart data error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

def validate_data_structure(data):
    """Validate chart data structure"""
    required_fields = ['labels', 'datasets']
    if not all(field in data for field in required_fields):
        return False
        
    if not data['datasets']:
        return False
        
    for dataset in data['datasets']:
        if 'data' not in dataset or not dataset['data']:
            return False
            
    return True

# JavaScript error handling
async function loadChartData() {
    try {
        const response = await fetch('/api/chart-data');
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to load chart data');
        }
        
        const data = await response.json();
        return data;
        
    } catch (error) {
        console.error('Data loading error:', error);
        displayError('Failed to load chart data. Please try again.');
        throw error;
    }
}
```

### 3. Update and Animation Issues

#### Symptoms
- Chart updates not reflecting
- Animations not working
- Performance issues during updates

#### Solutions
```javascript
// 1. Proper update handling
function updateChart(chart, newData) {
    // Update data references
    chart.data.labels = newData.labels;
    chart.data.datasets.forEach((dataset, i) => {
        Object.assign(dataset, newData.datasets[i]);
    });
    
    // Use appropriate update mode
    chart.update('active');  // For smooth transitions
    // or
    chart.update('none');    // For performance
}

// 2. Animation control
const chartConfig = {
    options: {
        animation: {
            duration: 1000,  // Milliseconds
            easing: 'easeInOutQuart',
            onProgress: function(animation) {
                // Monitor animation progress
                console.log(`Progress: ${animation.currentStep / animation.numSteps}`);
            },
            onComplete: function() {
                // Handle animation completion
                console.log('Animation completed');
            }
        },
        transitions: {
            active: {
                animation: {
                    duration: 300
                }
            }
        }
    }
};

// 3. Performance optimization
function optimizeUpdates(chart) {
    let updateTimeout;
    
    return function(newData) {
        // Cancel pending updates
        if (updateTimeout) {
            clearTimeout(updateTimeout);
        }
        
        // Debounce updates
        updateTimeout = setTimeout(() => {
            requestAnimationFrame(() => {
                updateChart(chart, newData);
            });
        }, 100);
    };
}
```

## Debugging Techniques

### 1. Chart State Inspection

```javascript
class ChartDebugger {
    constructor(chart) {
        this.chart = chart;
    }
    
    logChartState() {
        console.log({
            type: this.chart.config.type,
            data: {
                labels: this.chart.data.labels,
                datasets: this.chart.data.datasets.map(ds => ({
                    label: ds.label,
                    dataCount: ds.data.length
                }))
            },
            options: this.chart.options
        });
    }
    
    validateDataConsistency() {
        const datasets = this.chart.data.datasets;
        const labelCount = this.chart.data.labels.length;
        
        datasets.forEach((dataset, i) => {
            if (dataset.data.length !== labelCount) {
                console.error(
                    `Dataset ${i} length mismatch: ` +
                    `expected ${labelCount}, got ${dataset.data.length}`
                );
            }
        });
    }
    
    inspectScales() {
        const scales = this.chart.scales;
        Object.entries(scales).forEach(([key, scale]) => {
            console.log(`Scale ${key}:`, {
                min: scale.min,
                max: scale.max,
                ticks: scale.ticks
            });
        });
    }
}

// Usage
const debugger = new ChartDebugger(chart);
debugger.logChartState();
debugger.validateDataConsistency();
debugger.inspectScales();
```

### 2. Network Monitoring

```python
# Flask debugging middleware
class ChartDebugMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        # Track request timing
        start_time = time.time()
        
        def debug_start_response(status, headers, exc_info=None):
            # Log response info
            duration = time.time() - start_time
            path = environ.get('PATH_INFO', '')
            
            if path.startswith('/api/chart'):
                app.logger.debug(
                    f"Chart API Response: {status} "
                    f"Duration: {duration:.3f}s "
                    f"Path: {path}"
                )
            
            return start_response(status, headers, exc_info)
        
        return self.app(environ, debug_start_response)

# Enable in development
if app.debug:
    app.wsgi_app = ChartDebugMiddleware(app.wsgi_app)
```

### 3. Error Tracking

```python
class ChartErrorTracker:
    def __init__(self):
        self.errors = []
        self.error_counts = {}
    
    def track_error(self, error_type, message, context=None):
        """Track a chart-related error"""
        error = {
            'type': error_type,
            'message': str(message),
            'timestamp': datetime.utcnow(),
            'context': context or {}
        }
        
        self.errors.append(error)
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Log if error is frequent
        if self.error_counts[error_type] > 10:
            app.logger.warning(
                f"Frequent {error_type} errors: "
                f"{self.error_counts[error_type]} occurrences"
            )
    
    def get_error_summary(self):
        """Get error statistics"""
        return {
            'total_errors': len(self.errors),
            'error_types': self.error_counts,
            'recent_errors': self.errors[-10:]
        }
    
    def clear_errors(self):
        """Clear error history"""
        self.errors = []
        self.error_counts = {}

# Usage in routes
error_tracker = ChartErrorTracker()

@app.route('/api/chart-data')
def get_chart_data():
    try:
        data = generate_chart_data()
        return jsonify(data)
    except Exception as e:
        error_tracker.track_error(
            'data_generation',
            str(e),
            {'endpoint': 'chart-data'}
        )
        raise
```

## Working with Development Tools

### Browser DevTools Integration

```javascript
class ChartDevTools {
    constructor(chart) {
        this.chart = chart;
        this.setupDebugger();
    }
    
    setupDebugger() {
        // Add chart instance to window for console access
        window.__chartDebug = {
            chart: this.chart,
            getState: () => this.getChartState(),
            updateData: (newData) => this.updateChartData(newData),
            toggleAnimation: () => this.toggleAnimation()
        };
        
        console.log(
            'Chart debugger available at window.__chartDebug\n' +
            'Methods: getState(), updateData(newData), toggleAnimation()'
        );
    }
    
    getChartState() {
        return {
            data: this.chart.data,
            options: this.chart.options,
            scales: Object.fromEntries(
                Object.entries(this.chart.scales).map(([key, scale]) => [
                    key,
                    {
                        min: scale.min,
                        max: scale.max,
                        ticks: scale.ticks
                    }
                ])
            )
        };
    }
    
    updateChartData(newData) {
        this.chart.data = newData;
        this.chart.update();
        console.log('Chart data updated');
    }
    
    toggleAnimation() {
        const animation = this.chart.options.animation;
        animation.duration = animation.duration > 0 ? 0 : 1000;
        this.chart.update();
        console.log(
            `Animations ${animation.duration > 0 ? 'enabled' : 'disabled'}`
        );
    }
}

// Initialize DevTools
const devTools = new ChartDevTools(chart);
```

This documentation provides comprehensive troubleshooting guidance for Chart.js with Flask, including common issues, debugging techniques, and development tools integration. Each section includes practical examples and solutions for various scenarios you might encounter during development.
