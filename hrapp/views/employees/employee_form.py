import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, modelfactory
from ..connection import Connection
from .details import get_employee


def get_employees():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = modelfactory(Employee)
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
        WHERE e.id = ?
        """)

        return db_cursor.fetchall()


@login_required
def employee_form(request):
    if request.method == 'GET':
        employees = get_employees()
        template = 'employees/employee_form.html'
        context = {
            'all_employees': employees
        }

        return render(request, template, context)


@login_required
def employee_edit_form(request, employee_id):

    if request.method == 'GET':
        employee = get_employee(employee_id)
        employees = get_employees()

        template = 'employees/employee_form.html'
        context = {
            'employee': employee,
            'all_employees': employees
        }

        return render(request, template, context)