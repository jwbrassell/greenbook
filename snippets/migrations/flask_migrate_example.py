"""
Flask-Migrate Example - Database Schema Management
Shows how to handle database changes properly compared to PHP's manual migrations
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql://user:password@localhost/dbname')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

"""
PHP Traditional Migration (Manual SQL):
```php
// migrations/001_create_users_table.php
function up() {
    $sql = "CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(80) NOT NULL,
        email VARCHAR(120) NOT NULL
    )";
    mysql_query($sql);
}

function down() {
    mysql_query("DROP TABLE users");
}

// migrations/002_add_user_status.php
function up() {
    mysql_query("ALTER TABLE users ADD COLUMN status VARCHAR(20)");
}

function down() {
    mysql_query("ALTER TABLE users DROP COLUMN status");
}

// Running migrations manually
foreach (glob("migrations/*.php") as $file) {
    require_once($file);
    up();
}
```
"""

# Initial Models
"""
Step 1: Initial database schema
Run: flask db init
     flask db migrate -m "Initial migration"
     flask db upgrade
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

"""
Step 2: Add new fields
Run: flask db migrate -m "Add user status and role"
     flask db upgrade
"""

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # New fields
    status = db.Column(db.String(20), default='active')
    role = db.Column(db.String(20), default='user')

"""
Step 3: Add relationships
Run: flask db migrate -m "Add posts table with user relationship"
     flask db upgrade
"""

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')
    role = db.Column(db.String(20), default='user')
    # Add relationship
    posts = db.relationship('Post', backref='author', lazy=True)

"""
Step 4: Complex schema changes
Run: flask db migrate -m "Add categories and tags"
     flask db upgrade
"""

# Many-to-many relationship table
post_tags = db.Table('post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    posts = db.relationship('Post', backref='category', lazy=True)

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add category relationship
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # Add tags relationship
    tags = db.relationship('Tag', secondary=post_tags, lazy='subquery',
                          backref=db.backref('posts', lazy=True))

# Custom Migration Examples

"""
Example 1: Data Migration
Create migration file: flask db revision -m "Migrate user roles"

```python
# migrations/versions/xxxx_migrate_user_roles.py
from alembic import op
import sqlalchemy as sa
from datetime import datetime

def upgrade():
    # Get database connection
    connection = op.get_bind()
    
    # Update all admin emails to have admin role
    connection.execute(
        sa.text('''
            UPDATE user 
            SET role = 'admin' 
            WHERE email LIKE '%@admin.com'
        ''')
    )
    
    # Set default role for others
    connection.execute(
        sa.text('''
            UPDATE user 
            SET role = 'user' 
            WHERE role IS NULL
        ''')
    )

def downgrade():
    connection = op.get_bind()
    connection.execute(sa.text('UPDATE user SET role = NULL'))
```
"""

"""
Example 2: Column Modification
Create migration file: flask db revision -m "Modify email column"

```python
# migrations/versions/xxxx_modify_email_column.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create temporary column
    op.add_column('user', sa.Column('new_email', sa.String(150)))
    
    # Copy and transform data
    connection = op.get_bind()
    connection.execute(
        sa.text('UPDATE user SET new_email = LOWER(email)')
    )
    
    # Drop old column and rename new one
    op.drop_column('user', 'email')
    op.alter_column('user', 'new_email',
                    new_column_name='email',
                    existing_type=sa.String(150),
                    nullable=False)
    
    # Add unique constraint
    op.create_unique_constraint('uq_user_email', 'user', ['email'])

def downgrade():
    op.drop_constraint('uq_user_email', 'user', type_='unique')
    op.alter_column('user', 'email',
                    existing_type=sa.String(150),
                    type_=sa.String(120))
```
"""

"""
Example 3: Table Restructuring
Create migration file: flask db revision -m "Restructure user profiles"

```python
# migrations/versions/xxxx_restructure_user_profiles.py
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Create new table
    op.create_table(
        'user_profile',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('full_name', sa.String(100)),
        sa.Column('bio', sa.Text),
        sa.Column('location', sa.String(100)),
        sa.ForeignKeyConstraint(['user_id'], ['user.id']),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Migrate existing data
    connection = op.get_bind()
    connection.execute(
        sa.text('''
            INSERT INTO user_profile (user_id, full_name)
            SELECT id, username FROM user
        ''')
    )

def downgrade():
    op.drop_table('user_profile')
```
"""

# Best Practices

"""
1. Migration Organization:
   - Use meaningful migration names
   - Keep migrations atomic
   - Include both upgrade and downgrade
   - Test migrations thoroughly

2. Data Safety:
   - Backup database before migrating
   - Test migrations on copy of production data
   - Handle data transformation carefully
   - Implement rollback procedures

3. Performance:
   - Consider table size when altering
   - Use batching for large data migrations
   - Schedule migrations during low traffic
   - Monitor migration duration

4. Version Control:
   - Commit migrations with related code
   - Never modify existing migrations
   - Use sequential version numbers
   - Document migration dependencies

5. Example Backup Script:
```python
def backup_database():
    import subprocess
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f'backup_{timestamp}.sql'
    
    # MySQL backup
    subprocess.run([
        'mysqldump',
        '-u', 'user',
        '-p password',
        'database_name',
        '>', backup_file
    ])
    
    return backup_file
```

6. Migration Testing:
```python
def test_migration(migration_id):
    # Create test database
    test_db = create_test_database()
    
    try:
        # Run migration
        flask db upgrade {migration_id}
        
        # Verify data integrity
        verify_data_integrity()
        
        # Test downgrade
        flask db downgrade {migration_id}
        verify_original_state()
        
    finally:
        drop_test_database(test_db)
```

7. Large Data Migration:
```python
def batch_migrate_data(batch_size=1000):
    connection = op.get_bind()
    
    while True:
        # Process batch
        result = connection.execute(
            sa.text('''
                UPDATE user 
                SET new_status = 'active'
                WHERE status IS NULL
                LIMIT :batch_size
            '''),
            {'batch_size': batch_size}
        )
        
        if result.rowcount == 0:
            break
```
"""

if __name__ == '__main__':
    app.run(debug=True)
