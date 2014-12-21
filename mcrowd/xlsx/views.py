import io
import json
import logging

from django.shortcuts import get_object_or_404

from rest_framework import exceptions
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView

import openpyxl

from .models import Workbook, Worksheet, Table
from .serializers import WorkbookSerializer, WorksheetSerializer
from .serializers import TableSerializer
from .settings import SAMPLE_SIZE

from mcrowd.common.exceptions import BadRequest

logger = logging.getLogger(__name__)


class WorkbookUploaderView(APIView):
    parser_classes = (FileUploadParser,)
    content_type = \
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def post(self, request):
        xlsx = request.FILES.get('file')
        if xlsx is None:
            raise BadRequest()
        if xlsx.content_type != self.content_type:
            raise exceptions.UnsupportedMediaType(xlsx.content_type)
        table = Workbook.objects.create(
            owner=request.user,
            data=xlsx.read(),
            filename=xlsx.name)
        return Response(WorkbookSerializer(table).data, status=200)

    def get(self, request, pk=None):
        queryset = Workbook.objects.filter(owner=request.user)
        return Response(
            WorkbookSerializer(queryset, many=True).data, status=200)


class WorkbookView(RetrieveAPIView):
    serializer_class = WorkbookSerializer

    def get_queryset(self):
        return Workbook.objects.filter(owner=self.request.user)


class WorksheetsView(ListAPIView):
    serializer_class = WorksheetSerializer

    def get_queryset(self):
        return Worksheet.objects.filter(
            workbook__owner=self.request.user,
            workbook__pk=self.kwargs.get("workbook"))


class WorksheetView(RetrieveAPIView, APIView):
    serializer_class = WorksheetSerializer
    lookup_field = "number"

    def get_queryset(self):
        return Worksheet.objects.filter(
            workbook__owner=self.request.user,
            workbook__pk=self.kwargs.get("workbook"))


class TablesView(ListCreateAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(
            worksheet__workbook__owner=self.request.user,
            worksheet__workbook__pk=self.kwargs.get("workbook"),
            worksheet__number=self.kwargs.get("number"))


class TableView(RetrieveUpdateDestroyAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(
            worksheet__workbook__owner=self.request.user,
            worksheet__workbook__pk=self.kwargs.get("workbook"),
            worksheet__number=self.kwargs.get("number"))


class SampleView(APIView):
    def get(self, request, workbook=None, number=None, pk=None):
        table = get_object_or_404(
            Table,
            worksheet__workbook__owner=self.request.user,
            worksheet__workbook__pk=workbook,
            worksheet__number=number,
            pk=pk)
        data = {
            "col_names": table.get_col_names(),
            "col_ids": table.get_col_ids(),
            "rows": table.get_rows(limit=SAMPLE_SIZE)
        }
        return Response(data, status=200)
