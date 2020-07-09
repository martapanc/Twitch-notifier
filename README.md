# ~ <img src="images/twitch.png" width="3%"/> to <img src="images/slack.png" width="3%"/> notifier ~

Simple cron task that sends a notification to a Slack channel whenever the Twitch streamers that a user follows start a live.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/6ab92d34d3c341b1952b4417a3992b39)](https://app.codacy.com/manual/martapanc/Twitch-notifier?utm_source=github.com&utm_medium=referral&utm_content=martapanc/Twitch-notifier&utm_campaign=Badge_Grade_Dashboard)

<img src="images/sample.png" width="70%" />

## Slack Webhook setup
In order to send messages to a Slack channel, you need to create an [Incoming Webhook](https://api.slack.com/messaging/webhooks): refer to the [webhook ReadMe](Slack-incoming-webhooks.md) for details on how to setup this.

The Webhook url obtained will look like `https://hooks.slack.com/services/xxx/yyy/zzzz`. The last three parts, `xxx/yyy/zzzz`, need to be placed in the `.env` file, which must remain a local file as it contains API secrets.

### Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli).

```sh
git clone git@github.com:martapanc/Twitch-notifier.git
cd Twitch-notifier

pip install -r requirements.txt
python3 cronjob.py
```

## Deploying to Heroku

```sh
heroku create
git push heroku master

heroku run python manage.py migrate
heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Deploy and start cron job
```sh
git push heroku master

heroku ps:scale clock=1
```

To view logs, run the command:
```sh
heroku logs --tail
```
## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

-   [Python on Heroku](https://devcenter.heroku.com/categories/python)
-   [APScheduler - Cron](https://apscheduler.readthedocs.io/en/v2.1.2/cronschedule.html)
-   [dotenv](https://pypi.org/project/python-dotenv/)
-   [Slack webook](https://pypi.org/project/slack-webhook/)
-   [Hiding API keys on Heroku](https://medium.com/better-programming/how-to-hide-your-api-keys-c2b952bc07e6)
-   [Errors for incoming webhooks](https://api.slack.com/changelog/2016-05-17-changes-to-errors-for-incoming-webhooks)
-   [Deploy Python cron jobs on Heroku](https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/)
-   [Twitch API Reference](https://dev.twitch.tv/docs/api/reference#get-users-follows)
-   [Slack message layout](https://api.slack.com/messaging/composing/layouts)
