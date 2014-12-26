import json
import logging

from rest_framework import serializers

from .models import AuditLog

logger = logging.getLogger(__name__)


class UsernameField(serializers.RelatedField):
    def to_native(self, value):
        return value.username


class EventField(serializers.CharField):
    def to_native(self, value):
        return json.loads(value)


class AuditLogSerializer(serializers.ModelSerializer):
    user = UsernameField()
    timestamp = serializers.DateTimeField()
    model = serializers.CharField()
    type = serializers.ChoiceField(choices=AuditLog.TYPES)
    event = EventField()

    class Meta:
        model = AuditLog
        fields = ("user", "timestamp", "model", "type", "event")
