from foundry_db.sdk import SQLDatabase
from ..enums import InsertionMode, InsertionModeFactory


class DatabaseManager:
    """Handles database connection and insertion mode creation."""

    @staticmethod
    def get_sql_database() -> SQLDatabase:
        """Create and return a SQLDatabase instance.

        Returns:
            SQLDatabase: A new database connection object.
        """
        return SQLDatabase()

    @staticmethod
    def get_insertion_mode(description: str) -> InsertionMode:
        """Build and return an insertion mode based on the description.

        Args:
            description (str): The description for the insertion mode.

        Returns:
            InsertionMode: The resulting insertion mode.
        """
        return InsertionModeFactory.build(description)
