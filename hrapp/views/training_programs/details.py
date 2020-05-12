import sqlite3
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hrapp.models import TrainingProgram
from hrapp.models import model_factory
from ..connection import Connection


def get_training_program(trainingprogram_id):
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
        """, (trainingprogram_id,))

        return db_cursor.fetchone()

@login_required
def training_program_details(request, training_program_id):
    if request.method == 'GET':
        training_program = get_training_program(training_program_id)

        template = 'training_programs/detail.html'
        context = {
            'training_program': training_program
        }

        return render(request, template, context)

    if request.method == 'POST':
        form_data = request.POST

        # Check if this POST is for deleting a training_program
        #
        # Note: You can use parenthesis to break up complex
        #       `if` statements for higher readability
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