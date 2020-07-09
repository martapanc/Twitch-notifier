from datetime import datetime, timedelta, timezone

from slack_webhook import Slack

from config import config
import os
import requests
import pytz


def cron_job(minutes_elapsed):
    utc_time = datetime.utcnow()
    time_of_last_update = utc_time - timedelta(minutes=minutes_elapsed)
    print('⏰ Last update: {}'.format(utc_to_local(time_of_last_update)))
    print('🕙 Current time: %s' % utc_to_local(utc_time))

    token_rs = requests.post(
        config['twitch-token-url'].format(os.getenv('TWITCH_CLIENT_ID'), os.getenv('TWITCH_SECRET')))

    if token_rs.status_code < 299:
        token = token_rs.json()['access_token']
        url = config['twitch-user-follows-url'].format(os.getenv('TWITCH_USER_ID'))
        headers = {
            'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
            'Authorization': 'Bearer {}'.format(token)
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
                    # 'data' has content if a streamer is live
                    if live_data:
                        live_started_at = datetime.strptime(live_data[0]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
                        not_notified_yet = live_started_at > time_of_last_update

                        channel = live_data[0]['user_name']
                        game = get_game_from_id(live_data[0]['game_id'], headers)
                        print(('🟣 ' if not_notified_yet else ' - ') + '{} streaming "{}" on {}'
                              .format(channel, game, utc_to_local(live_started_at)))

                        if not_notified_yet:
                            channel_url = config['twitch-channel-url'].format(live_data[0]['user_name'])
                            title = live_data[0]['title']
                            viewers = live_data[0]['viewer_count']
                            thumbnail_url = live_data[0]['thumbnail_url'].format(width=100, height=75)

                            slack = Slack(url=config['webhook-url'].format(os.getenv('SLACK_API_KEY')))
                            slack.post(
                                text='{} is live: {}'.format(channel, game),
                                blocks=[
                                    {
                                        'type': 'section',
                                        'text': {
                                            'type': 'mrkdwn',
                                            'text': '*{} is live: {}*'.format(live_data[0]['user_name'], game)
                                        }
                                    },
                                    {
                                        'type': 'section',
                                        'text': {
                                            'type': 'mrkdwn',
                                            'text': '<{url}|{channel}: {title}>\n{channel} now streaming "{game} - {title}" with {viewers} viewers ({time})'
                                                .format(url=channel_url, channel=channel, title=title, viewers=viewers,
                                                        game=game,
                                                        time=utc_to_local(live_started_at).strftime(
                                                            '%d %b %Y at %H:%M'))
                                        },
                                        'accessory': {
                                            'type': 'image',
                                            'image_url': thumbnail_url,
                                            'alt_text': 'Twitch thumbnail'
                                        }
                                    }
                                ]
                            )
                else:
                    print('Error: Twitch Live Stream API returned {}'.format(live_rs.json()))
        else:
            print('Error: Twitch User Follows API returned {}'.format(follows_rs.json()))
    else:
        print('Error: Twitch Token API returned {}'.format(token_rs.json()))


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Europe/London'))


def get_game_from_id(game_id, headers):
    if game_id == 509658:
        return 'Just Chatting'
    games_rs = requests.get(config['twitch-games-url'].format(game_id), headers=headers)
    if games_rs.status_code < 299:
        return games_rs.json()['data'][0]['name']
    else:
        return 'n/a'
