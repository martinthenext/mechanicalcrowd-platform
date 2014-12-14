import re
import json
import logging

from rest_framework import serializers
from rest_framework import exceptions

from mcrowd.xlsx.models import Table

from .models import Task, Row


logger = logging.getLogger(__name__)


class TaskSerializer(serializers.ModelSerializer):
    sheet = serializers.CharField()
    columns = serializers.CharField(default="", required=False)
    header_location = serializers.CharField(default="A1:", required=False)
    data_location = serializers.CharField(default="A2:", required=False)
    wrong_rows_definition = serializers.CharField(default="", required=False)
    task_definition = serializers.CharField(default="", required=False)
    deduplicate = serializers.BooleanField(default=False, required=False)
    edit_allowed = serializers.BooleanField(default=True, required=False)
    delete_allowed = serializers.BooleanField(default=True, required=False)
    active = serializers.BooleanField(read_only=True)

    def validate_header_location(self, attrs, source):
        value = attrs[source].strip()
        if not re.match(r'^\w+\d+:(\w+\d+)?$', value, re.S | re.M | re.U):
            raise serializers.ValidationError(
                "Expected format: 'A0:C0' or 'A0:'")
        return attrs

    def validate_data_location(self, attrs, source):
        value = attrs[source].strip()
        if not re.match(r'^\w+\d+:(\w+\d+)?$', value, re.S | re.M | re.U):
            raise serializers.ValidationError(
                "Expected format: 'A1:C100' or 'A1:'")
        return attrs

    def transform_columns(self, obj, value):
        if not obj:
            return value
        try:
            value = json.loads(value)
            return ",".join(
                map(lambda x: x[1], sorted(value.items())))
        except ValueError:
            return value

    class Meta:
        model = Task
        depth = 0


class TableSerializer(serializers.ModelSerializer):
    col_names = serializers.Field(source='get_col_names')
    col_ids = serializers.Field(source='get_col_ids')
    rows = serializers.Field(source='get_rows_dict')

    class Meta:
        model = Task
        depth = 1
        fields = ('id', 'col_names', 'col_ids', 'rows')
