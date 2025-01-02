# macOS Development Environment Setup Guide

This guide covers installation and setup of essential development tools on macOS.

## Table of Contents
- [macOS Development Environment Setup Guide](#macos-development-environment-setup-guide)
  - [Table of Contents](#table-of-contents)
  - [Homebrew](#homebrew)
    - [Installation](#installation)
    - [Common Brew Commands](#common-brew-commands)
  - [Python](#python)
    - [Installation](#installation)
- [Install latest Python version](#install-latest-python-version)
- [Verify installation](#verify-installation)
    - [Python Environment Management](#python-environment-management)
- [Install virtualenv](#install-virtualenv)
- [Create new virtual environment](#create-new-virtual-environment)
- [Activate virtual environment](#activate-virtual-environment)
- [Deactivate virtual environment](#deactivate-virtual-environment)
- [Install packages in virtual environment](#install-packages-in-virtual-environment)
- [Generate requirements.txt](#generate-requirementstxt)
- [Install from requirements.txt](#install-from-requirementstxt)
  - [HashiCorp Vault](#hashicorp-vault)
    - [Installation](#installation)
    - [Starting Vault in Dev Mode](#starting-vault-in-dev-mode)
- [Start Vault server in dev mode](#start-vault-server-in-dev-mode)
- [In a new terminal, set Vault address](#in-a-new-terminal,-set-vault-address)
- [Set root token (use token from server output)](#set-root-token-use-token-from-server-output)
    - [Common Vault Commands](#common-vault-commands)
- [Check status](#check-status)
- [List secrets engines](#list-secrets-engines)
- [Enable secrets engine](#enable-secrets-engine)
- [Write secret](#write-secret)
- [Read secret](#read-secret)
- [Delete secret](#delete-secret)
  - [MySQL](#mysql)
    - [Installation](#installation)
- [Start MySQL service](#start-mysql-service)
- [Secure MySQL installation](#secure-mysql-installation)
    - [Common MySQL Commands](#common-mysql-commands)
- [Connect to MySQL](#connect-to-mysql)
- [Create database](#create-database)
- [Create user](#create-user)
- [Grant privileges](#grant-privileges)
- [Show databases](#show-databases)
- [Use database](#use-database)
- [Show tables](#show-tables)
    - [MySQL Service Management](#mysql-service-management)
- [Start MySQL](#start-mysql)
- [Stop MySQL](#stop-mysql)
- [Restart MySQL](#restart-mysql)
- [Check status](#check-status)
  - [Useful macOS Shortcuts](#useful-macos-shortcuts)
    - [General](#general)
    - [Terminal](#terminal)
    - [Finder](#finder)
    - [Text Editing](#text-editing)
    - [Screenshots](#screenshots)
    - [Development](#development)

## Homebrew

### Installation
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After installation, add Homebrew to your PATH:
```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### Common Brew Commands
- Update Homebrew: `brew update`
- Upgrade packages: `brew upgrade`
- Install package: `brew install <package>`
- Remove package: `brew uninstall <package>`
- List installed packages: `brew list`
- Search for package: `brew search <package>`
- Get package info: `brew info <package>`
- Cleanup old versions: `brew cleanup`
- Check system for issues: `brew doctor`

## Python

### Installation
```bash
# Install latest Python version
brew install python

# Verify installation
python3 --version
pip3 --version
```

### Python Environment Management
```bash
# Install virtualenv
pip3 install virtualenv

# Create new virtual environment
virtualenv venv

# Activate virtual environment
source venv/bin/activate

# Deactivate virtual environment
deactivate

# Install packages in virtual environment
pip install <package>

# Generate requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt
pip install -r requirements.txt
```

## HashiCorp Vault

### Installation
```bash
brew tap hashicorp/tap
brew install hashicorp/tap/vault
```

### Starting Vault in Dev Mode
```bash
# Start Vault server in dev mode
vault server -dev

# In a new terminal, set Vault address
export VAULT_ADDR='http://127.0.0.1:8200'

# Set root token (use token from server output)
export VAULT_TOKEN='your-root-token'
```

### Common Vault Commands
```bash
# Check status
vault status

# List secrets engines
vault secrets list

# Enable secrets engine
vault secrets enable -path=secret kv-v2

# Write secret
vault kv put secret/myapp/config api_key=123456

# Read secret
vault kv get secret/myapp/config

# Delete secret
vault kv delete secret/myapp/config
```

## MySQL

### Installation
```bash
brew install mysql

# Start MySQL service
brew services start mysql

# Secure MySQL installation
mysql_secure_installation
```

### Common MySQL Commands
```bash
# Connect to MySQL
mysql -u root -p

# Create database
CREATE DATABASE mydatabase;

# Create user
CREATE USER 'myuser'@'localhost' IDENTIFIED BY 'mypassword';

# Grant privileges
GRANT ALL PRIVILEGES ON mydatabase.* TO 'myuser'@'localhost';
FLUSH PRIVILEGES;

# Show databases
SHOW DATABASES;

# Use database
USE mydatabase;

# Show tables
SHOW TABLES;
```

### MySQL Service Management
```bash
# Start MySQL
brew services start mysql

# Stop MySQL
brew services stop mysql

# Restart MySQL
brew services restart mysql

# Check status
brew services list
```

## Useful macOS Shortcuts

### General
- `Command + Space`: Open Spotlight Search
- `Command + Tab`: Switch between applications
- `Command + ~`: Switch between windows of same application
- `Command + Q`: Quit application
- `Command + W`: Close window/tab
- `Command + M`: Minimize window
- `Command + H`: Hide application

### Terminal
- `Control + A`: Move cursor to beginning of line
- `Control + E`: Move cursor to end of line
- `Control + U`: Clear line before cursor
- `Control + K`: Clear line after cursor
- `Control + W`: Delete word before cursor
- `Control + R`: Search command history
- `Command + K`: Clear terminal screen
- `Command + T`: New terminal tab
- `Command + N`: New terminal window

### Finder
- `Command + Shift + G`: Go to folder
- `Command + Shift + .`: Show/hide hidden files
- `Command + Up`: Go to parent directory
- `Command + Down`: Open selected item
- `Command + Delete`: Move to trash
- `Command + Shift + Delete`: Empty trash
- `Space`: Quick Look selected item

### Text Editing
- `Command + C`: Copy
- `Command + V`: Paste
- `Command + X`: Cut
- `Command + A`: Select all
- `Command + Z`: Undo
- `Command + Shift + Z`: Redo
- `Option + Left/Right`: Move cursor by word
- `Command + Left/Right`: Move cursor to start/end of line
- `Command + Up/Down`: Move cursor to start/end of document

### Screenshots
- `Command + Shift + 3`: Capture entire screen
- `Command + Shift + 4`: Capture selected area
- `Command + Shift + 4 + Space`: Capture window/menu
- `Command + Shift + 5`: Screenshot/recording options

### Development
- `Command + B`: Build project
- `Command + R`: Run project
- `Command + .`: Stop running process
- `Command + /`: Comment/uncomment line
- `Command + [`: Indent left
- `Command + ]`: Indent right
- `Command + F`: Find in file
- `Command + Shift + F`: Find in project
