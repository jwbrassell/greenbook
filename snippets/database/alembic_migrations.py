"""
Alembic Database Migrations Example
Shows how to handle database schema changes - something that would require manual SQL in PHP
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/dbname')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""
Migration Commands (run in terminal):

# Initialize migrations (first time only)
flask db init

# Create a new migration
flask db migrate -m "Add user table"

# Apply migrations
flask db upgrade

# Rollback migrations
flask db downgrade
"""

# Example 1: Initial Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

"""
After creating this model:
1. Run: flask db migrate -m "Create user table"
2. Review generated migration in migrations/versions/
3. Run: flask db upgrade
"""

# Example 2: Adding new fields to existing model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # New fields added
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)

"""
After adding new fields:
1. Run: flask db migrate -m "Add user timestamps and status"
2. Review migration - Alembic detects the new columns
3. Run: flask db upgrade
"""

# Example 3: Adding a new table with relationship
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# Update User model to include relationship
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    # Add relationship
    posts = db.relationship('Post', backref='author', lazy=True)

"""
After adding new table and relationship:
1. Run: flask db migrate -m "Add posts table"
2. Review migration - should create posts table and foreign key
3. Run: flask db upgrade
"""

# Example 4: Data Migration
"""
Sometimes you need to migrate data, not just schema.
Create a new migration file with upgrade() and downgrade():

```python
# migrations/versions/xxxx_migrate_user_data.py
from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    # Get connection
    conn = op.get_bind()
    
    # Example: Update all inactive users' status
    conn.execute(
        sa.text("UPDATE user SET is_active = FALSE WHERE last_login < :cutoff"),
        {"cutoff": datetime(2023, 1, 1)}
    )

def downgrade():
    # Reverse the changes if needed
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE user SET is_active = TRUE"))
```
"""

# Example 5: Index Creation
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    is_active = db.Column(db.Boolean, default=True)
    posts = db.relationship('Post', backref='author', lazy=True)
    
    # Add index for faster queries
    __table_args__ = (
        db.Index('idx_user_username_email', 'username', 'email'),
    )

"""
After adding index:
1. Run: flask db migrate -m "Add user indexes"
2. Review migration - should create new index
3. Run: flask db upgrade
"""

# Common Scenarios and Best Practices

"""
1. Handling Large Tables:
   For large tables, consider batching migrations:

```python
def upgrade():
    conn = op.get_bind()
    # Process in batches
    offset = 0
    batch_size = 1000
    while True:
        users = conn.execute(
            sa.text("SELECT id FROM user LIMIT :limit OFFSET :offset"),
            {"limit": batch_size, "offset": offset}
        ).fetchall()
        
        if not users:
            break
            
        for user in users:
            conn.execute(
                sa.text("UPDATE user SET is_active = TRUE WHERE id = :id"),
                {"id": user.id}
            )
            
        offset += batch_size
```

2. Testing Migrations:
   Always test migrations on a copy of production data:
   - Create a staging database
   - Copy production schema and data
   - Run migrations
   - Verify data integrity
   - Measure migration time

3. Backup Before Migrating:
   ```bash
   # MySQL
   mysqldump -u user -p database > backup.sql
   
   # PostgreSQL
   pg_dump -U user database > backup.sql
   ```

4. Rolling Back:
   Always implement downgrade() functions:
   ```python
   def upgrade():
       op.add_column('user', sa.Column('new_field', sa.String(50)))
       
   def downgrade():
       op.drop_column('user', 'new_field')
   ```
"""
