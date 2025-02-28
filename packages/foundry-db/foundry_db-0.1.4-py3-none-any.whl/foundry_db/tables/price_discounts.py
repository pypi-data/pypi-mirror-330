from .base_table import BaseTable, IDColumn


class PriceDiscountsTable(BaseTable):

    NAME: str = "price_discounts"

    ID_COLUMN = str(IDColumn("datapointID"))
    DATAPOINT_ID_COLUMN: str = str(IDColumn("datapointID"))
    DISCOUNT_COLUMN: str = "discount"

    COLUMN_NAMES: list[str] = [DATAPOINT_ID_COLUMN, DISCOUNT_COLUMN]
