# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Main cronjob function.
from main import cron_job, utc_to_local

from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime

import asyncio

# Setup functions to read from .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


if __name__ == "__main__":
    scheduler = AsyncIOScheduler()

    scheduler.add_job(cron_job, trigger='cron', hour="*", minute="*/5", next_run_time=datetime.now())

    print('🌅 Script started at {}'.format(utc_to_local(datetime.utcnow())))
    scheduler.start()

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass
