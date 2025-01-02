# Windows DevOps Setup Guide

This guide covers essential setup instructions for DevOps tools and utilities on Windows, along with useful shortcuts and productivity tips.

## Table of Contents
- [Windows DevOps Setup Guide](#windows-devops-setup-guide)
  - [Table of Contents](#table-of-contents)
  - [MySQL Setup](#mysql-setup)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [HashiCorp Vault Setup](#hashicorp-vault-setup)
    - [Prerequisites](#prerequisites)
    - [Installation Steps](#installation-steps)
  - [Windows Shortcuts](#windows-shortcuts)
    - [General Shortcuts](#general-shortcuts)
    - [PowerShell Shortcuts](#powershell-shortcuts)
    - [Windows Terminal Shortcuts](#windows-terminal-shortcuts)
  - [DevOps Utilities](#devops-utilities)
    - [Essential Tools](#essential-tools)
    - [Monitoring Tools](#monitoring-tools)
    - [Network Utilities](#network-utilities)
    - [Development Utilities](#development-utilities)
  - [Best Practices](#best-practices)
    - [Security](#security)
    - [Performance Optimization](#performance-optimization)
    - [Backup Strategy](#backup-strategy)
    - [Troubleshooting](#troubleshooting)

## MySQL Setup

### Prerequisites
- Windows 10/11 (64-bit)
- Administrative privileges
- Minimum 4GB RAM
- At least 2GB free disk space

### Installation Steps

1. Download MySQL Installer
   - Visit [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
   - Choose "MySQL Installer for Windows"
   - Download the larger package (mysql-installer-community-x.x.x.x.msi)

2. Run the Installer
   ```powershell
   # Verify the installer checksum (PowerShell)
   Get-FileHash mysql-installer-community-x.x.x.x.msi -Algorithm SHA256
   ```

3. Configuration Steps
   - Choose "Developer Default" for development environments
   - Select "Server only" for production environments
   - Configure MySQL Root Password
   - Configure Windows Service
     ```powershell
     # Verify MySQL Service is running
     Get-Service MySQL80
     ```

4. Network Configuration
   ```powershell
   # Open MySQL port in Windows Firewall
   New-NetFirewallRule -DisplayName "MySQL Server" -Direction Inbound -LocalPort 3306 -Protocol TCP -Action Allow
   ```

5. Basic Security Setup
   ```sql
   -- Run in MySQL Command Line Client
   ALTER USER 'root'@'localhost' IDENTIFIED BY 'new_password';
   CREATE USER 'devuser'@'localhost' IDENTIFIED BY 'devpass';
   GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'devuser'@'localhost';
   FLUSH PRIVILEGES;
   ```

## HashiCorp Vault Setup

### Prerequisites
- Windows 10/11
- PowerShell 5.1 or later
- Administrative privileges

### Installation Steps

1. Install Chocolatey (Package Manager)
   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
   ```

2. Install Vault
   ```powershell
   choco install vault
   # Verify installation
   vault --version
   ```

3. Configure Vault Server
   ```hcl
   # config.hcl
   storage "file" {
     path = "C:/vault/data"
   }

   listener "tcp" {
     address     = "127.0.0.1:8200"
     tls_disable = 1
   }

   api_addr = "http://127.0.0.1:8200"
   ```

4. Initialize Vault
   ```powershell
   # Create data directory
   mkdir C:\vault\data

   # Start Vault server
   vault server -config=config.hcl

   # In a new PowerShell window
   $env:VAULT_ADDR="http://127.0.0.1:8200"
   vault operator init
   ```

5. Unseal and Login
   ```powershell
   # Unseal vault (repeat 3 times with different keys)
   vault operator unseal

   # Login
   vault login
   ```

## Windows Shortcuts

### General Shortcuts
- `Win + X`: Power User menu (Admin PowerShell, Device Manager, etc.)
- `Win + E`: File Explorer
- `Win + I`: Settings
- `Win + V`: Clipboard history
- `Win + Shift + S`: Screenshot tool
- `Ctrl + Shift + Esc`: Task Manager

### PowerShell Shortcuts
- `F7`: Command history
- `Ctrl + R`: Search command history
- `Alt + Space + E`: Edit mode
- `Ctrl + Left/Right`: Move word by word
- `Ctrl + Shift + Left/Right`: Select word by word

### Windows Terminal Shortcuts
- `Ctrl + Shift + T`: New tab
- `Ctrl + Shift + W`: Close tab
- `Alt + Shift + D`: Split pane
- `Alt + Left/Right/Up/Down`: Switch between panes
- `Ctrl + Shift + P`: Command palette

## DevOps Utilities

### Essential Tools
1. Windows Terminal
   ```powershell
   winget install Microsoft.WindowsTerminal
   ```

2. PowerShell 7
   ```powershell
   winget install Microsoft.PowerShell
   ```

3. Git for Windows
   ```powershell
   winget install Git.Git
   ```

4. Visual Studio Code
   ```powershell
   winget install Microsoft.VisualStudioCode
   ```

### Monitoring Tools
1. Process Explorer
   - Download from [Sysinternals](https://docs.microsoft.com/en-us/sysinternals/downloads/process-explorer)
   - Advanced task manager replacement
   - Process tree view
   - Resource usage monitoring

2. Windows Performance Monitor
   ```powershell
   # Launch Performance Monitor
   perfmon.exe
   ```

### Network Utilities
1. TCPView
   ```powershell
   # Install using chocolatey
   choco install tcpview
   ```

2. Wireshark
   ```powershell
   winget install WiresharkFoundation.Wireshark
   ```

### Development Utilities
1. Windows Subsystem for Linux (WSL)
   ```powershell
   wsl --install
   ```

2. Docker Desktop
   ```powershell
   winget install Docker.DockerDesktop
   ```

## Best Practices

### Security
1. Regular Updates
   ```powershell
   # Check for Windows updates
   Get-WindowsUpdate
   
   # Install updates
   Install-WindowsUpdate
   ```

2. Firewall Configuration
   ```powershell
   # Check firewall status
   Get-NetFirewallProfile
   
   # Enable firewall for all profiles
   Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
   ```

3. Antivirus Integration
   ```powershell
   # Check Windows Defender status
   Get-MpComputerStatus
   
   # Start a scan
   Start-MpScan
   ```

### Performance Optimization
1. Disk Cleanup
   ```powershell
   # Clean system files
   cleanmgr /sagerun:1
   ```

2. Defragmentation (for HDDs)
   ```powershell
   # Analyze disk
   defrag C: /A
   
   # Optimize disk
   defrag C: /O
   ```

### Backup Strategy
1. System Restore Points
   ```powershell
   # Create restore point
   Checkpoint-Computer -Description "Pre-deployment backup"
   ```

2. File History
   ```powershell
   # Enable File History
   Enable-ComputerRestore -Drive "C:\"
   ```

### Troubleshooting
1. System Logs
   ```powershell
   # View system logs
   Get-EventLog -LogName System -Newest 50
   
   # View application logs
   Get-EventLog -LogName Application -Newest 50
   ```

2. Network Diagnostics
   ```powershell
   # Test network connectivity
   Test-NetConnection -ComputerName google.com -Port 80
   
   # View network statistics
   netstat -ano
   ```

3. Resource Monitoring
   ```powershell
   # CPU usage
   Get-Counter '\Processor(_Total)\% Processor Time'
   
   # Memory usage
   Get-Counter '\Memory\Available MBytes'
   ```

Remember to regularly update all tools and maintain proper security practices. For production environments, ensure all services are properly secured and monitored.
