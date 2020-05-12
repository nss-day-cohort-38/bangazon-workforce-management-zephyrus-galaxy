import sqlite3
from django.shortcuts import render
from hrapp.models import Computer
from ..connection import Connection


def computer_list(request):
    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            db_cursor.execute("""
            SELECT
                c.id,
                c.make,
                c.manufacturer,
                c.purchase_date,
                c.decomission_date
            FROM hrapp_computer c
            """)

            all_computers = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                computer = Computer()
                computer.id = row['id']
                computer.make = row['make']
                computer.manufacturer = row['manufacturer']
                computer.purchase_date = row['purchase_date']
                computer.decomission_date = row['decomission_date']
                all_computers.append(computer)

    template = 'computer/computer_list.html'
    context = {
        'computers': all_computers
    }

    return render(request, template, context)
