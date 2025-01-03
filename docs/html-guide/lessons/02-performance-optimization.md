# HTML Performance Optimization and Monitoring

## Overview

This lesson focuses on HTML performance optimization techniques and monitoring strategies, particularly relevant for performance engineers and system administrators. We'll explore how HTML structure affects page load times, rendering performance, and resource utilization.

## Performance Metrics

### Key Performance Indicators (KPIs)
```python
# Example Python script for collecting performance metrics
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def measure_page_metrics(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    # Navigation Timing API metrics
    timing = driver.execute_script("return window.performance.timing")
    
    metrics = {
        'dns_lookup': timing['domainLookupEnd'] - timing['domainLookupStart'],
        'tcp_connection': timing['connectEnd'] - timing['connectStart'],
        'ttfb': timing['responseStart'] - timing['requestStart'],
        'dom_interactive': timing['domInteractive'] - timing['navigationStart'],
        'dom_complete': timing['domComplete'] - timing['navigationStart']
    }
    
    driver.quit()
    return metrics
```

## HTML Structure Impact on Performance

### Inefficient Structure
```html
<!-- Anti-pattern: Deeply nested elements -->
<div>
    <div>
        <div>
            <div>
                <p>Deeply nested content</p>
            </div>
        </div>
    </div>
</div>

<!-- Anti-pattern: Inline styles and scripts -->
<div style="complex styles">
    <script>complex JavaScript</script>
</div>
```

### Optimized Structure
```html
<!-- Efficient: Flat hierarchy -->
<main>
    <section class="content">
        <p>Content with minimal nesting</p>
    </section>
</main>

<!-- Efficient: External resources with proper loading attributes -->
<link rel="stylesheet" href="styles.css">
<script src="script.js" defer></script>
```

## Resource Loading Optimization

### Preloading Critical Resources
```html
<head>
    <!-- Preload critical CSS -->
    <link rel="preload" href="critical.css" as="style">
    
    <!-- Preload important fonts -->
    <link rel="preload" href="font.woff2" as="font" crossorigin>
    
    <!-- Prefetch likely next-page resources -->
    <link rel="prefetch" href="next-page.html">
</head>
```

### Lazy Loading
```html
<!-- Images -->
<img src="large-image.jpg" loading="lazy" alt="Description">

<!-- iframes -->
<iframe src="widget.html" loading="lazy"></iframe>
```

## Monitoring Implementation

### Performance Observer
```html
<script>
// Create performance observer
const observer = new PerformanceObserver((list) => {
    list.getEntries().forEach((entry) => {
        // Log performance metrics
        console.log(`${entry.name}: ${entry.startTime}ms`);
        
        // Send to monitoring system
        sendToMonitoring({
            metric: entry.name,
            value: entry.startTime,
            timestamp: Date.now()
        });
    });
});

// Observe specific performance entries
observer.observe({
    entryTypes: ['navigation', 'resource', 'paint', 'layout-shift']
});

// Function to send metrics to monitoring system
function sendToMonitoring(data) {
    fetch('/metrics', {
        method: 'POST',
        body: JSON.stringify(data)
    });
}
</script>
```

### Real User Monitoring (RUM)
```html
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Collect navigation timing metrics
    const navigationTiming = performance.getEntriesByType('navigation')[0];
    
    // Collect resource timing metrics
    const resourceTiming = performance.getEntriesByType('resource');
    
    // Collect Core Web Vitals
    const cls = getCumulativeLayoutShift();
    const lcp = getLargestContentfulPaint();
    const fid = getFirstInputDelay();
    
    // Send metrics to analytics
    sendAnalytics({
        pageLoad: navigationTiming.duration,
        resourceCount: resourceTiming.length,
        coreWebVitals: { cls, lcp, fid }
    });
});
</script>
```

## Performance Testing Tools

### Lighthouse CLI Integration
```bash
# Install Lighthouse
npm install -g lighthouse

# Run performance audit
lighthouse https://example.com --output json --output html --output-path ./audit
```

### Python-based Performance Testing
```python
import asyncio
from pyppeteer import launch

async def measure_performance(url):
    browser = await launch()
    page = await browser.newPage()
    
    # Enable performance metrics
    await page.setRequestInterception(True)
    
    metrics = []
    page.on('request', lambda req: 
        metrics.append({
            'url': req.url,
            'resourceType': req.resourceType,
            'timestamp': time.time()
        })
    )
    
    # Navigate and collect metrics
    response = await page.goto(url)
    performance_metrics = await page.metrics()
    
    await browser.close()
    return performance_metrics

# Run performance test
metrics = asyncio.get_event_loop().run_until_complete(
    measure_performance('https://example.com')
)
```

## Optimization Techniques

### Critical CSS Extraction
```python
from bs4 import BeautifulSoup
import requests

def extract_critical_css(url):
    # Fetch page content
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all CSS rules
    styles = soup.find_all('style')
    linked_css = soup.find_all('link', rel='stylesheet')
    
    # Extract and minimize critical CSS
    critical_css = []
    for style in styles:
        # Process inline styles
        critical_css.append(style.string)
    
    for link in linked_css:
        # Fetch and process external CSS
        css_response = requests.get(link['href'])
        critical_css.append(css_response.text)
    
    return '\n'.join(critical_css)
```

### Resource Hints Generator
```python
def generate_resource_hints(urls):
    hints = []
    for url in urls:
        if url.endswith(('.css', '.js')):
            hints.append(f'<link rel="preload" href="{url}" as="style">')
        elif url.endswith(('.jpg', '.png', '.webp')):
            hints.append(f'<link rel="prefetch" href="{url}">')
    return '\n'.join(hints)
```

## Monitoring Dashboard Example

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Performance Dashboard</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="metrics-dashboard">
        <div id="page-load-chart"></div>
        <div id="resource-timing-chart"></div>
        <div id="web-vitals-chart"></div>
    </div>
    
    <script>
    class PerformanceDashboard {
        constructor() {
            this.metrics = [];
            this.initializeObserver();
        }
        
        initializeObserver() {
            const observer = new PerformanceObserver((list) => {
                const entries = list.getEntries();
                this.processEntries(entries);
            });
            
            observer.observe({
                entryTypes: ['navigation', 'resource', 'paint']
            });
        }
        
        processEntries(entries) {
            entries.forEach(entry => {
                this.metrics.push({
                    name: entry.name,
                    type: entry.entryType,
                    duration: entry.duration,
                    timestamp: Date.now()
                });
            });
            
            this.updateCharts();
        }
        
        updateCharts() {
            // Implementation for updating charts with Plotly
            // This would create time-series visualizations of the metrics
        }
    }
    
    // Initialize dashboard
    const dashboard = new PerformanceDashboard();
    </script>
</body>
</html>
```

## Practical Exercises

1. **Performance Audit**
   - Run Lighthouse audits on your web pages
   - Analyze Core Web Vitals
   - Implement recommended optimizations
   - Measure improvement

2. **Resource Loading Analysis**
   ```python
   # Analyze resource loading patterns
   async def analyze_resources(url):
       browser = await launch()
       page = await browser.newPage()
       
       resources = []
       page.on('request', lambda req: resources.append(req))
       
       await page.goto(url)
       
       # Analyze resource timing
       timing = await page.evaluate('''() => {
           return performance.getEntriesByType('resource')
               .map(entry => ({
                   name: entry.name,
                   duration: entry.duration,
                   size: entry.transferSize
               }));
       }''')
       
       await browser.close()
       return timing
   ```

3. **Optimization Implementation**
   - Implement resource hints
   - Set up performance monitoring
   - Create performance budgets
   - Automate performance testing

## Next Steps

1. Implement continuous performance monitoring
2. Set up automated performance testing in CI/CD
3. Create custom performance metrics for your use case
4. Develop performance optimization strategies

## Additional Resources

1. [Web Vitals](https://web.dev/vitals/)
2. [Performance Testing Tools](https://github.com/topics/performance-testing)
3. [Browser Performance APIs](https://developer.mozilla.org/en-US/docs/Web/API/Performance_API)
4. [Performance Monitoring Best Practices](https://web.dev/metrics/)
