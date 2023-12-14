from dataclasses import dataclass
import logging

import pandas as pd

logger = logging.getLogger(__name__)


class DataReporter:
    """
    A class to report
    """

    def __init__(self):
        self.num_album = SuccessFailureCount

    def albums(self, df:pd.DataFrame):
        success_mask = ((df["spotify_add_album"] == True) & ~df["spotify_album_uri"].isna())
        self.num_album.success = df[success_mask]["spotify_search_album"].nunique()
        logger.info(f"Albums successfully requested {self.num_album.success}")

        fail_mask = ((df["spotify_add_album"] == True) & df["spotify_album_uri"].isna())
        self.num_album.failure = df[fail_mask]["spotify_search_album"].nunique()
        logger.info(f"Albums Failed requested {self.num_album.failure}")


@dataclass
class SuccessFailureCount:
    success: int = 0
    failure: int = 0
