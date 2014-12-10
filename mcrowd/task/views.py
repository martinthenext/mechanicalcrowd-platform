from rest_framework import status
from rest_framework import exceptions
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.generics import ListCreateAPIView

from django.shortcuts import get_object_or_404

import openpyxl

import io
import logging

from .models import Task, Row
from .serializers import TaskSerializer

from mcrowd.xlsx.models import Table
from mcrowd.xlsx.utils import get_sheet_by_name, get_header_columns
from mcrowd.xlsx.utils import get_data_rows

logger = logging.getLogger(__name__)


def parse_header(sheet, location):
    location = location.strip()
    return tuple(get_header_columns(sheet, location))


def parse_columns(header, columns):
    columns = columns.strip()
    if not columns:
        columns = map(lambda x: x.value or "", header)
    else:
        columns = map(lambda x: x.strip(), columns.split(","))
    return tuple(filter(lambda x: x, columns))


class TaskSaveHook:
    def pre_save(self, obj):
        logger.debug("pre_save")
        book = Table.get_workbook(obj.table.pk)
        sheet = get_sheet_by_name(book, obj.sheet.strip())
        header = parse_header(sheet, obj.header_location)
        columns = parse_columns(header, obj.columns)
        logger.debug(columns)
        obj.columns = ",".join(columns)
        self.rows = get_data_rows(sheet, header, columns, obj.data_location)

    def post_save(self, obj, created=False):
        logger.debug("post_save")
        if not created:
            obj.rows.all().delete()
        objects = []
        for number, row in self.rows:
            values = dict(map(lambda x: (x.column, x.value), row))
            objects.append(Row(task=obj, number=number, values=values))
        Row.objects.bulk_create(objects)


class TasksView(TaskSaveHook, ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(table__owner=self.request.user)


class TaskView(TaskSaveHook, RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(table__owner=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, **self.kwargs)
        if obj.active and self.request.method in ["DELETE", "PUT", "PATCH"]:
            raise exceptions.MethodNotAllowed(
                self.request.method, detail="Could not change active task")
        return obj
