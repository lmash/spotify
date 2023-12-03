import logging
from typing import List

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:

    def __init__(self, spotify):
        self.spotify = spotify

    @staticmethod
    def pickle(df: pd.DataFrame, name: str):
        df.to_pickle(f'data/in_progress/{name}')

    def add_tracks_to_spotify(self, tracks: List):
        self.spotify.current_user_saved_tracks_add(tracks=tracks)
