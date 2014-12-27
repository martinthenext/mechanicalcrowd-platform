import hashlib
import logging
import binascii

logger = logging.getLogger(__name__)


def create_token(sender, instance, *args, **kwargs):
    if instance.done:
        return
    token = hashlib.pbkdf2_hmac(
        'sha256', bytes(instance.turker.ident, encoding="utf-8"),
        bytes(str(instance.ident), encoding="utf-8"), 100)
    instance.token = binascii.hexlify(token).decode("utf-8")
    logger.info("token for %s was created: %s", instance.ident, token)


def check_constraint(sender, instance, *args, **kwargs):
    assert not(instance.done is False and instance.approved is True)
