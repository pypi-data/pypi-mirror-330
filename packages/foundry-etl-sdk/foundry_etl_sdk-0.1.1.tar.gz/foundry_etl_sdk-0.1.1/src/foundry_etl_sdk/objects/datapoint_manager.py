from .table_manager import BaseMultiRowManager
from .data_points import DataPoints
from .products import Products
from .stores import Stores
from .dates import Dates
from .skus import SKUs


from foundry_db.tables import BaseTable, StoresTable, ProductsTable, DatesTable
from foundry_db.sdk import SQLDatabase


class DataMap:

    def __init__(self, map: dict, missing_value: float):
        self.map = map
        self.missing_value = missing_value

    def get(self, key: tuple) -> float:
        return self.map.get(key, self.missing_value)


class DataPointRowsFactory:
    """
    Factory class for building a list of data values.
    """

    @staticmethod
    def build(
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
        data_map: DataMap,
    ) -> list[float]:
        """
        Builds a list of data values by mapping store names, product names, and dates to their corresponding values.

        Parameters
        ----------
        products : Products
            An instance containing product information.
        stores : Stores
            An instance containing store information.
        dates : Dates
            An instance containing date information.
        data_map : DataMap
            An instance containing data values mapped to store names, product names, and dates.

        Returns
        -------
        list of float
            A list of data values ordered by store, product, and date.
        """

        # Preload store, product, and date information once
        store_ids = stores.get_ids()
        store_names = list(stores.get_df()[StoresTable.NAME_COLUMN])
        product_ids = products.get_ids()
        product_names = list(products.get_df()[ProductsTable.NAME_COLUMN])
        date_ids = dates.get_ids()
        date_values = list(dates.get_df()[DatesTable.DATE_COLUMN])

        # Zip the IDs with their corresponding names/dates for clarity, renamed as items
        stores_items = list(zip(store_ids, store_names))
        products_items = list(zip(product_ids, product_names))
        dates_items = list(zip(date_ids, date_values))

        # Preload SKU IDs for all (product, store) pairs
        sku_requests = [
            (prod_id, store_id)
            for store_id, _ in stores_items
            for prod_id, _ in products_items
        ]
        sku_ids = skus.get_ids(sku_requests)
        sku_map = {
            (prod_id, store_id): sku_id
            for (prod_id, store_id), sku_id in zip(sku_requests, sku_ids)
        }

        # Preload Data Point IDs for every (sku, date) combination
        dp_requests = [
            (sku_map[(prod_id, store_id)], date_id)
            for store_id, _ in stores_items
            for prod_id, _ in products_items
            for date_id, _ in dates_items
        ]
        dp_ids = data_points.get_ids(dp_requests)

        # Map each (sku, date) to its corresponding data point ID
        dp_map = {}
        i = 0
        for store_id, _ in stores_items:
            for prod_id, _ in products_items:
                sku_id = sku_map[(prod_id, store_id)]
                for date_id, _ in dates_items:
                    dp_map[(sku_id, date_id)] = dp_ids[i]
                    i += 1

        # Build rows using preloaded IDs and data_map
        rows = []
        for store_id, store_name in stores_items:
            for prod_id, prod_name in products_items:
                sku_id = sku_map[(prod_id, store_id)]
                for date_id, date in dates_items:
                    data_point_id = dp_map[(sku_id, date_id)]
                    data_value = data_map.get((store_name, prod_name, date))
                    rows.append((data_point_id, data_value))

        return rows


class AbstractDataPointLevelManager(BaseMultiRowManager):
    """
    Abstract class for managing data points at a specific level.
    """

    def __init__(
        self,
        table: BaseTable,
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
        data_map: DataMap,
        db: SQLDatabase,
    ):
        rows = DataPointRowsFactory.build(
            products, stores, skus, dates, data_points, data_map
        )
        super().__init__(table, rows, db)
