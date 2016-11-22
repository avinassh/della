# della

Della is a Django app for managing Secret Santa/Gift Exchange. It is written for small communities where participants are in range of 200-250 but not more ([Why so?](more.md#why-not-large-number-of-users)).

## Features

Della has very limited set of features, however if you need some extra feature then feel free to [tweet me](https://twitter.com/iavins) and I _might_ consider adding it.

- User signup (with invite code)
- Messaging and secret/sneaky messaging
- Gallery
- Admin features - Drawing names, Sending mass emails


## System Requirements

- Python 3.5
- MySQL (or [PostgreSQL](more.md#using-postgresql))
- nginx

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

## To Do

- Add tests
- Mark/confirm gifts received (or not)
- Add commenting system for Gallery
- Allow multiple exchanges
- Ability to set preference questionnaire for exchanges

## Name

The name Della comes from O. Henry's short story [The Gift of the Magi](http://www.gutenberg.org/files/7256/7256-h/7256-h.htm).


## License

The mighty MIT license. Please check `LICENSE` for more details.
