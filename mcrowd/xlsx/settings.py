import os

from django.conf import settings as S


if hasattr(S, "XLSX"):
    XLSX = S.XLSX
else:
    XLSX = {}

LOCALSTORE = XLSX.get("LOCALSTORE", "cache")
if not os.path.isdir(LOCALSTORE):
    os.makedirs(LOCALSTORE)

HEADER_LOCATION = XLSX.get("HEADER_LOCATION", "A1:")

DATA_LOCATION = XLSX.get("DATA_LOCATION", "A2:")

SKIP_EMPTY_ROWS = XLSX.get("SKIP_EMPTY_ROWS", True)

SAMPLE_SIZE = XLSX.get("SAMPLE_SIZE", 10)
