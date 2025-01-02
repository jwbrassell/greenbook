# PHP and Apache Setup Guide

## Table of Contents
- [PHP and Apache Setup Guide](#php-and-apache-setup-guide)
  - [Apache HTTP Server Setup](#apache-http-server-setup)
    - [Installing Apache](#installing-apache)
      - [On Ubuntu/Debian:](#on-ubuntu/debian:)
      - [On RHEL/CentOS:](#on-rhel/centos:)
      - [On macOS:](#on-macos:)
    - [Apache Configuration](#apache-configuration)
- [Enable PHP processing](#enable-php-processing)
- [Document root configuration](#document-root-configuration)
- [Default directory index](#default-directory-index)
  - [PHP Installation](#php-installation)
    - [Installing PHP](#installing-php)
      - [On Ubuntu/Debian:](#on-ubuntu/debian:)
      - [On RHEL/CentOS:](#on-rhel/centos:)
      - [On macOS:](#on-macos:)
    - [PHP Configuration](#php-configuration)
  - [Testing the Setup](#testing-the-setup)
  - [Development Environment](#development-environment)
    - [Recommended IDE Setup](#recommended-ide-setup)
    - [Setting Up XDebug](#setting-up-xdebug)
  - [Next Steps](#next-steps)
  - [Troubleshooting](#troubleshooting)
    - [Common Issues](#common-issues)



## Apache HTTP Server Setup

### Installing Apache

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install apache2
```

#### On RHEL/CentOS:
```bash
sudo dnf install httpd
sudo systemctl start httpd
sudo systemctl enable httpd
```

#### On macOS:
Apache comes pre-installed. Enable it with:
```bash
sudo apachectl start
```

### Apache Configuration

1. Main configuration file locations:
   - Ubuntu/Debian: `/etc/apache2/apache2.conf`
   - RHEL/CentOS: `/etc/httpd/conf/httpd.conf`
   - macOS: `/etc/apache2/httpd.conf`

2. Basic Apache configuration:
```apache
# Enable PHP processing
LoadModule php_module modules/libphp.so
AddHandler php-script .php

# Document root configuration
<Directory /var/www/html>
    Options Indexes FollowSymLinks
    AllowOverride All
    Require all granted
</Directory>

# Default directory index
DirectoryIndex index.php index.html
```

## PHP Installation

### Installing PHP

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install php php-mysql php-curl php-json php-cgi php-gd php-mbstring php-xml
```

#### On RHEL/CentOS:
```bash
sudo dnf install php php-mysqlnd php-curl php-json php-gd php-mbstring php-xml
```

#### On macOS:
PHP comes pre-installed. For the latest version, use Homebrew:
```bash
brew install php
```

### PHP Configuration

1. Main php.ini location:
   - Ubuntu/Debian: `/etc/php/8.x/apache2/php.ini`
   - RHEL/CentOS: `/etc/php.ini`
   - macOS: `/etc/php.ini` or `/usr/local/etc/php/8.x/php.ini`

2. Important PHP Configuration Settings:
```ini
; Maximum execution time of each script
max_execution_time = 30

; Maximum amount of memory a script may consume
memory_limit = 128M

; Maximum size of POST data
post_max_size = 8M

; Maximum allowed size for uploaded files
upload_max_filesize = 2M

; Display errors during development
display_errors = On
error_reporting = E_ALL

; Set timezone
date.timezone = UTC
```

## Testing the Setup

1. Create a test PHP file:
```bash
echo "<?php phpinfo(); ?>" | sudo tee /var/www/html/info.php
```

2. Access the test file in your browser:
```
http://localhost/info.php
```

## Development Environment

### Recommended IDE Setup
1. Install Visual Studio Code
2. Install PHP extensions:
   - PHP IntelliSense
   - PHP Debug
   - PHP Extension Pack

### Setting Up XDebug
1. Install XDebug:
```bash
sudo pecl install xdebug
```

2. Add to php.ini:
```ini
[XDebug]
zend_extension=xdebug.so
xdebug.mode=debug
xdebug.start_with_request=yes
xdebug.client_port=9003
```

## Next Steps
- Proceed to [CRUD Fundamentals](../02-crud/README.md)
- Set up a local development database
- Learn about PHP coding standards and best practices

## Troubleshooting

### Common Issues

1. Apache not starting:
   - Check error logs: `sudo tail -f /var/log/apache2/error.log`
   - Verify ports: `sudo netstat -tulpn | grep apache2`

2. PHP not working:
   - Verify PHP module: `apache2ctl -M | grep php`
   - Check PHP version: `php -v`

3. Permission issues:
   - Set proper ownership: `sudo chown -R www-data:www-data /var/www/html`
   - Set proper permissions: `sudo chmod -R 755 /var/www/html`
