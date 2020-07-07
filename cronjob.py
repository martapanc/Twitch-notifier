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

# Determine the frequency of the updates based on the time of day
minutes_elapsed = schedule[datetime.utcnow().hour]

cron_job(minutes_elapsed)

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(lambda: cron_job(minutes_elapsed), "interval", minutes=minutes_elapsed)

scheduler.start()
