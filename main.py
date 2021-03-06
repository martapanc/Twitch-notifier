from datetime import datetime, timezone

from slack_webhook import Slack

from config import config
import os
import requests
import pytz
import aiohttp
import asyncio

from live_queue import remove_from_queue, is_in_queue, get_queue, add_to_queue

live_queue = get_queue()


async def cron_job():
    print('⏰ Current time: %s' % utc_to_local(datetime.utcnow()))

    # Obtain Auth token
    token_rs = requests.post(
        config['twitch-token-url'].format(os.getenv('TWITCH_CLIENT_ID'), os.getenv('TWITCH_SECRET')))

    if token_rs.status_code < 299:
        token = token_rs.json()['access_token']
        url = config['twitch-user-follows-url'].format(os.getenv('TWITCH_USER_ID'))
        headers = {
            'Client-ID': os.getenv('TWITCH_CLIENT_ID'),
            'Authorization': 'Bearer {}'.format(token)
        }
        # Get followed channels
        follows_rs = requests.get(url, headers=headers)

        if follows_rs.status_code < 299:
            await asyncio.gather(
                *[get_live_status_response(headers,
                                           config['twitch-live-url'].format(streamer['to_id']),
                                           streamer['to_name'])
                  for streamer in follows_rs.json()['data']])
        else:
            print('Error: Twitch User Follows API returned {}'.format(follows_rs.json()))

        print('🎥 Live channels: {} ({})'.format(live_queue, len(live_queue)))
    else:
        print('Error: Twitch Token API returned {}'.format(token_rs.json()))


async def get_live_status_response(headers, live_url, channel):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=live_url, headers=headers) as rs:
                response = await rs.json()
                live_data = response['data']
                # 'data' has content if a streamer is live
                if live_data:
                    started_at = datetime.strptime(live_data[0]['started_at'], '%Y-%m-%dT%H:%M:%SZ')
                    game = get_game_from_id(live_data[0]['game_id'], headers)

                    if not is_in_queue(channel):
                        add_to_queue(channel)

                        print('🟣 {} streaming "{}" on {}'.format(channel, game, utc_to_local(started_at)))

                        channel_url = config['twitch-channel-url'].format(live_data[0]['user_name'])
                        title = live_data[0]['title']
                        viewers = live_data[0]['viewer_count']
                        thumbnail_url = live_data[0]['thumbnail_url'].format(width=100, height=75)

                        send_slack_notification(channel, channel_url, game, started_at, thumbnail_url, title,
                                                viewers)
                else:
                    remove_from_queue(channel)

    except Exception as e:
        print("Unable to get url {} due to {}: \n{}.".format(live_url, e.__class__, e))


def send_slack_notification(channel, channel_url, game, live_started_at, thumbnail_url, title, viewers):
    slack = Slack(url=config['webhook-url'].format(os.getenv('SLACK_API_KEY')))
    slack.post(
        text='{} is live: {}'.format(channel, game),
        blocks=[
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '*{} is live: {}*'.format(channel, game)
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': '<{url}|{channel}: {title}>\n{channel} now streaming "{game} - {title}" with {viewers} viewers ({time})'
                        .format(url=channel_url, channel=channel, title=title, viewers=viewers, game=game,
                                time=utc_to_local(live_started_at).strftime('%d %b %Y at %H:%M'))
                },
                'accessory': {
                    'type': 'image',
                    'image_url': thumbnail_url,
                    'alt_text': 'Twitch thumbnail'
                }
            }
        ]
    )


def utc_to_local(utc_dt):
    return utc_dt.replace(tzinfo=timezone.utc).astimezone(pytz.timezone('Europe/London'))


def get_game_from_id(game_id, headers):
    if game_id == 509658:
        return 'Just Chatting'
    games_rs = requests.get(config['twitch-games-url'].format(game_id), headers=headers)
    if games_rs.status_code < 299 and len(games_rs.json()['data']) > 0:
        return games_rs.json()['data'][0]['name']
    else:
        return 'n/a'
