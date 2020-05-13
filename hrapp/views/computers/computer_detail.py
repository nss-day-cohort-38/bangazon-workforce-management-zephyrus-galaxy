import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import model_factory, Computer
from ..connection import Connection


def get_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = create_computer
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT 
            c.id,
            c.make,
            c.manufacturer,
            c.purchase_date,
            c.decommission_date
        FROM hrapp_computer c
        WHERE id = ?
        """,(computer_id,))

        return db_cursor.fetchone()

def get_employee_computer(computer_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()
        
        db_cursor.execute('''
        SELECT c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decommission_date,
                ec.assign_date,
                ec.unassign_date,
                e.first_name,
                e.last_name
                from hrapp_computer c
                left join hrapp_employeecomputer ec on ec.computer_id = c.id
                left join hrapp_employee e on ec.employee_id = e.id
                where c.id = ?
            ''', (computer_id,))
         
        return db_cursor.fetchone()

@login_required
def computer_detail(request, computer_id):
    if request.method == 'GET':
        computer = get_computer(computer_id)
        employee_computer = get_employee_computer(computer_id)
        

        context = {
            'computer': computer,
            'employee_computer': employee_computer
        }
        template_name = 'computers/computer_detail.html'

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
                    DELETE FROM hrapp_computer
                    WHERE id = ?
                """, (computer_id,))

            return redirect(reverse('hrapp:computer_list'))

def create_computer(cursor, row):
    _row = sqlite3.Row(cursor, row)

    computer = Computer()
    computer.id = _row["id"]
    computer.manufacturer = _row["manufacturer"]
    computer.make = _row["make"]
    computer.purchase_date = _row["purchase_date"]
    computer.decommission_date = _row["decommission_date"]

    return computer
