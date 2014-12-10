import logging

from rest_framework import exceptions

from openpyxl.cell import coordinate_from_string
from openpyxl.cell import column_index_from_string, get_column_letter

logger = logging.getLogger(__name__)


def get_sheet_by_name(book, name):
    sheet = book.get_sheet_by_name(name)
    if not sheet:
        raise exceptions.ParseError(
            detail="Sheet should be one of: %s" % book.get_sheet_names())
    return sheet


def get_square_indices(sheet, location):
    logger.debug("location: '%s'", location)
    left, right = location.upper().split(':')
    left_column_letter, left_row = coordinate_from_string(left)
    left_column = column_index_from_string(left_column_letter)
    if right:
        right_column_letter, right_row = coordinate_from_string(right)
        right_column = column_index_from_string(right_column_letter)
        right_defined = True
    else:
        right_row = sheet.get_highest_row()
        right_column = sheet.get_highest_column()
        right_defined = False
    logger.debug("square: %s.%s:%s.%s",
                 left_column, left_row, right_column, right_row)
    if left_column > right_column:
        raise exceptions.ParseError(
            detail="Left column should be less than right")
    if left_row <= 0 or right_row <= 0:
        raise exceptions.ParseError(
            detail="Row index should be greater than 0")
    if left_row > right_row:
        raise exceptions.ParseError(
            detail="Left row index should be less or equal than right row")
    return left_column, left_row, right_column, right_row, right_defined


def get_range(sheet, left_column, left_row, right_column, right_row):
    range_string = "%s%d:%s%d" % (get_column_letter(left_column), left_row,
                                  get_column_letter(right_column), right_row)
    return sheet.range(range_string)


def get_header_columns(sheet, header_location):
    logger.debug("get_header_columns")
    left_column, left_row, right_column, right_row, right_defined = \
        get_square_indices(sheet, header_location)
    if not right_defined:
        right_row = left_row
    if right_row != left_row:
        raise exceptions.ParseError(
            detail="Multiline headers not implemented yet")
    logger.debug("header square: %s.%s:%s.%s",
                 left_column, left_row, right_column, right_row)
    header = get_range(sheet, left_column, left_row, right_column, right_row)
    for row in header:
        for value in row:
            if value.value or right_defined:
                yield value  # it is openpyxl.cell.Cell object
            else:
                raise StopIteration()


def get_header_index_by_name(header, name):
    found = list(filter(lambda x: str(x.value) == str(name), header))
    if found:
        logger.debug("column: %s -> %s", name, found[0].column)
        return found[0].column
    raise exceptions.ParseError(
        detail="Could not find column with name: '%s'" % name)


def is_empty_row(row):
    not_empty = filter(lambda x: x.value, row)
    return not bool(not_empty)


def get_data_rows(sheet, header, columns, data_location):
    column_indices = set(map(lambda x: get_header_index_by_name(header, x),
                         columns))
    left_column, left_row, right_column, right_row, right_defined = \
        get_square_indices(sheet, data_location)
    if not right_defined:
        right_column = left_column + len(header)
    if column_index_from_string(header[0].column) != left_column:
        raise exceptions.ParseError(
            detail="Header left index should be equals to data left index")
    logger.debug("data square: %s.%s:%s.%s",
                 left_column, left_row, right_column, right_row)
    logger.debug("columns: %s : %s", columns, column_indices)
    data = get_range(sheet, left_column, left_row, right_column, right_row)
    for i, row in enumerate(data):
        selected = tuple(filter(lambda x: x.column in column_indices, row))
        if not is_empty_row(selected) or right_defined:
            yield left_row + i, selected
        else:
            raise StopIteration()
