# della

Della is a Django app for managing Secret Santa/Gift Exchange. 

## System Requirements

- Python 3.5
- MySQL
- nginx

## Deployment

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

1. Clone the repo and rename/copy `della/settings/sample_secret.py` to `della/settings/secret.py` and set the variables appropriately.

2. Install the requirements 

        pip3 install -r requirements.txt

3. Setup ngnix (use `configs/nginx`)

4. Setup uWSGI (use `configs/uwsgi.conf`)

## Name

The name Della comes from O. Henry's short story [The Gift of the Magi](http://www.gutenberg.org/files/7256/7256-h/7256-h.htm).

## License

The mighty MIT license. Please check `LICENSE` for more details.
