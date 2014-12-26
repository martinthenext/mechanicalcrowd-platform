import json

from .models import AuditLog

from mcrowd.common.serializers import serialize


def get_user():
    import inspect
    request = None
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            request = frame_record[0].f_locals['request']
            break
    if request:
        return request.user
    else:
        return None


def cretead(sender, instance, *args, **kwargs):
    AuditLog.objects.create(
        user=get_user(),
        model=sender.__class__.__name__,
        type="C", event=json.dumps(serialize(instance)))


def updated(sender, instance, *args, **kwargs):
    AuditLog.objects.create(
        user=get_user(),
        model=sender.__class__.__name__,
        type="U", event=json.dumps(serialize(instance)))


def deleted(sender, instance, *args, **kwargs):
    AuditLog.objects.create(
        user=get_user(),
        model=sender.__class__.__name__,
        type="D", event=json.dumps(serialize(instance)))
