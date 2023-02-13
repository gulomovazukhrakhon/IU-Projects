from habit import *


class TestHabits:
    def test_add_habit(self):
        """ Tests the “CreateHabit” class. """
        create_habit = CreateHabit(name="coding", frequency="daily", periodicity="15 months")

        create_habit.add_habit(db_file="predefined-habits.db")

    def test_manage_habit(self):
        """ Tests the “ManageHabit” class. """
        manage_habit = ManageHabit()
        manage_habit.edit(name="workout", thing="periodicity", value="6 months", db_file="predefined-habits.db")
        manage_habit.check(name="workout", db_file="predefined-habits.db")
        manage_habit.report_all(db_file="predefined-habits.db")
        manage_habit.report_by_frequency(frequency='daily', db_file="predefined-habits.db")
        manage_habit.report_one(name="workout", db_file="predefined-habits.db")

    def test_delete_habit(self):
        """ Tests the “DeleteHabit” class. """
        delete_habit = DeleteHabit()
        delete_habit.delete(db_file="predefined-habits.db", name="walking")
