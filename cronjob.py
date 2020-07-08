# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cron_job

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from config import schedule

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour="0-23")
def scheduled_job():
    # Determine the frequency of the updates based on the time of day
    minutes_elapsed = schedule[datetime.utcnow().hour]
    print("Adjusting time intervals to {} minutes, on {}".format(minutes_elapsed, datetime.now()))

    # Create an instance of scheduler and add function.
    scheduler.add_job(lambda: cron_job(minutes_elapsed), "interval", minutes=minutes_elapsed)


if __name__ == "__main__":
    scheduler.start()
