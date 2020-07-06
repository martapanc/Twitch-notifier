from datetime import datetime
from slack_webhook import Slack
from config import config
from dotenv import load_dotenv
from pathlib import Path
import os


def cron_job():
    """
    Main cron job.
    The main cronjob to be run continuously.
    """

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    print("Cron job is running")
    print("Tick! The time is: %s" % datetime.now())

    slack = Slack(url=config['webhook-url'].format(os.getenv("SLACK_API_KEY")))
    slack.post(
        text="Robert DeSoto added a new task",
        attachments=[{
            "fallback": "Plan a vacation",
            "author_name": "Owner: rdesoto",
            "title": "Plan a vacation",
            "text": "I've been working too hard, it's time for a break.",
            "actions": [
                {
                    "name": "action",
                    "type": "button",
                    "text": "Complete this task",
                    "style": "",
                    "value": "complete"
                },
                {
                    "name": "tags_list",
                    "type": "select",
                    "text": "Add a tag...",
                    "data_source": "static",
                    "options": [
                        {
                            "text": "Launch Blocking",
                            "value": "launch-blocking"
                        },
                        {
                            "text": "Enhancement",
                            "value": "enhancement"
                        },
                        {
                            "text": "Bug",
                            "value": "bug"
                        }
                    ]
                }
            ]
        }]
    )
