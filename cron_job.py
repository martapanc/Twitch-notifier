# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cron_job, utc_to_local

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

scheduler = BlockingScheduler()

scheduler.add_job(lambda: cron_job(5), trigger='cron', hour="*", minute="*/5", next_run_time=datetime.now())

if __name__ == "__main__":
    print('🌅 Script started at {}'.format(utc_to_local(datetime.utcnow())))
    scheduler.start()
