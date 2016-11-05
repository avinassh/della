import json

from django.conf import settings


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
