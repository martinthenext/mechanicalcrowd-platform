import json

from django.db import models
from django.contrib.auth.models import User


class AuditLog(models.Model):
    TYPES = (("U", "update"), ("C", "create"), ("D", "delete"))

    user = models.ForeignKey(User, null=True)
    type = models.CharField(
        max_length=2, blank=False, null=False, default="U",
        choices=TYPES)
    model = models.CharField(
        max_length=255, blank=True, null=False, default="")
    timestamp = models.DateTimeField(
        auto_now=True, auto_now_add=True, null=False)
    event = models.TextField(null=False, blank=False)
