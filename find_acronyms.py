import os
import re
import argparse
from pathlib import Path

def get_existing_acronyms(acronyms_file):
    """Extract existing acronyms from acronyms.md"""
    existing = set()
    try:
        with open(acronyms_file, 'r') as f:
            content = f.read()
            # Find headers like "## ABC (Some Description)"
            matches = re.finditer(r'##\s+([A-Z][A-Z0-9/]+(?:-[A-Z0-9]+)*)', content)
            for match in matches:
                existing.add(match.group(1))
    except FileNotFoundError:
        print(f"Warning: {acronyms_file} not found")
    return existing

def is_in_code_block(content, position):
    """Check if the position is within a code block"""
    # Find all code blocks (both ``` and indented)
    code_blocks = list(re.finditer(r'```[\s\S]*?```|(?:(?:^|\n)    [^\n]*)+', content))
    return any(block.start() <= position <= block.end() for block in code_blocks)

def is_likely_acronym(word, content, position):
    """Determine if a word is likely to be an acronym"""
    # Skip if too long (likely not an acronym)
    if len(word) > 10:
        return False
    
    # Skip if too short (likely not an acronym)
    if len(word) < 3:
        return False
    
    # Skip if it looks like a version number (e.g., V1.0)
    if re.match(r'^V\d', word):
        return False
    
    # Skip if it's a common file extension with path
    if '.' in word:
        return False
    
    # Skip if it looks like a hex color or hash
    if re.match(r'^[A-F0-9]+$', word):
        return False
    
    # Skip if it's a common programming pattern like ALL_CAPS
    if '_' in word:
        return False
    
    # Skip if it's in a code block
    if is_in_code_block(content, position):
        return False
    
    return True

def find_acronyms_in_file(file_path):
    """Find potential acronyms in a file"""
    acronyms = set()
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Common terms to exclude
            exclude_terms = {
                # SQL Keywords and Database Terms
                'SELECT', 'WHERE', 'FROM', 'JOIN', 'AND', 'OR', 'NULL', 'INT', 'VARCHAR',
                'CREATE', 'TABLE', 'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'INDEX',
                'PRIMARY', 'KEY', 'FOREIGN', 'REFERENCES', 'DEFAULT', 'NOT', 'UNIQUE',
                'ORDER', 'GROUP', 'BY', 'ASC', 'DESC', 'LIMIT', 'OFFSET', 'TRUE', 'FALSE',
                'BEGIN', 'END', 'COMMIT', 'ROLLBACK', 'INTO', 'VALUES', 'SET',
                
                # Programming Terms and Keywords
                'STRING', 'BOOL', 'VOID', 'CHAR', 'CONST', 'STATIC', 'PUBLIC', 'PRIVATE',
                'CLASS', 'INTERFACE', 'RETURN', 'THROW', 'CATCH', 'TRY', 'NEW', 'THIS',
                'SUPER', 'EXTENDS', 'IMPLEMENTS', 'FINAL', 'ABSTRACT', 'ASYNC', 'AWAIT',
                'BREAK', 'CASE', 'CONTINUE', 'DO', 'ELSE', 'FOR', 'IF', 'IN', 'INSTANCEOF',
                'PACKAGE', 'PROTECTED', 'SWITCH', 'SYNCHRONIZED', 'THROWS', 'TRANSIENT',
                'WHILE', 'WITH',
                
                # Common Words Often in Caps
                'README', 'LICENSE', 'CONTRIBUTING', 'TODO', 'FIXME', 'NOTE', 'WARNING',
                'ERROR', 'DEBUG', 'INFO', 'FATAL', 'SUCCESS', 'FAIL', 'YES', 'NO',
                'ON', 'OFF', 'ENABLE', 'DISABLE', 'ADD', 'REMOVE', 'GET', 'SET', 'PUT',
                'POST', 'HEAD', 'OPTIONS', 'PATCH', 'COPY', 'MOVE', 'LINK', 'UNLINK',
                
                # File Extensions & Formats
                'MD', 'TXT', 'CSV', 'JSON', 'XML', 'YAML', 'YML', 'INI', 'CONF', 'CFG',
                'LOG', 'PID', 'ENV', 'BAK', 'TMP', 'TEMP', 'LOCK', 'SOCKET', 'FIFO',
                'BIN', 'EXE', 'DLL', 'SO', 'JAR', 'WAR', 'EAR', 'TAR', 'ZIP', 'GZ',
                'RAR', 'ISO', 'IMG',
                
                # Date/Time Related
                'YYYY', 'MM', 'DD', 'HH', 'MIN', 'SEC', 'MS', 'NS', 'AM', 'PM', 'UTC',
                'GMT', 'ISO', 'NOW', 'TODAY', 'TOMORROW', 'YESTERDAY',
                
                # Units & Measurements
                'KB', 'MB', 'GB', 'TB', 'PB', 'KIB', 'MIB', 'GIB', 'TIB', 'PIB',
                'HZ', 'MHZ', 'GHZ', 'BPS', 'KBPS', 'MBPS', 'GBPS',
                
                # Common Variable Names & Programming Concepts
                'ID', 'NUM', 'MAX', 'MIN', 'COUNT', 'SUM', 'AVG', 'NAME', 'TYPE',
                'SIZE', 'LEN', 'POS', 'VAL', 'TEMP', 'TMP', 'BUF', 'PTR', 'REF',
                'OBJ', 'STR', 'ARR', 'LIST', 'DICT', 'MAP', 'SET', 'QUEUE', 'STACK',
                'TREE', 'GRAPH', 'NODE', 'EDGE', 'PATH', 'ROOT', 'LEAF', 'PARENT',
                'CHILD', 'NEXT', 'PREV', 'HEAD', 'TAIL', 'FRONT', 'BACK',
                
                # System Commands & Terms
                'CD', 'PWD', 'LS', 'CP', 'MV', 'RM', 'MKDIR', 'RMDIR', 'CHMOD', 'CHOWN',
                'CHGRP', 'SUDO', 'SU', 'SSH', 'SCP', 'SFTP', 'GREP', 'AWK', 'SED',
                'CAT', 'LESS', 'MORE', 'HEAD', 'TAIL', 'TOUCH', 'FIND', 'WHICH',
                'WHEREIS', 'WHO', 'PS', 'TOP', 'KILL', 'PKILL', 'SLEEP', 'WAIT',
                
                # Technical Terms (Not Acronyms)
                'ACTIVE', 'BACKUP', 'CACHE', 'CONFIG', 'DATA', 'DOMAIN', 'FILE',
                'HOST', 'INPUT', 'JOB', 'KEY', 'LINE', 'MODE', 'NET', 'OUTPUT',
                'PORT', 'QUERY', 'ROUTE', 'STATUS', 'TIME', 'USER', 'VALUE',
                'WORK', 'ZONE', 'COMMAND', 'PROCESS', 'SERVICE', 'SYSTEM', 'VERSION',
                'WINDOW', 'SCREEN', 'DEVICE', 'DRIVER', 'MODULE', 'PACKAGE', 'SCRIPT',
                'SHELL', 'SOCKET', 'THREAD', 'VOLUME', 'CLIENT', 'SERVER', 'PROXY',
                'MASTER', 'SLAVE', 'WORKER', 'MANAGER', 'AGENT', 'BROKER', 'ROUTER',
                'SWITCH', 'BRIDGE', 'GATEWAY', 'FIREWALL', 'NETWORK', 'DATABASE',
                'CLUSTER', 'POOL', 'QUEUE', 'STACK', 'HEAP', 'BUFFER', 'STREAM',
                'FILTER', 'PARSER', 'LOGGER', 'MONITOR', 'TRACKER', 'COUNTER',
                'TIMER', 'SCHEDULER', 'BUILDER', 'FACTORY', 'PROVIDER', 'CONSUMER',
                'PRODUCER', 'SUBSCRIBER', 'PUBLISHER', 'LISTENER', 'HANDLER', 'WRAPPER',
                'CONTAINER', 'RESOURCE', 'TEMPLATE', 'PATTERN', 'FORMAT', 'STYLE',
                'THEME', 'LAYOUT', 'VIEW', 'MODEL', 'CONTROLLER', 'ACTION', 'EVENT',
                'TRIGGER', 'SIGNAL', 'MESSAGE', 'REQUEST', 'RESPONSE', 'SESSION',
                'COOKIE', 'CACHE', 'STORE', 'REPOSITORY', 'REGISTRY', 'CONTEXT',
                'SCOPE', 'NAMESPACE', 'MODULE', 'LIBRARY', 'FRAMEWORK', 'PLATFORM',
                'RUNTIME', 'ENGINE', 'COMPILER', 'INTERPRETER', 'DEBUGGER', 'PROFILER',
                'ANALYZER', 'VALIDATOR', 'CONVERTER', 'TRANSFORMER', 'ENCODER',
                'DECODER', 'PARSER', 'FORMATTER', 'SERIALIZER', 'DESERIALIZER'
            }
            
            # Find potential acronyms (3+ letters, all caps)
            matches = re.finditer(r'\b[A-Z][A-Z0-9]{2,}(?:/[A-Z0-9]+)*\b', content)
            for match in matches:
                acronym = match.group(0)
                # Skip if it matches any of our exclusion criteria
                if (is_likely_acronym(acronym, content, match.start()) and
                    acronym not in exclude_terms):
                    acronyms.add(acronym)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return acronyms

def main():
    parser = argparse.ArgumentParser(description='Find acronyms in markdown files')
    parser.add_argument('--recursive', '-r', action='store_true', help='Search recursively in subdirectories')
    args = parser.parse_args()
    
    # Get existing acronyms
    existing_acronyms = get_existing_acronyms('acronyms.md')
    
    # Find markdown files
    all_acronyms = set()
    
    # Directories to skip
    skip_dirs = {'snippets', 'node_modules', '.git', '__pycache__', 'venv', 'env'}
    
    if args.recursive:
        # Recursive search
        for root, dirs, files in os.walk('.'):
            # Skip unwanted directories
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if file.endswith('.md') and file != 'acronyms.md':
                    file_path = os.path.join(root, file)
                    print(f"Scanning {file_path}...")
                    found_acronyms = find_acronyms_in_file(file_path)
                    all_acronyms.update(found_acronyms)
    else:
        # Only search top-level markdown files
        for file in os.listdir('.'):
            if file.endswith('.md') and file != 'acronyms.md':
                print(f"Scanning {file}...")
                found_acronyms = find_acronyms_in_file(file)
                all_acronyms.update(found_acronyms)
    
    # Find new acronyms
    new_acronyms = all_acronyms - existing_acronyms
    
    if new_acronyms:
        print("\nNew acronyms found:")
        for acronym in sorted(new_acronyms):
            print(f"- {acronym}")
            
        # Add new acronyms to acronyms.md
        with open('acronyms.md', 'a') as f:
            f.write("\n")  # Add a blank line for separation
            for acronym in sorted(new_acronyms):
                f.write(f"\n## {acronym} ()\n")
                f.write("- **Category**: Description\n")
                
        print(f"\nAdded {len(new_acronyms)} new acronyms to acronyms.md")
    else:
        print("\nNo new acronyms found!")

if __name__ == '__main__':
    main()
