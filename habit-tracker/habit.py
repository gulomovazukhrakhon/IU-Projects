from db import *
import datetime as dt
from datetime import timedelta
from dateutil.relativedelta import relativedelta


def habit_names(db_file):
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    names = cursor.execute(f"SELECT name FROM habit_data")
    rows = [list(name)[0] for name in names]

    return rows


class CreateHabit:
    """
        This class is responsible for creating a habit and storing it in database.

            Attributes:
                name (str):
                    the name of the habit
                frequency (str):
                    the frequency of the habit ("daily", "weekly")
                periodicity (str):
                    how long the habit lasts ("20 days", "10 weeks", "2 months")
                unitset (str):
                    the unit set of the habit ("20 minutes", "10 pages")
                start_date (str):
                    the start date of the habit (DD/MM/YYYY)
                end_date (str):
                    the end date of the habit (DD/MM/YYYY)
                check_off (int):
                    how many times the habit has been completed
                last_updated_day (str):
                    last time when the habit completed (DD/MM/YYYY)
                streak_days (int):
                    counts the number of streak days

            Methods:
                end_date(self, periodicity, date)
                    Calculates when the habit should end
                add_habit(self)
                    Adds a new habit and stores it in the database

    """

    def __init__(self, name: str, frequency: str, periodicity: str, unitset: str, start_date: str):

        """
        :param name: the name of the habit
        :param frequency: the frequency of the habit ("daily", "weekly")
        :param periodicity: how long the habit lasts ("20 days", "10 weeks", "2 months")
        :param unitset: the unit set of the habit ("20 minutes", "10 pages")
        :param start_date: the start date of the habit (DD/MM/YYYY)
        """

        self.name = name
        self.frequency = frequency
        self.periodicity = periodicity
        self.unitset = unitset
        self.start_date = start_date

        date = self.start_date.replace('/', ' ').split()
        periodicity = self.periodicity.split()
        self.end_date = self.end_date(periodicity, date)
        self.check_off = 0
        self.last_updated_day = "-"
        self.streak_days = 0

    def end_date(self, periodicity, date):

        """
        This function calculates when the habit should end

        :param periodicity: how long the habit lasts ("20 days", "10 weeks", "2 months")
        :param date: start date in (DDMMYYYY) format without /.
        :return: end_date

        Parameters are automatically assigned to the function and the function cannot be called directly.

        """

        if periodicity[1] == "days":
            end_date = (dt.datetime(int(date[2]), int(date[1]), int(date[0])) +
                        timedelta(days=int(periodicity[0]))).strftime("%d/%m/%Y")
            return end_date

        elif periodicity[1] == "weeks":
            end_date = (dt.datetime(int(date[2]), int(date[1]), int(date[0])) +
                        relativedelta(weeks=int(periodicity[0]))).strftime("%d/%m/%Y")
            return end_date

        elif periodicity[1] == "months":
            end_date = (dt.datetime(int(date[2]), int(date[1]), int(date[0])) +
                        relativedelta(months=int(periodicity[0]))).strftime("%d/%m/%Y")
            return end_date

    def add_habit(self, db_file):

        """
        :return: a new habit in the database
        """

        db = get_db(name=db_file)

        add_habits(db, self.name, self.frequency, self.periodicity, self.unitset, self.start_date,
                   self.end_date, self.check_off, self.last_updated_day, self.streak_days)

        table = get_rows(db=db, thing="name", value=f'{self.name}')
        print(table)


class ManageHabit:
    """
    Once a habit has been created, it needs to be marked, which will be done via this class.
    Users will also be able to change the name and the frequency of existing habits.
    Additionally, this class is responsible for analytics module.

        Methods:
            edit(self, name, thing, value)
                Changes the name and frequency of the specified habit.

            report_all(self)
                Shows all habits in a pretty table

            report_one(self, name):
                Shows a specified habit in a pretty table

            report_by_frequency(self, frequency):
                Shows specified habits in a pretty table based on their frequency (daily or weekly)

            check(self, name):
                The user can mark the habit when it is completed.

            streak_days(self, name, frequency):
                Counts streak days
    """

    def edit(self, name: str, thing: str, value: str, db_file):

        """
        :param db_file: the name of the database file
        :param name: the specified habit that needs to be changed
        :param thing: the name or the frequency that needs to be changed in the habit
        :param value: the new value of the name or the frequency
        :return:
            Updated name or frequency of the specified habit in the database
        """

        db = get_db(name=db_file)

        db.cursor().execute(f"UPDATE habit_data SET {thing} = '{value}'"
                            f"WHERE name = '{name}';")
        db.commit()

        if thing == "name":
            table = get_rows(db=db, thing="name", value=f'{value}')
        else:
            table = get_rows(db=db, thing="name", value=f'{name}')

        print(table)

    def report_all(self, db_file):
        """
        :param db_file: the name of the database file
        Shows all habits in a pretty table
        """

        db = get_db(name=db_file)
        table = get_rows(db=db, thing=None, value=None)
        print(table)

    def report_one(self, name: str, db_file):

        """
        :param db_file: the name of the database file
        :param name: the name of the specified habit
        Shows a specified habit in a pretty table
        """

        db = get_db(name=db_file)
        table = get_rows(db, thing="name", value=f'{name}')
        print(table)

    def report_by_frequency(self, frequency: str, db_file):

        """
        :param db_file: the name of the database file
        :param frequency: "daily" or "weekly"
        Shows the specified habits in a pretty table based on their frequency
        """

        db = get_db(db_file)
        table = get_rows(db, thing="frequency", value=f'{frequency}')
        print(table)

    def check(self, name: str, db_file):
        """
        :param db_file: the name of the database file
        :param name: the name of the habit that needs to be marked
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute(f"SELECT check_off FROM habit_data "
                       f"WHERE name = '{name}';")
        check_off = list(cursor.fetchone())[0]

        cursor.execute(f"SELECT frequency FROM habit_data "
                       f"WHERE name = '{name}';")
        frequency = list(cursor.fetchone())[0]

        self.streak_days(name, frequency, db_file)

        today = dt.datetime.now().strftime("%d/%m/%Y")
        cursor.execute(f"UPDATE habit_data SET check_off = '{check_off + 1}', last_updated_day = '{today}'"
                       f"WHERE name = '{name}';")

        connection.commit()
        self.report_one(name=name, db_file=db_file)

    def streak_days(self, name: str, frequency: str, db_file):

        """
        :param db_file: the name of the database file
        :param name: the specified habit
        :param frequency: the frequency of the habit
        Counts streak days.
        Parameters are automatically assigned to the function and the function cannot be called directly.

        """

        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        difference = ''

        if frequency == 'daily':
            difference = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%d/%m/%Y")

        elif frequency == 'weekly':
            difference = (dt.datetime.now() - dt.timedelta(weeks=1)).strftime("%d/%m/%Y")

        cursor.execute(f"SELECT last_updated_day FROM habit_data "
                       f"WHERE name = '{name}';")
        last_updated_day = list(cursor.fetchone())[0]

        cursor.execute(f"SELECT streak_days FROM habit_data "
                       f"WHERE name = '{name}';")
        streak_days = list(cursor.fetchone())[0]

        if difference == last_updated_day:
            cursor.execute(f"UPDATE habit_data SET streak_days = '{streak_days + 1}'"
                           f"WHERE name = '{name}';")
            connection.commit()
        else:
            streak_days = 1
            cursor.execute(f"UPDATE habit_data SET streak_days = '{streak_days}'"
                           f"WHERE name = '{name}';")
            connection.commit()


class PredefinedHabits:

    """
        Shows all predefined habits in a pretty table
    """

    def report_all_ph(self, db_file):
        """
        :param db_file: the name of the database file
        """
        db = get_db(name=db_file)
        table = get_rows(db=db, thing=None, value=None)
        print(table)


class DeleteHabit:
    """
        This class will delete a habit(s) manually or automatically after the duration expires.

            Attribute:
                habit_name (str):
                    the name of the habit that needs to be deleted
            Methods:
                delete_habit_manually(self)
                delete(self)

    """

    def __init__(self, habit_name: str):
        self.habit_name = habit_name

    def delete_habit_manually(self, db_file):
        """
        :param db_file: the name of the database file
        This function allows a user to delete a habit manually
        """

        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()

        cursor.execute(f"DELETE FROM habit_data "
                       f"WHERE name='{self.habit_name}'")
        connection.commit()

    def delete(self, db_file):
        """
        :param db_file: the name of the database file
        This function deletes a habit automatically after the duration expires.
        """
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        row_list = habit_names(db_file)
        for name in row_list:
            end_date = cursor.execute(f"SELECT end_date FROM habit_data WHERE name='{name}'")
            if end_date == dt.datetime.now().strftime("%d/%m/%Y"):
                cursor.execute(f"DELETE * FROM habit_data WHERE name='{name}'")
                connection.commit()
