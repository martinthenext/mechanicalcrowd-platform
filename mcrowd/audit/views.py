from rest_framework import exceptions
from rest_framework import status
from rest_framework import permissions
from rest_framework.generics import ListAPIView

from .models import AuditLog
from .serializers import AuditLogSerializer


class LogView(ListAPIView):
    serializer = AuditLogSerializer
    queryset = AuditLog.objects
    paginate_by = 10
    paginate_by_param = 'page_size'
    max_paginate_by = 100
    permission_classes = (IsAdminUser,)
