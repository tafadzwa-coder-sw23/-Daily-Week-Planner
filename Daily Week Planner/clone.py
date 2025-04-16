import random
import datetime
import schedule
import time
import os
import json

def get_weekday_name(day_number):
    """
    Returns the name of the weekday given a day number (0-6, where 0 is Monday).
    """
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[day_number]

def load_weekly_plan():
    """
    Loads the weekly plan from a file (plans.json).  Handles file not found and other errors.
    Returns:
        dict: The weekly plan (plans, challenges), or None if no plan exists.
    """
    try:
        with open("plans.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print("Error: plans.json file is corrupted.  Creating a new plan.")
        return None  # Return None to indicate no valid plan

def save_weekly_plan(plan_data):
    """
    Saves the weekly plan to a file (plans.json).
    Args:
        plan_data (dict): The weekly plan (plans, challenges).
    """
    try:
        with open("plans.json", "w") as f:
            json.dump(plan_data, f, indent=4)  # Use indent for pretty formatting
    except Exception as e:
        print(f"Error saving weekly plan: {e}")  # Handle other potential errors

def week_planner():
    """
    This function helps users plan their week, checks in daily, and asks about the weekend.
    It is designed to be run daily by a scheduler.
    """
    today = datetime.datetime.now()
    day_of_week = today.weekday()
    weekday_name = get_weekday_name(day_of_week)

    weekly_plan = load_weekly_plan() # Load plan at the start of the function.

    if day_of_week == 0:  # Monday
        print("\n🌟 Happy Monday! Let's plan your week. 🌟")
        print("------------------------------------------")
        weekend_input = input("How was your weekend? Any highlights?\n> ")
        plans = input("What do you want to accomplish this week? \n(Examples: 'exercise more', 'finish a project', 'learn new skill')\n> ")
        challenges = input("\nWhat might make this challenging for you?\n> ")

        weekly_plan = {"plans": plans, "challenges": challenges}  # Store in dict
        save_weekly_plan(weekly_plan)  # Save the plan to the file
        print(f"\nOkay, great! Your plan for the week is: {plans}")
        print(f"You anticipate these challenges: {challenges}")

    elif 1 <= day_of_week <= 4:  # Tuesday to Friday
        print(f"\n👋 Good {weekday_name}! How is your week going?")
        print("--------------------------------------------------")
        if weekly_plan: # Check if a plan exists.
            print(f"Your plan for the week is: {weekly_plan['plans']}")
            print(f"Challenges you anticipated: {weekly_plan['challenges']}")
            progress = input("What progress have you made on your goals, and how are you managing your challenges?\n> ")
        else:
            print("No weekly plan found.  Please run on Monday to create a plan.")
    elif day_of_week == 5:  # Saturday
        print(f"\n🎉 Happy {weekday_name}! 🎉")
        print("--------------------------------------------------")
        weekend_plans = input("What are your plans for the weekend?\n> ")
        print("Enjoy your weekend!")

    elif day_of_week == 6:  # Sunday
        print(f"\n😌 Happy {weekday_name}! 😌")
        print("--------------------------------------------------")
        reflection = input("How did your week go? Did you accomplish what you wanted to do?\n> ")
        if weekly_plan:
            print(f"You had planned to do: {weekly_plan['plans']}")
        else:
            print("No weekly plan was saved for this week.")

def run_daily():
    """
    Runs the week_planner function daily.  This is what the scheduler calls.
    """
    week_planner()

if __name__ == "__main__":
    # Schedule the week_planner function to run every day at 9:00 AM
    schedule.every().day.at("09:00").do(run_daily) # Change time as needed.

    print("Weekly planner scheduled to run daily at 9:00 AM.  Keep this script running.")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute
