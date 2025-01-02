# SSH Key Management Guide

## Table of Contents
- [SSH Key Management Guide](#ssh-key-management-guide)
  - [Table of Contents](#table-of-contents)
  - [Table of Contents](#table-of-contents)
  - [Creating SSH Keys](#creating-ssh-keys)
    - [Linux/macOS](#linux/macos)
- [Generate new SSH key pair](#generate-new-ssh-key-pair)
- [Alternative using RSA with 4096 bits (for legacy systems)](#alternative-using-rsa-with-4096-bits-for-legacy-systems)
- [View public key](#view-public-key)
- [Check permissions](#check-permissions)
    - [Windows (PowerShell)](#windows-powershell)
- [Generate new SSH key pair](#generate-new-ssh-key-pair)
- [View public key](#view-public-key)
- [Check permissions](#check-permissions)
  - [Local to Remote Transfer](#local-to-remote-transfer)
    - [Linux/macOS to Remote Linux](#linux/macos-to-remote-linux)
- [Method 1: Using ssh-copy-id (Recommended)](#method-1:-using-ssh-copy-id-recommended)
- [Method 2: Manual copy](#method-2:-manual-copy)
    - [Windows to Remote Linux](#windows-to-remote-linux)
- [Method 1: Using ssh-copy-id (if available)](#method-1:-using-ssh-copy-id-if-available)
- [Method 2: Manual copy (PowerShell)](#method-2:-manual-copy-powershell)
    - [To Remote Windows](#to-remote-windows)
- [On remote Windows machine (PowerShell Admin)](#on-remote-windows-machine-powershell-admin)
- [Create .ssh directory if it doesn't exist](#create-ssh-directory-if-it-doesn't-exist)
- [Set proper permissions](#set-proper-permissions)
- [Add public key to authorized_keys](#add-public-key-to-authorized_keys)
  - [Remote to Local Transfer](#remote-to-local-transfer)
    - [Remote Linux to Local Linux/macOS](#remote-linux-to-local-linux/macos)
- [On remote machine: Generate key](#on-remote-machine:-generate-key)
- [Copy public key content](#copy-public-key-content)
- [On local machine: Add to authorized_keys](#on-local-machine:-add-to-authorized_keys)
    - [Remote Linux to Local Windows](#remote-linux-to-local-windows)
- [On local Windows machine (PowerShell Admin)](#on-local-windows-machine-powershell-admin)
- [Create .ssh directory](#create-ssh-directory)
- [Set permissions](#set-permissions)
- [Add remote public key to authorized_keys](#add-remote-public-key-to-authorized_keys)
    - [Remote Windows to Local](#remote-windows-to-local)
- [On remote Windows (PowerShell)](#on-remote-windows-powershell)
- [View public key](#view-public-key)
- [Copy content and add to local authorized_keys file](#copy-content-and-add-to-local-authorized_keys-file)
- [For Linux/macOS local:](#for-linux/macos-local:)
- [For Windows local:](#for-windows-local:)
  - [Platform-Specific Instructions](#platform-specific-instructions)
    - [macOS Additional Steps](#macos-additional-steps)
- [Start ssh-agent](#start-ssh-agent)
- [Add key to keychain](#add-key-to-keychain)
- [Configure SSH to use keychain (in ~/.ssh/config)](#configure-ssh-to-use-keychain-in-~/ssh/config)
    - [Windows OpenSSH Service](#windows-openssh-service)
- [Check OpenSSH service status](#check-openssh-service-status)
- [Start OpenSSH service](#start-openssh-service)
- [Add key to agent](#add-key-to-agent)
    - [Linux SSH Agent](#linux-ssh-agent)
- [Start ssh-agent](#start-ssh-agent)
- [Add key to agent](#add-key-to-agent)
- [Configure SSH agent (in ~/.bashrc or ~/.zshrc)](#configure-ssh-agent-in-~/bashrc-or-~/zshrc)
  - [Best Practices](#best-practices)
    - [Key Management](#key-management)
    - [Security Recommendations](#security-recommendations)
    - [Testing Connection](#testing-connection)
- [Test SSH connection](#test-ssh-connection)
- [Test specific key](#test-specific-key)
- [Test connection without login](#test-connection-without-login)
    - [Troubleshooting](#troubleshooting)



This guide covers SSH key creation and transfer across different operating systems, including both local-to-remote and remote-to-local scenarios.

## Table of Contents
1. [Creating SSH Keys](#creating-ssh-keys)
2. [Local to Remote Transfer](#local-to-remote-transfer)
3. [Remote to Local Transfer](#remote-to-local-transfer)
4. [Platform-Specific Instructions](#platform-specific-instructions)
5. [Best Practices](#best-practices)

## Creating SSH Keys

### Linux/macOS
```bash
# Generate new SSH key pair
ssh-keygen -t ed25519 -C "your_email@example.com"

# Alternative using RSA with 4096 bits (for legacy systems)
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# View public key
cat ~/.ssh/id_ed25519.pub

# Check permissions
ls -la ~/.ssh/
```

### Windows (PowerShell)
```powershell
# Generate new SSH key pair
ssh-keygen -t ed25519 -C "your_email@example.com"

# View public key
type $env:USERPROFILE\.ssh\id_ed25519.pub

# Check permissions
Get-Acl $env:USERPROFILE\.ssh\id_ed25519*
```

## Local to Remote Transfer

### Linux/macOS to Remote Linux
```bash
# Method 1: Using ssh-copy-id (Recommended)
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@remote_host

# Method 2: Manual copy
cat ~/.ssh/id_ed25519.pub | ssh username@remote_host "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
```

### Windows to Remote Linux
```powershell
# Method 1: Using ssh-copy-id (if available)
ssh-copy-id -i $env:USERPROFILE\.ssh\id_ed25519.pub username@remote_host

# Method 2: Manual copy (PowerShell)
$key = Get-Content "$env:USERPROFILE\.ssh\id_ed25519.pub"
$remoteCommand = "mkdir -p ~/.ssh && chmod 700 ~/.ssh && echo '$key' >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
ssh username@remote_host $remoteCommand
```

### To Remote Windows
```powershell
# On remote Windows machine (PowerShell Admin)
# Create .ssh directory if it doesn't exist
mkdir $env:USERPROFILE\.ssh -ErrorAction SilentlyContinue

# Set proper permissions
icacls $env:USERPROFILE\.ssh /inheritance:r
icacls $env:USERPROFILE\.ssh /grant:r "%USERNAME%":"(F)"

# Add public key to authorized_keys
Add-Content -Path $env:USERPROFILE\.ssh\authorized_keys -Value "ssh-ed25519 AAAA..."
```

## Remote to Local Transfer

### Remote Linux to Local Linux/macOS
```bash
# On remote machine: Generate key
ssh-keygen -t ed25519 -C "remote@example.com"

# Copy public key content
cat ~/.ssh/id_ed25519.pub

# On local machine: Add to authorized_keys
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "ssh-ed25519 AAAA..." >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### Remote Linux to Local Windows
```powershell
# On local Windows machine (PowerShell Admin)
# Create .ssh directory
mkdir $env:USERPROFILE\.ssh -ErrorAction SilentlyContinue

# Set permissions
icacls $env:USERPROFILE\.ssh /inheritance:r
icacls $env:USERPROFILE\.ssh /grant:r "%USERNAME%":"(F)"

# Add remote public key to authorized_keys
Add-Content -Path $env:USERPROFILE\.ssh\authorized_keys -Value "ssh-ed25519 AAAA..."
```

### Remote Windows to Local
```powershell
# On remote Windows (PowerShell)
ssh-keygen -t ed25519 -C "remote_windows@example.com"

# View public key
type $env:USERPROFILE\.ssh\id_ed25519.pub

# Copy content and add to local authorized_keys file
# For Linux/macOS local:
echo "ssh-ed25519 AAAA..." >> ~/.ssh/authorized_keys

# For Windows local:
Add-Content -Path $env:USERPROFILE\.ssh\authorized_keys -Value "ssh-ed25519 AAAA..."
```

## Platform-Specific Instructions

### macOS Additional Steps
```bash
# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to keychain
ssh-add --apple-use-keychain ~/.ssh/id_ed25519

# Configure SSH to use keychain (in ~/.ssh/config)
Host *
  UseKeychain yes
  AddKeysToAgent yes
  IdentityFile ~/.ssh/id_ed25519
```

### Windows OpenSSH Service
```powershell
# Check OpenSSH service status
Get-Service ssh-agent

# Start OpenSSH service
Start-Service ssh-agent
Set-Service ssh-agent -StartupType Automatic

# Add key to agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

### Linux SSH Agent
```bash
# Start ssh-agent
eval "$(ssh-agent -s)"

# Add key to agent
ssh-add ~/.ssh/id_ed25519

# Configure SSH agent (in ~/.bashrc or ~/.zshrc)
if [ -z "$SSH_AUTH_SOCK" ]; then
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
fi
```

## Best Practices

### Key Management
1. **Secure Storage:**
   ```bash
   # Set correct permissions
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```

2. **Backup Keys:**
   ```bash
   # Create encrypted backup
   tar czf ssh_backup.tar.gz ~/.ssh/
   gpg -c ssh_backup.tar.gz
   ```

### Security Recommendations

1. **Use Strong Key Types:**
   - Prefer Ed25519 over RSA
   - If using RSA, use minimum 4096 bits

2. **Key Passphrase:**
   - Always use a strong passphrase
   - Use ssh-agent to cache passphrase

3. **Regular Maintenance:**
   ```bash
   # List all authorized keys
   cat ~/.ssh/authorized_keys
   
   # Remove unused keys
   vim ~/.ssh/authorized_keys
   
   # Check for unauthorized access
   grep "ssh" /var/log/auth.log
   ```

### Testing Connection
```bash
# Test SSH connection
ssh -v username@remote_host

# Test specific key
ssh -i ~/.ssh/id_ed25519 username@remote_host

# Test connection without login
ssh -T git@github.com
```

### Troubleshooting

1. **Permission Issues:**
   ```bash
   # Fix permissions
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   ```

2. **Connection Issues:**
   ```bash
   # Debug connection
   ssh -vvv username@remote_host
   
   # Check SSH service
   systemctl status sshd
   
   # Check SSH config
   sshd -T
   ```

3. **Key Issues:**
   ```bash
   # Verify key format
   ssh-keygen -l -f ~/.ssh/id_ed25519
   
   # Check if key is loaded in agent
   ssh-add -l
