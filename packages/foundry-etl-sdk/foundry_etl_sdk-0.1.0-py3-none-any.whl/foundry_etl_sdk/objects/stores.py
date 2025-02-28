from .table_manager import BaseMultiRowManager
from .company import Company
from .regions import Regions

from foundry_db.tables.regions import RegionsTable
from foundry_db.tables.stores import StoresTable

from foundry_db.sdk import SQLDatabase


class Stores(BaseMultiRowManager):
    def __init__(
        self,
        store_region_map: dict[str, str],
        regions: Regions,
        company: Company,
        db: SQLDatabase,
    ):
        company_id = company.get_id()
        regions_df = regions.get_df().set_index(
            RegionsTable.ABBREVIATION_COLUMN, drop=False
        )

        region_values = [
            regions_df.loc[abbr].values.tolist() for abbr in store_region_map.values()
        ]

        region_ids = regions.get_ids(region_values)
        rows = [
            (company_id, region_id, store_name)
            for store_name, region_id in zip(store_region_map.keys(), region_ids)
        ]

        super().__init__(StoresTable, rows, db)
