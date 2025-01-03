from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import math

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/employees'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100))
    office = db.Column(db.String(100))
    age = db.Column(db.Integer)
    start_date = db.Column(db.Date)
    salary = db.Column(db.Float)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/employees', methods=['POST'])
def get_employees():
    # Get DataTables parameters
    draw = request.form.get('draw', type=int)
    start = request.form.get('start', type=int)
    length = request.form.get('length', type=int)
    search_value = request.form.get('search[value]', type=str)
    order_column = request.form.get('order[0][column]', type=int)
    order_dir = request.form.get('order[0][dir]', type=str)

    # Column list for ordering
    columns = ['name', 'position', 'office', 'age', 'start_date', 'salary']
    
    # Base query
    query = Employee.query

    # Search filter
    if search_value:
        search_value = f"%{search_value}%"
        query = query.filter(
            db.or_(
                Employee.name.like(search_value),
                Employee.position.like(search_value),
                Employee.office.like(search_value)
            )
        )

    # Column specific filters
    for i, column in enumerate(columns):
        column_search_value = request.form.get(f'columns[{i}][search][value]')
        if column_search_value:
            column_obj = getattr(Employee, column)
            query = query.filter(column_obj.like(f"%{column_search_value}%"))

    # Get total records count
    total_records = query.count()
    
    # Ordering
    if order_column is not None:
        column = columns[order_column]
        order_obj = getattr(Employee, column)
        if order_dir == 'desc':
            order_obj = order_obj.desc()
        query = query.order_by(order_obj)

    # Pagination
    query = query.offset(start).limit(length)

    # Execute query
    employees = query.all()

    # Format data for DataTables
    data = []
    for emp in employees:
        data.append({
            'id': emp.id,
            'name': emp.name,
            'position': emp.position,
            'office': emp.office,
            'age': emp.age,
            'start_date': emp.start_date.strftime('%Y-%m-%d'),
            'salary': f"{emp.salary:,.2f}"
        })

    return jsonify({
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': data
    })

@app.route('/api/employee/<int:id>', methods=['DELETE'])
def delete_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        db.session.delete(employee)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/employee/<int:id>', methods=['PUT'])
def update_employee(id):
    try:
        employee = Employee.query.get_or_404(id)
        data = request.json
        
        employee.name = data.get('name', employee.name)
        employee.position = data.get('position', employee.position)
        employee.office = data.get('office', employee.office)
        employee.age = data.get('age', employee.age)
        employee.salary = data.get('salary', employee.salary)
        
        if 'start_date' in data:
            employee.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
