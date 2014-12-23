import json

from django.db import models
from django.db.models.signals import post_save, pre_save

from .managers import HitManager
from .hooks import create_token

from mcrowd.task.models import Task


class Turker(models.Model):
    ident = models.CharField(
        max_length=40, null=False, blank=False, db_index=True, unique=True)


class Hit(models.Model):
    task = models.ForeignKey(Task, null=False, related_name="hits")
    ident = models.CharField(
        max_length=40, null=False, blank=False, db_index=True, unique=True)
    values = models.TextField(blank=False, null=False)
    upper_task = models.TextField(blank=True, null=False, default="")
    lower_task = models.TextField(blank=True, null=False, default="")
    functions = models.TextField(blank=False, null=False)
    url = models.URLField(blank=False, null=False)
    reward = models.DecimalField(
        blank=False, null=False, max_digits=3, decimal_places=2)  # max 9.99$
    max_assignments = models.IntegerField(blank=False, null=False)
    disabled = models.BooleanField(blank=False, null=False, default=False)

    def get_rows(self):
        values = json.loads(self.values)
        return list(map(lambda x: x[1], values))

    def get_original_rows(self):
        return json.loads(self.values)

    def get_functions(self):
        return json.loads(self.functions)

    def enough_assignments(self):
        if len(self.assignments.filter(done=True)) >= self.max_assignments:
            return True
        return False

    def disable(self):
        connection = Hit.objects.get_connection()
        connection.disable_hit(self.ident)
        self.disabled = True

    objects = HitManager()


class Assignment(models.Model):
    ident = models.CharField(
        max_length=40, null=False, blank=False, unique=True, db_index=True)
    hit = models.ForeignKey(Hit, related_name="assignments", null=False)
    turker = models.ForeignKey(Turker, related_name="assignments", null=False)
    token = models.TextField(blank=False, null=False)
    done = models.BooleanField(blank=False, null=False, default=False)


pre_save.connect(create_token, Assignment)
