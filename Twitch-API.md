## Twitch API Endpoints

### Token
Obtain auth token to be used in the data requests:
```bash
curl --location --request POST 'https://id.twitch.tv/oauth2/token?client_id=<client_id>&client_secret=<client_secret>&grant_type=client_credentials'
```
### User info
```bash
curl --location --request GET 'https://api.twitch.tv/helix/users?login=<user_name>' \
--header 'Client-ID: xxx' \
--header 'Authorization: Bearer yyy'
```
### Info of a channel that is currently streaming
```bash
curl --location --request GET 'https://api.twitch.tv/helix/streams?user_id=<user_id>' \
--header 'Client-ID: xxx' \
--header 'Authorization: Bearer yyy'
```
### Channels that a user follows
```bash
curl --location --request GET 'https://api.twitch.tv/helix/users/follows?from_id=<your_user_id>&first=100' \
--header 'Client-ID: xxx' \
--header 'Authorization: Bearer yyy'
```
### Info about a game
```bash
curl --location --request GET 'https://api.twitch.tv/helix/games?id=<game_id>' \
--header 'Client-ID: xxx' \
--header 'Authorization: Bearer yyy'
```
