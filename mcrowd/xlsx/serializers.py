import json
import logging
import re

from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Worksheet, Workbook, Table
from .settings import HEADER_LOCATION, DATA_LOCATION

logger = logging.getLogger(__name__)


class UsernameField(serializers.RelatedField):
    def to_native(self, value):
        return value.username


class SheetField(serializers.RelatedField):
    def to_native(self, value):
        return {"number": value.number, "name": value.__unicode__()}

    def from_native(self, native):
        bookname, sheetname = native.get("name", "!").split("!")
        return Worksheet.get_object_or_404(
            name=sheetname, workbook__filename=bookname,
            number=native.get("number"))


class WorkbookSerializer(serializers.ModelSerializer):
    owner = UsernameField()
    sheets = SheetField(many=True)

    class Meta:
        model = Workbook
        fields = ("id", "owner", "filename", "sheets")
        depth = 1


class WorksheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worksheet
        fields = ("number", "name",)


class TableSheetField(serializers.Field):
    def to_native(self, value):
        return value.__unicode__()

    def from_native(self, native):
        if not native:
            native = "!"
        bookname, sheetname = native.split("!")
        return Worksheet.get_object_or_404(
            name=sheetname, workbook__filename=bookname)


class JsonField(serializers.CharField):
    def to_native(self, value):
        return json.loads(value)

    def from_native(self, value):
        return json.dumps(value)


class TableSerializer(serializers.ModelSerializer):
    worksheet = serializers.CharField(source="worksheet")
    col_names = JsonField(read_only=True)
    col_ids = JsonField(read_only=True)
    header_location = serializers.CharField(
        max_length=100,
        default=HEADER_LOCATION)
    data_location = serializers.CharField(
        max_length=100,
        default=DATA_LOCATION)

    def validate_header_location(self, attrs, source):
        value = attrs[source].strip()
        if not re.match(r'^\w+\d+:(\w+\d+)?$', value, re.S | re.M | re.U):
            raise serializers.ValidationError(
                "Expected format: 'A1:C1' or 'A1:'")
        return attrs

    def validate_data_location(self, attrs, source):
        value = attrs[source].strip()
        if not re.match(r'^\w+\d+:(\w+\d+)?$', value, re.S | re.M | re.U):
            raise serializers.ValidationError(
                "Expected format: 'A2:C100' or 'A2:'")
        return attrs

    def validate_worksheet(self, attrs, source):
        value = attrs[source]
        logger.debug("value: %s", value)
        if not value:
            value = "!"
        bookname, sheetname = value.split("!")
        attrs[source] = get_object_or_404(
            Worksheet, name=sheetname, workbook__filename=bookname)
        return attrs

    class Meta:
        model = Table
