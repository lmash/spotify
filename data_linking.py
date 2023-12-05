import logging

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataLinker:
    """
    A class to link extracted records with their ISRC.
    International Standard Recording Code (ISRC) is the international identification system for sound recordings and
    music video recordings.
    We currently retrieve this from Spotify
    """

    SINGLES = ["Single", "EP"]

    def __init__(self, spotify):
        self.spotify = spotify

    @staticmethod
    def _is_single(search_album) -> bool:
        """Return True if the album field is not nan and doesn't contain any of the words in the SINGLES list"""
        if pd.isnull(search_album):
            return True

        return any(single in search_album for single in DataLinker.SINGLES)

    @staticmethod
    def _has_release_year(search_release_year) -> bool:
        """Return True if the search_release_year field is not nan"""
        if pd.isnull(search_release_year):
            return False

        return True

    @staticmethod
    def _how_to_search():
        pass

    def _get_isrc_from_spotify(self, row: pd.Series) -> pd.Series:
        """
        Might have to cycle through a few markets?
        https://github.com/spotipy-dev/spotipy/issues/522
        Fixed the issue where half of my requests were failing when set to ES!! Changed to GB!
        Also set the track_id, artist_id and album_id
        """
        search_artist = row["spotify_search_artist"]
        search_track = row["spotify_search_track_name"]
        search_release_year = row["spotify_release_year"]

        if self._has_release_year(search_release_year):
            search_str = f"artist:{search_artist} track:{search_track} year:{search_release_year}"
        else:
            search_str = f"artist:{search_artist} track:{search_track}"

        result = self.spotify.search(
            search_str, type="track", market="GB", offset=0, limit=5
        )

        try:
            row["isrc"] = result["tracks"]["items"][0]["external_ids"]["isrc"]
            row["spotify_track_uri"] = result["tracks"]["items"][0]["uri"]
            row["spotify_artist_uri"] = result["tracks"]["items"][0]["artists"][0][
                "uri"
            ]
            # row["spotify_album_uri"] = result["tracks"]["items"][0]['album']['uri']
            row["spotify_total_tracks"] = int(
                result["tracks"]["items"][0]["album"]["total_tracks"]
            )
            logger.info(f"Found spotify ISRC for: {search_str}")
        except IndexError:
            logger.warning(f"Failed to get spotify ISRC for: {search_str}")
            row["isrc"] = np.nan
        except TypeError:
            logger.warning(
                f"Failed to get spotify ISRC with TypeError for: {search_str}"
            )
        return row

    def extract_all_isrc_with_na(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info(
            f"Search spotify for all ISRC's which are currently na. Search using the track & artist"
        )

        extracted = df[df["isrc"].isna()]
        extracted = extracted.apply(self._get_isrc_from_spotify, axis=1)

        df.update(extracted)
        return df

    def extract_isrc(
        self, df: pd.DataFrame, spotify_search_artist, spotify_search_track_name
    ) -> pd.DataFrame:
        logger.info(f"Search spotify for a single ISRC using the track & artist")

        extracted = df[
            (
                (df["spotify_search_artist"] == spotify_search_artist)
                & (df["spotify_search_track_name"] == spotify_search_track_name)
            )
        ]
        extracted = extracted.apply(self._get_isrc_from_spotify, axis=1)

        df.update(extracted)
        return df

    def _get_album_uri_from_spotify(self, row: pd.Series) -> pd.Series:
        """Retrieve an album uri from Spotify"""
        search_album = row["spotify_search_album"]
        search_str = f"album:{search_album} "

        result = self.spotify.search(
            search_str, type="album", market="GB", offset=0, limit=1
        )
        try:
            row["spotify_album_uri"] = result["albums"]["items"][0]["uri"]
            logger.info(f"Found spotify album for: {search_str}")
        except IndexError:
            logger.warning(f"Failed to get spotify album for: {search_str}")
        except TypeError:
            logger.warning(
                f"Failed to get spotify album with TypeError for: {search_str}"
            )

        return row

    def extract_spotify_album_uri(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Return a dataframe with spotify_album_uri populated. Only retrieves the uri for albums
        with spotify_add_album set to True
        """
        logger.info(f"Search spotify for all album uri's. Search using the album")

        albums_mask = df["spotify_add_album"] == True

        # Create a dataframe with albums to be requested from Spotify
        albums = (
            df[albums_mask]
            .groupby("spotify_search_album")
            .agg({"spotify_album_uri": lambda x: np.nan})
        ).reset_index()
        albums = albums.apply(self._get_album_uri_from_spotify, axis=1)

        df = pd.merge(
            df,
            albums,
            left_on="spotify_search_album",
            right_on="spotify_search_album",
            how="left",
        )
        # Cleanup after merge
        df = df.drop(columns="spotify_album_uri_x")
        df = df.rename(columns={"spotify_album_uri_y": "spotify_album_uri"})

        return df
