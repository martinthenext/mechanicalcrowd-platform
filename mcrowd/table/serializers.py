import logging

from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Table, Task

logger = logging.getLogger(__name__)


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
    sheet = serializers.CharField()
    columns = serializers.CharField(
        validators=[RegexValidator(
            r'([^,]+?)(,([^,]+?))*',
            code=u'Expected comma separated list')])
    header_location = serializers.CharField(
        validators=[RegexValidator(
            r'^\w+\d+:(\w+\d+)?$',
            code=u'Expected format: <LETTER><NUMBER>:(<LETTER><NUMBER>)?')],
        default="A0:")
    data_location = serializers.CharField(
        validators=[RegexValidator(
            r'^\w+\d+:(\w+\d+)?$',
            code=u'Expected format: <LETTER><NUMBER>:(<LETTER><NUMBER>)?')],
        default="B0:")

    def validate_sheet(self, attrs, source):
        value = attrs[source].strip()
        table = attrs['table'].pk
        sheets = Table.get_workbook(table).get_sheet_names()
        if value not in sheets:
            raise serializers.ValidationError(
                "Sheet should be one of: {}".format(sheets))
        return attrs

    class Meta:
        model = Task
        depth = 0
