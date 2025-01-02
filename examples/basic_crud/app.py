"""
Basic CRUD Application Example
This example demonstrates a simple CRUD application using Flask and SQLAlchemy.
It shows the transition from PHP-style file-based data storage to a proper database.
"""

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

# Routes for Web Interface
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

@app.route('/items/new', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        item = Item(
            name=request.form['name'],
            description=request.form['description']
        )
        db.session.add(item)
        db.session.commit()
        return jsonify(item.to_dict()), 201
    return render_template('create.html')

@app.route('/items/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(id):
    item = Item.query.get_or_404(id)
    
    if request.method == 'GET':
        return render_template('detail.html', item=item)
    
    elif request.method == 'PUT':
        data = request.get_json()
        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        db.session.commit()
        return jsonify(item.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return '', 204

# API Routes
@app.route('/api/items', methods=['GET'])
def list_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/api/items', methods=['POST'])
def api_create_item():
    data = request.get_json()
    item = Item(
        name=data['name'],
        description=data.get('description', '')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

@app.route('/api/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@app.route('/api/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/api/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)
