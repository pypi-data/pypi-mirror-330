from .base_table import BaseTable, IDColumn


class StoresTable(BaseTable):

    NAME: str = "stores"

    ID_COLUMN = str(IDColumn("ID"))

    COMPANY_ID_COLUMN: str = str(IDColumn("companyID"))
    REGION_ID_COLUMN: str = str(IDColumn("regionID"))
    NAME_COLUMN: str = "name"

    COLUMN_NAMES = [
        COMPANY_ID_COLUMN,
        REGION_ID_COLUMN,
        NAME_COLUMN,
    ]
