import json
import random
from collections import deque

from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from bulk_update.helper import bulk_update


def _get_default_file_content():
    return {'status': False}


def _write_status_file():
    file_path = settings.STATUS_FILE
    with open(file_path, 'w') as f:
        json.dump({'status': True}, f)
    return True


def _get_status_file():
    file_path = settings.STATUS_FILE
    try:
        with open(file_path) as f:
            return json.load(f)
    except FileNotFoundError:
        with open(file_path, 'w') as f:
            response = _get_default_file_content()
            json.dump(response, f)
            return response


def get_draw_status():
    return _get_status_file()['status']


def flip_draw_status():
    if not _get_status_file()['status']:
        return _write_status_file()
    return True


def draw_names():
    users = User.objects.filter(userprofile__is_enabled_exchange=True).all()
    user_profiles = []
    user_ids = [u.id for u in users]
    pairs = make_pairs(user_ids=user_ids)
    with transaction.atomic():
        for user in users:
            user.userprofile.santee_id = pairs[user.id]
            user_profiles.append(user.userprofile)
        bulk_update(user_profiles)
    flip_draw_status()
    return True


def make_pairs(user_ids):
    while True:
        pairs = _get_pairs(user_ids=user_ids)
        if _is_valid_pair(pairs=pairs):
            break
    return dict(pairs)


def _get_pairs(user_ids):
    user_ids_copy = user_ids.copy()
    random.shuffle(user_ids_copy)
    pairs = deque(user_ids_copy)
    pairs.rotate()
    return list(zip(user_ids, user_ids_copy))


def _is_valid_pair(pairs):
    """
    Checks if the pair and list of pairs is valid. A pair is invalid if both
    santa and santee are same i.e. (1, 1)
    """
    for pair in pairs:
        if pair[0] == pair[1]:
            return False
    return True
