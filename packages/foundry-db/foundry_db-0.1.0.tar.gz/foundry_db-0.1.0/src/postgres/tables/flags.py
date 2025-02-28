from .base_table import BaseTable, IDColumn

from enum import Enum


class FlagNames(Enum):

    NOT_FOR_SALE: str = "not_for_sale"


class FlagsTable(BaseTable):

    NAME: str = "flags"

    ID_COLUMN = str(IDColumn("datapointID"))

    DATAPOINT_ID_COLUMN: str = str(IDColumn("datapointID"))
    NAME_COLUMN: str = "name"

    COLUMN_NAMES: list[str] = [DATAPOINT_ID_COLUMN, NAME_COLUMN]
