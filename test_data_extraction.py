import numpy as np
import pandas as pd
import pytest

from data_extraction import DataExtractor


@pytest.fixture
def data_extractor():
    """Returns a DataExtractor instance for Music"""
    return DataExtractor()


def test_extract_isrc(data_extractor):
    """Test function _set_isrc extracts ISRC from xid when it exists"""
    df = pd.DataFrame(data=[['Universal:isrc:SEYBD0800402'], [np.nan]], columns=['xid'])
    cleaned_df = data_extractor._set_isrc(df)
    assert cleaned_df["isrc"][0] == 'SEYBD0800402'
