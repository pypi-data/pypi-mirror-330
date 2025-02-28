from .table_manager import BaseMultiRowManager
from .data_points import DataPoints
from .dates import Dates
from .skus import SKUs
from .products import Products
from .stores import Stores

from foundry_db.tables.products import ProductsTable
from foundry_db.tables.stores import StoresTable
from foundry_db.tables.dates import DatesTable


from foundry_db.tables.flags import FlagsTable, FlagNames

from foundry_db.sdk import SQLDatabase


class NotForSaleFlag(BaseMultiRowManager):

    def __init__(
        self,
        data_points: DataPoints,
        dates: Dates,
        skus: SKUs,
        products: Products,
        stores: Stores,
        not_for_sale_map: dict[
            (str, str), list[str]
        ],  # (product_name store_name) -> list of dates
        db: SQLDatabase,
    ):

        # Load dataframes and set indexes
        products_df = products.get_df().set_index(ProductsTable.NAME_COLUMN, drop=False)
        stores_df = stores.get_df().set_index(StoresTable.NAME_COLUMN, drop=False)
        dates_df = dates.get_df()

        # Preload product IDs
        product_names = {p for (p, _) in not_for_sale_map.keys()}
        product_rows = [products_df.loc[name].tolist() for name in product_names]
        product_ids = products.get_ids(product_rows)
        product_map = dict(zip(product_names, product_ids))

        # Preload store IDs
        store_names = {s for (_, s) in not_for_sale_map.keys()}
        store_rows = [stores_df.loc[name].tolist() for name in store_names]
        store_ids = stores.get_ids(store_rows)
        store_map = dict(zip(store_names, store_ids))

        # Preload SKU IDs
        sku_requests = [
            (product_map[p], store_map[s]) for p, s in not_for_sale_map.keys()
        ]
        sku_ids = skus.get_ids(sku_requests)
        sku_map = dict(zip(sku_requests, sku_ids))

        # Preload date IDs
        unique_dates = {date for dates in not_for_sale_map.values() for date in dates}
        date_rows = dates_df[dates_df[DatesTable.DATE_COLUMN].isin(unique_dates)]
        date_ids = dates.get_ids(date_rows.values.tolist())
        date_map = dict(zip(date_rows[DatesTable.DATE_COLUMN], date_ids))

        # Build data point rows
        data_point_rows = []
        for (product_name, store_name), flag_dates in not_for_sale_map.items():
            sku_id = sku_map[(product_map[product_name], store_map[store_name])]
            for date in date_rows.loc[
                date_rows[DatesTable.DATE_COLUMN].isin(flag_dates),
                DatesTable.DATE_COLUMN,
            ]:
                data_point_rows.append((sku_id, date_map[date]))

        # Get data point IDs in one batch
        data_point_ids = data_points.get_ids(data_point_rows)

        # Prepare final rows
        rows = [(dp_id, FlagNames.NOT_FOR_SALE) for dp_id in data_point_ids]

        super().__init__(FlagsTable, rows, db)
