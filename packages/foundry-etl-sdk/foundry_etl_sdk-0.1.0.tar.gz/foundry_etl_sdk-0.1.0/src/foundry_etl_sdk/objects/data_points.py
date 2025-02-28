from .table_manager import BaseMultiRowManager
from .dates import Dates
from .skus import SKUs

from foundry_db.tables.datapoints import DataPointsTable

from foundry_db.sdk import SQLDatabase


class DataPoints(BaseMultiRowManager):
    """
    Class to represent data points
    """

    def __init__(self, skus: SKUs, dates: Dates, db: SQLDatabase):
        """
        Initialize DataPoints object

        Args:

        skus: SKUs
            SKUs object
        dates: Dates
            Dates object
        """

        rows = [
            (sku_id, date_id)
            for sku_id in skus.get_ids()
            for date_id in dates.get_ids()
        ]

        super().__init__(DataPointsTable, rows, db)
