# della

Della is a Django app for managing Secret Santa/Gift Exchange. It is written for small communities where participants are in the range of 200-250 but not more ([Why so?](more.md#why-not-large-number-of-users)).

## Features

Della has very limited set of features, however, if you need some extra feature then feel free to [tweet me](https://twitter.com/iavins) and I _might_ consider adding it.

- User signup (with invite code)
- Messaging and secret/sneaky messaging (with email notifications)
- Gallery
- Admin features - Drawing names, Sending mass emails

## Screenshots

Check [here](http://avi.im/della/#screenshots).

## System Requirements

- Python 3.5
- PostgreSQL (or [MySQL](more.md#using-mysql))
- nginx
- supervisord

### Other requirements

Della uses [Sparkpost](https://www.sparkpost.com/) to send emails. So you need Sparkpost API Key and also an email address which can be used to send emails with Sparkpost. 

While signing up, every participant needs an invite code, which can be set to any string by admin.

These settings are to be set in `della/settings/secret.py` as `SPARKPOST_API_KEY`, `SENDER_EMAIL` and `INVITE_CODE`.

## Deployment

1. Clone the repo and rename/copy `della/settings/sample_secret.py` to `della/settings/secret.py` and set the variables appropriately.

2. Install the requirements 

        pip3 install -r requirements.txt

3. Setup ngnix (use `configs/nginx`)

4. Setup uWSGI (use `configs/uwsgi.conf`)

5. Setup supervisord (use `configs/supervisor.conf`)

Once everything is setup, CD into della directory and run following:

    pip3 install -r requirements.txt
    python3 manage.py migrate --settings=della.settings.production
    python3 manage.py collectstatic --settings=della.settings.production --noinput
    python3 manage.py createsuperuser --settings=della.settings.production
    python3 manage.py makemigrations background_task --settings=della.settings.production
    python3 manage.py migrate --settings=della.settings.production
    systemctl start della.uwsgi.service
    supervisorctl start della_background_tasks

## To Do

- Add tests
- Mark/confirm gifts received (or not)
- Add commenting system for Gallery
- Allow multiple exchanges
- Ability to set preference questionnaire for exchanges

## Name

The name Della comes from O. Henry's short story [The Gift of the Magi](http://www.gutenberg.org/files/7256/7256-h/7256-h.htm).

## Send me love

You will probably going to use a VPS to host Della, please consider using any of the following referral links:

- [Digital Ocean](https://m.do.co/c/6eae876c2650)
- [Vultr](http://www.vultr.com/?ref=7047034)
- [Ramnode](https://clientarea.ramnode.com/aff.php?aff=1647)

Or some bitcoins: `1LAmWUmdu1r1KLQrcZ2uK6r5P7xx5gRmnW`. Thank you! 🎅

## Contributing

Check the logged [issues](https://github.com/avinassh/della/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement) with tag `enhancement`. Do submit a new issue if you have any UI/UX suggestion.

## License

The mighty MIT license. Please check `LICENSE` for more details.