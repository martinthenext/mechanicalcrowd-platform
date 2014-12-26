import json
import logging

from django.contrib.auth.models import User
from django.db import models

from .managers import RowDiffManager

from mcrowd.xlsx.models import Table

logger = logging.getLogger(__name__)


class Task(models.Model):
    table = models.ForeignKey(
        Table, null=False, related_name="tasks")
    columns = models.TextField(
        blank=True, null=False, default="")
    wrong_rows_definition = models.TextField(
        blank=True, null=False, default="")
    task_definition = models.TextField(
        blank=True, null=False, default="")
    deduplicate = models.BooleanField(
        null=False, default=False)
    active = models.BooleanField(null=False, default=False)
    edit_allowed = models.BooleanField(null=False, default=True)
    delete_allowed = models.BooleanField(null=False, default=True)
    hits_per_user = models.IntegerField(null=False, default=1)

    def get_col_names(self):
        return json.loads(self.columns)

    def get_col_ids(self):
        return list(map(lambda x: self.table.get_index(x),
                        self.get_col_names()))

    def get_original_rows(self):
        return list(map(lambda x: [x.number, json.loads(x.values)],
                        self.rows.all()))

    def get_functions(self):
        functions = []
        if self.edit_allowed:
            functions.append("edit")
        if self.delete_allowed:
            functions.append("delete")
        return functions


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

    def get_values(self):
        return json.loads(self.values)


class RowDiff(models.Model):
    task = models.ForeignKey(Task, null=False, related_name="diff")
    number = models.IntegerField(null=False, db_index=True)
    values = models.TextField(blank=False, null=True)  # null means deleted
    meta = models.TextField(blank=False, null=False, default="{}")

    def get_values(self):
        return json.loads(self.values)

    def get_meta(self):
        return json.loads(self.meta)

    objects = RowDiffManager()
