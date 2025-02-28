from foundry_db.sdk import SQLDatabase

from ..enums import InsertionMode

from abc import ABC, abstractmethod
import logging
from enum import Enum

from foundry_db.tables import BaseTable

import pandas as pd


class RowType(Enum):
    SingleRow = "SingleRow"
    MultiRow = "MultiRow"


class BaseTableManager(ABC):
    def __init__(
        self, table: BaseTable, row_type: RowType, db: SQLDatabase | None = None
    ):
        self._table = table
        self._row_type = row_type

        self._db = db

    def _get_db(self):
        return SQLDatabase()

    @abstractmethod
    def _already_exists_in_db(self):
        pass

    @abstractmethod
    def insert_into_db(self, **kwargs):
        pass

    @abstractmethod
    def update_in_db(self):
        pass

    def write_to_db(self, insertion_mode: InsertionMode):

        if self._already_exists_in_db():

            if insertion_mode == InsertionMode.IGNORE:
                return
            elif insertion_mode == InsertionMode.RAISE:
                raise Exception(f"{self._table.NAME} already exists")
            elif insertion_mode == InsertionMode.UPDATE:
                logging.info(f"Updating {self._table.NAME} in the database")
                self.update_in_db()
            elif (
                insertion_mode == InsertionMode.INSERT_MISSING
                and self._row_type == RowType.MultiRow
            ):
                logging.info(f"Inserting missing rows in {self._table.NAME}")
                self.insert_into_db(
                    insert_rows=[id_val is None for id_val in self._ids]
                )
        else:
            logging.info(f"Inserting {self._table.NAME} into the database")
            self.insert_into_db()


# ---------- SingleRow Manager using parameterized queries ----------


class BaseSingleRowManager(BaseTableManager):

    def __init__(self, table: BaseTable, row: list, db: SQLDatabase | None = None):
        self._row = row
        super().__init__(table, RowType.SingleRow, db)
        self._id = self._fetch_id()

    def _fetch_id(self):

        sql_db = self._get_db()

        query = (
            f"SELECT {self._table.ID_COLUMN} FROM {self._table.NAME} "
            "WHERE " + " AND ".join(f"{col} = %s" for col in self._table.COLUMN_NAMES)
        )
        result = sql_db.execute_query(query, tuple(self._row), fetchone=True)
        if result is not None:
            return int(result[0])

    def _already_exists_in_db(self):
        return self._id is not None

    def _set_id(self, id_val: int | None = None):
        self._id = self._fetch_id() if id_val is None else id_val

    def get_row(self):
        return self._row

    def get_id(self):
        return self._id

    def insert_into_db(self):

        sql_db = self._get_db()

        col_names = ", ".join(self._table.COLUMN_NAMES)
        placeholders = ", ".join(["%s"] * len(self._row))
        query = (
            f"INSERT INTO {self._table.NAME} ({col_names}) "
            f"VALUES ({placeholders}) RETURNING {self._table.ID_COLUMN}"
        )
        result = sql_db.execute_query(
            query, tuple(self._row), fetchone=True, commit=True
        )
        if result:
            self._set_id(int(result[0]))

    def update_in_db(self):

        sql_db = self._get_db()

        set_clause = ", ".join(f"{col} = %s" for col in self._table.COLUMN_NAMES)
        query = f"UPDATE {self._table.NAME} SET {set_clause} WHERE {self._table.ID_COLUMN} = %s"
        params = tuple(self._row) + (self._id,)
        sql_db.execute_query(query, params, commit=True)
        self._set_id()


# ---------- MultiRow Manager using fetch_ids_bulk ----------


class BaseMultiRowManager(BaseTableManager):

    def __init__(
        self, table: BaseTable, rows: list[tuple], db: SQLDatabase | None = None
    ):

        self._df = pd.DataFrame(rows, columns=table.COLUMN_NAMES)

        self._n_rows = len(rows)
        super().__init__(table, RowType.MultiRow, db)
        self._ids = self._fetch_ids()

    def __len__(self):
        return self._n_rows

    def _get_rows(self, df: pd.DataFrame | None = None):
        if df is None:
            df = self._df
        return df.values.tolist()

    def _set_ids(self):
        self._ids = self._fetch_ids()

    def _fetch_ids(self, rows: list[tuple] | None = None):

        sql_db = self._get_db()

        if rows is None:
            rows = self._get_rows()
        return sql_db.fetch_ids_bulk(
            self._table.NAME, self._table.ID_COLUMN, self._table.COLUMN_NAMES, rows
        )

    def _already_exists_in_db(self):
        return any(id_val is not None for id_val in self._ids)

    def get_df(self):
        return self._df

    def get_ids(self, rows: list[tuple] | None = None):
        if rows is None:
            return self._ids
        return self._fetch_ids(rows)

    def insert_into_db(self, insert_rows: list[bool] | None = None):

        sql_db = self._get_db()

        if insert_rows is None:
            insert_rows = [True] * self._n_rows
        placeholders = ", ".join(["%s"] * len(self._table.COLUMN_NAMES))
        query = f"INSERT INTO {self._table.NAME} ({', '.join(self._table.COLUMN_NAMES)}) VALUES ({placeholders})"
        params = [row for row, flag in zip(self._get_rows(), insert_rows) if flag]
        if params:
            sql_db.execute_multiple_queries(query, params, commit=True)
        self._set_ids()

    def update_in_db(self):

        sql_db = self._get_db()

        set_clause = ", ".join([f"{col} = %s" for col in self._table.COLUMN_NAMES])
        query = f"UPDATE {self._table.NAME} SET {set_clause} WHERE {self._table.ID_COLUMN} = %s"
        update_params = [
            list(row) + [id_val]
            for id_val, row in zip(self._ids, self._get_rows())
            if id_val is not None
        ]
        if update_params:
            sql_db.execute_multiple_queries(query, update_params, commit=True)
        insert_rows = [id_val is None for id_val in self._ids]
        self.insert_into_db(insert_rows)
        self._set_ids()
