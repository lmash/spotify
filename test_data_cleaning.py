import numpy as np
import pandas as pd
import pytest

from config import SpotifyArtist, SpotifyTrackName
from data_cleaning import DataCleaner


@pytest.fixture
def data_cleaner():
    """Returns a DataCleaning instance for Music"""
    return DataCleaner()


def test_isrc_extracted_from_xid_where_populated(data_cleaner):
    """Test function _set_isrc extracts ISRC from xid when it exists"""
    df = pd.DataFrame(data=[["Universal:isrc:SEYBD0800402"], [np.nan]], columns=["xid"])
    cleaned_df = data_cleaner._set_isrc(df)
    assert cleaned_df["isrc"][0] == "SEYBD0800402"


def test_single_quote_in_multiple_fields(data_cleaner):
    """Test function _remove_from_spotify_requests replaces single quotes in
    spotify_search_track_name and spotify_search_artist
    """
    df = pd.DataFrame(
        data=[["Artis't", "'Track Name"], ["Artist", "Track Name"]],
        columns=["spotify_search_artist", "spotify_search_track_name"],
    )
    cleaned_df = data_cleaner._remove_from_spotify_requests(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Track Name"
    assert cleaned_df["spotify_search_track_name"][1] == "Track Name"
    assert cleaned_df["spotify_search_artist"][0] == "Artist"
    assert cleaned_df["spotify_search_artist"][1] == "Artist"


def test_remove_not_applied_where_na(data_cleaner):
    """Test function _remove_from_spotify_requests replaces single quotes in
    spotify_search_track_name and spotify_search_artist
    """
    df = pd.DataFrame(
        data=[[np.nan, "'Track Name"], ["Artist", np.nan]],
        columns=["spotify_search_artist", "spotify_search_track_name"],
    )
    cleaned_df = data_cleaner._remove_from_spotify_requests(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Track Name"
    assert cleaned_df["spotify_search_artist"][1] == "Artist"


def test_remove_backticks_and_single_quote(data_cleaner):
    """Test function _remove_from_spotify_requests replaces backticks in
    spotify_search_track_name
    """
    df = pd.DataFrame(
        data=[["Moby", "I`m In Love"], ["Moby", "I'm In Love"]],
        columns=["spotify_search_artist", "spotify_search_track_name"],
    )
    cleaned_df = data_cleaner._remove_from_spotify_requests(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Im In Love"
    assert cleaned_df["spotify_search_track_name"][1] == "Im In Love"


def test_updating_spotify_artists(data_cleaner):
    """Verify a list of artist updates are applied to spotify_search_artist"""
    artist_updates = [
        SpotifyArtist(
            from_spotify_search_artist="Morcheeba", to_spotify_search_artist="Morch"
        ),
        SpotifyArtist(
            from_spotify_search_artist="Madonna", to_spotify_search_artist="Madoon"
        ),
    ]

    df = pd.DataFrame(
        data=[["Morcheeba"], ["Madonna"]],
        columns=["spotify_search_artist"],
    )
    cleaned_df = data_cleaner._update_spotify_artists(df, artist_updates)
    assert cleaned_df["spotify_search_artist"][0] == "Morch"
    assert cleaned_df["spotify_search_artist"][1] == "Madoon"


def test_updating_spotify_tracks(data_cleaner):
    """Verify a list of track updates are applied to spotify_search_artist"""
    track_updates = [
        SpotifyTrackName(
            meta_artist="Skin",
            from_spotify_search_track_name="Til Morning Comes",
            to_spotify_search_track_name="Til Morning",
        ),
        SpotifyTrackName(
            meta_artist="Suede",
            from_spotify_search_track_name="Pantomine Horse",
            to_spotify_search_track_name="Pantomime Horse",
        ),
    ]
    df = pd.DataFrame(
        data=[["Skin", "Til Morning Comes"], ["Suede", "Pantomine Horse"]],
        columns=["meta_artist", "spotify_search_track_name"],
    )

    cleaned_df = data_cleaner._update_spotify_tracks(df, track_updates)
    assert cleaned_df["spotify_search_track_name"][0] == "Til Morning"
    assert cleaned_df["spotify_search_track_name"][1] == "Pantomime Horse"

