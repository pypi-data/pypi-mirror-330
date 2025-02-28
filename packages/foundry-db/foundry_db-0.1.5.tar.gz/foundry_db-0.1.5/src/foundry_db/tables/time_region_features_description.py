from .base_table import BaseTable, IDColumn


class TimeRegionFeaturesDescriptionTable(BaseTable):
    NAME: str = "time_region_features_description"

    # "ID" is provided as a primary key column
    ID_COLUMN = str(IDColumn("ID"))

    NAME_COLUMN = "name"
    DESCRIPTION_COLUMN = "description"

    COLUMN_NAMES: list[str] = [NAME_COLUMN, DESCRIPTION_COLUMN]
