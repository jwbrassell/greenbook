# Chart.js Performance Optimization with Flask

## Table of Contents
- [Chart.js Performance Optimization with Flask](#chartjs-performance-optimization-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Performance Implementation](#basic-performance-implementation)
    - [Flask Route with Data Optimization](#flask-route-with-data-optimization)
    - [HTML Template with Performance Optimizations](#html-template-with-performance-optimizations)
  - [Example 1: Large Dataset Handling](#example-1:-large-dataset-handling)
    - [Flask Implementation](#flask-implementation)
    - [Large Dataset Configuration](#large-dataset-configuration)
  - [Example 2: Memory Management](#example-2:-memory-management)
    - [Flask Implementation](#flask-implementation)
    - [Memory Management Configuration](#memory-management-configuration)
  - [Example 3: WebWorker Implementation](#example-3:-webworker-implementation)
    - [Flask Implementation](#flask-implementation)
    - [WebWorker Configuration](#webworker-configuration)
  - [Working with Database Data](#working-with-database-data)



Performance optimization is crucial when working with large datasets or multiple charts. This guide demonstrates techniques for optimizing Chart.js performance when integrated with Flask.

## Basic Performance Implementation

### Flask Route with Data Optimization
```python
from flask import Flask, jsonify, render_template
import numpy as np
from datetime import datetime, timedelta

@app.route('/optimized-chart')
def optimized_chart():
    return render_template('optimized_chart.html')

@app.route('/api/chart-data')
def chart_data():
    # Example: Optimize data points by sampling
    num_points = 1000
    raw_data = generate_large_dataset(num_points)
    
    # Downsample data based on screen width
    screen_width = int(request.args.get('width', 800))
    target_points = min(screen_width // 2, num_points)
    
    optimized_data = downsample_data(raw_data, target_points)
    
    return jsonify(optimized_data)

def downsample_data(data, target_points):
    """Reduce number of data points while preserving trends"""
    if len(data) <= target_points:
        return data
        
    # Use window averaging for downsampling
    window_size = len(data) // target_points
    downsampled = []
    
    for i in range(0, len(data), window_size):
        window = data[i:i + window_size]
        downsampled.append({
            'x': window[0]['x'],
            'y': sum(point['y'] for point in window) / len(window)
        })
    
    return downsampled
```

### HTML Template with Performance Optimizations
```html
<div class="chart-container">
    <canvas id="optimizedChart"></canvas>
</div>

<script>
// Performance optimization configurations
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.animation.duration = 0;  // Disable animations for better performance

document.addEventListener('DOMContentLoaded', async function() {
    // Get screen width for data optimization
    const width = window.innerWidth;
    
    // Fetch optimized data
    const response = await fetch(`/api/chart-data?width=${width}`);
    const data = await response.json();
    
    const ctx = document.getElementById('optimizedChart').getContext('2d');
    
    // Use requestAnimationFrame for smooth rendering
    requestAnimationFrame(() => {
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                datasets: [{
                    data: data,
                    borderWidth: 1,  // Minimize rendering overhead
                    pointRadius: 0,   // Hide points for better performance
                    tension: 0        // Disable bezier curves
                }]
            },
            options: {
                parsing: false,  // Disable parsing if data is pre-formatted
                normalized: true,  // Use normalized data
                spanGaps: true,   // Optimize gaps in data
                elements: {
                    line: {
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        type: 'linear',
                        ticks: {
                            source: 'auto',
                            maxRotation: 0
                        }
                    },
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    decimation: {
                        enabled: true,
                        algorithm: 'min-max'
                    }
                }
            }
        });
    });
});
</script>
```

## Example 1: Large Dataset Handling

This example demonstrates techniques for efficiently handling large datasets.

### Flask Implementation
```python
@app.route('/api/large-dataset')
def large_dataset():
    # Parameters for data optimization
    chunk_size = int(request.args.get('chunk_size', 1000))
    page = int(request.args.get('page', 1))
    
    # Generate or fetch large dataset
    full_data = generate_large_dataset()
    
    # Implement pagination
    start_idx = (page - 1) * chunk_size
    end_idx = start_idx + chunk_size
    chunk = full_data[start_idx:end_idx]
    
    # Optimize data structure
    optimized_chunk = [{
        'x': point['x'],
        'y': round(point['y'], 2)  # Reduce decimal precision
    } for point in chunk]
    
    return jsonify({
        'data': optimized_chunk,
        'meta': {
            'total_points': len(full_data),
            'current_page': page,
            'total_pages': len(full_data) // chunk_size + 1
        }
    })

def generate_large_dataset():
    """Generate sample large dataset with optimization"""
    points = []
    base_date = datetime.now()
    
    for i in range(100000):
        # Use efficient data structures
        points.append({
            'x': (base_date + timedelta(minutes=i)).timestamp(),
            'y': float(np.sin(i / 1000) * 100)
        })
    
    return points
```

### Large Dataset Configuration
```javascript
class ChunkLoader {
    constructor(baseUrl, chunkSize = 1000) {
        this.baseUrl = baseUrl;
        this.chunkSize = chunkSize;
        this.cache = new Map();
        this.loading = false;
    }
    
    async getChunk(page) {
        if (this.cache.has(page)) {
            return this.cache.get(page);
        }
        
        if (this.loading) {
            return null;
        }
        
        this.loading = true;
        
        try {
            const response = await fetch(
                `${this.baseUrl}?chunk_size=${this.chunkSize}&page=${page}`
            );
            const data = await response.json();
            
            // Cache the chunk
            this.cache.set(page, data);
            
            // Implement LRU cache
            if (this.cache.size > 10) {
                const firstKey = this.cache.keys().next().value;
                this.cache.delete(firstKey);
            }
            
            return data;
        } finally {
            this.loading = false;
        }
    }
}

const loader = new ChunkLoader('/api/large-dataset');
let currentChart;

async function updateChart(page) {
    const chunk = await loader.getChunk(page);
    if (!chunk) return;
    
    if (!currentChart) {
        // Initialize chart with first chunk
        currentChart = new Chart('chart', {
            type: 'line',
            data: {
                datasets: [{
                    data: chunk.data,
                    borderWidth: 1,
                    pointRadius: 0
                }]
            },
            options: {
                animation: false,
                parsing: false,
                normalized: true
            }
        });
    } else {
        // Update existing chart
        currentChart.data.datasets[0].data = chunk.data;
        currentChart.update('none');
    }
}
```

## Example 2: Memory Management

This example shows how to implement efficient memory management for charts.

### Flask Implementation
```python
@app.route('/api/memory-efficient-data')
def memory_efficient_data():
    # Use generators for memory efficiency
    def generate_data_stream():
        for i in range(10000):
            yield {
                'x': i,
                'y': calculate_value(i)
            }
    
    # Stream response for large datasets
    return Response(
        stream_with_context(generate_json_stream(generate_data_stream())),
        mimetype='application/json'
    )

def generate_json_stream(data_generator):
    """Generate JSON stream for memory efficiency"""
    yield '{"data":['
    
    first = True
    for item in data_generator:
        if not first:
            yield ','
        yield json.dumps(item)
        first = False
    
    yield ']}'
```

### Memory Management Configuration
```javascript
class ChartMemoryManager {
    constructor(chartId, options = {}) {
        this.chartId = chartId;
        this.maxDataPoints = options.maxDataPoints || 10000;
        this.chart = null;
        this.dataBuffer = [];
    }
    
    initialize() {
        // Clean up existing chart if any
        if (this.chart) {
            this.chart.destroy();
        }
        
        // Initialize with empty data
        this.chart = new Chart(this.chartId, {
            type: 'line',
            data: {
                datasets: [{
                    data: [],
                    borderWidth: 1,
                    pointRadius: 0
                }]
            },
            options: {
                animation: false,
                parsing: false,
                normalized: true
            }
        });
        
        // Setup data streaming
        this.setupDataStream();
    }
    
    setupDataStream() {
        const reader = new ReadableStreamDefaultReader(
            fetch('/api/memory-efficient-data').body
        );
        
        this.processStreamData(reader);
    }
    
    async processStreamData(reader) {
        try {
            while (true) {
                const {value, done} = await reader.read();
                if (done) break;
                
                // Process chunk
                const chunk = JSON.parse(value);
                this.addData(chunk);
            }
        } finally {
            reader.releaseLock();
        }
    }
    
    addData(data) {
        // Add to buffer
        this.dataBuffer.push(data);
        
        // Maintain buffer size
        if (this.dataBuffer.length > this.maxDataPoints) {
            this.dataBuffer.shift();
        }
        
        // Update chart efficiently
        if (this.dataBuffer.length % 100 === 0) {  // Batch updates
            this.updateChart();
        }
    }
    
    updateChart() {
        if (!this.chart) return;
        
        this.chart.data.datasets[0].data = this.dataBuffer;
        this.chart.update('none');
    }
    
    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
        this.dataBuffer = [];
    }
}
```

## Example 3: WebWorker Implementation

This example demonstrates how to use WebWorkers for data processing.

### Flask Implementation
```python
@app.route('/api/worker-data')
def worker_data():
    data = {
        'raw_data': generate_raw_data(),
        'processing_params': {
            'smoothing_factor': 0.1,
            'threshold': 50
        }
    }
    return jsonify(data)
```

### WebWorker Configuration
```javascript
// dataWorker.js
self.onmessage = function(e) {
    const { data, params } = e.data;
    
    // Process data in background
    const processed = processData(data, params);
    
    // Send back processed data
    self.postMessage(processed);
};

function processData(data, params) {
    // Implement data processing logic
    return data.map(point => ({
        x: point.x,
        y: applyProcessing(point.y, params)
    }));
}

// Main script
const worker = new Worker('dataWorker.js');
let chart;

worker.onmessage = function(e) {
    const processedData = e.data;
    
    if (!chart) {
        initializeChart(processedData);
    } else {
        updateChart(processedData);
    }
};

async function loadAndProcessData() {
    const response = await fetch('/api/worker-data');
    const data = await response.json();
    
    // Send data to worker for processing
    worker.postMessage({
        data: data.raw_data,
        params: data.processing_params
    });
}
```

## Working with Database Data

Here's how to implement efficient database queries and data handling:

```python
class ChartData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True)
    value = db.Column(db.Float)
    
    @staticmethod
    def get_optimized_data(start_date, end_date, resolution):
        """
        Get data with optimized resolution based on date range
        """
        date_range = end_date - start_date
        
        if date_range.days > 30:
            # Use daily aggregation for longer ranges
            return db.session.query(
                func.date(ChartData.timestamp),
                func.avg(ChartData.value)
            ).filter(
                ChartData.timestamp.between(start_date, end_date)
            ).group_by(
                func.date(ChartData.timestamp)
            ).all()
        else:
            # Use hourly aggregation for shorter ranges
            return db.session.query(
                func.date_trunc('hour', ChartData.timestamp),
                func.avg(ChartData.value)
            ).filter(
                ChartData.timestamp.between(start_date, end_date)
            ).group_by(
                func.date_trunc('hour', ChartData.timestamp)
            ).all()

@app.route('/api/optimized-db-data')
def get_optimized_db_data():
    start_date = request.args.get('start_date', type=lambda x: datetime.fromisoformat(x))
    end_date = request.args.get('end_date', type=lambda x: datetime.fromisoformat(x))
    resolution = request.args.get('resolution', type=int, default=100)
    
    data = ChartData.get_optimized_data(start_date, end_date, resolution)
    
    return jsonify({
        'labels': [d[0].isoformat() for d in data],
        'values': [float(d[1]) for d in data]
    })
```

This documentation provides three distinct examples of Chart.js performance optimization with varying complexity and features. Each example demonstrates different aspects of performance optimization when integrated with Flask, from basic data optimization to advanced techniques like WebWorkers and efficient memory management.
