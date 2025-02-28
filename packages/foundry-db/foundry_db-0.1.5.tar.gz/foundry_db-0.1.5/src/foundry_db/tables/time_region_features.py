from .base_table import BaseTable, IDColumn


class TimeRegionFeaturesTable(BaseTable):
    NAME: str = "time_region_features"

    # Primary key column is "trID"
    ID_COLUMN = str(IDColumn("trfID"))

    DATE_ID_COLUMN = str(IDColumn("dateID"))
    REGION_ID_COLUMN = str(IDColumn("regionID"))
    VALUE_COLUMN = "value"

    COLUMN_NAMES: list[str] = [
        ID_COLUMN,
        DATE_ID_COLUMN,
        REGION_ID_COLUMN,
        VALUE_COLUMN,
    ]
