from habit import *


class TestHabitTracking:

    def test_add_habit(self):
        create_habit = CreateHabit(name="workout", frequency="daily", periodicity="12 weeks",
                                   unitset="20 minutes", start_date="15/12/2022")

        create_habit.add_habit(db_file="test.db")

    def test_manage_habit(self):
        manage_habit = ManageHabit()
        manage_habit.edit(name="workout", thing="unitset", value="30 minutes", db_file="test.db")
        manage_habit.check(name="workout", db_file="test.db")
        manage_habit.report_all(db_file="test.db")
        manage_habit.report_by_frequency(frequency='daily', db_file="test.db")
        manage_habit.report_one(name="workout", db_file="test.db")

    def test_delete_habit(self):
        delete_habit = DeleteHabit(habit_name="workout")
        delete_habit.delete_habit_manually(db_file="test.db")
        delete_habit.delete(db_file="test.db")
        import os
        os.remove('test.db')
