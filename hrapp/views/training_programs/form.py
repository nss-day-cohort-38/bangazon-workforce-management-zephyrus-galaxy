import sqlite3
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from hrapp.models import model_factory
from ..connection import Connection
from .details import get_training_program


def get_training_programs():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(TrainingProgram)
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

        return db_cursor.fetchall()

# @login_required
def training_program_form(request):
    if request.method == 'GET':
        training_programs = get_training_programs()
        template = 'training_programs/form.html'
        context = {
            'all_training_programs': training_programs
        }

        return render(request, template, context)


def training_program_edit_form(request, training_program_id):

    if request.method == 'GET':
        training_program = get_training_program(training_program_id)

        template = 'training_programs/form.html'
        context = {
            'training_program': training_program,
        }

        return render(request, template, context)