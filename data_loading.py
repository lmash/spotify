import logging

import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:

    def __init__(self):
        pass

    @staticmethod
    def pickle(df: pd.DataFrame, name: str):
        df.to_pickle(f'data/in_progress/{name}')

    @staticmethod
    def read_pickle(name: str) -> pd.DataFrame:
        return pd.read_pickle(f'data/in_progress/{name}')
