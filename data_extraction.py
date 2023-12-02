import getpass
import logging
import os
from pathlib import Path
import subprocess
from typing import Dict, List

import numpy as np
from dotenv import load_dotenv
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

logger = logging.getLogger(__name__)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)


class DataExtractor:
    def __init__(self):
        # TODO enhance the below for OS (Add windows!)
        self.MUSIC_PATH_APPLE = "Music/Music/Media.localized/Apple Music"
        self.MUSIC_PATH_LOCAL = "Music/Music/Media.localized/Music"
        # self.MUSIC_PATH_APPLE = 'src/spotify_isrc/data/apple'
        # self.MUSIC_PATH_LOCAL = 'src/spotify_isrc/data/external'
        self.user = getpass.getuser()

    def process_itunes_tracks(self):
        """
        So you have several problems here,
        1. Apple music (Apple Music folder) has an xid which can be retrieved with mp4, also there is a playlist tag
        2. Locally loaded music (Music folder) has much fewer tags
        suggestion is to load all into dataframes and then see where we go from there!
        """
        path_apple = Path(f"/Users/{self.user}") / self.MUSIC_PATH_APPLE
        apple_music_tracks = self._get_tags_from_music(path_apple)
        df_apple = pd.DataFrame(apple_music_tracks)

        path_local = Path(f"/Users/{self.user}") / self.MUSIC_PATH_LOCAL
        local_tracks = self._get_tags_from_music(path_local)
        df_loaded = pd.DataFrame(local_tracks)

        return df_apple, df_loaded

    @staticmethod
    def _header(previous_line):
        return previous_line.startswith("Track\t")

    @staticmethod
    def _header_encountered(read_from_here, previous_line):
        """Continue processing if either read_from_here or if the previous line contained our starting text"""
        return read_from_here is True or previous_line.startswith("Track\t")

    def _call_mp4info(self, track: Path) -> Dict:
        """
        Pre-Requisite: brew install mp4v2 (try get it into your pip install!)
        Accepts a track (Path with Full path to track)
        We are only interested in rows after the line with 'Track\t'
        Process the header row (may appear on different row if there were atom issues encountered)
        Process and clean the tag. The tag is a colon (key, value) delimited pair
        """
        try:
            result = subprocess.run(
                ["mp4info", str(track)],
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
        except UnicodeDecodeError:
            result = subprocess.run(
                ["mp4info", str(track)],
                capture_output=True,
                text=True,
                check=True,
                encoding="latin-1",
            )
        track_details = {}
        read_from_here, previous_line = (False, "")

        lines = result.stdout.split("\n")
        for line in lines:
            # Start processing tags after the line with 'Track\t'
            if line and self._header_encountered(read_from_here, previous_line):
                if self._header(previous_line):
                    read_from_here = True
                    track_details["Track"] = line.split("\t")[0]
                else:
                    key, _, value = line.partition(":")
                    key, value = key.lstrip(), value.lstrip()
                    track_details[key] = value

            previous_line = line

        return track_details

    def _get_tags_from_music(self, path: Path) -> List[Dict]:
        """Apple music has more tags (with the xid) than copied music"""
        tracks = []

        for item in path.rglob("*.*"):
            # TODO MPS and mp3 not returning any tags yet!
            if item.suffix in [".m4p", ".m4a", "mp3", ".MP3"]:
                track_tags = self._call_mp4info(item)
                logger.debug(item.name)
                tracks.append(track_tags)

        return tracks
    #
    # @staticmethod
    # def _get_isrc_from_spotify(row: pd.Series):
    #     """
    #     Might have to cycle through a few markets?
    #     https://github.com/spotipy-dev/spotipy/issues/522
    #     Fixed the issue where half of my requests were failing when set to ES!! Changed to GB!
    #     """
    #     search_str = f'artist:{row["spotify_search_artist"]} track:{row["spotify_search_track_name"]}'
    #     result = sp.search(search_str, type="track", market="GB", offset=0, limit=10)
    #
    #     try:
    #         row["isrc"] = result["tracks"]["items"][0]["external_ids"]["isrc"]
    #         logger.info(f"Found spotify ISRC for: artist: {search_str}")
    #     except IndexError:
    #         logger.warning(f"Failed to get spotify ISRC for: artist: {search_str}")
    #         row["isrc"] = np.nan
    #     except TypeError:
    #         logger.warning(
    #             f"Failed to get spotify ISRC with TypeError for: artist: {search_str}"
    #         )
    #     return row
    #
    # def extract_all_isrc_with_na(self, df: pd.DataFrame) -> pd.DataFrame:
    #     logger.info(
    #         f"Search spotify for all ISRC's which are currently na. Search using the track & artist"
    #     )
    #
    #     extracted = df[df["isrc"].isna()]
    #     extracted = extracted.apply(self._get_isrc_from_spotify, axis=1)
    #
    #     df.update(extracted)
    #     return df
    #
    # def extract_isrc(
    #     self, df: pd.DataFrame, spotify_search_artist, spotify_search_track_name
    # ) -> pd.DataFrame:
    #     logger.info(f"Search spotify for a single ISRC using the track & artist")
    #
    #     extracted = df[
    #         (
    #             (df["spotify_search_artist"] == spotify_search_artist)
    #             & (df["spotify_search_track_name"] == spotify_search_track_name)
    #         )
    #     ]
    #     extracted = extracted.apply(self._get_isrc_from_spotify, axis=1)
    #
    #     df.update(extracted)
    #     return df
