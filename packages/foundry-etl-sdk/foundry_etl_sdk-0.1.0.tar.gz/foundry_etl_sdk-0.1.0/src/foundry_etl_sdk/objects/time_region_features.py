from .regions import Regions
from .dates import Dates
from .company import Company
from .table_manager import BaseSingleRowManager, BaseMultiRowManager


from foundry_db.tables.time_region_features_description import TimeRegionFeaturesDescriptionTable
from foundry_db.tables.time_region_features_company import TimeRegionFeaturesCompanyTable
from foundry_db.tables.time_region_features import TimeRegionFeaturesTable
from foundry_db.tables.regions import RegionsTable

from foundry_db.sdk import SQLDatabase


class TimeRegions:
    MISSING_VALUE: int = 0


class TimeRegionFeatureDescription(BaseSingleRowManager):
    """
    Represents a description of time-region features.

    Attributes
    ----------
    name : str
        The name of the feature.
    description : str
        A brief description of the feature.
    """

    def __init__(self, name: str, description: str, db: SQLDatabase):
        """
        Initializes a TimeRegionDescription instance.

        Parameters
        ----------
        name : str
            The name of the time-region feature.
        description : str
            A description of the feature.
        """
        super().__init__(
            TimeRegionFeaturesDescriptionTable,
            [name, description],
            db,
        )


class TimeRegionCompany(BaseSingleRowManager):
    """
    Represents time-region features for a company.
    """

    def __init__(
        self,
        company: Company,
        time_region_description: TimeRegionFeatureDescription,
        db: SQLDatabase,
    ):

        trf_id = time_region_description.get_id()
        cmp_id = company.get_id()

        super().__init__(
            TimeRegionFeaturesCompanyTable,
            [trf_id, cmp_id],
            db,
        )


class TimeRegionFeatures(BaseMultiRowManager):
    """
    Represents time-region features.
    """

    def __init__(
        self,
        dates: Dates,
        time_region_description: TimeRegionFeatureDescription,
        regions: Regions,
        feature_values_map: dict,
        db: SQLDatabase,
    ):
        trf_id = time_region_description.get_id()

        rows = []

        region_df = regions.get_df().set_index(
            RegionsTable.ABBREVIATION_COLUMN, drop=False
        )
        region_ids = regions.get_ids(region_df.values.tolist())

        region_abbrs = region_df[RegionsTable.ABBREVIATION_COLUMN].tolist()

        rows = [
            (
                trf_id,
                date_id,
                region_id,
                feature_values_map.get((region, date), TimeRegions.MISSING_VALUE),
            )
            for date, date_id in zip(dates.get_date_range(), dates.get_ids())
            for region_id, region in zip(region_ids, region_abbrs)
        ]
        super().__init__(TimeRegionFeaturesTable, rows, db)
