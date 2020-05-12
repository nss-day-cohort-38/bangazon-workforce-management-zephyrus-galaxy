import sqlite3
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from hrapp.models import computer, Department, model_factory, Computer
from ..connection import Connection
from .computer_detail import get_computer


def get_computers():
    with sqlite3.connect(Connection.db_path) as conn:
        conn.row_factory = model_factory(Computer)
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            c.id computer_id,
            c.manufacturer,
            c.make,
            c.purchase_date,
            c.decommission_date,
          
            
        FROM hrapp_computer c
        """)

        return db_cursor.fetchall()


@login_required
def computer_form(request):

    if request.method == 'GET':
        template = 'computers/computer_form.html'

        return render(request, template)
    elif request.method == 'POST':
        form_data = request.POST
        if (
            "actual_method" in form_data
            and form_data["actual_method"] == "PUT"
        ):
            with sqlite3.connect(Connection.db_path) as conn:
                db_cursor = conn.cursor()

                db_cursor.execute("""
                UPDATE hrapp_computer
                SET manufacturer = ?,
                    make = ?,
                    purchase_date = ?,
                    decommission_date = ?
                """,
                    (
                        form_data['manufacturer'], form_data['make'],
                        form_data['purchase_date'], form_data['decommission_date']
                    ))

            return redirect('hrapp:computer_list')
    