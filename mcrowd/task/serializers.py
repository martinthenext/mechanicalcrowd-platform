import re
import json
import logging

from rest_framework import serializers
from rest_framework import exceptions

from mcrowd.xlsx.models import Worksheet, Table
from mcrowd.xlsx.serializers import TableSerializer

from .models import Task, Row

logger = logging.getLogger(__name__)


class CommaSeparatedValuesField(serializers.CharField):
    def to_native(self, value):
        return ",".join(json.loads(value))

    def from_native(self, value):
        values = value.strip().split(",")
        values = map(lambda x: x.strip(), values)
        return json.dumps(list(values))


class TaskSerializer(serializers.ModelSerializer):
    table = TableSerializer()
    columns = CommaSeparatedValuesField(required=False)
    wrong_rows_definition = serializers.CharField(default="", required=False)
    task_definition = serializers.CharField(default="", required=False)
    deduplicate = serializers.BooleanField(default=False, required=False)
    edit_allowed = serializers.BooleanField(default=True, required=False)
    delete_allowed = serializers.BooleanField(default=True, required=False)
    active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Task
        depth = 1


class TaskRelatedSerializer(TaskSerializer):
    table = serializers.PrimaryKeyRelatedField()

    class Meta:
        model = Task
        depth = 0
