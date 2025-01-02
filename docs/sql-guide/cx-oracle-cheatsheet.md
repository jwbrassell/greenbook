# cx_Oracle Cheat Sheet

## Table of Contents
- [cx_Oracle Cheat Sheet](#cx_oracle-cheat-sheet)
  - [Installation](#installation)
  - [Basic Connection Methods](#basic-connection-methods)
    - [Simple Connection](#simple-connection)
- [Basic connection](#basic-connection)
    - [Connection Using TNS](#connection-using-tns)
- [Using tnsnames.ora](#using-tnsnamesora)
    - [Connection String Format](#connection-string-format)
- [Full connection string](#full-connection-string)
    - [Connection Pool](#connection-pool)
- [Create connection pool](#create-connection-pool)
- [Acquire connection from pool](#acquire-connection-from-pool)
  - [Basic Operations](#basic-operations)
    - [Execute Simple Query](#execute-simple-query)
    - [Parameterized Queries](#parameterized-queries)
- [Using bind variables (preferred method)](#using-bind-variables-preferred-method)
- [Using multiple parameters](#using-multiple-parameters)
    - [Fetch Methods](#fetch-methods)
- [Fetch all rows](#fetch-all-rows)
- [Fetch one row](#fetch-one-row)
- [Fetch specific number of rows](#fetch-specific-number-of-rows)
- [Iterate through results](#iterate-through-results)
    - [DML Operations](#dml-operations)
- [Insert](#insert)
- [Update](#update)
- [Delete](#delete)
- [Commit changes](#commit-changes)
    - [Batch Operations](#batch-operations)
- [Batch insert](#batch-insert)
  - [LOB Operations](#lob-operations)
    - [CLOB Operations](#clob-operations)
- [Read CLOB](#read-clob)
- [Write CLOB](#write-clob)
    - [BLOB Operations](#blob-operations)
- [Read BLOB](#read-blob)
- [Write BLOB](#write-blob)
  - [Transaction Management](#transaction-management)
- [Start transaction](#start-transaction)
  - [Error Handling](#error-handling)
  - [Resource Management](#resource-management)
- [Using context managers (recommended)](#using-context-managers-recommended)
- [Manual cleanup](#manual-cleanup)
  - [Advanced Features](#advanced-features)
    - [Array DML](#array-dml)
- [Enable array DML](#enable-array-dml)
- [Perform batch operation](#perform-batch-operation)
    - [Output Parameters](#output-parameters)
- [Using output parameters with PL/SQL](#using-output-parameters-with-pl/sql)
    - [PL/SQL Blocks](#pl/sql-blocks)
- [Execute PL/SQL block](#execute-pl/sql-block)
  - [Performance Tips](#performance-tips)



## Installation
```bash
pip install cx_Oracle
```

## Basic Connection Methods

### Simple Connection
```python
import cx_Oracle

# Basic connection
connection = cx_Oracle.connect(
    user="username",
    password="password",
    dsn="hostname:port/service_name"
)
```

### Connection Using TNS
```python
# Using tnsnames.ora
connection = cx_Oracle.connect(
    user="username",
    password="password",
    dsn="tns_alias"
)
```

### Connection String Format
```python
# Full connection string
conn_str = "username/password@hostname:port/service_name"
connection = cx_Oracle.connect(conn_str)
```

### Connection Pool
```python
# Create connection pool
pool = cx_Oracle.SessionPool(
    user="username",
    password="password",
    dsn="hostname:port/service_name",
    min=2,
    max=5,
    increment=1
)

# Acquire connection from pool
connection = pool.acquire()
```

## Basic Operations

### Execute Simple Query
```python
cursor = connection.cursor()
cursor.execute("SELECT * FROM employees")
rows = cursor.fetchall()
```

### Parameterized Queries
```python
# Using bind variables (preferred method)
cursor.execute(
    "SELECT * FROM employees WHERE department_id = :dept_id",
    dept_id=10
)

# Using multiple parameters
cursor.execute(
    "INSERT INTO employees (id, name, salary) VALUES (:1, :2, :3)",
    [1001, "John Doe", 50000]
)
```

### Fetch Methods
```python
# Fetch all rows
rows = cursor.fetchall()

# Fetch one row
row = cursor.fetchone()

# Fetch specific number of rows
rows = cursor.fetchmany(5)

# Iterate through results
for row in cursor:
    print(row)
```

### DML Operations
```python
# Insert
cursor.execute(
    "INSERT INTO employees (id, name) VALUES (:1, :2)",
    [101, "Jane Smith"]
)

# Update
cursor.execute(
    "UPDATE employees SET salary = :1 WHERE id = :2",
    [55000, 101]
)

# Delete
cursor.execute(
    "DELETE FROM employees WHERE id = :1",
    [101]
)

# Commit changes
connection.commit()
```

### Batch Operations
```python
# Batch insert
data = [
    (1, "John"),
    (2, "Jane"),
    (3, "Bob")
]
cursor.executemany(
    "INSERT INTO employees (id, name) VALUES (:1, :2)",
    data
)
connection.commit()
```

## LOB Operations

### CLOB Operations
```python
# Read CLOB
cursor.execute("SELECT clob_column FROM my_table WHERE id = :1", [1])
clob = cursor.fetchone()[0]
content = clob.read()

# Write CLOB
clob_var = cursor.var(cx_Oracle.CLOB)
clob_var.setvalue(0, "Large text content...")
cursor.execute(
    "UPDATE my_table SET clob_column = :1 WHERE id = :2",
    [clob_var, 1]
)
```

### BLOB Operations
```python
# Read BLOB
cursor.execute("SELECT blob_column FROM my_table WHERE id = :1", [1])
blob = cursor.fetchone()[0]
content = blob.read()

# Write BLOB
blob_var = cursor.var(cx_Oracle.BLOB)
blob_var.setvalue(0, b"Binary content...")
cursor.execute(
    "UPDATE my_table SET blob_column = :1 WHERE id = :2",
    [blob_var, 1]
)
```

## Transaction Management
```python
# Start transaction
connection.begin()

try:
    # Execute multiple operations
    cursor.execute("INSERT INTO table1 VALUES (:1)", [1])
    cursor.execute("UPDATE table2 SET col = :1", [2])
    
    # Commit if all operations successful
    connection.commit()
except Exception as e:
    # Rollback on error
    connection.rollback()
    raise e
```

## Error Handling
```python
import cx_Oracle

try:
    cursor.execute("SELECT * FROM nonexistent_table")
except cx_Oracle.DatabaseError as e:
    error, = e.args
    print("Oracle Error:", error.code)
    print("Error Message:", error.message)
```

## Resource Management
```python
# Using context managers (recommended)
with cx_Oracle.connect(user="user", password="pass", dsn="dsn") as connection:
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM employees")
        rows = cursor.fetchall()

# Manual cleanup
cursor.close()
connection.close()
pool.close()
```

## Advanced Features

### Array DML
```python
# Enable array DML
cursor.arraysize = 1000

# Perform batch operation
cursor.executemany(
    "INSERT INTO table (col1, col2) VALUES (:1, :2)",
    [(1, "a"), (2, "b"), (3, "c")]
)
```

### Output Parameters
```python
# Using output parameters with PL/SQL
output_val = cursor.var(cx_Oracle.NUMBER)
cursor.callproc(
    "my_procedure",
    [123, output_val]
)
result = output_val.getvalue()
```

### PL/SQL Blocks
```python
# Execute PL/SQL block
plsql = """
BEGIN
    UPDATE employees
    SET salary = salary * 1.1
    WHERE department_id = :dept_id;
    
    :rows_updated := SQL%ROWCOUNT;
END;
"""

rows_updated = cursor.var(cx_Oracle.NUMBER)
cursor.execute(plsql, dept_id=10, rows_updated=rows_updated)
print(f"Rows updated: {rows_updated.getvalue()}")
```

## Performance Tips

1. Use bind variables instead of string concatenation
2. Use connection pooling for multiple connections
3. Set appropriate arraysize for batch operations
4. Use cursor.executemany() for bulk operations
5. Commit transactions in batches
6. Close cursors and connections properly
7. Use context managers when possible
