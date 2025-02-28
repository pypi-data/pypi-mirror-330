from .table_manager import BaseMultiRowManager
from .categories import Category
from .company import Company
import pandas as pd

from foundry_db.tables.products import ProductsTable
from foundry_db.tables.product_categories import ProductCategoriesTable

from foundry_db.sdk import SQLDatabase


class Products(BaseMultiRowManager):
    """
    Class to represent a product
    """

    def __init__(self, names: list, company: Company, db: SQLDatabase):
        """
        Initialize Products object

        Args:

        names: str
            Names of the products
        """

        cmp_id = company.get_id()

        rows = [[name, cmp_id] for name in names]

        super().__init__(ProductsTable, rows, db)


class ProductCategories(BaseMultiRowManager):
    """
    Class to represent a product category
    """

    def __init__(
        self, products: Products, categories: list[Category] | Category, db: SQLDatabase
    ):
        """
        Initialize ProductCategories object

        Args:

        products: Products
            Products object
        categories: list[Category] | Category
            List of Category objects or a single Category
        """

        if isinstance(categories, Category):
            category_ids = [categories.get_id()] * len(products)
        else:
            category_ids = [category.get_id() for category in categories]

        product_ids = products.get_ids()

        product_category_df = pd.DataFrame(
            data=list(zip(product_ids, category_ids)),
            columns=["productID", "categoryID"],
        )

        rows = product_category_df.values.tolist()

        super().__init__(ProductCategoriesTable, rows, db)
