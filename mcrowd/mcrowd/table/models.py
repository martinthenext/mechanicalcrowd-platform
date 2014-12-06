from django.db import models
from django.contrib.auth.models import User


class Table(models.Model):
    owner = models.ForeignKey(User, null=False)
    table = models.BinaryField(null=False, blank=False)
    filename = models.TextField(null=False, blank=True, default="")

    def __unicode__(self):
        return "{}: {}".format(self.pk, self.filename)


class Task(models.Model):
    table = models.ForeignKey(Table, null=False, related_name="tasks")
    sheet = models.TextField(blank=False, null=False)
    columns = models.TextField(blank=False, null=False)
    header_location = models.TextField(blank=False, null=False)
    data_location = models.TextField(blank=False, null=False)
    wrong_rows_definition = models.TextField(blank=False, null=False)
    task_definition = models.TextField(blank=False, null=False)
    deduplicate = models.BooleanField(null=False, default=False)
    active = models.BooleanField(null=False, default=False)


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
