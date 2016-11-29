# More

## Why not for large number of users

Della is written for small communities and I have left out many [optimizations](https://en.wikipedia.org/wiki/Program_optimization) because they are not at all required when number of users is small. (In future, I _might_ make changes and make it better for large number of users.)

There is only one rule while making pairs - santa and santee cannot be same. If you add more rules, then it will take a lot of time to make pairs (since it has to generate pairs and make sure they are valid). Also, pairs are not made in background job (using Celery etc).

[![some fancy math explanation](https://img.youtube.com/vi/5kC5k5QBqcc/0.jpg)](https://www.youtube.com/watch?v=5kC5k5QBqcc)

While [readme](README.md) mentions that users should be in range of 200-250, I don't really have any tests to show that. Thats just a smallish number that came to me when I woke up from my sleep. So Della might work perfectly fine for even more number of users (or may not).

If you are interested in developing a better polynomial time algorithm, read this [paper](https://www.lix.polytechnique.fr/~liberti/sesan.pdf).

## Admin features

Admin can send mass emails and also draw names. Do note that when you create an admin user using `createsuperuser` command, then it won't be part of participants. Because participation is decided by `UserProfile.is_enabled_exchange` and when you create a user using `createsuperuser`, he won't have corresponding `UserProfile`. The assumption made here is that Admins won't be participating in the exchange.

## Deployment notes

- Make sure `libmysqlclient-dev` is also installed (if you are using MySQL):

        sudo apt-get install libmysqlclient-dev

- One of the requirement `Pillow` depends on `libjpeg8-dev`:
    
        sudo apt-get install libjpeg8-dev


## Using MySQL

If you want to use MySQL instead of Postgres, then you need to make following changes:

1. Install `mysqlclient`:

        pip3 install mysqlclient

2. Update settings file `della/settings/production.py` to use MySQL driver:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
        }
    }
    ```
