# PHP Error Handling and Debugging

## Table of Contents
- [PHP Error Handling and Debugging](#php-error-handling-and-debugging)
  - [Error Types](#error-types)
  - [Basic Error Handling](#basic-error-handling)
    - [Error Reporting Configuration](#error-reporting-configuration)
  - [Exception Handling](#exception-handling)
    - [Try-Catch Blocks](#try-catch-blocks)
    - [Custom Exceptions](#custom-exceptions)
  - [Error Logging](#error-logging)
    - [Custom Error Handler](#custom-error-handler)
    - [Error Logging with Different Handlers](#error-logging-with-different-handlers)
  - [Debugging Techniques](#debugging-techniques)
    - [Var Dumping](#var-dumping)
    - [Debug Backtrace](#debug-backtrace)
  - [Using XDebug](#using-xdebug)
    - [Installation and Configuration](#installation-and-configuration)
    - [Basic Usage with VS Code](#basic-usage-with-vs-code)
  - [Best Practices](#best-practices)
  - [Next Steps](#next-steps)



This guide covers error handling, logging, and debugging techniques in PHP.

## Error Types

PHP has several predefined error constants:
- E_ERROR: Fatal run-time errors
- E_WARNING: Run-time warnings
- E_PARSE: Compile-time parse errors
- E_NOTICE: Run-time notices
- E_DEPRECATED: Warnings about code that will not work in future versions
- E_ALL: All errors and warnings

## Basic Error Handling

### Error Reporting Configuration
```php
<?php
// Development environment
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Production environment
ini_set('display_errors', 0);
error_reporting(E_ALL & ~E_DEPRECATED & ~E_STRICT);
ini_set('log_errors', 1);
ini_set('error_log', '/path/to/error.log');
?>
```

## Exception Handling

### Try-Catch Blocks
```php
<?php
try {
    // Code that might throw an exception
    $result = someFunction();
    if (!$result) {
        throw new Exception('Function failed');
    }
} catch (Exception $e) {
    // Handle the exception
    error_log($e->getMessage());
    // Show user-friendly message
    echo "An error occurred";
} finally {
    // Code that always runs
    cleanupResources();
}
?>
```

### Custom Exceptions
```php
<?php
class DatabaseException extends Exception {
    public function __construct($message, $code = 0, Exception $previous = null) {
        parent::__construct($message, $code, $previous);
    }
    
    public function __toString() {
        return __CLASS__ . ": [{$this->code}]: {$this->message}\n";
    }
}

class ValidationException extends Exception {
    private $field;
    
    public function __construct($message, $field = '', $code = 0, Exception $previous = null) {
        parent::__construct($message, $code, $previous);
        $this->field = $field;
    }
    
    public function getField() {
        return $this->field;
    }
}

// Usage
try {
    if (!validateEmail($email)) {
        throw new ValidationException('Invalid email format', 'email');
    }
    
    if (!$db->connect()) {
        throw new DatabaseException('Database connection failed');
    }
} catch (ValidationException $e) {
    echo "Validation error in field {$e->getField()}: {$e->getMessage()}";
} catch (DatabaseException $e) {
    error_log($e->getMessage());
    echo "Database error occurred";
} catch (Exception $e) {
    error_log($e->getMessage());
    echo "An unexpected error occurred";
}
?>
```

## Error Logging

### Custom Error Handler
```php
<?php
function customErrorHandler($errno, $errstr, $errfile, $errline) {
    $message = sprintf(
        "[%s] Error %d: %s in %s on line %d\n",
        date('Y-m-d H:i:s'),
        $errno,
        $errstr,
        $errfile,
        $errline
    );
    
    // Log error
    error_log($message, 3, "app_errors.log");
    
    // Display error based on environment
    if (ENVIRONMENT === 'development') {
        echo "<pre>$message</pre>";
    } else {
        echo "An error occurred. Please try again later.";
    }
    
    // Don't execute PHP internal error handler
    return true;
}

// Set the custom error handler
set_error_handler("customErrorHandler");
?>
```

### Error Logging with Different Handlers
```php
<?php
class Logger {
    const ERROR = 1;
    const WARNING = 2;
    const INFO = 3;
    
    private $logFile;
    private $emailTo;
    
    public function __construct($logFile, $emailTo = '') {
        $this->logFile = $logFile;
        $this->emailTo = $emailTo;
    }
    
    public function log($message, $level = self::INFO) {
        $timestamp = date('Y-m-d H:i:s');
        $levelStr = $this->getLevelString($level);
        $logMessage = "[$timestamp] [$levelStr] $message\n";
        
        // Write to file
        file_put_contents($this->logFile, $logMessage, FILE_APPEND);
        
        // Email critical errors
        if ($level === self::ERROR && $this->emailTo) {
            mail($this->emailTo, 'Critical Error', $message);
        }
    }
    
    private function getLevelString($level) {
        switch ($level) {
            case self::ERROR:
                return 'ERROR';
            case self::WARNING:
                return 'WARNING';
            case self::INFO:
                return 'INFO';
            default:
                return 'UNKNOWN';
        }
    }
}

// Usage
$logger = new Logger('/path/to/app.log', 'admin@example.com');
$logger->log('User authentication failed', Logger::WARNING);
$logger->log('Database connection failed', Logger::ERROR);
?>
```

## Debugging Techniques

### Var Dumping
```php
<?php
// Basic var_dump
var_dump($variable);

// Pretty print
echo "<pre>";
print_r($variable);
echo "</pre>";

// Debug with context
function debug($var, $context = '') {
    echo "<pre>";
    if ($context) {
        echo "<strong>$context:</strong>\n";
    }
    var_dump($var);
    echo "</pre>";
}

// Usage
debug($user, 'User Object');
?>
```

### Debug Backtrace
```php
<?php
function getDebugBacktrace() {
    $trace = debug_backtrace();
    $output = '';
    
    foreach ($trace as $t) {
        $output .= sprintf(
            "%s:%d %s%s%s()\n",
            isset($t['file']) ? $t['file'] : 'unknown',
            isset($t['line']) ? $t['line'] : 0,
            isset($t['class']) ? $t['class'] : '',
            isset($t['type']) ? $t['type'] : '',
            $t['function']
        );
    }
    
    return $output;
}

// Usage in error handler
function errorHandler($errno, $errstr, $errfile, $errline) {
    $message = "$errstr in $errfile on line $errline\n";
    $message .= "Backtrace:\n" . getDebugBacktrace();
    error_log($message);
}
?>
```

## Using XDebug

### Installation and Configuration
```ini
[xdebug]
zend_extension=xdebug.so
xdebug.mode=debug
xdebug.start_with_request=yes
xdebug.client_port=9003
xdebug.client_host=127.0.0.1
xdebug.idekey=VSCODE
```

### Basic Usage with VS Code
1. Install PHP Debug extension
2. Configure launch.json:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Listen for XDebug",
            "type": "php",
            "request": "launch",
            "port": 9003
        }
    ]
}
```

## Best Practices

1. **Error Handling**
   - Use try-catch blocks for recoverable errors
   - Create custom exceptions for specific error types
   - Never show detailed error messages to users in production
   - Always log errors with sufficient context

2. **Logging**
   - Use different log levels appropriately
   - Include timestamp and context in log messages
   - Rotate log files to manage disk space
   - Monitor logs for critical errors

3. **Debugging**
   - Use XDebug for step-by-step debugging
   - Implement comprehensive error logging
   - Create debug tools for development
   - Use version control for tracking changes

4. **Security**
   - Sanitize all output in error messages
   - Limit error details in production
   - Secure log file permissions
   - Monitor for security-related errors

## Next Steps
- Set up automated error monitoring
- Implement log rotation
- Configure error alerting
- Study debugging tools and techniques
