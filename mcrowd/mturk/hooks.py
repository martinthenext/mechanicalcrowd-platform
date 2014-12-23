import hashlib
import binascii


def create_token(sender, instance, *args, **kwargs):
    if instance.done:
        return
    token = hashlib.pbkdf2_hmac(
        'sha256', bytes(instance.turker.ident, encoding="utf-8"),
        bytes(str(instance.ident), encoding="utf-8"), 100)
    instance.token = binascii.hexlify(token).decode("utf-8")
