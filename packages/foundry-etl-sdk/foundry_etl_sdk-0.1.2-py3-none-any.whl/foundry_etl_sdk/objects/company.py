from .table_manager import BaseSingleRowManager
from foundry_db.tables.company import CompanyTable

from foundry_db.sdk import SQLDatabase


class Company(BaseSingleRowManager):
    """
    Class to represent a company

    Attributes:

    name: str
        Name of the company
    table_name: str
        Name of the table (company)
    column: str
        Type of dataset
    """

    def __init__(self, name, dataset_type, description, db: SQLDatabase):
        """
        Initialize Company object

        Args:

        name: str
            Name of the company
        dataset_type: str
            Type of dataset
        description: str
            Description of the company
        """

        row = [name, dataset_type, description]

        super().__init__(CompanyTable, row, db)
