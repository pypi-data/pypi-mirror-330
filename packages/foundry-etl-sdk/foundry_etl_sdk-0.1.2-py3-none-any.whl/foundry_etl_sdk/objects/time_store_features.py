from .dates import Dates
from .stores import Stores

from .table_manager import BaseSingleRowManager, BaseMultiRowManager

from foundry_db.tables.stores import StoresTable
from foundry_db.tables.time_store_features_description import TimeStoreFeaturesDescriptionTable
from foundry_db.tables.time_store_features import TimeStoreFeaturesTable

from foundry_db.sdk import SQLDatabase


class TimeStoreFeatureDescription(BaseSingleRowManager):
    """
    Represents a description of time-store features.

    Attributes
    ----------
    name : str
        The name of the feature.
    description : str
        A brief description of the feature.
    """

    def __init__(self, name: str, description: str, db: SQLDatabase):
        """
        Initializes a TimeStoreFeaturesDescription instance.

        Parameters
        ----------
        name : str
            The name of the time-store feature.
        description : str
            A description of the feature.
        """

        super().__init__(
            TimeStoreFeaturesDescriptionTable,
            [name, description],
            db,
        )


class FeatureValuesListFactory:
    """
    Factory class for building a list of feature values.
    """

    @staticmethod
    def build(stores: Stores, dates: Dates, feature_values_map: dict) -> list:
        """
        Builds a feature values list by mapping store names and dates to their corresponding feature values.

        Parameters
        ----------
        stores : Stores
            An instance containing store information.
        dates : Dates
            An instance containing date information.
        feature_values_map : dict
            A dictionary mapping (store_name, date) to a feature value.

        Returns
        -------
        list
            A list of feature values ordered by store and date.
        """
        feature_values_list = []

        for store_name in stores.get_names():
            for date in dates.get_date_range():
                feauture_value = feature_values_map.get((store_name, date), 0)
                feature_values_list.append(feauture_value)

        return feature_values_list


class TimeStoreFeatures(BaseMultiRowManager):
    """
    Manages time-store features by storing feature values for each store and date combination.
    """

    def __init__(
        self,
        stores: Stores,
        dates: Dates,
        time_store_features_description: TimeStoreFeatureDescription,
        feature_values_map: dict,
    ):
        """
        Initializes a TimeStoreFeatures instance.

        Parameters
        ----------
        stores : Stores
            An instance containing store information.
        dates : Dates
            An instance containing date information.
        time_store_features_description : TimeStoreFeaturesDescription
            The description of the time-store feature.
        feature_values_map : dict
            A dictionary mapping (store_name, date) to a feature value.
        """
        rows = []

        tsfid = time_store_features_description.get_id()

        stores_names = stores.get_df()[StoresTable.NAME_COLUMN].values
        store_ids = stores.get_ids()

        for date, date_id in zip(dates.get_date_range(), dates.get_ids()):

            for store, store_id in zip(stores_names, store_ids):

                feature_value = feature_values_map.get((store, date), 0)

                rows.append((date_id, store_id, tsfid, feature_value))

        super().__init__(TimeStoreFeaturesTable, rows)
