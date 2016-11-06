from django.conf import settings
from django.core.signing import TimestampSigner
from django.core.signing import BadSignature, SignatureExpired


def generate_key(user):
    signer = TimestampSigner(settings.SECRET_KEY)
    return signer.sign(str(user.id))


def validate_key(key, user):
    signer = TimestampSigner(settings.SECRET_KEY)
    try:
        value = signer.unsign(key, max_age=settings.EMAIL_LINK_EXPIRY_DAYS)
        return str(user.id) == value
    except (BadSignature, SignatureExpired):
        return False
