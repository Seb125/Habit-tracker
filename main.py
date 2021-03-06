import argparse
import pickle
import classes_Kopie as cl
from prettytable import PrettyTable

def load_data(name):
    '''This function loads a saved habit_profile from a shelve'''
    obj = pickle.load(open(name, 'rb'))
    return obj

def save_data(profile,name):
    '''This function saves a habit_profile in a shelve'''
    pickle.dump(profile, open(name, 'wb'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog = "test",
                                     usage = '''
------------------------------------------------------------------------------------------------------------

    This is a habit tracker. This habit tracker will help you to train new habits. It provides ways to create
    and delete habits, you can manage your habits and also analyze them. 
    For further instructions and help use '-h'.
                                         
------------------------------------------------------------------------------------------------------------

    ''',
    description='''
 
----------------------------------------------------------------------------------------------------------

 To use the habit tracker you need to create a profile or load an existing one. 
 
 The habit tracker then offers the following functions:

 1) Create habits -> enter create  
    Here you can create a new habit, by specifying the name, the quality (good vs. bad) 
    and the period (daily, weekly or monthly) of your habit.E.g.: workout good daily
    
 2) Delete habits -> enter delete  
    You can enter the name of an existing habit, to delete it from your habit list.

 3) Analyze habits -> enter analyze  
    Here you can analyze your performance on your habits. You can either analyze a single habit
    or get a summary over all habits. The keyword summary can be used to create an overview of all 
    habits and a specific name to analyze a particular habit.

 4) Manage your habits -> enter manage  
    Here you can check off your habits. If you finished a good habit or if you did not follow a
    bad habit, you can save this here by providing the name of the corresponding habit.

-----------------------------------------------------------------------------------------------------------
 ''',

    formatter_class = argparse.RawDescriptionHelpFormatter, add_help = True)
    parser.add_argument("argument", type = str, help = "", metavar = "Profilename.pkl")
    arg = parser.parse_args()
    profile_name = arg.argument

    try:
        profile = load_data(profile_name)
    except FileNotFoundError:
        profile = cl.Habit_profile(profile_name)

    while True:
        z = PrettyTable(["", "Your current habits"])
        z.add_row(["Daily habits", str([habit.name for habit in profile.good_daily_habits])])
        z.add_row(["Weekly habits", str([habit.name for habit in profile.good_weekly_habits])])
        z.add_row(["Monthly habits", str([habit.name for habit in profile.good_monthly_habits])])
        z.add_row(["Bad habits", str([habit.name for habit in profile.bad_habits])])
        print(z)
        print("You can analyze, manage, create or delete habits.\nPlease enter the name of one of these editing modes.\nIf you want to exit the habit tracker please type 'exit'.")
        action = input()
        
        if action == "create":
            print("Please enter the follwowing for a good habit: name quality periodicity\nPlease enter the following for a bad habit: name quality\n(Quality is either good or bad and periodicity can be daily, weekly or monthly)")
            profile.create_habit()

        elif action == "delete":
            print("Please enter the name of the habit you want to delete.")
            profile.delete_habit()

        elif action == "manage":
            print("Which of your good habits did you finish? or Which of your bad habits could'nt you avoid?")
            n = input()
            for h in profile.all_habits:
                if h.name == n:
                    h.check_off_habit()

        elif action == "analyze":
            print("To analyze a single habit enter the corresponding habitname.\nTo get a summary over all habits enter 'summary'.")
            analysis = input()
            if analysis != 'summary':
                for object in profile.all_habits:
                    if object.name == analysis:
                        object.generate_table()
            if analysis == 'summary':
                profile.summary()

        elif action == "exit":
            break

    save_data(profile, profile_name)