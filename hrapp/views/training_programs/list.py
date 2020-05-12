import sqlite3
from django.shortcuts import render, redirect
from hrapp.models import TrainingProgram
from ..connection import Connection
from django.urls import reverse
from datetime import datetime


def training_program_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            select
                t.id,
                t.title,
                t.start_date,
                t.end_date,
                t.capacity
            from hrapp_trainingprogram t
            """)

            all_training_programs = []

            dataset = db_cursor.fetchall()

            for row in dataset:
                training_program = TrainingProgram()
                training_program.id = row['id']
                training_program.title = row['title']
                training_program.start_date = row['start_date']
                training_program.end_date = row['end_date']
                training_program.capacity = row['capacity']
              

                all_training_programs.append(training_program)

        template = 'training_programs/list.html'

        upcoming_training_programs = []

        for program in all_training_programs:
            end_date = datetime.strptime(program.end_date, '%Y-%m-%d')
            if end_date > datetime.today():
                upcoming_training_programs.append(program)


        context = {
            'upcoming_training_programs': upcoming_training_programs
        }

        return render(request, template, context)

    elif request.method == 'POST':
        form_data = request.POST

        with sqlite3.connect(Connection.db_path) as conn:
            db_cursor = conn.cursor()

            db_cursor.execute("""
            INSERT INTO hrapp_trainingprogram
            (
                title, start_date, end_date, capacity
            )
            VALUES (?, ?, ?, ?)
            """,
            (form_data['title'], form_data['start_date'],
                form_data['end_date'], form_data['capacity']))

        return redirect(reverse('hrapp:training_programs'))