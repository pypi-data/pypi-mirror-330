from .base_table import BaseTable, IDColumn


class TimeRegionFeaturesCompanyTable(BaseTable):
    NAME: str = "time_region_features_company"

    # Assuming "trID" acts as the primary key here
    ID_COLUMN = str(IDColumn("trfID"))

    COMPANY_ID_COLUMN = str(IDColumn("companyID"))

    COLUMN_NAMES: list[str] = [ID_COLUMN, COMPANY_ID_COLUMN]
