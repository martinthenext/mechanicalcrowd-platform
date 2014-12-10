import logging

from django.db import models
from django.contrib.auth.models import User

from mcrowd.xlsx.models import Table

logger = logging.getLogger(__name__)


class Task(models.Model):
    table = models.ForeignKey(
        Table, null=False, related_name="tasks")
    sheet = models.TextField(
        blank=False, null=False)
    columns = models.TextField(
        blank=True, null=False, default="")
    header_location = models.TextField(
        blank=False, null=False, default="A1:")
    data_location = models.TextField(
        blank=False, null=False, default="A2:")
    wrong_rows_definition = models.TextField(
        blank=True, null=False, default="")
    task_definition = models.TextField(
        blank=True, null=False, default="")
    deduplicate = models.BooleanField(
        null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    edit_allowed = models.BooleanField(null=False, default=True)
    delete_allowed = models.BooleanField(null=False, default=True)


class Row(models.Model):
    ROW_STATUS = (
        ("G", "GOOD, IN PROGRESS"),
        ("B", "BAD, IN PROGRESS"),
        ("F", "FIXED"),
        ("D", "DELETED")
    )

    task = models.ForeignKey(Task, null=False, related_name="rows")
    number = models.IntegerField(null=False, db_index=True)
    values = models.TextField(blank=False, null=False)
    status = models.CharField(blank=False, null=False, choices=ROW_STATUS,
                              max_length=2, default="G")
