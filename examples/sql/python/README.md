# SQL Operations with Python Examples

## Table of Contents
- [SQL Operations with Python Examples](#sql-operations-with-python-examples)
  - [Examples Overview](#examples-overview)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
  - [Basic Operations](#basic-operations)
  - [Advanced Features](#advanced-features)
  - [Security Considerations](#security-considerations)
  - [Performance Optimization](#performance-optimization)
  - [Testing](#testing)
  - [Contributing](#contributing)
  - [License](#license)

## Examples Overview

1. Basic Operations
   - Connection management
   - CRUD operations
   - Transaction handling
   - Batch processing

2. Advanced Features
   - Complex queries
   - Stored procedures
   - Triggers and events
   - Replication management

3. Integration Features
   - ORM integration
   - Migration management
   - Backup automation
   - Monitoring integration

4. Full Applications
   - Data warehouse ETL
   - Query analyzer
   - Schema manager
   - Backup manager

## Project Structure

```
python/
├── basic/
│   ├── connection/
│   │   ├── app.py
│   │   ├── requirements.txt
│   │   └── config.py
│   ├── crud/
│   ├── transactions/
│   └── batch/
├── advanced/
│   ├── queries/
│   ├── procedures/
│   ├── triggers/
│   └── replication/
├── integration/
│   ├── orm/
│   ├── migrations/
│   ├── backup/
│   └── monitoring/
└── applications/
    ├── etl_manager/
    ├── query_analyzer/
    ├── schema_manager/
    └── backup_manager/
```

## Getting Started

1. Setup Environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
.\venv\Scripts\activate   # Windows
```

2. Install Dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Database Connection:
```python
# config.py
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your-password',
    'database': 'test_db'
}

POSTGRES_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'your-password',
    'database': 'test_db',
    'port': 5432
}
```

## Basic Operations

### Connection Management
```python
import mysql.connector
import psycopg2
from contextlib import contextmanager
from config import MYSQL_CONFIG, POSTGRES_CONFIG

class DatabaseManager:
    def __init__(self, db_type='mysql'):
        self.db_type = db_type
        self.config = MYSQL_CONFIG if db_type == 'mysql' else POSTGRES_CONFIG
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context management"""
        if self.db_type == 'mysql':
            conn = mysql.connector.connect(**self.config)
        else:
            conn = psycopg2.connect(**self.config)
        
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query, params=None):
        """Execute query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            try:
                cursor.execute(query, params or ())
                if query.strip().upper().startswith('SELECT'):
                    return cursor.fetchall()
                return cursor.rowcount
            finally:
                cursor.close()
```

### CRUD Operations
```python
class CRUDManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_record(self, table, data):
        """Insert new record"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        return self.db.execute_query(query, list(data.values()))
    
    def read_records(self, table, conditions=None, fields=None):
        """Read records with optional conditions"""
        fields = fields or ['*']
        query = f"SELECT {', '.join(fields)} FROM {table}"
        params = []
        
        if conditions:
            clauses = []
            for key, value in conditions.items():
                clauses.append(f"{key} = %s")
                params.append(value)
            query += " WHERE " + " AND ".join(clauses)
        
        return self.db.execute_query(query, params)
    
    def update_record(self, table, data, conditions):
        """Update records matching conditions"""
        set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
        
        params = list(data.values()) + list(conditions.values())
        return self.db.execute_query(query, params)
    
    def delete_record(self, table, conditions):
        """Delete records matching conditions"""
        where_clause = ' AND '.join([f"{k} = %s" for k in conditions.keys()])
        query = f"DELETE FROM {table} WHERE {where_clause}"
        
        return self.db.execute_query(query, list(conditions.values()))
```

### Transaction Management
```python
class TransactionManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    @contextmanager
    def transaction(self):
        """Handle transaction with context management"""
        with self.db.get_connection() as conn:
            try:
                yield conn
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
    
    def transfer_funds(self, from_account, to_account, amount):
        """Example of transaction usage"""
        with self.transaction() as conn:
            cursor = conn.cursor()
            
            # Debit from account
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance - %s 
                WHERE account_id = %s AND balance >= %s
            """, (amount, from_account, amount))
            
            if cursor.rowcount == 0:
                raise ValueError("Insufficient funds")
            
            # Credit to account
            cursor.execute("""
                UPDATE accounts 
                SET balance = balance + %s 
                WHERE account_id = %s
            """, (amount, to_account))
            
            cursor.close()
```

## Advanced Features

### Complex Queries
```python
class QueryManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def get_sales_report(self, start_date, end_date):
        """Complex query with joins and aggregations"""
        query = """
            SELECT 
                p.category,
                COUNT(s.id) as total_sales,
                SUM(s.amount) as revenue,
                AVG(s.amount) as avg_sale,
                STRING_AGG(DISTINCT c.name, ', ') as customers
            FROM sales s
            JOIN products p ON s.product_id = p.id
            JOIN customers c ON s.customer_id = c.id
            WHERE s.sale_date BETWEEN %s AND %s
            GROUP BY p.category
            HAVING COUNT(s.id) > 5
            ORDER BY revenue DESC
        """
        return self.db.execute_query(query, (start_date, end_date))
    
    def get_customer_insights(self, customer_id):
        """Complex query with window functions"""
        query = """
            WITH customer_stats AS (
                SELECT 
                    sale_date,
                    amount,
                    SUM(amount) OVER (
                        PARTITION BY EXTRACT(MONTH FROM sale_date)
                    ) as monthly_total,
                    AVG(amount) OVER (
                        ORDER BY sale_date
                        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
                    ) as moving_avg
                FROM sales
                WHERE customer_id = %s
            )
            SELECT *,
                CASE 
                    WHEN amount > monthly_total * 0.5 THEN 'High Value'
                    WHEN amount > monthly_total * 0.2 THEN 'Medium Value'
                    ELSE 'Low Value'
                END as transaction_category
            FROM customer_stats
        """
        return self.db.execute_query(query, (customer_id,))
```

### Stored Procedures
```python
class ProcedureManager:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_update_inventory_procedure(self):
        """Create stored procedure for inventory management"""
        query = """
            CREATE PROCEDURE update_inventory(
                IN product_id INT,
                IN quantity INT,
                IN operation VARCHAR(10)
            )
            BEGIN
                DECLARE current_stock INT;
                
                SELECT stock INTO current_stock
                FROM inventory
                WHERE id = product_id;
                
                IF operation = 'add' THEN
                    UPDATE inventory
                    SET stock = current_stock + quantity
                    WHERE id = product_id;
                ELSEIF operation = 'remove' THEN
                    IF current_stock >= quantity THEN
                        UPDATE inventory
                        SET stock = current_stock - quantity
                        WHERE id = product_id;
                    ELSE
                        SIGNAL SQLSTATE '45000'
                        SET MESSAGE_TEXT = 'Insufficient stock';
                    END IF;
                END IF;
            END
        """
        self.db.execute_query(query)
    
    def call_procedure(self, procedure_name, params):
        """Call stored procedure"""
        placeholders = ', '.join(['%s'] * len(params))
        query = f"CALL {procedure_name}({placeholders})"
        return self.db.execute_query(query, params)
```

## Security Considerations

1. SQL Injection Prevention:
```python
class SecureQueryBuilder:
    @staticmethod
    def build_select(table, conditions=None, fields=None):
        """Build secure parameterized query"""
        fields = fields or ['*']
        query = f"SELECT {', '.join(fields)} FROM {table}"
        params = []
        
        if conditions:
            clauses = []
            for key, value in conditions.items():
                if isinstance(value, (list, tuple)):
                    placeholders = ', '.join(['%s'] * len(value))
                    clauses.append(f"{key} IN ({placeholders})")
                    params.extend(value)
                else:
                    clauses.append(f"{key} = %s")
                    params.append(value)
            query += " WHERE " + " AND ".join(clauses)
        
        return query, params
```

2. Access Control:
```python
class DatabaseAccessControl:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_user(self, username, password, privileges):
        """Create database user with specific privileges"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create user
            cursor.execute(
                "CREATE USER %s@'localhost' IDENTIFIED BY %s",
                (username, password)
            )
            
            # Grant privileges
            for table, actions in privileges.items():
                grant_sql = f"GRANT {', '.join(actions)} ON {table} TO %s@'localhost'"
                cursor.execute(grant_sql, (username,))
            
            cursor.close()
    
    def revoke_access(self, username, privileges):
        """Revoke specific privileges"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            for table, actions in privileges.items():
                revoke_sql = f"REVOKE {', '.join(actions)} ON {table} FROM %s@'localhost'"
                cursor.execute(revoke_sql, (username,))
            
            cursor.close()
```

## Performance Optimization

1. Query Optimization:
```python
class QueryOptimizer:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def analyze_query(self, query, params=None):
        """Analyze query execution plan"""
        explain_query = f"EXPLAIN ANALYZE {query}"
        return self.db.execute_query(explain_query, params)
    
    def create_indexes(self, table, columns):
        """Create indexes for performance"""
        for column in columns:
            index_name = f"idx_{table}_{column}"
            query = f"CREATE INDEX {index_name} ON {table} ({column})"
            self.db.execute_query(query)
    
    def optimize_table(self, table):
        """Optimize table structure"""
        return self.db.execute_query(f"OPTIMIZE TABLE {table}")
```

2. Connection Pooling:
```python
from mysql.connector import pooling

class ConnectionPool:
    def __init__(self, pool_name, pool_size=5):
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            pool_name=pool_name,
            pool_size=pool_size,
            **MYSQL_CONFIG
        )
    
    @contextmanager
    def get_connection(self):
        """Get connection from pool"""
        conn = self.pool.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
```

## Testing

1. Unit Tests:
```python
import unittest
from unittest.mock import patch

class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager('mysql')
        self.crud = CRUDManager(self.db)
    
    def test_crud_operations(self):
        # Create record
        data = {
            'name': 'Test Product',
            'price': 99.99,
            'category': 'Test'
        }
        result = self.crud.create_record('products', data)
        self.assertEqual(result, 1)
        
        # Read record
        records = self.crud.read_records(
            'products',
            {'name': 'Test Product'}
        )
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['price'], 99.99)
    
    def test_transaction_handling(self):
        manager = TransactionManager(self.db)
        
        with self.assertRaises(ValueError):
            manager.transfer_funds(1, 2, 1000000)  # Should fail
```

2. Integration Tests:
```python
class DatabaseIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db = DatabaseManager('mysql')
        self.query = QueryManager(self.db)
    
    def test_complex_query(self):
        # Setup test data
        self.setup_test_data()
        
        # Run complex query
        results = self.query.get_sales_report(
            '2023-01-01',
            '2023-12-31'
        )
        
        # Verify results
        self.assertTrue(len(results) > 0)
        self.assertTrue(all(
            'revenue' in row and 'avg_sale' in row
            for row in results
        ))
        
        # Clean up
        self.cleanup_test_data()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your example with documentation
4. Include tests
5. Submit a pull request

## License

MIT License - feel free to use these examples in your own projects.
