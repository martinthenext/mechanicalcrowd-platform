import logging

from django.forms import widgets
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import Table

logger = logging.getLogger(__name__)


class UsernameField(serializers.RelatedField):
    def to_native(self, value):
        return value.username


class TableSerializer(serializers.ModelSerializer):
    owner = UsernameField()
    sheets = serializers.Field(source='get_sheet_names')

    class Meta:
        model = Table
        fields = ("id", "owner", "filename", "sheets")
        depth = 1
