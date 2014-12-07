import os
import stat
import logging
import pickle

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import openpyxl

logger = logging.getLogger(__name__)

LOCALSTORE = settings.MCROWD_TABLE.get("LOCALSTORE", ".")

# TODO: remove it
INMEMORYCACHE = {}


class Table(models.Model):
    owner = models.ForeignKey(User, null=False)
    table = models.BinaryField(null=False, blank=False)
    filename = models.TextField(null=False, blank=True, default="")

    def __unicode__(self):
        return "{}: {}".format(self.pk, self.filename)

    def get_sheets(self):
        pass

    @staticmethod
    def get_chached_name(pk):
        return os.path.join(LOCALSTORE, "{}.xlsx".format(pk))

    def save_to_cache(self):
        filename = self.get_chached_name(self.pk)
        logger.debug("saving table %s to filename %s", self.pk, filename)
        with open(filename, 'wb') as h:
            h.write(bytes(self.table))
        os.chmod(filename, stat.S_IRUSR)

    @staticmethod
    def get_workbook(pk):
        if pk in INMEMORYCACHE:
            return INMEMORYCACHE[pk]
        logger.debug("retrieving woorkbook: %s", pk)
        filename = Table.get_chached_name(pk)
        logger.debug("local filename: %s", filename)
        if not os.path.exists(filename):
            logger.debug("retrieving from database")
            obj = Table.objects.get(pk=pk)
            obj.save_to_cache()
        filename_pkl = "{}.pkl".format(filename)
        if os.path.exists(filename_pkl):
            with open(filename_pkl, 'rb') as h:
                book = pickle.load(h)
        else:
            book = openpyxl.load_workbook(filename)
            with open(filename_pkl, 'wb') as h:
                pickle.dump(book, h, pickle.HIGHEST_PROTOCOL)
        INMEMORYCACHE[pk] = book
        return book


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
