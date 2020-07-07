from datetime import datetime, timedelta, timezone
from slack_webhook import Slack
from config import config
import os
import requests
import pytz


def cron_job(minutes_elapsed):
    """
    Main cron job.
    The main cronjob to be run continuously.
    """
    time_of_last_update = datetime.now() - timedelta(minutes=minutes_elapsed)
    print("Last update: {}".format(time_of_last_update))

    print("Cron job is running")
    print("Current time: %s" % datetime.now())

    token_rs = requests.post(
        config['twitch-token-url'].format(os.getenv("TWITCH_CLIENT_ID"), os.getenv("TWITCH_SECRET")))

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

            for streamer in follows:
                live_url = config['twitch-live-url'].format(streamer['id'])
                live_rs = requests.get(live_url, headers=headers)

                if live_rs.status_code < 299:
                    live_data = live_rs.json()['data']
                    # "data" has content if a streamer is live
                    if live_data:
                        live_started_at = datetime.strptime(live_data[0]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
                        not_notified_yet = live_started_at > time_of_last_update
                        if not_notified_yet:
                            channel_url = config['twitch-channel-url'].format(live_data[0]['user_name'])
                            channel = live_data[0]['user_name']
                            title = live_data[0]['title']
                            viewers = live_data[0]['viewer_count']
                            thumbnail_url = live_data[0]['thumbnail_url'].format(width=100, height=75)

                            slack = Slack(url=config['webhook-url'].format(os.getenv("SLACK_API_KEY")))
                            slack.post(
                                text="{} is live".format(channel),
                                blocks=[
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": "*{} is live*".format(live_data[0]['user_name'])
                                        }
                                    },
                                    {
                                        "type": "section",
                                        "text": {
                                            "type": "mrkdwn",
                                            "text": '<{}|{}: {}>\n{} now streaming "{}" with {} viewers ({})'
                                                .format(channel_url, channel, title, channel, title, viewers,
                                                        utc_to_local(live_started_at).strftime("%d %b %Y at %H:%M"))
                                        },
                                        "accessory": {
                                            "type": "image",
                                            "image_url": thumbnail_url,
                                            "alt_text": "Twitch thumbnail"
                                        }
                                    }
                                ]
                            )
                            print(" - {} streaming on {}".format(channel, utc_to_local(live_started_at)))
                else:
                    print("Error: Twitch Live Stream API returned {}".format(live_rs.json()))
        else:
            print("Error: Twitch User Follows API returned {}".format(follows_rs.json()))
    else:
        print("Error: Twitch Token API returned {}".format(token_rs.json()))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Europe/London'))
