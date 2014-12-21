from rest_framework import exceptions
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

import openpyxl

import collections
import io
import json
import logging

from .models import Task, Row, RowDiff
from .serializers import TaskRelatedSerializer
from .serializers import TaskSerializer
from .settings import BATCH_SIZE

from mcrowd.xlsx.models import Table
from mcrowd.xlsx.utils import is_empty_row

from mcrowd.common.exceptions import BadRequest

logger = logging.getLogger(__name__)


class TaskCommonMixin:
    def pre_save(self, obj):
        if not obj.columns:
            obj.columns = obj.table.col_names
            return
        unknown = set(obj.get_col_names()) - set(obj.table.get_col_names())
        if unknown:
            raise BadRequest(detail="Unknown columns: %s" % unknown)

    def post_save(self, obj, created=False):
        if not created:
            oldobj = Task.objects.get(pk=obj.pk)
            if oldobj.table != obj.table or oldobj.columns != obj.columns:
                if oldobj.active:
                    raise BadRequest("Could not redefine table: "
                                     "task was committed already")
                obj.rows.all().delete()
            else:
                return  # rows already created
        objects = []
        for number, row in obj.table.get_rows(col_ids=obj.get_col_ids()):
            objects.append(Row(task=obj, number=number,
                               values=json.dumps(row)))
        Row.objects.bulk_create(objects, batch_size=BATCH_SIZE)

    def get_serializer_class(self):
        if self.request.method in ("POST", "PUT"):
            table = self.request.DATA.get("table")
            if table is None:
                raise BadRequest("Undefined table")
            elif isinstance(table, collections.Mapping):
                return TaskSerializer
            else:
                return TaskRelatedSerializer
        else:
            return TaskRelatedSerializer


class TasksView(TaskCommonMixin, ListCreateAPIView):
    def get_queryset(self):
        return Task.objects.filter(
            table__worksheet__workbook__owner=self.request.user)


class TaskView(TaskCommonMixin, RetrieveUpdateDestroyAPIView):
    def get_queryset(self):
        return Task.objects.filter(
            table__worksheet__workbook__owner=self.request.user)


class OriginalRowsView(APIView):
    def get(self, request, pk=None):
        task = get_object_or_404(
            Task, pk=pk, table__worksheet__workbook__owner=self.request.user)
        data = {
            "col_names": task.get_col_names(),
            "col_ids": task.get_col_ids(),
            "rows": task.get_original_rows()
        }
        return Response(data, status=200)


class RowDiffView(APIView):
    def get(self, request, pk=None):
        task = get_object_or_404(
            Task, pk=pk, table__worksheet__workbook__owner=self.request.user)
        row_diff = []
        meta_diff = []
        logger.debug(self.request.GET)
        if "aggregated" in self.request.GET:
            queryset = RowDiff.objects.get_last(task)
        else:
            queryset = task.diff.all()
        for diff in queryset:
                row_diff.append([diff.number, diff.get_values()])
                meta_diff.append(diff.get_meta())
        data = {
            "row_diff": row_diff,
            "meta_diff": meta_diff
        }
        return Response(data, status=200)

    def post(self, request, pk=None):
        task = get_object_or_404(
            Task, pk=pk, table__worksheet__workbook__owner=self.request.user)
        row_diff = self.request.DATA.get("row_diff", [])
        meta_diff = self.request.DATA.get("meta_diff", [])
        if len(row_diff) != len(meta_diff):
            raise BadRequest(detail="Length of rows and meta are not equals")
        if not row_diff:
            raise BadRequest(detail="row_diff is required")
        diff = []
        for (number, values), meta in zip(row_diff, meta_diff):
            if values is not None and len(task.get_col_ids()) != len(values):
                raise BadRequest(
                    detail="Length of diff and original row are not equals")
            meta = meta or {}
            meta["user"] = self.request.user.username
            diff.append(RowDiff(task=task, number=number,
                                values=json.dumps(values),
                                meta=json.dumps(meta)))
        RowDiff.objects.bulk_create(diff, batch_size=BATCH_SIZE)
        return Response(status=201)
