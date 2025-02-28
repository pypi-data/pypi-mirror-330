from .table_manager import BaseMultiRowManager

from foundry_db.tables.regions import RegionsTable, RegionTypes
from foundry_db.sdk import SQLDatabase


class Regions(BaseMultiRowManager):
    def __init__(
        self,
        parent_regions: list[int | None],
        names: list[str],
        abbreviations: list[str],
        region_types: list[str],
        countries: list[str] = None,
        db: SQLDatabase = None,
    ):
        """
        Initialize Regions object.

        Args:
            parent_regions (list[int | None]): Parent region IDs (None for SQL NULL)
            names (list[str]): Region names
            abbreviations (list[str]): Region abbreviations
            region_types (list[str]): Region types
        """
        rows = [
            (parent_region, name, abbreviation, region_type, country)
            for parent_region, name, abbreviation, region_type, country in zip(
                parent_regions, names, abbreviations, region_types, countries
            )
        ]

        super().__init__(RegionsTable, rows, db)

    def _fetch_ids(self, rows: list[tuple] | None = None):

        sql_db = self._get_db()

        if rows is None:
            rows = self._get_rows()

        queries = f"""
            SELECT {RegionsTable.ID_COLUMN}
            FROM {RegionsTable.NAME}
            WHERE {RegionsTable.PARENT_REGION_ID_COLUMN} IS NOT DISTINCT FROM  %s
            AND {RegionsTable.NAME_COLUMN} = %s
            AND {RegionsTable.ABBREVIATION_COLUMN} = %s
            AND {RegionsTable.TYPE_COLUMN} = %s
        """

        return [
            i[0] for i in sql_db.execute_multiple_queries(queries, rows, fetchrows=True)
        ]

    def set_countries(self) -> None:
        """
        Set countries for regions of type country to its own ID if not already set.
        """

        sql_db = self._get_db()

        # Query that sets the country to its own ID if not already set and the region is of type country
        query = f"""
            UPDATE {RegionsTable.NAME}
            SET {RegionsTable.COUNTRY_COLUMN} = {RegionsTable.ID_COLUMN}
            WHERE {RegionsTable.TYPE_COLUMN} = '{RegionTypes.COUNTRY.value}'
            AND {RegionsTable.COUNTRY_COLUMN} IS NULL
        """

        sql_db.execute_query(query, commit=True)

    def write_to_db(self, insertion_mode):
        super().write_to_db(insertion_mode)
        self.set_countries()
