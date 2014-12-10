from rest_framework import status
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

import openpyxl

import io
import logging
import json

from .models import Table
from .serializers import TableSerializer

logger = logging.getLogger(__name__)


class TablesView(APIView):
    parser_classes = (FileUploadParser,)
    content_type = \
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    def validate(self, xlsx_obj):
        if xlsx_obj.content_type != self.content_type:
            raise exceptions.UnsupportedMediaType(xlsx_obj.content_type)
        try:
            data = xlsx_obj.read()
            book = openpyxl.load_workbook(io.BytesIO(data))
            logger.info("validated book: sheets: %s", book.get_sheet_names())
        except Exception as e:
            logger.exception(e)
            raise exceptions.UnsupportedMediaType(xlsx_obj.content_type)
        return (data, book)

    def post(self, request):
        xlsx_obj = request.FILES['file']
        logger.debug("table: size: %s", xlsx_obj.size)
        logger.debug("table: content-type: %s", xlsx_obj.content_type)
        data, book = self.validate(xlsx_obj)
        table = Table.objects.create(
            owner=request.user,
            table=data,
            filename=xlsx_obj.name,
            sheets=json.dumps(book.get_sheet_names()))
        return Response(TableSerializer(table).data, status=200)

    def get(self, request, pk=None):
        queryset = Table.objects.filter(owner=request.user)
        return Response(TableSerializer(queryset, many=True).data, status=200)


class TableView(RetrieveAPIView):
    serializer_class = TableSerializer

    def get_queryset(self):
        return Table.objects.filter(owner=self.request.user)
