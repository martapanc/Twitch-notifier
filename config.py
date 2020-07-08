
config = {
    'webhook-url': 'https://hooks.slack.com/services/{}',
    'twitch-live-url': 'https://api.twitch.tv/helix/streams?user_id={}',
    'twitch-token-url': 'https://id.twitch.tv/oauth2/token?client_id={}&client_secret={}&grant_type=client_credentials',
    'twitch-user-follows-url': 'https://api.twitch.tv/helix/users/follows?from_id={}&first=100',
    'twitch-channel-url': 'https://www.twitch.tv/{}',
    'twitch-games-url': 'https://api.twitch.tv/helix/games?id={}'
}

schedule = {
    0: 60,
    1: 60,
    2: 60,
    3: 60,
    4: 60,
    5: 60,
    6: 60,
    7: 60,
    8: 30,
    9: 30,
    10: 30,
    11: 30,
    12: 10,
    13: 10,
    14: 10,
    15: 10,
    16: 5,
    17: 5,
    18: 5,
    19: 5,
    20: 5,
    21: 5,
    22: 5,
    23: 5
}
