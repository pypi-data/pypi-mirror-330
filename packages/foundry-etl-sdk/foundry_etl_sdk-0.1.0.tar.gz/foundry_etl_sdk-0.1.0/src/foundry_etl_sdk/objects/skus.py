from .table_manager import BaseMultiRowManager
from .products import Products
from .stores import Stores


from foundry_db.tables.stores import StoresTable
from foundry_db.tables.products import ProductsTable
from foundry_db.tables.sku_table import SkuTable

from foundry_db.sdk import SQLDatabase


class SKUs(BaseMultiRowManager):
    def __init__(
        self,
        products: Products,
        stores: Stores,
        store_product_map: dict | None = None,  # store_name -> list of product_names
        db: SQLDatabase = None,
    ):
        # Get DataFrames and set indices to store data by name
        stores_df = stores.get_df().set_index(StoresTable.NAME_COLUMN, drop=False)
        products_df = products.get_df().set_index(ProductsTable.NAME_COLUMN, drop=False)

        # Default: each store gets all products
        if store_product_map is None:
            store_product_map = {
                store: products_df.index.tolist() for store in stores_df.index
            }

        # Preload store data for all needed stores in one get_ids call
        store_names = list(store_product_map.keys())
        store_rows = [stores_df.loc[name].tolist() for name in store_names]
        store_ids = stores.get_ids(store_rows)
        store_map = dict(zip(store_names, store_ids))

        # Preload product data for all unique products in one get_ids call
        unique_product_names = {
            p for products in store_product_map.values() for p in products
        }
        unique_product_names = list(unique_product_names)
        product_rows = [products_df.loc[name].tolist() for name in unique_product_names]
        product_ids = products.get_ids(product_rows)
        product_map = dict(zip(unique_product_names, product_ids))

        # Build SKU rows using the preloaded IDs
        rows = []
        for store_name, product_names in store_product_map.items():
            store_id = store_map[store_name]
            for product_name in product_names:
                product_id = product_map[product_name]
                rows.append([product_id, store_id])

        super().__init__(SkuTable, rows)
