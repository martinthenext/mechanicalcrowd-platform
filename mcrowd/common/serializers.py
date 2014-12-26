import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)


def serialize(obj):
    meta = type('Meta', (object,), dict(model=obj.__class__))
    serilizer = type('%sSerializer' % obj.__class__.__name__,
                     (serializers.ModelSerializer,), dict(Meta=meta))
    return serilizer(obj).data
