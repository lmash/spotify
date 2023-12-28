from dataclasses import dataclass
import logging

import pandas as pd

from config import CHECKPOINTS_PATH, HISTORY_PATH

logger = logging.getLogger(__name__)


class DataReporter:
    """
    A class to report
    """

    def __init__(self):
        self.num_album = SuccessFailureCount

    def albums(self, df: pd.DataFrame):
        success_mask = (df["spotify_add_album"] == True) & ~df[
            "spotify_album_uri"
        ].isna()
        self.num_album.success = df[success_mask]["spotify_search_album"].nunique()
        logger.info(f"Albums successfully requested {self.num_album.success}")

        fail_mask = (df["spotify_add_album"] == True) & df["spotify_album_uri"].isna()
        self.num_album.failure = df[fail_mask]["spotify_search_album"].nunique()
        logger.info(f"Albums Failed requested {self.num_album.failure}")

        albums_failed = HISTORY_PATH / "albums_failed_detailed.csv"
        df_failed = df[fail_mask]
        df_failed.to_csv(albums_failed)
        logger.info(f"Albums failed written to {albums_failed}")

        albums_summary = HISTORY_PATH / "albums_failed_summary.csv"
        df_summary = df_failed.groupby("spotify_search_album")[
            "spotify_search_artist"
        ].count()
        df_summary.to_csv(albums_summary)
        logger.info(f"Albums failed summary written to {albums_summary}")

    @staticmethod
    def playlists(df_playlist: pd.DataFrame):
        """Write failed playlist track requests to a .csv file"""
        playlists_failed = HISTORY_PATH / "playlists_failed.csv"
        missing_tracks_on_playlists = df_playlist[
            df_playlist["spotify_track_uri"].isna()
        ]
        missing_tracks_on_playlists.to_csv(playlists_failed)
        logger.info(f"Playlist tracks failed written to {playlists_failed}")

    @staticmethod
    def tracks(df):
        """Write failed track requests to a .csv file"""
        tracks_failed = HISTORY_PATH / "tracks_failed.csv"
        requested_albums = df[
            ((df["spotify_add_album"] == True) & ~df["spotify_album_uri"].isna())
        ]
        tracks_only = pd.concat([df, requested_albums]).drop_duplicates(keep=False)
        missing_tracks = tracks_only[tracks_only["spotify_track_uri"].isna()]
        missing_tracks.to_csv(tracks_failed)
        logger.info(f"Tracks failed written to {tracks_failed}")


@dataclass
class SuccessFailureCount:
    success: int = 0
    failure: int = 0
