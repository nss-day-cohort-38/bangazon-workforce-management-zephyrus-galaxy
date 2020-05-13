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
            c.decommission_date  
        FROM hrapp_computer c
        """)

        return db_cursor.fetchall()


@login_required
def computer_form(request):

    if request.method == 'GET':
        computers = get_computers()
        template = 'computers/computer_form.html'
        context = {
            'all_computers': computers
        }
        return render(request, template, context)
    