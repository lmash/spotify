from types import MappingProxyType

import numpy as np
import pandas as pd
import pytest
import spotipy

from data_linking import DataLinker


@pytest.fixture
def data_linker():
    """Returns a DataCleaning instance for Music"""
    sp = spotipy.Spotify(auth_manager=spotipy.SpotifyClientCredentials(client_id='ID', client_secret='SECRET'))
    return DataLinker(spotify=sp)


def test_albums_search_string_includes_artist_when_over_half_same_artist(data_linker):
    data = {
        "spotify_search_album": "Platinum Collection",
        "artist_count": 2,
        "spotify_search_artist": "Queen",
        "library_total_tracks": 15,
        "spotify_album_uri": np.nan,
    }
    row = pd.Series(
        data=data,
        index=[
            "spotify_search_album",
            "artist_count",
            "spotify_search_artist",
            "library_total_tracks",
            "spotify_album_uri",
        ],
    )

    search_str = data_linker._build_search_string_for_album_request(row=row)
    assert search_str == "album:Platinum Collection artist:Queen"


def test_get_albums_uri_returned(data_linker, monkeypatch):
    def mock_search(*args, **kwargs):
        # Need a MappingProxy as dict not hashable
        return MappingProxyType(
            {"albums": {"items": [{"uri": "spotify:album:63SYDOduS7UPFCbRo7g9cy"}]}}
        )

    df = pd.DataFrame(
        data=[
            ["Platinum Collection", "Queen", 7, True, np.nan],
            ["Platinum Collection", "Queen", 7, True, np.nan],
            ["Platinum Collection", "Freddie Mercury", 7, True, np.nan],
            ["Platinum Collection", "Queen", 7, True, np.nan],
            ["Platinum Collection", "Queen", 7, True, np.nan],
            ["Platinum Collection", "Queen", 7, True, np.nan],
            ["Platinum Collection", "Queen", 7, True, np.nan],
        ],
        columns=[
            "spotify_search_album",
            "spotify_search_artist",
            "library_total_tracks",
            "spotify_add_album",
            "spotify_album_uri",
        ],
    )

    monkeypatch.setattr(spotipy.Spotify, "search", mock_search)
    df = data_linker.extract_spotify_album_uri(df)
    assert df["spotify_album_uri"][0] == "spotify:album:63SYDOduS7UPFCbRo7g9cy"
    assert list(df.columns) == [
        "spotify_search_album",
        "spotify_search_artist",
        "spotify_add_album",
        "spotify_album_uri",
    ]
