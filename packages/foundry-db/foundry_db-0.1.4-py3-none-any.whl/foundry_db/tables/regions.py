from .base_table import BaseTable, IDColumn
from enum import Enum


class RegionTypes(Enum):
    COUNTRY = "country"
    STATE = "state"


class RegionsTable(BaseTable):

    NAME: str = "regions"

    ID_COLUMN = str(IDColumn("ID"))

    PARENT_REGION_ID_COLUMN: str = str(IDColumn("parent_regionID"))
    NAME_COLUMN: str = "name"
    ABBREVIATION_COLUMN: str = "abbreviation"
    TYPE_COLUMN: str = "type"
    COUNTRY_COLUMN: str = "country"

    COLUMN_NAMES: list[str] = [
        PARENT_REGION_ID_COLUMN,
        NAME_COLUMN,
        ABBREVIATION_COLUMN,
        TYPE_COLUMN,
        COUNTRY_COLUMN,
    ]
