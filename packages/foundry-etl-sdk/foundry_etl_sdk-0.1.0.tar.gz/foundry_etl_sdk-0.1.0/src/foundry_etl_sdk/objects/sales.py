from .datapoint_manager import AbstractDataPointLevelManager, DataMap
from .products import Products
from .stores import Stores
from .dates import Dates
from .skus import SKUs

from .data_points import DataPoints

from foundry_db.tables.sales import SalesTable

from foundry_db.sdk import SQLDatabase


class SALES:
    MISSING_VALUE = 0


class Sales(AbstractDataPointLevelManager):
    def __init__(
        self,
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
        sales_map: dict,
        db: SQLDatabase,
    ):

        data_map = DataMap(sales_map, SALES.MISSING_VALUE)
        super().__init__(
            SalesTable,
            products,
            stores,
            skus,
            dates,
            data_points,
            data_map,
            db,
        )
