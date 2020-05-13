import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from hrapp.models import model_factory
from ..connection import Connection
from datetime import date


def get_training_program(training_program_id):
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            t.id,
            t.title,
            t.start_date,
            t.end_date,
            t.capacity
        FROM hrapp_trainingprogram t
        WHERE t.id = ?
        """, (training_program_id,))

        return db_cursor.fetchone()
        

def get_employee_training_program(training_program_id): 
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            etp.id, 
                etp.employee_id,
                etp.training_program_id, 
                e.id, 
                e.first_name, 
                e.last_name, 
                t.id,
                t.title,
                t.start_date,
                t.end_date,
                t.capacity
            FROM hrapp_employeetrainingprogram etp
            JOIN hrapp_trainingprogram t ON t.id = etp.training_program_id    
            JOIN hrapp_employee e ON e.id = etp.employee_id     
            WHERE t.id = ?
        """, (training_program_id,))
        return db_cursor.fetchall()


def training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)
        employee_training_program = get_employee_training_program(training_program_id)
        template = 'training_programs/detail.html'
        context = {
            'training_program': training_program,
            'employee_training_program': employee_training_program
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_trainingprogram
                SET title = ?,
                    start_date = ?,
                    end_date = ?,
                    capacity = ?
                WHERE id = ?
                """,
                (
                    form_data['title'], form_data['start_date'],
                    form_data['end_date'], form_data['capacity'],
                    training_program_id,
                ))

            return redirect(reverse('hrapp:training_programs'))

    if request.method == 'POST':
        form_data = request.POST

        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "DELETE"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                DELETE FROM hrapp_trainingprogram
                WHERE id = ?
                """, (training_program_id,))

            return redirect(reverse('hrapp:training_programs'))