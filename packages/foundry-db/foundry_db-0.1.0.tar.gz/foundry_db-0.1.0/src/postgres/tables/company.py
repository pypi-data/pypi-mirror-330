from .base_table import BaseTable, IDColumn


class CompanyTable(BaseTable):

    NAME: str = "companies"

    ID_COLUMN = str(IDColumn("ID"))

    NAME_COLUMN: str = "name"
    DATASET_TYPE_COLUMN: str = "dataset_type"
    DESCRIPTION_COLUMN: str = "description"

    COLUMN_NAMES: list[str] = [NAME_COLUMN, DATASET_TYPE_COLUMN, DESCRIPTION_COLUMN]
