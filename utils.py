import pathlib
import pickle

import pandas as pd

import config


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
    return pd.read_pickle(config.CHECKPOINTS_PATH / f'{filename}')


def to_pickle_df(df: pd.DataFrame, filename: str):
    df.to_pickle(config.CHECKPOINTS_PATH / f'{filename}')


def read_pickle(filename: str):
    with open(config.HISTORY_PATH / f'{filename}', 'rb') as fh:
        return pickle.load(fh)


def to_pickle(obj_to_pickle, filename: str):
    with open(config.HISTORY_PATH / f'{filename}', 'wb') as fh:
        pickle.dump(obj_to_pickle, fh)


def create_folder_structure():
    paths = (config.HISTORY_PATH, config.ITUNES_PATH, config.PLAYLIST_PATH, config.CHECKPOINTS_PATH, config.EXTERNAL_PATH)

    for path in paths:
        pathlib.Path(path).mkdir(exist_ok=True)
