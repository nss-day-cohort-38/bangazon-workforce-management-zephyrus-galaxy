import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, model_factory
from ..connection import Connection
from .detail import get_employee


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Employee)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id employee_id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.department_id,
            e.is_supervisor,
            d.id department_id
        FROM hrapp_employee e
        JOIN hrapp_department d ON e.department_id = d.id
        """)

        return db_cursor.fetchall()

def get_departments():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Department)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            d.id,
            d.dept_name,
            d.budget
        FROM hrapp_department d
        """)

        return db_cursor.fetchall()


@login_required
def employee_form(request):
    if request.method == 'GET':
        departments = get_departments()
        template = 'employees/employee_form.html'
        context = {
            'all_departments': departments
        }
        return render(request, template, context)
    elif request.method == 'POST':
        form_data = request.POST

    with sqlite3.connect(Connection.db_path) as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO hrapp_employee
        (
            first_name, last_name, start_date, is_supervisor, department_id
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (form_data['first_name'], form_data['last_name'], form_data['start_date'],
        form_data['is_supervisor'], form_data['department']))

    return redirect('hrapp:employee_list')


@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = get_employee(employee_id)
        employees = get_employees()
        departments = get_departments()

        template = 'employees/employee_form.html'
        context = {
            'employee': employee,
            'all_employees': employees,
            'all_departments': departments
        }

        return render(request, template, context)
