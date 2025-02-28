from .base_table import BaseTable, IDColumn


class DataPointsTable(BaseTable):

    NAME: str = "datapoints"

    ID_COLUMN = str(IDColumn("ID"))

    SKU_ID_COLUMN: str = str(IDColumn("skuID"))
    DATE_ID_COLUMN: str = str(IDColumn("dateID"))

    COLUMN_NAMES: list[str] = [SKU_ID_COLUMN, DATE_ID_COLUMN]
