import numpy as np
import pandas as pd
import pytest

from data_cleaning import DataCleaner


@pytest.fixture
def data_cleaner():
    """Returns a DataCleaning instance for Music"""
    return DataCleaner()


def test_isrc_extracted_from_xid_where_populated(data_cleaner):
    """Test function _set_isrc extracts ISRC from xid when it exists"""
    df = pd.DataFrame(data=[['Universal:isrc:SEYBD0800402'], [np.nan]], columns=['xid'])
    cleaned_df = data_cleaner._set_isrc(df)
    assert cleaned_df["isrc"][0] == 'SEYBD0800402'


def test_single_quote_workaround(data_cleaner):
    """Test function _single_quote_workaround replaces single quotes in tracks where no isrc"""
    df = pd.DataFrame(
        data=[['SEYBD0800402', "No replacement'"],
              [np.nan, "replacement''"]],
        columns=['isrc', 'track_name']
    )
    cleaned_df = data_cleaner._single_quote_workaround(df)
    assert cleaned_df["track_name"][0] == "No replacement'"
    assert cleaned_df["track_name"][1] == "replacement"
