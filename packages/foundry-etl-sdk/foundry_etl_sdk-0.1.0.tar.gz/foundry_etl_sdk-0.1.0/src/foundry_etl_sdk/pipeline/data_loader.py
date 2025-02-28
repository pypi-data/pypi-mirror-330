from ..objects import (
    Company,
    Dates,
    InsertionMode,
    Stores,
    DummyCategory,
    Products,
    ProductCategories,
    SKUs,
    DataPoints,
    PriceDiscounts,
    Sales,
    TimeRegionFeatureDescription,
    TimeRegionCompany,
    TimeRegionFeatures,
    Regions,
    TimeStoreFeatureDescription,
    TimeStoreFeatures,
    NotForSaleFlag,
)

from foundry_db.sdk import SQLDatabase

from functools import wraps

import logging

SKIPPED_EXECUTION = "SKIPPED"


def skip_if_empty(func):
    """Decorator to skip function execution if any argument is None or empty."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args[1:]:  # Skipping 'self'
            if arg is None or (hasattr(arg, "__len__") and len(arg) == 0):
                logging.warning(
                    f"Skipping function {func.__name__} due to empty argument {arg}"
                )
                return SKIPPED_EXECUTION
        for arg in kwargs.values():
            if arg is None or (hasattr(arg, "__len__") and len(arg) == 0):
                logging.warning(
                    f"Skipping function {func.__name__} due to empty argument {arg}"
                )
                return SKIPPED_EXECUTION
        return func(*args, **kwargs)

    return wrapper


class DataLoader:
    """Handles loading of data into the database using the write_* methods."""

    def __init__(self, db: SQLDatabase, insertion_mode: InsertionMode):
        """
        Args:
            db (SQLDatabase): Database connection object.
            insertion_mode (InsertionMode): Mode for database insertion.
        """
        self.db = db
        self.insertion_mode = insertion_mode

    @skip_if_empty
    def write_company(self, name: str, dataset_type: str, description: str) -> Company:
        """Create and write a company to the database.

        Args:
            name (str): Company name.
            dataset_type (str): Dataset type.
            description (str): Company description.

        Returns:
            Company: The created company.
        """
        company = Company(name, dataset_type, description, self.db)
        company.write_to_db(self.insertion_mode)
        return company

    @skip_if_empty
    def write_stores(
        self, store_region_map: dict, regions: Regions, company: Company
    ) -> Stores:
        """Create and write store entries to the database.

        Args:
            store_region_map (dict): Mapping of store identifiers to regions.
            regions (Regions): Regions object.
            company (Company): Company object.

        Returns:
            Stores: The created Stores object.
        """
        stores = Stores(store_region_map, regions, company, self.db)
        stores.write_to_db(self.insertion_mode)
        return stores

    @skip_if_empty
    def write_categories(self, company: Company) -> DummyCategory:
        """Create and write a dummy product category.

        Args:
            company (Company): Company object.

        Returns:
            DummyCategory: The created dummy category.
        """
        dummy_category = DummyCategory(company, self.db)
        dummy_category.write_to_db(self.insertion_mode)
        return dummy_category

    @skip_if_empty
    def write_products(self, product_names: list, company: Company) -> Products:
        """Create and write product entries.

        Args:
            product_names (list): List of product identifiers.
            company (Company): Company object.

        Returns:
            Products: The created Products object.
        """
        products = Products(product_names, company, self.db)
        products.write_to_db(self.insertion_mode)
        return products

    @skip_if_empty
    def write_product_categories(
        self, products: Products, dummy_category: DummyCategory
    ) -> ProductCategories:
        """Link products to a category and write associations.

        Args:
            products (Products): Products object.
            dummy_category (DummyCategory): Dummy category object.

        Returns:
            ProductCategories: The created associations.
        """
        product_categories = ProductCategories(products, dummy_category, self.db)
        product_categories.write_to_db(self.insertion_mode)
        return product_categories

    @skip_if_empty
    def write_skus(self, products: Products, stores: Stores) -> SKUs:
        """Create and write SKU entries.

        Args:
            products (Products): Products object.
            stores (Stores): Stores object.

        Returns:
            SKUs: The created SKUs object.
        """
        skus = SKUs(products, stores, None, self.db)
        skus.write_to_db(self.insertion_mode)
        return skus

    @skip_if_empty
    def write_data_points(self, skus: SKUs, dates: Dates) -> DataPoints:
        """Create and write data point entries.

        Args:
            skus (SKUs): SKUs object.
            dates (Dates): Dates object.

        Returns:
            DataPoints: The created DataPoints object.
        """
        data_points = DataPoints(skus, dates, self.db)
        data_points.write_to_db(self.insertion_mode)
        return data_points

    @skip_if_empty
    def write_price_discounts(
        self,
        price_discounts_map: dict,
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
    ) -> PriceDiscounts:
        """Create and write price discount entries.

        Args:
            price_discounts_map (dict): Mapping of (date, shop, product) to promotion flag.
            products (Products): Products object.
            stores (Stores): Stores object.
            skus (SKUs): SKUs object.
            dates (Dates): Dates object.
            data_points (DataPoints): DataPoints object.

        Returns:
            PriceDiscounts: The created PriceDiscounts object.
        """
        price_discounts = PriceDiscounts(
            products, stores, skus, dates, data_points, price_discounts_map, self.db
        )
        price_discounts.write_to_db(self.insertion_mode)
        return price_discounts

    @skip_if_empty
    def write_sales(
        self,
        sales_map: dict,
        products: Products,
        stores: Stores,
        skus: SKUs,
        dates: Dates,
        data_points: DataPoints,
    ) -> Sales:
        """Create and write sales entries.

        Args:
            sales_map (dict): Mapping of (date, shop, product) to sales demand.
            products (Products): Products object.
            stores (Stores): Stores object.
            skus (SKUs): SKUs object.
            dates (Dates): Dates object.
            data_points (DataPoints): DataPoints object.

        Returns:
            Sales: The created Sales object.
        """
        sales = Sales(products, stores, skus, dates, data_points, sales_map, self.db)
        sales.write_to_db(self.insertion_mode)
        return sales

    @skip_if_empty
    def write_time_region_features(
        self,
        feature_map: dict,
        feature_description_map: dict,
        dates: Dates,
        company: Company,
        regions: Regions,
    ) -> list:
        """Create and write time-region features.

        Args:
            feature_map (dict): Mapping of (region, date) to holiday feature values.
            feature_description_map (dict): Mapping of holiday feature names to descriptions.
            dates (Dates): Dates object.
            company (Company): Company object.
            regions (Regions): Regions object.

        Returns:
            list: List of TimeRegionFeatures objects.
        """
        features = []
        for feature_name, description in feature_description_map.items():
            mapped_features = {
                date: feature_map[date][feature_name] for date in feature_map
            }
            feature_description = TimeRegionFeatureDescription(
                feature_name, description, self.db
            )
            feature_description.write_to_db(self.insertion_mode)
            time_region_company = TimeRegionCompany(
                company, feature_description, self.db
            )
            time_region_company.write_to_db(self.insertion_mode)
            feature = TimeRegionFeatures(
                dates, feature_description, regions, mapped_features, self.db
            )
            feature.write_to_db(self.insertion_mode)
            features.append(feature)
        return features

    @skip_if_empty
    def write_time_store_features(
        self,
        feature_map: dict,
        feature_description_map: dict,
        stores: Stores,
        dates: Dates,
    ) -> list:
        """Create and write time-store features.

        Args:
            feature_map (dict): Mapping of (date, store) to weather feature values.
            feature_description_map (dict): Mapping of weather feature names to descriptions.
            stores (Stores): Stores object.
            dates (Dates): Dates object.

        Returns:
            list: List of TimeStoreFeatures objects.
        """
        features = []
        for feature_name, description in feature_description_map.items():
            mapped_features = {
                (store, date): feature_map[(date, store)][feature_name]
                for (date, store) in feature_map
            }
            feature_description = TimeStoreFeatureDescription(
                feature_name, description, self.db
            )
            feature_description.write_to_db(self.insertion_mode)
            feature = TimeStoreFeatures(
                stores, dates, feature_description, mapped_features
            )
            feature.write_to_db(self.insertion_mode)
            features.append(feature)
        return features

    @skip_if_empty
    def write_not_for_sales_flag(
        self,
        data_points: DataPoints,
        dates: Dates,
        skus: SKUs,
        products: Products,
        stores: Stores,
        not_for_sales_map: dict,
    ) -> NotForSaleFlag:
        """Create and write not-for-sales flag entries.

        Args:
            data_points (DataPoints): DataPoints object.
            dates (Dates): Dates object.
            skus (SKUs): SKUs object.
            products (Products): Products object.
            stores (Stores): Stores object.
            not_for_sales_map (dict): Mapping of (product, store) to list of unsold dates.

        Returns:
            NotForSaleFlag: The created flag object.
        """
        not_for_sales_flag = NotForSaleFlag(
            data_points, dates, skus, products, stores, not_for_sales_map, self.db
        )
        not_for_sales_flag.write_to_db(self.insertion_mode)
        return not_for_sales_flag
