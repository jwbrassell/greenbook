# Chart.js Testing with Flask

## Table of Contents
- [Chart.js Testing with Flask](#chartjs-testing-with-flask)
  - [Table of Contents](#table-of-contents)
  - [Basic Test Implementation](#basic-test-implementation)
    - [Flask Test Setup](#flask-test-setup)
    - [JavaScript Test Setup](#javascript-test-setup)
  - [Example 1: Integration Testing](#example-1:-integration-testing)
    - [Flask Integration Tests](#flask-integration-tests)
    - [JavaScript Integration Tests](#javascript-integration-tests)
  - [Example 2: Unit Testing Chart Components](#example-2:-unit-testing-chart-components)
    - [Flask Unit Tests](#flask-unit-tests)
    - [JavaScript Unit Tests](#javascript-unit-tests)
  - [Example 3: End-to-End Testing](#example-3:-end-to-end-testing)
    - [Flask E2E Test Setup](#flask-e2e-test-setup)
    - [JavaScript E2E Tests](#javascript-e2e-tests)
  - [Working with Test Data](#working-with-test-data)



Testing Chart.js visualizations in a Flask application involves multiple testing layers to ensure both backend data processing and frontend rendering work correctly. This guide demonstrates how to implement comprehensive testing for Chart.js integrations.

## Basic Test Implementation

### Flask Test Setup
```python
import unittest
from flask import Flask, json
from flask_testing import TestCase
from your_app import app, db

class ChartTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app
    
    def setUp(self):
        db.create_all()
        self.sample_data = {
            'labels': ['Jan', 'Feb', 'Mar'],
            'datasets': [{
                'label': 'Test Dataset',
                'data': [10, 20, 30]
            }]
        }
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_chart_data_endpoint(self):
        """Test chart data API endpoint"""
        response = self.client.get('/api/chart-data')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('labels', data)
        self.assertIn('datasets', data)
        
        # Validate data structure
        self.assertIsInstance(data['labels'], list)
        self.assertIsInstance(data['datasets'], list)
        self.assertTrue(len(data['datasets']) > 0)
        
        # Validate dataset structure
        dataset = data['datasets'][0]
        self.assertIn('label', dataset)
        self.assertIn('data', dataset)
        self.assertIsInstance(dataset['data'], list)
```

### JavaScript Test Setup
```javascript
// test/chart.test.js
import { expect } from 'chai';
import { JSDOM } from 'jsdom';
import Chart from 'chart.js';

describe('Chart Rendering', () => {
    let dom;
    let document;
    let window;
    
    beforeEach(() => {
        dom = new JSDOM('<!DOCTYPE html><canvas id="testChart"></canvas>');
        document = dom.window.document;
        window = dom.window;
        
        // Mock Canvas context
        window.HTMLCanvasElement.prototype.getContext = () => ({
            // Minimal mock implementation
            clearRect: () => {},
            beginPath: () => {},
            moveTo: () => {},
            lineTo: () => {},
            stroke: () => {}
        });
    });
    
    it('should create chart with correct configuration', () => {
        const ctx = document.getElementById('testChart');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Jan', 'Feb', 'Mar'],
                datasets: [{
                    label: 'Test Data',
                    data: [10, 20, 30]
                }]
            }
        });
        
        expect(chart.config.type).to.equal('line');
        expect(chart.data.labels).to.have.lengthOf(3);
        expect(chart.data.datasets[0].data).to.have.lengthOf(3);
    });
});
```

## Example 1: Integration Testing

This example demonstrates how to implement integration tests for Chart.js and Flask.

### Flask Integration Tests
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ChartIntegrationTest(TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()  # or webdriver.Chrome()
        self.driver.implicitly_wait(10)
        
        # Setup test data
        self.setup_test_data()
    
    def tearDown(self):
        self.driver.quit()
        self.cleanup_test_data()
    
    def test_chart_rendering(self):
        """Test that chart renders correctly with data"""
        self.driver.get(self.get_server_url() + '/chart')
        
        # Wait for chart canvas to be present
        canvas = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myChart'))
        )
        
        # Verify chart dimensions
        self.assertGreater(canvas.size['width'], 0)
        self.assertGreater(canvas.size['height'], 0)
        
        # Verify chart data through API
        response = self.client.get('/api/chart-data')
        data = json.loads(response.data)
        
        # Execute JavaScript to get chart instance data
        chart_data = self.driver.execute_script(
            'return document.getElementById("myChart").__chart__.data'
        )
        
        # Compare API data with rendered chart data
        self.assertEqual(
            len(data['datasets'][0]['data']),
            len(chart_data['datasets'][0]['data'])
        )
    
    def test_chart_interactivity(self):
        """Test chart interactive features"""
        self.driver.get(self.get_server_url() + '/chart')
        
        # Wait for chart to be ready
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, 'myChart'))
        )
        
        # Simulate click on chart
        canvas = self.driver.find_element(By.ID, 'myChart')
        action = webdriver.ActionChains(self.driver)
        action.move_to_element_with_offset(canvas, 100, 100).click().perform()
        
        # Verify tooltip or click handler response
        tooltip = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'chartjs-tooltip'))
        )
        self.assertTrue(tooltip.is_displayed())
```

### JavaScript Integration Tests
```javascript
// test/integration.test.js
describe('Chart Integration', () => {
    let page;
    
    before(async () => {
        page = await browser.newPage();
    });
    
    after(async () => {
        await page.close();
    });
    
    it('should load and render chart', async () => {
        await page.goto('http://localhost:5000/chart');
        
        // Wait for chart to be rendered
        await page.waitForSelector('canvas#myChart');
        
        // Verify chart is properly initialized
        const chartInitialized = await page.evaluate(() => {
            const chart = Chart.getChart('myChart');
            return chart !== undefined;
        });
        
        expect(chartInitialized).to.be.true;
    });
    
    it('should update chart with new data', async () => {
        await page.goto('http://localhost:5000/chart');
        
        // Click update button
        await page.click('#updateChart');
        
        // Verify chart data is updated
        const newData = await page.evaluate(() => {
            const chart = Chart.getChart('myChart');
            return chart.data.datasets[0].data;
        });
        
        expect(newData).to.have.lengthOf.above(0);
    });
});
```

## Example 2: Unit Testing Chart Components

This example shows how to implement unit tests for individual chart components.

### Flask Unit Tests
```python
class ChartDataProcessingTest(unittest.TestCase):
    def setUp(self):
        self.processor = ChartDataProcessor()
    
    def test_data_formatting(self):
        """Test data formatting for chart consumption"""
        raw_data = [
            {'date': '2023-01-01', 'value': 10},
            {'date': '2023-01-02', 'value': 20}
        ]
        
        formatted = self.processor.format_for_chart(raw_data)
        
        self.assertIn('labels', formatted)
        self.assertIn('datasets', formatted)
        self.assertEqual(len(formatted['labels']), 2)
        self.assertEqual(
            formatted['datasets'][0]['data'],
            [10, 20]
        )
    
    def test_data_aggregation(self):
        """Test data aggregation functions"""
        data = [1, 2, 3, 4, 5]
        
        result = self.processor.aggregate_data(data, 'avg')
        self.assertEqual(result, 3)
        
        result = self.processor.aggregate_data(data, 'sum')
        self.assertEqual(result, 15)
    
    def test_invalid_data_handling(self):
        """Test handling of invalid data"""
        invalid_data = [
            {'date': 'invalid', 'value': 'not_number'}
        ]
        
        with self.assertRaises(ValueError):
            self.processor.format_for_chart(invalid_data)
```

### JavaScript Unit Tests
```javascript
// test/chart-components.test.js
describe('Chart Components', () => {
    describe('DataFormatter', () => {
        const formatter = new DataFormatter();
        
        it('should format data correctly', () => {
            const rawData = [
                { x: 1, y: 10 },
                { x: 2, y: 20 }
            ];
            
            const formatted = formatter.format(rawData);
            
            expect(formatted.labels).to.deep.equal([1, 2]);
            expect(formatted.datasets[0].data).to.deep.equal([10, 20]);
        });
        
        it('should handle missing values', () => {
            const rawData = [
                { x: 1, y: null },
                { x: 2, y: 20 }
            ];
            
            const formatted = formatter.format(rawData);
            
            expect(formatted.datasets[0].data).to.deep.equal([0, 20]);
        });
    });
    
    describe('ChartOptions', () => {
        it('should generate correct options', () => {
            const options = new ChartOptions({
                title: 'Test Chart',
                yAxisLabel: 'Values'
            });
            
            const config = options.generate();
            
            expect(config.plugins.title.text).to.equal('Test Chart');
            expect(config.scales.y.title.text).to.equal('Values');
        });
    });
});
```

## Example 3: End-to-End Testing

This example demonstrates how to implement end-to-end tests for Chart.js applications.

### Flask E2E Test Setup
```python
from playwright.sync_api import sync_playwright

class ChartE2ETest(unittest.TestCase):
    def setUp(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page()
        
        # Start Flask server
        self.server_thread = threading.Thread(
            target=app.run,
            kwargs={'port': 5000}
        )
        self.server_thread.daemon = True
        self.server_thread.start()
    
    def tearDown(self):
        self.page.close()
        self.browser.close()
        self.playwright.stop()
    
    def test_chart_workflow(self):
        """Test complete chart workflow"""
        # Navigate to chart page
        self.page.goto('http://localhost:5000/chart')
        
        # Wait for chart to load
        self.page.wait_for_selector('canvas#myChart')
        
        # Interact with chart controls
        self.page.click('#dateRange')
        self.page.click('text=Last 7 Days')
        
        # Verify chart updates
        self.assertTrue(
            self.page.wait_for_selector('.chart-tooltip')
        )
        
        # Test export functionality
        self.page.click('#exportChart')
        
        # Verify download
        download = self.page.wait_for_download()
        self.assertTrue(download.path().endswith('.png'))
```

### JavaScript E2E Tests
```javascript
// test/e2e.test.js
describe('Chart E2E', () => {
    let browser;
    let page;
    
    before(async () => {
        browser = await puppeteer.launch();
        page = await browser.newPage();
    });
    
    after(async () => {
        await browser.close();
    });
    
    it('should complete full chart workflow', async () => {
        await page.goto('http://localhost:5000/chart');
        
        // Wait for initial render
        await page.waitForSelector('canvas#myChart');
        
        // Test data loading
        const initialData = await page.evaluate(() => {
            const chart = Chart.getChart('myChart');
            return chart.data.datasets[0].data;
        });
        expect(initialData).to.have.lengthOf.above(0);
        
        // Test interactions
        await page.click('#updateData');
        await page.waitForTimeout(1000);  // Wait for animation
        
        const updatedData = await page.evaluate(() => {
            const chart = Chart.getChart('myChart');
            return chart.data.datasets[0].data;
        });
        expect(updatedData).to.not.deep.equal(initialData);
        
        // Test export
        const downloadPromise = page.waitForDownload();
        await page.click('#exportChart');
        const download = await downloadPromise;
        
        expect(download.suggestedFilename()).to.match(/chart-\d+\.png$/);
    });
});
```

## Working with Test Data

Here's how to implement test data generation and management:

```python
class TestDataGenerator:
    def __init__(self):
        self.base_date = datetime.now()
    
    def generate_time_series(self, points=100, trend='random'):
        """Generate time series data for testing"""
        data = []
        
        if trend == 'random':
            values = np.random.normal(100, 15, points)
        elif trend == 'increasing':
            values = np.linspace(50, 150, points) + np.random.normal(0, 5, points)
        elif trend == 'seasonal':
            x = np.linspace(0, 4*np.pi, points)
            values = 100 + 30*np.sin(x) + np.random.normal(0, 5, points)
        
        for i in range(points):
            data.append({
                'timestamp': self.base_date + timedelta(hours=i),
                'value': float(values[i])
            })
        
        return data
    
    def generate_categorical(self, categories=5):
        """Generate categorical data for testing"""
        return {
            'labels': [f'Category {i}' for i in range(categories)],
            'values': np.random.randint(50, 150, categories).tolist()
        }

class ChartTestData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    data = db.Column(db.JSON)
    
    @classmethod
    def setup_test_data(cls):
        """Setup test data in database"""
        generator = TestDataGenerator()
        
        test_cases = [
            ('time_series_random', generator.generate_time_series()),
            ('time_series_trend', generator.generate_time_series(trend='increasing')),
            ('categorical', generator.generate_categorical())
        ]
        
        for name, data in test_cases:
            test_data = cls(name=name, data=data)
            db.session.add(test_data)
        
        db.session.commit()
```

This documentation provides three distinct examples of Chart.js testing with varying complexity and features. Each example demonstrates different aspects of testing when integrated with Flask, from basic unit tests to comprehensive end-to-end testing.
