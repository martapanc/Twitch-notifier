# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cron_job

from dotenv import load_dotenv
from pathlib import Path

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
seconds_elapsed = 30

cron_job(seconds_elapsed)

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(lambda: cron_job(seconds_elapsed), "interval", seconds=seconds_elapsed)

scheduler.start()
