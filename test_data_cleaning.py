import numpy as np
import pandas as pd
import pytest

from data_cleaning import DataCleaner


@pytest.fixture
def music_cleaner():
    """Returns a DataCleaning instance for Music"""
    return DataCleaner()


def test_isrc_extracted_from_xid_where_populated(music_cleaner):
    """Test function _set_isrc extracts ISRC from xid when it exists"""
    df = pd.DataFrame(data=[['Universal:isrc:SEYBD0800402']], columns=['xid'])
    cleaned_df = music_cleaner._set_isrc(df)
    assert cleaned_df["isrc"][0] == 'SEYBD0800402'


def test_isrc_ignores_where_not_populated(music_cleaner):
    """Test function _set_isrc adds column isrc when there are no values in xid"""
    df = pd.DataFrame(data=[[np.nan]], columns=['xid'])
    cleaned_df = music_cleaner._set_isrc(df)
    assert "isrc" in cleaned_df.columns
