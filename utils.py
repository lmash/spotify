import pickle

import pandas as pd

from config import DATA_PATH


def chunked(sequence, n):
    """Returns an iterator which produces chunks from the sequence of size n."""
    chunk = []

    for index, item in enumerate(sequence):
        chunk.append(item)

        if (index + 1) % n == 0:
            yield chunk
            chunk = []

    if chunk:
        yield chunk


def read_pickle_df(filename: str) -> pd.DataFrame:
    return pd.read_pickle(DATA_PATH / f'{filename}')


def to_pickle_df(df: pd.DataFrame, filename: str):
    df.to_pickle(DATA_PATH / f'{filename}')


def read_pickle(filename: str):
    with open(DATA_PATH / f'{filename}', 'rb') as fh:
        return pickle.load(fh)


def to_pickle(obj_to_pickle, filename: str):
    with open(DATA_PATH / f'{filename}', 'wb') as fh:
        pickle.dump(obj_to_pickle, fh)
