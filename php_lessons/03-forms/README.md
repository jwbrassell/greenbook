# Form Handling in PHP

## Table of Contents
- [Form Handling in PHP](#form-handling-in-php)
  - [Basic Form Handling](#basic-form-handling)
    - [HTML Form](#html-form)
    - [Processing Form Data](#processing-form-data)
  - [File Uploads](#file-uploads)
    - [HTML Form with File Upload](#html-form-with-file-upload)
    - [Processing File Uploads](#processing-file-uploads)
  - [AJAX Form Submission](#ajax-form-submission)
    - [HTML Form with AJAX](#html-form-with-ajax)
    - [Processing AJAX Requests](#processing-ajax-requests)
  - [Form Validation Best Practices](#form-validation-best-practices)
  - [CSRF Protection Example](#csrf-protection-example)
  - [Next Steps](#next-steps)



This guide covers form handling, data validation, and file uploads in PHP.

## Basic Form Handling

### HTML Form
```html
<!DOCTYPE html>
<html>
<head>
    <title>User Registration</title>
</head>
<body>
    <form action="process.php" method="POST">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
        </div>
        <button type="submit">Register</button>
    </form>
</body>
</html>
```

### Processing Form Data
```php
<?php
// process.php

// Check if form was submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize input data
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    $password = $_POST['password']; // Will be hashed
    
    // Validate data
    $errors = [];
    
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Valid email is required";
    }
    
    if (empty($password) || strlen($password) < 8) {
        $errors[] = "Password must be at least 8 characters";
    }
    
    // If no errors, process the data
    if (empty($errors)) {
        // Hash password
        $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
        
        // Save to database (example)
        try {
            $pdo = new PDO("mysql:host=localhost;dbname=test_db", "username", "password");
            $stmt = $pdo->prepare("INSERT INTO users (name, email, password) VALUES (?, ?, ?)");
            $stmt->execute([$name, $email, $hashedPassword]);
            
            // Redirect on success
            header("Location: success.php");
            exit();
        } catch (PDOException $e) {
            $errors[] = "Database error: " . $e->getMessage();
        }
    }
    
    // If there are errors, display them
    if (!empty($errors)) {
        foreach ($errors as $error) {
            echo "<p style='color: red;'>$error</p>";
        }
    }
}
?>
```

## File Uploads

### HTML Form with File Upload
```html
<form action="upload.php" method="POST" enctype="multipart/form-data">
    <div>
        <label for="profile_pic">Profile Picture:</label>
        <input type="file" id="profile_pic" name="profile_pic" accept="image/*">
    </div>
    <button type="submit">Upload</button>
</form>
```

### Processing File Uploads
```php
<?php
// upload.php

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Check if file was uploaded without errors
    if (isset($_FILES["profile_pic"]) && $_FILES["profile_pic"]["error"] == 0) {
        $allowed = ["jpg" => "image/jpg", "jpeg" => "image/jpeg", "gif" => "image/gif", "png" => "image/png"];
        $filename = $_FILES["profile_pic"]["name"];
        $filetype = $_FILES["profile_pic"]["type"];
        $filesize = $_FILES["profile_pic"]["size"];
    
        // Verify file extension
        $ext = pathinfo($filename, PATHINFO_EXTENSION);
        if (!array_key_exists($ext, $allowed)) {
            die("Error: Please select a valid file format.");
        }
    
        // Verify file size - 5MB maximum
        $maxsize = 5 * 1024 * 1024;
        if ($filesize > $maxsize) {
            die("Error: File size is larger than the allowed limit.");
        }
    
        // Verify MYME type of the file
        if (in_array($filetype, $allowed)) {
            // Check whether file exists before uploading it
            if (file_exists("uploads/" . $filename)) {
                echo $filename . " already exists.";
            } else {
                if (move_uploaded_file($_FILES["profile_pic"]["tmp_name"], "uploads/" . $filename)) {
                    echo "Your file was uploaded successfully.";
                } else {
                    echo "Error: There was a problem uploading your file.";
                }
            }
        } else {
            echo "Error: There was a problem uploading your file.";
        }
    } else {
        echo "Error: " . $_FILES["profile_pic"]["error"];
    }
}
?>
```

## AJAX Form Submission

### HTML Form with AJAX
```html
<!DOCTYPE html>
<html>
<head>
    <title>AJAX Form</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <form id="ajaxForm">
        <div>
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>
        </div>
        <div>
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <button type="submit">Submit</button>
    </form>
    <div id="result"></div>

    <script>
    $(document).ready(function() {
        $('#ajaxForm').on('submit', function(e) {
            e.preventDefault();
            
            $.ajax({
                type: 'POST',
                url: 'process_ajax.php',
                data: $(this).serialize(),
                dataType: 'json',
                success: function(response) {
                    if (response.success) {
                        $('#result').html('<p style="color: green;">' + response.message + '</p>');
                    } else {
                        $('#result').html('<p style="color: red;">' + response.message + '</p>');
                    }
                },
                error: function() {
                    $('#result').html('<p style="color: red;">Error processing request</p>');
                }
            });
        });
    });
    </script>
</body>
</html>
```

### Processing AJAX Requests
```php
<?php
// process_ajax.php

header('Content-Type: application/json');

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
    $email = filter_input(INPUT_POST, 'email', FILTER_SANITIZE_EMAIL);
    
    $errors = [];
    
    if (empty($name)) {
        $errors[] = "Name is required";
    }
    
    if (empty($email) || !filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Valid email is required";
    }
    
    if (empty($errors)) {
        // Process the data
        echo json_encode([
            'success' => true,
            'message' => 'Form submitted successfully'
        ]);
    } else {
        echo json_encode([
            'success' => false,
            'message' => implode(', ', $errors)
        ]);
    }
} else {
    echo json_encode([
        'success' => false,
        'message' => 'Invalid request method'
    ]);
}
?>
```

## Form Validation Best Practices

1. **Client-Side Validation**
   - Use HTML5 validation attributes (required, pattern, etc.)
   - Implement JavaScript validation for better UX
   - Remember: Client-side validation is for UX, not security

2. **Server-Side Validation**
   - Always validate on the server
   - Use PHP's filter functions
   - Implement custom validation rules
   - Sanitize all input data

3. **Security Considerations**
   - Use CSRF tokens
   - Implement rate limiting
   - Validate file uploads thoroughly
   - Use prepared statements for database operations

4. **Error Handling**
   - Display user-friendly error messages
   - Log validation failures
   - Maintain form state on error
   - Return clear error responses for AJAX requests

## CSRF Protection Example
```php
<?php
session_start();

// Generate CSRF token
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== $_SESSION['csrf_token']) {
        die('CSRF token validation failed');
    }
    
    // Process form...
}
?>

<form method="POST">
    <input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">
    <!-- form fields -->
</form>
```

## Next Steps
- Learn about session management
- Implement user authentication
- Study security best practices
- Explore API development
