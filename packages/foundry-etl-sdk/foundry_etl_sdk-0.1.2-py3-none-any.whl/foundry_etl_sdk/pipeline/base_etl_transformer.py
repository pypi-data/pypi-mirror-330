from ..objects import Dates, Regions
from abc import ABC

class BaseETLTransformer(ABC):
    """Abstract base transformer with stub implementations returning empty objects.
    
    This class serves as a template for ETL transformers, providing method stubs
    that should be overridden by subclasses. The methods return empty objects
    as placeholders for actual data transformations.
    """

    def get_dates(self) -> Dates:
        """Retrieve date-related data.
        
        Returns:
            Dates: An object representing the date range for the dataset.
        """
        return {}

    def get_time_store_feature_map(self) -> dict:
        """Construct a mapping of time-store features.
        
        Returns:
            dict: A dictionary where:
                - Keys are tuples of (store_id: str, date: str in YYYY-MM-DD format).
                - Values are another dictionary mapping feature names (str) to feature values (float or int).
                Example:
                {
                    ("store_1", "2023-01-01"): {"temperature": 15.2, "rain": 0.0},
                    ("store_2", "2023-01-02"): {"temperature": 18.5, "rain": 1.2}
                }
        """
        return {}

    def get_time_store_feature_description_map(self) -> dict:
        """Provide descriptions for time-store features.
        
        Returns:
            dict: A dictionary mapping feature names (str) to human-readable descriptions (str).
                Example:
                {
                    "temperature": "Average temperature in Celsius",
                    "rain": "Total precipitation in mm"
                }
        """
        return {}

    def get_time_region_feature_map(self, dates: Dates) -> dict:
        """Generate a mapping of time-region features.
        
        Args:
            dates (Dates): A Dates object containing the date range.
        
        Returns:
            dict: A dictionary where:
                - Keys are tuples of (region: str, date: str in YYYY-MM-DD format).
                - Values are dictionaries mapping feature names to values.
                Example:
                {
                    ("region_1", "2023-01-01"): {"public_holiday": 1},
                    ("region_2", "2023-01-02"): {"public_holiday": 0}
                }
        """
        return {}

    def get_time_region_feature_description_map(self) -> dict:
        """Provide descriptions for time-region features.
        
        Returns:
            dict: A dictionary mapping feature names (str) to descriptions (str).
                Example:
                {
                    "public_holiday": "Indicates if the date is a public holiday (1: Yes, 0: No)"
                }
        """
        return {}

    def get_not_for_sales_map(self, dates: Dates) -> dict:
        """Identify dates when products were not available for sale.
        
        Args:
            dates (Dates): A Dates object containing the full date range.
        
        Returns:
            dict: A mapping where:
                - Keys are tuples of (product_id: str, store_id: str).
                - Values are lists of strings representing dates (YYYY-MM-DD) when the product was unavailable.
                Example:
                {
                    ("product_1", "store_1"): ["2023-01-01", "2023-01-05"],
                    ("product_2", "store_2"): ["2023-01-02"]
                }
        """
        return {}

    def get_store_region_map(self) -> dict:
        """Generate a mapping of stores to their corresponding regions.
        
        Returns:
            dict: A dictionary where:
                - Keys are store identifiers (str).
                - Values are corresponding region identifiers (str).
                Example:
                {
                    "store_1": "region_1",
                    "store_2": "region_2"
                }
        """
        return {}

    def get_product_names(self):
        """Retrieve the list of available product names.
        
        Returns:
            list: A list of product identifiers (str).
                Example:
                ["product_1", "product_2", "product_3"]
        """
        return {}

    def get_price_discounts_map(self) -> dict:
        """Generate a mapping of product price discounts.
        
        Returns:
            dict: A dictionary where:
                - Keys are tuples of (product_id: str, store_id: str, date: str in YYYY-MM-DD format).
                - Values are discount percentages as float values.
                Example:
                {
                    ("product_1", "store_1", "2023-01-01"): 10.0,
                    ("product_2", "store_2", "2023-01-02"): 5.0
                }
        """
        return {}

    def get_sales_map(self) -> dict:
        """Generate a mapping of sales data.
        
        Returns:
            dict: A dictionary where:
                - Keys are tuples of (date: str in YYYY-MM-DD format, store_id: str, product_id: str).
                - Values are integers representing the sales count.
                Example:
                {
                    ("2023-01-01", "store_1", "product_1"): 100,
                    ("2023-01-02", "store_2", "product_2"): 50
                }
        """
        return {}

    def get_regions(self) -> Regions:
        """Retrieve the set of regions associated with the dataset.
        
        Returns:
            Regions: A Regions object representing geographical regions in the dataset.
        """
        return {}
