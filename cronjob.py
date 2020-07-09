# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cron_job, utc_to_local

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from config import schedule

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

scheduler = BlockingScheduler()


@scheduler.scheduled_job('cron', hour='0-23', minute='*/10')
def scheduled_job():
    # Determine the frequency of the updates based on the time of day
    minutes_elapsed = schedule[datetime.utcnow().hour]
    print('🔄️ Adjusting time intervals to {} minutes, on {}'.format(minutes_elapsed, utc_to_local(datetime.now())))

    # Reschedule Notifier based on new time interval
    scheduler.remove_job('notifier')
    scheduler.add_job(lambda: cron_job(minutes_elapsed), trigger='interval', minutes=minutes_elapsed, id='notifier',
                      next_run_time=datetime.now())
    # scheduler.reschedule_job(job_id='notifier', trigger='interval', minutes=minutes_elapsed)


if __name__ == "__main__":
    print('🌅 Script started at {}'.format(utc_to_local(datetime.utcnow())))
    # Initiate notifier job with static intervals
    scheduler.add_job(lambda: cron_job(5), trigger='interval', minutes=5, id='notifier', next_run_time=datetime.now())
    scheduler.start()
