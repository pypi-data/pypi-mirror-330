from .table_manager import BaseSingleRowManager
from .company import Company

from foundry_db.sdk import SQLDatabase
from foundry_db.tables.category import CategoryTable



# Constant dummy category name
class DUMMY_CATEGORY:
    NAME: str = "Dummy"


class Category(BaseSingleRowManager):
    """
    Class to represent a category
    """

    def __init__(self, name: str, company: Company, db: SQLDatabase):
        """
        Initialize Category object

        Args:

        name: str
            Name of the category
        company: Company
            Company object
        """

        cmp_id = company.get_id()

        super().__init__(CategoryTable, [name, cmp_id], db)


class DummyCategory(Category):
    """
    Class to represent a dummy category
    """

    def __init__(self, company: Company, db: SQLDatabase):
        """
        Initialize DummyCategory object

        Args:

        company: Company
            Company object
        """

        super().__init__(DUMMY_CATEGORY.NAME, company, db)
