from datetime import datetime
from slack_webhook import Slack
from config import config
import os
import requests


def cron_job(seconds_elapsed):
    """
    Main cron job.
    The main cronjob to be run continuously.
    """

    print("Cron job is running")
    print("Tick! The time is: %s" % datetime.now())

    token_rs = requests.post(config['twitch-token-url'].format(os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_SECRET")))

    if token_rs.status_code < 299:
        token = token_rs.json()['access_token']
        url = config['twitch-user-follows-url'].format(os.getenv("TWITCH_USER_ID"))
        headers = {
            "Client-ID": os.getenv("TWITCH_CLIENT_ID"),
            "Authorization": "Bearer {}".format(token)
        }

        follows_rs = requests.get(url, headers=headers)
        if follows_rs.status_code < 299:
            follows = []
            for f in follows_rs.json()['data']:
                follows.append({'id': f['to_id'], 'name': f['to_name']})

            live = []
            for streamer in follows:
                live_url = config['twitch-live-url'].format(streamer['id'])
                live_rs = requests.get(live_url, headers=headers)
                if live_rs.status_code < 299:
                    live_data = live_rs.json()['data']
                    # "data" has content if a streamer is live
                    if live_data:
                        slack = Slack(url=config['webhook-url'].format(os.getenv("SLACK_API_KEY")))
                        slack.post(
                            text="{} is live".format(live_data[0]['user_name']),
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
                else:
                    print("Error: Twitch Live Stream API returned {}".format(live_rs.json()))
        else:
            print("Error: Twitch User Follows API returned {}".format(follows_rs.json()))
    else:
        print("Error: Twitch Token API returned {}".format(token_rs.json()))
