# More

## Why not for large number of users

Della is written for small communities and I have left out many performance optimizations because they are not at all required when the number of users is small. I am running Della for a small community of users (~50) and it is working fine on a 512MB DO Droplet (which also runs other apps/services). I am not using a 'real' message broker, rather using Django Database with [Django Background Tasks](https://github.com/arteria/django-background-tasks) since the volume of messages is very very less (for my use-case) and I didn't want to introduce another system installation requirement. If the number of users is more and if there are lots of messages, then it would be better to use Rabbit MQ or Redis (with Celery).

Currently, I want to focus on adding more [features](README.md#to-do) and making the UI/UX better. So here are some things to start if you want to optimize for performance (and send a PR please):

 - Query optimizations
 - Template optimizations
 - Caching
 - Pagination (in ThreadList, MessageList, Gallery)

There is only one rule while making pairs - Santa and Santee cannot be same. If you add more rules, then it will take a lot of time to make pairs (since it has to generate pairs and make sure they are valid). Also, pairs are not made in background job (using Celery etc).

[![some fancy math explanation](https://img.youtube.com/vi/5kC5k5QBqcc/0.jpg)](https://www.youtube.com/watch?v=5kC5k5QBqcc)

While [readme](README.md) mentions that users should be in the range of 200-250, I don't really have any tests to show that. That's just a smallish number that came to me when I woke up from my sleep. So Della might work perfectly fine for even more number of users (or may not).

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
