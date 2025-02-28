from .base_table import BaseTable, IDColumn


class TimeStoreFeaturesTable(BaseTable):
    NAME: str = "time_store_features"

    # Primary key column "tsfiD"
    ID_COLUMN = (
        str(IDColumn("dateID")),
        str(IDColumn("storeID")),
        str(IDColumn("tsfID")),
    )

    DATE_ID_COLUMN: str = str(IDColumn("dateID"))
    STORE_ID_COLUMN = str(IDColumn("storeID"))
    TIME_STORE_FEATURES_ID_COLUMN: str = str(IDColumn("tsfID"))
    VALUE_COLUMN: str = "value"

    COLUMN_NAMES: list[str] = [
        DATE_ID_COLUMN,
        STORE_ID_COLUMN,
        TIME_STORE_FEATURES_ID_COLUMN,
        VALUE_COLUMN,
    ]
