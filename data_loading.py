import logging
from typing import List

import pandas as pd

from utils import chunked

logger = logging.getLogger(__name__)


class DataLoader:

    def __init__(self, spotify):
        self.spotify = spotify

    @staticmethod
    def pickle(df: pd.DataFrame, name: str):
        df.to_pickle(f'data/in_progress/{name}')

    def add_tracks_to_spotify(self, tracks: List):
        self.spotify.current_user_saved_tracks_add(tracks=tracks)

    def add_albums_to_spotify(self, df: pd.DataFrame, size=5):
        """Add the albums in lists broken into chunks"""
        exclude_na = ~df['spotify_album_uri'].isna()
        albums = df.loc[exclude_na, "spotify_album_uri"].unique().tolist()
        chunks = chunked(albums, size)

        for chunk in chunks:
            logger.debug(f"Adding list of album to spotify with uri's: {chunk}")
            self.spotify.current_user_saved_albums_add(albums=chunk)

    def remove_albums_from_spotify(self, df: pd.DataFrame, size=5):
        exclude_na = ~df['spotify_album_uri'].isna()
        albums = df.loc[exclude_na, "spotify_album_uri"].unique().tolist()
        chunks = chunked(albums, size)

        for chunk in chunks:
            logger.debug(f"Deleting list of album to spotify with uri's: {chunk}")
            self.spotify.current_user_saved_albums_delete(albums=chunk)
