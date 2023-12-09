import getpass
import logging
import os
from pathlib import Path
import subprocess
from typing import Dict, List


from dotenv import load_dotenv
from itunesLibrary import library
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import config

logger = logging.getLogger(__name__)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)


class DataExtractor:
    def __init__(self, mode='PROD'):
        # TODO enhance the below for OS (Add windows!)
        self.mode = mode
        if self.mode == 'TEST':
            self.MUSIC_PATH_APPLE = 'src/spotify_isrc/data/apple'
            self.MUSIC_PATH_LOCAL = 'src/spotify_isrc/data/external'
        else:
            self.MUSIC_PATH_APPLE = "Music/Music/Media.localized/Apple Music"
            self.MUSIC_PATH_LOCAL = "Music/Music/Media.localized/Music"
        self.user = getpass.getuser()

    def process_itunes_metadata(self):
        """
        So you have several problems here,
        1. Apple music (Apple Music folder) has an xid which can be retrieved with mp4, also there is a playlist tag
        2. Locally loaded music (Music folder) has much fewer tags
        suggestion is to load all into dataframes and then see where we go from there!
        """
        logger.info(f"Apple path: {self.MUSIC_PATH_APPLE}"
                    f" Non Apple path: {self.MUSIC_PATH_LOCAL}")

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

    @staticmethod
    def read_playlist(filename) -> pd.DataFrame:
        """Read a .txt file exported from an Apple playlist"""
        df = pd.read_csv(f'data/playlists/{filename}', encoding='utf_16_le', sep='\t')
        df['playlist_name'] = filename.split('.')[0]
        return df

    @staticmethod
    def read_apple_library(filename: str = "Library.xml") -> pd.DataFrame:
        """Read apple xml file, extract playlists and return as a dataframe"""
        lib = library.parse(config.PLAYLIST_PATH / filename, ignoreRemoteSongs=False)
        playlists = []

        for playlist in lib.playlists:
            if playlist.title in config.playlists_exclude:
                continue

            for item in playlist.items:
                data = {
                    'playlist_name': playlist.title,
                    'album': item.album,
                    'artist': item.artist,
                    'track_name': item.title,
                }
                playlists.append(data)

        return pd.json_normalize(playlists)
