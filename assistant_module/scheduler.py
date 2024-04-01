import schedule
import time

def schedule_task(time_str, callback):
    """
    Schedules the given callback function to run at the time specified in time_str.
    
    Args:
    - time_str (str): Time at which to run the task, in 'HHMM' format.
    - callback (function): The function to run at the scheduled time.
    """
    hour = int(time_str[:2])
    minute = int(time_str[2:])
    schedule_time = f"{hour:02d}:{minute:02d}"
    
    schedule.every().day.at(schedule_time).do(callback)
    print(f"Scheduled task to run at {schedule_time} every day.")

def run_scheduler():
    """
    Runs the scheduler to check and execute any pending tasks.
    """
    while True:
        schedule.run_pending()
        time.sleep(1)
