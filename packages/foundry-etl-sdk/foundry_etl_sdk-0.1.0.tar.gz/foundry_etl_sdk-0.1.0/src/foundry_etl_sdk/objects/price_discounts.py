from .datapoint_manager import AbstractDataPointLevelManager, DataMap

from .data_points import DataPoints
from .products import Products
from .stores import Stores
from .skus import SKUs
from .dates import Dates


from foundry_db.tables.price_discounts import PriceDiscountsTable

from foundry_db.sdk import SQLDatabase


class PRICE_DISCOUNTS:
    MISSING_VALUE = False


class PriceDiscounts(AbstractDataPointLevelManager):
    def __init__(
        self,
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
        price_discounts_map: dict,
        db: SQLDatabase,
    ):

        data_map = DataMap(price_discounts_map, PRICE_DISCOUNTS.MISSING_VALUE)

        super().__init__(
            PriceDiscountsTable,
            products,
            stores,
            skus,
            dates,
            data_points,
            data_map,
            db,
        )
