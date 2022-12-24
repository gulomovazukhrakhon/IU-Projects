import sqlite3
from prettytable import *


def get_db(name):
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS habit_data ("
                "name varchar(250) NOT NULL, frequency text, "
                "periodicity varchar(250) NOT NULL, unitset varchar(250) NOT NULL, "
                "start_date varchar(250) NOT NULL, end_date varchar(250) NOT NULL, check_off INTEGER,"
                "last_updated_day varchar(250) NOT NULL, streak_days INTEGER)")
    db.commit()


def add_habits(db, name: str, frequency: str, periodicity: str, unitset: str, start_date: str,
               end_date: str, check_off: int, last_updated_day: str, streak_days: int):
    cur = db.cursor()
    cur.execute(f"INSERT INTO habit_data VALUES('{name}', '{frequency}', "
                f"'{periodicity}', '{unitset}', '{start_date}', '{end_date}', "
                f"'{check_off}', '{last_updated_day}', '{streak_days}')")
    db.commit()


def get_rows(db, thing, value):
    cur = db.cursor()

    if thing is None and value is None:
        rows = cur.execute(f"SELECT * FROM habit_data;")
        db.commit()
    else:
        rows = cur.execute(f"SELECT * FROM habit_data WHERE {thing} = '{value}';")
        db.commit()

    def pretty_table(list_rows):
        p_table = PrettyTable()
        p_table.field_names = ['Name', 'Frequency', 'Periodicity', 'Unitset', 'Start Date', 'End Date',
                               'Check-off', 'Last Updated Day', 'Streak Days']
        rows_listed = [list(row) for row in list_rows]
        p_table.add_rows(rows_listed)
        p_table.set_style(ORGMODE)
        return p_table

    table = pretty_table(list_rows=rows)
    return table
