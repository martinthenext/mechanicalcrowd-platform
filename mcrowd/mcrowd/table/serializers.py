from django.forms import widgets
from rest_framework import serializers

from .models import Table, Task


class UsernameField(serializers.RelatedField):
    def to_native(self, value):
        return value.username


class TableSerializer(serializers.ModelSerializer):
    owner = UsernameField()

    class Meta:
        model = Table
        fields = ("id", "owner", "filename")
        depth = 1


class TaskSerializer(serializers.ModelSerializer):
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        depth = 0
