from habit import *
import questionary

print("Welcome to the Habit Tracking App!\n\n")


def cli():

    will_continue = True
    while will_continue:

        choice = questionary.select("Please select:\n",
                                    choices=['Create a habit', 'Manage', 'Review Predefined Habits', 'Delete', 'Off'],
                                    use_indicator=True, use_jk_keys=False).ask()

        if choice == 'Create a habit':
            name = questionary.text("Please type a name for your new habit: ").ask().lower()

            frequency = questionary.select("Frequency for your habit", choices=['daily', 'weekly']).ask()

            periodicity = questionary.text("Duration for your habit (e.g 10 days/6 weeks/2 months): ").ask().lower()
            unitset = questionary.text("Unitset for your habit (e.g. 30 minutes/2 hours): ").ask().lower()
            start_date = questionary.text("When do you want to start? (DD/MM/YYYY): ").ask()

            create_habit = CreateHabit(name, frequency, periodicity, unitset, start_date)

            create_habit.add_habit(db_file="data.db")
            print("\n")

        elif choice == 'Manage':
            try:
                manage = ManageHabit()
                choice = questionary.select("Please select:\n",
                                            choices=['Edit a habit', 'Report', 'Check'],
                                            use_indicator=True, use_jk_keys=False).ask().lower()
                if choice == "edit a habit":
                    name = questionary.select("Please select:\n",
                                              choices=habit_names(db_file='data.db')).ask().lower()
                    thing = questionary.select("What do you want to change? \n",
                                               choices=['name', 'frequency']).ask().lower()
                    value = questionary.text("Please type a new value: ").ask().lower()

                    manage.edit(db_file='data.db', name=name, thing=thing, value=value)

                elif choice == "report":
                    option = questionary.select("Please select:\n",
                                                choices=['All habits', 'One specific habit', 'Daily habits',
                                                         'Weekly habits'],
                                                use_indicator=True, use_jk_keys=False).ask().lower()
                    if option == "all habits":
                        manage.report_all(db_file="data.db")
                    elif option == "one specific habit":
                        name = questionary.select("Please select:\n",
                                                  choices=habit_names(db_file='data.db')).ask().lower()
                        manage.report_one(name, db_file="data.db")
                    elif option == "daily habits":
                        manage.report_by_frequency(frequency='daily', db_file="data.db")
                    elif option == "weekly habits":
                        manage.report_by_frequency(frequency='weekly', db_file="data.db")

                elif choice == "check":
                    name = questionary.select("Please select:\n",
                                              choices=habit_names(db_file='data.db')).ask().lower()
                    manage.check(name=name, db_file="data.db")

            except sqlite3.OperationalError and ValueError:
                print("Something went wrong. \nPlease, create a habit first")
                pass

        elif choice == 'Review Predefined Habits':
            predefined_habits = PredefinedHabits()
            predefined_habits.report_all_ph(db_file='predefined-habits.db')

        elif choice == 'Delete':
            try:
                name = questionary.select("Please select the habit you want to delete: ",
                                          choices=habit_names(db_file='data.db')).ask()
                delete = DeleteHabit(habit_name=name)
                delete.delete_habit_manually(db_file="data.db")

            except sqlite3.OperationalError and ValueError:
                print("Something went wrong. \nPlease, create a habit first")
                pass

        elif choice == 'Off':
            will_continue = False


if __name__ == "__main__":
    cli()
