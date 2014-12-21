import json
import logging

from .utils import get_header_columns

logger = logging.getLogger(__name__)


def load_native_workbook(sender, instance, *args, **kwargs):
    instance.load_workbook()


def save_to_cache(sender, instance, *args, **kwargs):
    instance.save_to_cache()


def create_worksheets(sender, instance, *args, **kwargs):
    from .models import Worksheet
    names = instance.get_workbook().get_sheet_names()
    sheets = []
    for i, name in enumerate(names):
        sheets.append(Worksheet(workbook=instance, name=name, number=i))
    Worksheet.objects.bulk_create(sheets)


def check_header(sender, instance, *ars, **kwargs):
    sheet = instance.worksheet.get_worksheet()
    header = get_header_columns(sheet, instance.header_location)
    col_names = []
    col_ids = []
    for cell in header:
        col_names.append(cell.value or "")
        col_ids.append(cell.column)
    instance.col_names = json.dumps(col_names)
    instance.col_ids = json.dumps(col_ids)


def deduplicate_table(sender, instance, *args, **kwargs):
    worksheet = instance.worksheet
    header_location = instance.header_location
    data_location = instance.data_location
    found = Table.objects.filter(
        worksheet=worksheet,
        header_location=header_location,
        data_location=data_location)
    if found:
        instance = found[0]
