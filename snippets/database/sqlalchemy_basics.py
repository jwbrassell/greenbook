"""
SQLAlchemy Basic Examples - Transitioning from PHP file-based storage to SQLAlchemy
This file demonstrates common database operations using SQLAlchemy ORM
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Replace with your database URL - Example shows MySQL since that's common in PHP environments
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model Definition
class User(db.Model):
    """
    Example user model showing common column types and relationships
    Equivalent to creating a users table in PHP/MySQL
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # One-to-many relationship example
    posts = db.relationship('Post', backref='author', lazy=True)

    def to_dict(self):
        """
        Convert to dictionary - similar to json_encode() in PHP
        """
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Example Operations

def create_user(username, email):
    """
    PHP Equivalent:
    $user = ['username' => $username, 'email' => $email];
    $users = json_decode(file_get_contents('users.json'), true);
    $users[] = $user;
    file_put_contents('users.json', json_encode($users));
    """
    try:
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

def get_user(user_id):
    """
    PHP Equivalent:
    $users = json_decode(file_get_contents('users.json'), true);
    $user = array_filter($users, function($u) use ($user_id) {
        return $u['id'] == $user_id;
    });
    """
    return User.query.get_or_404(user_id)

def update_user(user_id, new_username):
    """
    PHP Equivalent:
    $users = json_decode(file_get_contents('users.json'), true);
    foreach ($users as &$user) {
        if ($user['id'] == $user_id) {
            $user['username'] = $new_username;
            break;
        }
    }
    file_put_contents('users.json', json_encode($users));
    """
    try:
        user = User.query.get_or_404(user_id)
        user.username = new_username
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise e

def delete_user(user_id):
    """
    PHP Equivalent:
    $users = json_decode(file_get_contents('users.json'), true);
    $users = array_filter($users, function($u) use ($user_id) {
        return $u['id'] != $user_id;
    });
    file_put_contents('users.json', json_encode($users));
    """
    try:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        raise e

# Advanced Query Examples

def get_users_with_posts():
    """
    Demonstrates joining related data - much simpler than PHP file manipulation
    """
    return User.query.join(Post).all()

def search_users(email_domain):
    """
    Complex filtering - would require manual array filtering in PHP
    """
    return User.query.filter(
        User.email.endswith(email_domain)
    ).order_by(User.username).all()

def get_user_post_count():
    """
    Aggregation example - would require manual counting in PHP
    """
    from sqlalchemy import func
    return db.session.query(
        User.username,
        func.count(Post.id).label('post_count')
    ).join(Post).group_by(User.id).all()

# Example Usage in Flask Route
@app.route('/user/<int:user_id>')
def user_detail(user_id):
    user = get_user(user_id)
    return user.to_dict()
