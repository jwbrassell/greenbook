from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from typing import Optional
import json
from datetime import date, datetime

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'user',
    'password': 'password',
    'database': 'employees'
}

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/employees")
async def get_employees(request: Request):
    form_data = await request.form()
    
    # DataTables parameters
    draw = int(form_data.get('draw', 1))
    start = int(form_data.get('start', 0))
    length = int(form_data.get('length', 10))
    search_value = form_data.get('search[value]', '')
    order_column_index = int(form_data.get('order[0][column]', 0))
    order_dir = form_data.get('order[0][dir]', 'asc')

    # Column names for ordering
    columns = ['name', 'position', 'office', 'age', 'start_date', 'salary']
    order_column = columns[order_column_index]

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Base query
        query = """
            SELECT SQL_CALC_FOUND_ROWS 
                id, name, position, office, age, start_date, salary 
            FROM employees
        """
        params = []

        # Search condition
        if search_value:
            query += """ 
                WHERE name LIKE %s 
                OR position LIKE %s 
                OR office LIKE %s
            """
            search_param = f"%{search_value}%"
            params.extend([search_param, search_param, search_param])

        # Column specific filters
        for i, column in enumerate(columns):
            column_search = form_data.get(f'columns[{i}][search][value]')
            if column_search:
                if 'WHERE' not in query:
                    query += " WHERE"
                else:
                    query += " AND"
                query += f" {column} LIKE %s"
                params.append(f"%{column_search}%")

        # Ordering
        query += f" ORDER BY {order_column} {order_dir}"

        # Pagination
        query += " LIMIT %s, %s"
        params.extend([start, length])

        # Execute main query
        cursor.execute(query, params)
        data = cursor.fetchall()

        # Get total records count
        cursor.execute("SELECT FOUND_ROWS()")
        records_filtered = cursor.fetchone()['FOUND_ROWS()']

        # Get total records without filtering
        cursor.execute("SELECT COUNT(*) as count FROM employees")
        records_total = cursor.fetchone()['count']

        # Format data
        formatted_data = []
        for row in data:
            formatted_data.append({
                'id': row['id'],
                'name': row['name'],
                'position': row['position'],
                'office': row['office'],
                'age': row['age'],
                'start_date': row['start_date'].strftime('%Y-%m-%d'),
                'salary': f"{float(row['salary']):,.2f}"
            })

        return {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': formatted_data
        }

    finally:
        cursor.close()
        conn.close()

@app.delete("/api/employee/{employee_id}")
async def delete_employee(employee_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
        conn.commit()
        return {'success': True}
    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cursor.close()
        conn.close()

@app.put("/api/employee/{employee_id}")
async def update_employee(employee_id: int, request: Request):
    data = await request.json()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        query = """
            UPDATE employees 
            SET name = %s, position = %s, office = %s, 
                age = %s, start_date = %s, salary = %s
            WHERE id = %s
        """
        params = (
            data['name'],
            data['position'],
            data['office'],
            data['age'],
            data['start_date'],
            data['salary'],
            employee_id
        )
        
        cursor.execute(query, params)
        conn.commit()
        return {'success': True}
    except Exception as e:
        conn.rollback()
        return {'success': False, 'error': str(e)}
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
