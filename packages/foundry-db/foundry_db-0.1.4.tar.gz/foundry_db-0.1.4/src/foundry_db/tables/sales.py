from .base_table import BaseTable, IDColumn


class SalesTable(BaseTable):

    NAME: str = "sales"

    ID_COLUMN = str(IDColumn("datapointID"))
    DATAPOINT_ID_COLUMN: str = str(IDColumn("datapointID"))
    SALES_COLUMN: str = "sales"

    COLUMN_NAMES: list[str] = [DATAPOINT_ID_COLUMN, SALES_COLUMN]
