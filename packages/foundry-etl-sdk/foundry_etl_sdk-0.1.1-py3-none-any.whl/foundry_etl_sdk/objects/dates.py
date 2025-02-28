import pandas as pd

from .table_manager import BaseMultiRowManager
from foundry_db.tables import DatesTable

from foundry_db.sdk import SQLDatabase


class Dates(BaseMultiRowManager):

    @classmethod
    def from_series(cls, series: pd.Series, db: SQLDatabase):
        """
        Create a Dates object from a pandas Series object.

        Args:
        series: pd.Series
            Series object containing dates
        """

        start_date = series.min()
        end_date = series.max()

        return cls(start_date, end_date, db)

    def __init__(
        self, start_date: pd.Timestamp, end_date: pd.Timestamp, db: SQLDatabase
    ):
        """
        Initialize Dates object

        Args:

        start_date: pd.Timestamp
            Start date
        end_date: pd.Timestamp
            End date
        """

        rows = [
            (date.date(),) for date in pd.date_range(start=start_date, end=end_date)
        ]

        super().__init__(DatesTable, rows, db)

    def get_date_range(self):
        """
        Get date range

        Returns:
        pd.date_range
            Date range
        """
        date_df = self.get_df()
        min_date = date_df[DatesTable.DATE_COLUMN].min()
        max_date = date_df[DatesTable.DATE_COLUMN].max()
        return pd.date_range(start=min_date, end=max_date)
