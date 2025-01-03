# Highcharts with PHP Examples

## Table of Contents
- [Highcharts with PHP Examples](#highcharts-with-php-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Examples](#basic-examples)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Charts
   - Line charts with real-time updates
   - Bar charts with database integration
   - Pie charts with dynamic data
   - Area charts with time series

2. Advanced Features
   - Stock charts with technical indicators
   - 3D visualizations
   - Drilldown capabilities
   - Export functionality

3. Data Integration
   - PDO database integration
   - REST API endpoints
   - WebSocket real-time updates
   - CSV/JSON data import

4. Full Applications
   - Financial dashboard
   - Analytics platform
   - Stock market monitor
   - Data visualization tool

## Project Structure

```
php/
├── basic/
│   ├── line_chart/
│   │   ├── index.php
│   │   ├── composer.json
│   │   └── templates/
│   │       └── chart.php
│   ├── bar_chart/
│   ├── pie_chart/
│   └── area_chart/
├── advanced/
│   ├── stock_charts/
│   ├── 3d_charts/
│   ├── drilldown/
│   └── export/
├── integration/
│   ├── database/
│   ├── api/
│   ├── websocket/
│   └── data_import/
└── applications/
    ├── financial_dashboard/
    ├── analytics/
    ├── stock_monitor/
    └── visualization/
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
    DocumentRoot "/path/to/examples/highcharts/php"
    <Directory "/path/to/examples/highcharts/php">
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

### Real-time Line Chart
```php
<?php
// index.php
require 'vendor/autoload.php';

class DataController {
    public function getData() {
        return [
            'timestamp' => date('H:i:s'),
            'value' => rand(0, 100)
        ];
    }
}

// Handle AJAX request
if (isset($_GET['action']) && $_GET['action'] === 'getData') {
    $controller = new DataController();
    header('Content-Type: application/json');
    echo json_encode($controller->getData());
    exit;
}
?>

<!-- Template -->
<!DOCTYPE html>
<html>
<head>
    <title>Highcharts Example</title>
    <script src="https://code.highcharts.com/highcharts.js"></script>
    <script src="https://code.highcharts.com/modules/data.js"></script>
    <script src="https://code.highcharts.com/modules/exporting.js"></script>
</head>
<body>
    <div id="chart"></div>
    
    <script>
        const chart = Highcharts.chart('chart', {
            chart: {
                type: 'line',
                events: {
                    load: function() {
                        const series = this.series[0];
                        setInterval(() => {
                            fetch('index.php?action=getData')
                                .then(response => response.json())
                                .then(data => {
                                    series.addPoint([
                                        data.timestamp,
                                        data.value
                                    ], true, series.data.length > 20);
                                });
                        }, 1000);
                    }
                }
            },
            title: {
                text: 'Real-time Data'
            },
            xAxis: {
                type: 'category'
            },
            series: [{
                name: 'Value',
                data: []
            }]
        });
    </script>
</body>
</html>
```

### Database Integration
```php
<?php
class StockData {
    private $pdo;
    
    public function __construct() {
        $this->pdo = new PDO(
            'mysql:host=localhost;dbname=stocks',
            'user',
            'password',
            [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
        );
    }
    
    public function getStockData($symbol) {
        // Get last 30 days of data
        $stmt = $this->pdo->prepare("
            SELECT DATE(timestamp) as date, price
            FROM stock_prices
            WHERE symbol = ?
            AND timestamp >= DATE_SUB(NOW(), INTERVAL 30 DAY)
            ORDER BY timestamp
        ");
        
        $stmt->execute([$symbol]);
        $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
        
        return array_map(function($row) {
            return [
                strtotime($row['date']) * 1000, // Convert to milliseconds
                floatval($row['price'])
            ];
        }, $data);
    }
}

// Handle API request
if (isset($_GET['symbol'])) {
    $stockData = new StockData();
    header('Content-Type: application/json');
    echo json_encode([
        'data' => $stockData->getStockData($_GET['symbol'])
    ]);
    exit;
}
?>
```

## Advanced Features

### Stock Chart with Technical Indicators
```php
<?php
class TechnicalAnalysis {
    public function calculateSMA($data, $period = 20) {
        $result = [];
        for ($i = $period - 1; $i < count($data); $i++) {
            $sum = 0;
            for ($j = 0; $j < $period; $j++) {
                $sum += $data[$i - $j][1];
            }
            $result[] = [
                $data[$i][0],
                $sum / $period
            ];
        }
        return $result;
    }
    
    public function calculateBollingerBands($data, $period = 20) {
        $sma = $this->calculateSMA($data, $period);
        $bands = [];
        
        for ($i = $period - 1; $i < count($data); $i++) {
            $sum = 0;
            for ($j = 0; $j < $period; $j++) {
                $sum += pow($data[$i - $j][1] - $sma[$i - $period + 1][1], 2);
            }
            $stdDev = sqrt($sum / $period);
            $bands[] = [
                $data[$i][0],
                $sma[$i - $period + 1][1] + (2 * $stdDev),
                $sma[$i - $period + 1][1] - (2 * $stdDev)
            ];
        }
        
        return $bands;
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
use React\EventLoop\Factory;

class StockWebSocket implements MessageComponentInterface {
    protected $clients;
    
    public function __construct() {
        $this->clients = new \SplObjectStorage;
    }
    
    public function onMessage(ConnectionInterface $from, $msg) {
        $data = json_decode($msg);
        if ($data->action === 'subscribe') {
            // Start sending real-time updates
            $this->startUpdates($from, $data->symbol);
        }
    }
    
    protected function startUpdates($client, $symbol) {
        $loop = Factory::create();
        $loop->addPeriodicTimer(1, function() use ($client, $symbol) {
            $price = $this->getRealtimePrice($symbol);
            $client->send(json_encode([
                'symbol' => $symbol,
                'price' => $price,
                'timestamp' => time()
            ]));
        });
    }
}

$server = IoServer::factory(
    new HttpServer(
        new WsServer(
            new StockWebSocket()
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
class Validator {
    public static function validateSymbol($symbol) {
        if (!preg_match('/^[A-Z]{1,5}$/', $symbol)) {
            throw new InvalidArgumentException('Invalid symbol format');
        }
        return $symbol;
    }
    
    public static function validateDateRange($start, $end) {
        $startDate = DateTime::createFromFormat('Y-m-d', $start);
        $endDate = DateTime::createFromFormat('Y-m-d', $end);
        
        if (!$startDate || !$endDate || $startDate > $endDate) {
            throw new InvalidArgumentException('Invalid date range');
        }
        
        return [$startDate, $endDate];
    }
}

// Usage
try {
    $symbol = Validator::validateSymbol($_GET['symbol']);
    $data = getStockData($symbol);
} catch (InvalidArgumentException $e) {
    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
    exit;
}
?>
```

2. Rate Limiting:
```php
<?php
class RateLimiter {
    private $redis;
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379);
    }
    
    public function checkLimit($ip, $limit = 100, $period = 3600) {
        $key = "rate_limit:$ip";
        $current = $this->redis->incr($key);
        
        if ($current === 1) {
            $this->redis->expire($key, $period);
        }
        
        return $current <= $limit;
    }
}

// Usage
$limiter = new RateLimiter();
if (!$limiter->checkLimit($_SERVER['REMOTE_ADDR'])) {
    http_response_code(429);
    echo json_encode(['error' => 'Rate limit exceeded']);
    exit;
}
?>
```

## Performance Optimization

1. Data Aggregation:
```php
<?php
class DataAggregator {
    private $pdo;
    
    public function getAggregatedData($symbol, $interval) {
        $query = "
            SELECT 
                DATE_FORMAT(timestamp, ?) as period,
                AVG(price) as avg_price,
                MAX(price) as high_price,
                MIN(price) as low_price
            FROM stock_prices
            WHERE symbol = ?
            GROUP BY period
            ORDER BY period
        ";
        
        $stmt = $this->pdo->prepare($query);
        $stmt->execute([$interval, $symbol]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
?>
```

2. Caching:
```php
<?php
class ChartCache {
    private $redis;
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379);
    }
    
    public function getData($key) {
        if ($data = $this->redis->get($key)) {
            return json_decode($data, true);
        }
        return null;
    }
    
    public function setData($key, $data, $ttl = 300) {
        $this->redis->setex($key, $ttl, json_encode($data));
    }
}
?>
```

## Testing

1. Unit Tests:
```php
<?php
use PHPUnit\Framework\TestCase;

class HighchartsTest extends TestCase {
    private $controller;
    
    protected function setUp(): void {
        $this->controller = new ChartController();
    }
    
    public function testDataFormat() {
        $data = $this->controller->getData('AAPL');
        $this->assertArrayHasKey('data', $data);
        $this->assertIsArray($data['data']);
    }
}
?>
```

2. Integration Tests:
```php
<?php
class WebSocketTest extends TestCase {
    public function testRealtimeUpdates() {
        $client = new WebSocketClient('ws://localhost:8080');
        
        $client->send(json_encode([
            'action' => 'subscribe',
            'symbol' => 'AAPL'
        ]));
        
        $response = json_decode($client->receive(), true);
        $this->assertArrayHasKey('price', $response);
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
