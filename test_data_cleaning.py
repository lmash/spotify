import numpy as np
import pandas as pd
import pytest

from config import (
    SpotifyArtist,
    SpotifyTrackName,
    SpotifyTrackNameByContentId,
    SpotifyAlbum,
)
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
        data=[["Artis't", "'Track Name", "Album"], ["Artist", "Track Name", "Album"]],
        columns=["spotify_search_artist", "spotify_search_track_name", "spotify_search_album"],
    )
    cleaned_df = data_cleaner._remove_characters(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Track Name"
    assert cleaned_df["spotify_search_track_name"][1] == "Track Name"
    assert cleaned_df["spotify_search_artist"][0] == "Artist"
    assert cleaned_df["spotify_search_artist"][1] == "Artist"


def test_remove_not_applied_where_na(data_cleaner):
    """Test function _remove_from_spotify_requests replaces single quotes in
    spotify_search_track_name and spotify_search_artist
    """
    df = pd.DataFrame(
        data=[[np.nan, "'Track Name", np.nan], ["Artist", np.nan, np.nan]],
        columns=["spotify_search_artist", "spotify_search_track_name", "spotify_search_album"],
    )
    cleaned_df = data_cleaner._remove_characters(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Track Name"
    assert cleaned_df["spotify_search_artist"][1] == "Artist"


def test_remove_backticks_and_single_quote(data_cleaner):
    """Test function _remove_from_spotify_requests replaces backticks in
    spotify_search_track_name
    """
    df = pd.DataFrame(
        data=[["Moby", "I`m In Love", ""], ["Moby", "I'm In Love", ""]],
        columns=["spotify_search_artist", "spotify_search_track_name", "spotify_search_album"],
    )
    cleaned_df = data_cleaner._remove_characters(df)
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
            artist="Skin",
            from_spotify_search_track_name="Til Morning Comes",
            to_spotify_search_track_name="Til Morning",
        ),
        SpotifyTrackName(
            artist="Suede",
            from_spotify_search_track_name="Pantomine Horse",
            to_spotify_search_track_name="Pantomime Horse",
        ),
    ]
    df = pd.DataFrame(
        data=[["Skin", "Til Morning Comes"], ["Suede", "Pantomine Horse"]],
        columns=["artist", "spotify_search_track_name"],
    )

    cleaned_df = data_cleaner._update_spotify_tracks(df, track_updates)
    assert cleaned_df["spotify_search_track_name"][0] == "Til Morning"
    assert cleaned_df["spotify_search_track_name"][1] == "Pantomime Horse"


def test_updating_spotify_tracks_by_content_id(data_cleaner):
    """Verify a list of track updates by content_id are applied to spotify_search_artist"""
    track_updates = [
        SpotifyTrackNameByContentId(
            content_id="1485137457",
            to_spotify_search_track_name="The Last Time",
        ),
        SpotifyTrackNameByContentId(
            content_id="724357853",
            to_spotify_search_track_name="The Big Ship",
        ),
    ]
    df = pd.DataFrame(
        data=[["1485137457", np.nan], ["724357853", np.nan]],
        columns=["content_id", "spotify_search_track_name"],
    )

    cleaned_df = data_cleaner._update_spotify_tracks_by_content_id(
        df, track_updates=track_updates
    )
    assert cleaned_df["spotify_search_track_name"][0] == "The Last Time"
    assert cleaned_df["spotify_search_track_name"][1] == "The Big Ship"


def test_split_artist_by_delimiters(data_cleaner):
    df = pd.DataFrame(
        data=[
            ["George Michael With Queen", np.nan],
            ["Jack Savoretti & Alexander Brown", np.nan],
        ],
        columns=["spotify_search_artist", "isrc"],
    )
    cleaned_df = data_cleaner._split_artists_keep_first_only(df)
    assert cleaned_df["spotify_search_artist"][0] == "George Michael"
    assert cleaned_df["spotify_search_artist"][1] == "Jack Savoretti"


def test_updating_spotify_albums(data_cleaner):
    """Verify a list of album updates are applied to spotify_search_album"""
    album_updates = [
        SpotifyAlbum(
            from_spotify_search_album="Coco Part 1",
            to_spotify_search_album="Coco, Pt. 1",
        ),
        SpotifyAlbum(
            from_spotify_search_album="Coco Part 2",
            to_spotify_search_album="Coco, Pt. 2",
        ),
    ]
    df = pd.DataFrame(
        data=[["Coco Part 2"], ["Coco Part 1"]],
        columns=["spotify_search_album"],
    )

    cleaned_df = data_cleaner._update_spotify_albums(df, album_updates)
    assert cleaned_df["spotify_search_album"][0] == "Coco, Pt. 2"
    assert cleaned_df["spotify_search_album"][1] == "Coco, Pt. 1"


def test_set_spotify_release_year(data_cleaner):
    """"""
    df = pd.DataFrame(
        data=[["2015-04-17T12:00:00Z", np.nan], [np.nan, np.nan], ["2019", "2019"]],
        columns=["release_date", "spotify_release_year"],
    )
    cleaned_df = data_cleaner._set_spotify_release_year(df)
    assert cleaned_df["spotify_release_year"][0] == "2015"
    assert cleaned_df["spotify_release_year"][2] == "2019"


def test_clean_brackets(data_cleaner):
    df = pd.DataFrame(
        data=[["Suede [track]", np.nan], ["Pink (track )", np.nan]],
        columns=["spotify_search_track_name", "isrc"],
    )
    cleaned_df = data_cleaner._clean_brackets_from_spotify_search_fields(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Suede"
    assert cleaned_df["spotify_search_track_name"][1] == "Pink"


def test_clean_brackets_exits_where_all_isrc_populated(data_cleaner):
    df = pd.DataFrame(
        data=[["Suede", "Suede [Disc 1]", "1234"], ["Pink [", "Pink ]", "567"]],
        columns=["spotify_search_track_name", "spotify_search_album", "isrc"],
    )
    cleaned_df = data_cleaner._clean_brackets_from_spotify_search_fields(df)
    assert cleaned_df["spotify_search_track_name"][0] == "Suede"


def test_clean_brackets_spotify_search_album(data_cleaner):
    df = pd.DataFrame(
        data=[
            ["Suede [track]", "Suede [Disc 1]", "123"],
            ["Pink [", "Pink (disc 3245)", np.nan],
        ],
        columns=["spotify_search_track_name", "spotify_search_album", "isrc"],
    )
    cleaned_df = data_cleaner._clean_brackets_from_spotify_search_album(df)
    assert cleaned_df["spotify_search_album"][0] == "Suede"
    assert cleaned_df["spotify_search_album"][1] == "Pink"


def test_album_added_when_library_tracks_equals_spotify_tracks(data_cleaner):
    df = pd.DataFrame(
        data=[
            ["The Princess: The Vinyl Collection 2010 - 2012", "The Vamp", 2],
            ["The Princess: The Vinyl Collection 2010 - 2012", "Jimmys Gang", 2],
        ],
        columns=["spotify_search_album", "track_name", "spotify_total_tracks"],
    )
    cleaned_df = data_cleaner._should_add_album(df)
    assert cleaned_df["spotify_add_album"][0] == True


def test_album_not_added_when_library_tracks_equals_1(data_cleaner):
    df = pd.DataFrame(
        data=[["The Princess: The Vinyl Collection 2010 - 2012", "The Vamp", 1]],
        columns=["spotify_search_album", "track_name", "spotify_total_tracks"],
    )
    cleaned_df = data_cleaner._should_add_album(df)
    assert cleaned_df["spotify_add_album"][0] == False
