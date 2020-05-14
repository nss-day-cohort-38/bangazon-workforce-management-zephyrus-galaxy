import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import Employee, Department, model_factory, Computer, TrainingProgram
from ..connection import Connection


def get_employee(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_employee
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id employee_id,
            e.first_name,
            e.last_name,
            e.start_date,
            e.is_supervisor,
            d.id department_id,
            d.dept_name,
            c.id computer_id,
            c.manufacturer,
            c.make
        FROM hrapp_employee e
        JOIN hrapp_department d ON e.department_id = d.id
        JOIN hrapp_employeecomputer ec ON e.id = ec.employee_id
        JOIN hrapp_computer c ON ec.computer_id = c.id
        WHERE e.id = ?
        """, (employee_id,))

        return db_cursor.fetchone()

@login_required
def employee_detail(request, employee_id):
    if request.method == 'GET':
        employee = get_employee(employee_id)
        training_program = get_training(employee_id)
        template_name = 'employees/detail.html'
        context = {
            'employee': employee,
            'training_program': training_program
        }
        return render(request, template_name, context)

    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                    DELETE FROM hrapp_employee
                    WHERE id = ?
                """, (employee_id,))

            return redirect(reverse('hrapp:employee_list'))

def get_training(employee_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)

        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            t.title
        FROM
            hrapp_employee e
            LEFT JOIN hrapp_employeetrainingprogram et ON e.id = et.employee_id
            LEFT JOIN hrapp_trainingprogram t ON t.id = et.training_program_id
        WHERE
            e.id = ?
        """, (employee_id,))

        return db_cursor.fetchall()

def create_employee(cursor, row):
    _row = sqlite3.Row(cursor, row)

    employee = Employee()
    employee.id = _row["employee_id"]
    employee.first_name = _row["first_name"]
    employee.last_name = _row["last_name"]
    employee.start_date = _row["start_date"]
    employee.department_id = _row["department_id"]
    employee.is_supervisor = _row["is_supervisor"]

    department = Department()
    department.id = _row["department_id"]
    department.dept_name = _row["dept_name"]

    computer = Computer()
    computer.manufacturer = _row["manufacturer"]
    computer.make = _row["make"]
    computer.id = _row["computer_id"]

    # training_program = TrainingProgram()
    # training_program.title = _row["title"]

    employee.department = department
    employee.computer = computer
    # employee.training_program = training_program

    return employee