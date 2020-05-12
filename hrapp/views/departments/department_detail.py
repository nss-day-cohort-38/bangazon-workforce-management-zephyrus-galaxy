import sqlite3
from django.shortcuts import render, redirect, reverse
from hrapp.models import Department, Employee
from ..connection import Connection
from django.contrib.auth.decorators import login_required

def all_departments(department_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.dept_name,
            d.budget,
            e.id,
            e.first_name,
            e.last_name,
            e.department_id
        FROM hrapp_department d
        LEFT JOIN hrapp_employee e ON d.id = e.department_id
        where d.id = ?
        """, (department_id,))

        data =  db_cursor.fetchall()

        department_check = []
        employee_group = []
        for row in data:
            if(len(department_check) == 0):
                department = Department()
                department.id = row['department_id']
                department.name = row['dept_name']
                department.budget = row['budget']
                department_check.append(department)

            employee = Employee()
            employee.id = row['id']
            employee.first_name = row['first_name']
            employee.last_name = row['last_name']
            employee.department_id = row['department_id']
            employee_group.append(employee)


        department_obj = {}
        
        department_obj["department"] = department_check[0]
        department_obj["employees"] = employee_group
        return department_obj

@login_required
def department_detail(request, department_id):
    if request.method == 'GET':
        department = all_departments(department_id)

        template = 'departments/department_detail.html'
        context = {
            'department': department["department"],
            'employees': department["employees"]
        }

        return render(request, template, context)
