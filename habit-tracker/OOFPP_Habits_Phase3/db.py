import sqlite3
from prettytable import *


def get_db(name):
    """
    Opens the db file.
        :param name: the name of the db file
    """
    db = sqlite3.connect(name)
    create_tables(db)
    return db


def create_tables(db):
    """
    Creates tables in the database file.
        :param db: the name of the db file
    """
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS habit_data ("
                "name varchar(250) NOT NULL, frequency varchar(250) NOT NULL, "
                "periodicity varchar(250) NOT NULL, start_date varchar(250) NOT NULL, check_off INTEGER,"
                "last_updated_day varchar(250) NOT NULL, streak_days INTEGER, longest_st_days INTEGER)")
    db.commit()


def add_habits(db, name: str, frequency: str, periodicity: str, start_date: str,
               check_off: int, last_updated_day: str, streak_days: int, longest_st_days: int):
    """
    Stores habit data in a database file.
        :param db: the name of the db file
        :param name: the name of the habit
        :param frequency: the frequency of the habit
        :param start_date: the date when this habit was created
        :param periodicity: how long the habit lasts
        :param check_off: how many times the habit was performed
        :param last_updated_day: the day when the habit was marked as completed
        :param streak_days: the number of streak days
        :param longest_st_days: the number of the longest streak days
    """
    cur = db.cursor()
    cur.execute(f"INSERT INTO habit_data VALUES("
                f"'{name}', '{frequency}', '{periodicity}', '{start_date}', "
                f"'{check_off}', '{last_updated_day}', '{streak_days}', '{longest_st_days}')")
    db.commit()


def get_rows(db, thing, value):
    """
    Visualization of habit data in a table.
        :param db: the name of the db file
        :param thing: the name of the column in the table
        :param value: the value of the column
    """
    cur = db.cursor()

    if thing is None and value is None:
        rows = cur.execute(f"SELECT * FROM habit_data;")
        db.commit()
    else:
        rows = cur.execute(f"SELECT * FROM habit_data WHERE {thing} = '{value}';")
        db.commit()

    def pretty_table(list_rows):
        p_table = PrettyTable()
        p_table.field_names = ['Name', 'Frequency', 'Periodicity', 'Start Date',
                               'Check-off', 'Last Updated Day', 'Streak Days', 'Longest St. Days']
        rows_listed = [list(row) for row in list_rows]
        p_table.add_rows(rows_listed)
        p_table.set_style(ORGMODE)
        return p_table

    table = pretty_table(list_rows=rows)
    return table
