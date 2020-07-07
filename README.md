# ~ <img src="images/twitch.png" width="3%"/> to <img src="images/slack.png" width="3%"/> notifier ~

### Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
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

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
- [dotenv](https://pypi.org/project/python-dotenv/)
- [Slack webook](https://pypi.org/project/slack-webhook/)
- [Hiding API keys on Heroku](https://medium.com/better-programming/how-to-hide-your-api-keys-c2b952bc07e6)
- [Errors for incoming webhooks](https://api.slack.com/changelog/2016-05-17-changes-to-errors-for-incoming-webhooks)
- [Deploy Python cron jobs on Heroku](https://saqibameen.com/deploy-python-cron-job-scripts-on-heroku/)
= [Twitch API Reference](https://dev.twitch.tv/docs/api/reference#get-users-follows)


