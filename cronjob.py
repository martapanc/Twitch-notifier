# Package Scheduler
from apscheduler.schedulers.blocking import BlockingScheduler

# Main cronjob function.
from main import cron_job

# Create an instance of scheduler and add function.
scheduler = BlockingScheduler()
scheduler.add_job(cron_job, "interval", seconds=30)

scheduler.start()
