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

    def __init__(self, spotify):
        self.spotify = spotify

    def _get_isrc_from_spotify(self, row: pd.Series):
        """
        Might have to cycle through a few markets?
        https://github.com/spotipy-dev/spotipy/issues/522
        Fixed the issue where half of my requests were failing when set to ES!! Changed to GB!
        Also set the track_id, artist_id and album_id
        """
        search_str = f'artist:{row["spotify_search_artist"]} track:{row["spotify_search_track_name"]}'
        result = self.spotify.search(search_str, type="track", market="GB", offset=0, limit=10)

        try:
            row["isrc"] = result["tracks"]["items"][0]["external_ids"]["isrc"]
            row["spotify_track_uri"] = result["tracks"]["items"][0]["uri"]
            row["spotify_artist_uri"] = result["tracks"]["items"][0]['artists'][0]['uri']
            row["spotify_album_uri"] = result["tracks"]["items"][0]['album']['uri']
            logger.info(f"Found spotify ISRC for: {search_str}")
        except IndexError:
            logger.warning(f"Failed to get spotify ISRC for: {search_str}|")
            row["isrc"] = np.nan
        except TypeError:
            logger.warning(
                f"Failed to get spotify ISRC with TypeError for: {search_str}|"
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

