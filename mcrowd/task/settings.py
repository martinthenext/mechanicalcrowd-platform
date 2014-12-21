import os

from django.conf import settings as S


if hasattr(S, "TASK"):
    TASK = S.TASK
else:
    TASK = {}

BATCH_SIZE = TASK.get("BATCH_SIZE", 1000)
