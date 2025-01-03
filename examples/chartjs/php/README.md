# ChartJS with PHP Examples

## Table of Contents
- [ChartJS with PHP Examples](#chartjs-with-php-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Examples](#basic-examples)
  - [Advanced Examples](#advanced-examples)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Charts
   - Line chart with real-time updates
   - Bar chart with database integration
   - Pie chart with dynamic data
   - Area chart with date-based data

2. Advanced Features
   - Mixed chart types
   - Custom animations
   - Interactive legends
   - Responsive layouts

3. Data Integration
   - PDO database integration
   - REST API endpoints
   - WebSocket real-time updates
   - CSV/JSON data import

4. Full Applications
   - Dashboard example
   - Analytics platform
   - Data visualization tool
   - Reporting system

## Project Structure

```
php/
├── basic/
│   ├── line_chart/
│   │   ├── index.php
│   │   ├── composer.json
│   │   ├── src/
│   │   │   └── DataProvider.php
│   │   └── templates/
│   │       └── chart.php
│   ├── bar_chart/
│   ├── pie_chart/
│   └── area_chart/
├── advanced/
│   ├── mixed_charts/
│   ├── animations/
│   ├── interactions/
│   └── responsive/
├── integration/
│   ├── database_example/
│   ├── api_example/
│   ├── websocket_example/
│   └── data_import/
└── applications/
    ├── dashboard/
    ├── analytics/
    ├── visualization/
    └── reporting/
```

## Getting Started

1. Install Dependencies:
```bash
composer install
```

2. Configure Web Server:
```apache
# Apache configuration
<VirtualHost *:80>
    DocumentRoot "/path/to/examples/chartjs/php"
    <Directory "/path/to/examples/chartjs/php">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

3. Run Example:
```bash
php -S localhost:8000 -t basic/line_chart
```

## Basic Examples

### Line Chart Example
```php
<?php
// index.php
require 'vendor/autoload.php';

class DataController {
    public function getData() {
        $data = [
            'labels' => [date('H:i:s')],
            'datasets' => [[
                'label' => 'Real-time Data',
                'data' => [rand(0, 100)],
                'borderColor' => 'rgb(75, 192, 192)',
                'tension' => 0.1
            ]]
        ];
        
        header('Content-Type: application/json');
        echo json_encode($data);
    }
}

// Handle AJAX request
if (isset($_GET['action']) && $_GET['action'] === 'getData') {
    $controller = new DataController();
    $controller->getData();
    exit;
}
?>

<!-- Template -->
<!DOCTYPE html>
<html>
<head>
    <title>Line Chart Example</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <canvas id="myChart"></canvas>
    <script>
        const ctx = document.getElementById('myChart');
        const chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'Real-time Data',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            }
        });

        // Update data every second
        setInterval(() => {
            fetch('index.php?action=getData')
                .then(response => response.json())
                .then(data => {
                    chart.data.labels.push(data.labels[0]);
                    chart.data.datasets[0].data.push(data.datasets[0].data[0]);
                    if (chart.data.labels.length > 10) {
                        chart.data.labels.shift();
                        chart.data.datasets[0].data.shift();
                    }
                    chart.update();
                });
        }, 1000);
    </script>
</body>
</html>
```

### Bar Chart with Database
```php
<?php
// Database connection
$pdo = new PDO('mysql:host=localhost;dbname=test', 'user', 'password');

class ChartData {
    private $pdo;
    
    public function __construct(PDO $pdo) {
        $this->pdo = $pdo;
    }
    
    public function getData() {
        $stmt = $this->pdo->query('SELECT label, value FROM data');
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        return [
            'labels' => array_column($data, 'label'),
            'values' => array_column($data, 'value')
        ];
    }
}

$chartData = new ChartData($pdo);
$data = $chartData->getData();
?>

<!-- Template -->
<canvas id="barChart"></canvas>
<script>
new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: <?= json_encode($data['labels']) ?>,
        datasets: [{
            label: 'Values',
            data: <?= json_encode($data['values']) ?>
        }]
    }
});
</script>
```

## Advanced Examples

### Mixed Chart Types
```php
<?php
class MixedChartData {
    public function getData() {
        return [
            'labels' => ['Jan', 'Feb', 'Mar'],
            'datasets' => [
                [
                    'type' => 'line',
                    'label' => 'Line Dataset',
                    'data' => [10, 20, 15]
                ],
                [
                    'type' => 'bar',
                    'label' => 'Bar Dataset',
                    'data' => [12, 19, 17]
                ]
            ]
        ];
    }
}
?>
```

### WebSocket Integration
```php
<?php
// Using Ratchet WebSocket library
use Ratchet\Server\IoServer;
use Ratchet\Http\HttpServer;
use Ratchet\WebSocket\WsServer;

class ChartWebSocket implements MessageComponentInterface {
    protected $clients;

    public function __construct() {
        $this->clients = new \SplObjectStorage;
    }

    public function onMessage(ConnectionInterface $from, $msg) {
        foreach ($this->clients as $client) {
            $client->send(json_encode([
                'value' => rand(0, 100),
                'timestamp' => date('H:i:s')
            ]));
        }
    }
}

$server = IoServer::factory(
    new HttpServer(
        new WsServer(
            new ChartWebSocket()
        )
    ),
    8080
);

$server->run();
?>
```

## Security Considerations

1. Input Validation:
```php
<?php
class DataValidator {
    public static function validateNumeric($value) {
        if (!is_numeric($value)) {
            throw new InvalidArgumentException('Invalid numeric value');
        }
        return floatval($value);
    }
    
    public static function sanitizeString($value) {
        return htmlspecialchars(strip_tags($value));
    }
}
?>
```

2. CSRF Protection:
```php
<?php
session_start();

function generateToken() {
    return bin2hex(random_bytes(32));
}

function validateToken($token) {
    return hash_equals($_SESSION['token'], $token);
}

// Generate token
$_SESSION['token'] = generateToken();
?>
```

## Performance Optimization

1. Data Caching:
```php
<?php
class ChartCache {
    private $cache;
    
    public function __construct() {
        $this->cache = new Redis();
        $this->cache->connect('127.0.0.1', 6379);
    }
    
    public function getData($key) {
        if ($data = $this->cache->get($key)) {
            return json_decode($data, true);
        }
        return null;
    }
    
    public function setData($key, $data, $ttl = 60) {
        $this->cache->setex($key, $ttl, json_encode($data));
    }
}
?>
```

2. Query Optimization:
```php
<?php
class DataRepository {
    private $pdo;
    
    public function getAggregatedData() {
        return $this->pdo->query('
            SELECT DATE(timestamp) as date, 
                   AVG(value) as avg_value
            FROM measurements
            GROUP BY DATE(timestamp)
            ORDER BY date DESC
            LIMIT 30
        ')->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class ChartDataTest extends TestCase {
    public function testDataFormat() {
        $data = (new ChartData())->getData();
        $this->assertArrayHasKey('labels', $data);
        $this->assertArrayHasKey('datasets', $data);
    }
}
?>
```

2. Integration Tests:
```php
<?php
class DatabaseIntegrationTest extends TestCase {
    protected function setUp(): void {
        $this->pdo = new PDO('sqlite::memory:');
        // Set up test database
    }
    
    public function testDataRetrieval() {
        $repo = new DataRepository($this->pdo);
        $data = $repo->getData();
        $this->assertNotEmpty($data);
    }
}
?>
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
