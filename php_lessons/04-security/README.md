# PHP Security Best Practices

## Table of Contents
- [PHP Security Best Practices](#php-security-best-practices)
  - [Input Validation and Sanitization](#input-validation-and-sanitization)
    - [Input Validation](#input-validation)
    - [XSS Prevention](#xss-prevention)
  - [SQL Injection Prevention](#sql-injection-prevention)
    - [Using PDO with Prepared Statements](#using-pdo-with-prepared-statements)
  - [Password Security](#password-security)
    - [Password Hashing](#password-hashing)
  - [Session Security](#session-security)
    - [Secure Session Configuration](#secure-session-configuration)
    - [Session Hijacking Prevention](#session-hijacking-prevention)
  - [CSRF Protection](#csrf-protection)
    - [Token Generation and Validation](#token-generation-and-validation)
  - [File Upload Security](#file-upload-security)
    - [Secure File Upload Handling](#secure-file-upload-handling)
  - [Error Handling and Logging](#error-handling-and-logging)
    - [Secure Error Handling](#secure-error-handling)
  - [Security Headers](#security-headers)
    - [Implementing Security Headers](#implementing-security-headers)
  - [Best Practices Checklist](#best-practices-checklist)
  - [Next Steps](#next-steps)



This guide covers essential security practices for PHP applications.

## Input Validation and Sanitization

### Input Validation
```php
<?php
function validateInput($data, $type) {
    switch ($type) {
        case 'email':
            return filter_var($data, FILTER_VALIDATE_EMAIL);
        case 'int':
            return filter_var($data, FILTER_VALIDATE_INT);
        case 'url':
            return filter_var($data, FILTER_VALIDATE_URL);
        case 'string':
            return filter_var($data, FILTER_SANITIZE_STRING);
        default:
            return false;
    }
}

// Usage
$email = validateInput($_POST['email'], 'email');
if ($email === false) {
    die('Invalid email');
}
?>
```

### XSS Prevention
```php
<?php
// Always escape output
function e($string) {
    return htmlspecialchars($string, ENT_QUOTES, 'UTF-8');
}

// Usage in HTML
<div><?php echo e($userInput); ?></div>

// For JSON responses
header('Content-Type: application/json');
echo json_encode($data, JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT);
?>
```

## SQL Injection Prevention

### Using PDO with Prepared Statements
```php
<?php
try {
    $pdo = new PDO("mysql:host=localhost;dbname=test_db", "username", "password");
    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    
    // Prepared statement
    $stmt = $pdo->prepare("SELECT * FROM users WHERE email = :email AND status = :status");
    
    // Bind parameters
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->bindParam(':status', $status, PDO::PARAM_INT);
    
    // Execute
    $stmt->execute();
    
    // Fetch results
    $user = $stmt->fetch(PDO::FETCH_ASSOC);
} catch(PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    die("An error occurred");
}
?>
```

## Password Security

### Password Hashing
```php
<?php
// Hashing a password
function hashPassword($password) {
    return password_hash($password, PASSWORD_DEFAULT, ['cost' => 12]);
}

// Verifying a password
function verifyPassword($password, $hash) {
    return password_verify($password, $hash);
}

// Usage
$hashedPassword = hashPassword($_POST['password']);

// Later, verifying:
if (verifyPassword($_POST['password'], $userHashedPassword)) {
    // Password is correct
} else {
    // Password is incorrect
}
?>
```

## Session Security

### Secure Session Configuration
```php
<?php
// Configure session settings
ini_set('session.cookie_httponly', 1);
ini_set('session.use_only_cookies', 1);
ini_set('session.cookie_secure', 1);

// Start session
session_start();

// Regenerate session ID periodically
if (!isset($_SESSION['created'])) {
    $_SESSION['created'] = time();
} else if (time() - $_SESSION['created'] > 1800) {
    session_regenerate_id(true);
    $_SESSION['created'] = time();
}
?>
```

### Session Hijacking Prevention
```php
<?php
function isSessionValid() {
    if (!isset($_SESSION['user_agent'])) {
        $_SESSION['user_agent'] = $_SERVER['HTTP_USER_AGENT'];
        return true;
    }
    
    return $_SESSION['user_agent'] === $_SERVER['HTTP_USER_AGENT'];
}

// Usage
if (!isSessionValid()) {
    session_destroy();
    header('Location: login.php');
    exit();
}
?>
```

## CSRF Protection

### Token Generation and Validation
```php
<?php
class CSRFProtection {
    public static function generateToken() {
        if (empty($_SESSION['csrf_token'])) {
            $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        }
        return $_SESSION['csrf_token'];
    }
    
    public static function verifyToken($token) {
        if (empty($_SESSION['csrf_token']) || $token !== $_SESSION['csrf_token']) {
            throw new Exception('CSRF token validation failed');
        }
        return true;
    }
}

// Usage in form
<form method="POST">
    <input type="hidden" name="csrf_token" value="<?php echo CSRFProtection::generateToken(); ?>">
    <!-- form fields -->
</form>

// Validation in form handler
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    try {
        CSRFProtection::verifyToken($_POST['csrf_token']);
        // Process form
    } catch (Exception $e) {
        die($e->getMessage());
    }
}
?>
```

## File Upload Security

### Secure File Upload Handling
```php
<?php
class FileUploader {
    private $allowedTypes = ['jpg', 'jpeg', 'png', 'gif'];
    private $maxSize = 5242880; // 5MB
    private $uploadDir = 'uploads/';
    
    public function upload($file) {
        // Check file size
        if ($file['size'] > $this->maxSize) {
            throw new Exception('File is too large');
        }
        
        // Check file type
        $ext = strtolower(pathinfo($file['name'], PATHINFO_EXTENSION));
        if (!in_array($ext, $this->allowedTypes)) {
            throw new Exception('Invalid file type');
        }
        
        // Generate safe filename
        $filename = bin2hex(random_bytes(16)) . '.' . $ext;
        
        // Move file to upload directory
        if (!move_uploaded_file($file['tmp_name'], $this->uploadDir . $filename)) {
            throw new Exception('Failed to move uploaded file');
        }
        
        return $filename;
    }
}

// Usage
try {
    $uploader = new FileUploader();
    $filename = $uploader->upload($_FILES['profile_pic']);
    echo "File uploaded successfully: " . $filename;
} catch (Exception $e) {
    echo "Upload failed: " . $e->getMessage();
}
?>
```

## Error Handling and Logging

### Secure Error Handling
```php
<?php
// Production error handling
error_reporting(E_ALL);
ini_set('display_errors', 0);
ini_set('log_errors', 1);
ini_set('error_log', '/path/to/error.log');

// Custom error handler
function customErrorHandler($errno, $errstr, $errfile, $errline) {
    $message = date('Y-m-d H:i:s') . " Error [$errno]: $errstr in $errfile on line $errline\n";
    error_log($message);
    
    // Show generic error message to user
    if (error_reporting()) {
        echo "An error occurred. Please try again later.";
    }
    
    return true;
}

set_error_handler('customErrorHandler');
?>
```

## Security Headers

### Implementing Security Headers
```php
<?php
// Set security headers
header("Content-Security-Policy: default-src 'self'");
header("X-Frame-Options: DENY");
header("X-Content-Type-Options: nosniff");
header("X-XSS-Protection: 1; mode=block");
header("Referrer-Policy: strict-origin-when-cross-origin");
header("Strict-Transport-Security: max-age=31536000; includeSubDomains");
?>
```

## Best Practices Checklist

1. **Input/Output Security**
   - Validate all input data
   - Sanitize output data
   - Use prepared statements
   - Implement CSRF protection

2. **Authentication & Authorization**
   - Use secure password hashing
   - Implement proper session management
   - Use role-based access control
   - Implement rate limiting

3. **File Operations**
   - Validate file uploads
   - Use secure file permissions
   - Sanitize file names
   - Limit file sizes

4. **Configuration**
   - Use HTTPS
   - Set secure headers
   - Configure error handling
   - Implement logging

5. **Database Security**
   - Use prepared statements
   - Encrypt sensitive data
   - Limit database permissions
   - Regular backups

## Next Steps
- Implement user authentication system
- Set up logging and monitoring
- Configure web application firewall
- Regular security audits
