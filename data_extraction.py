import getpass
import logging
import os
from pathlib import Path
from typing import Dict, List


from dotenv import load_dotenv
from itunesLibrary import library
import mutagen
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
    # This mapping consolidates the 3 formats
    meta_tag_map = {
        # m4p Mappings
        'cnID': 'content_id',
        'soal': 'album',
        'soar': 'artist',
        'sonm': 'track_name',
        'xid ': 'xid',
        '©day': 'release_date',
        'stik': 'track_number',
        # m4a Mappings
        'aART': 'artist',
        'trkn': 'track_number',
        '©ART': 'album_artist',
        '©alb': 'album',
        '©nam': 'track_name',
        '©wrt': 'composer',
        # mp3 Mappings
        'TALB': 'album',
        'TDRC': 'release_date',
        'TIT2': 'track_name',
        'TPE1': 'artist',
        'TPE2': 'composer',
        'TPOS': 'track_number',
    }

    def __init__(self, mode='PROD'):
        self.mode = mode
        if self.mode == 'TEST':
            self.MUSIC_PATH_APPLE = 'src/spotify/.data/apple'
            self.MUSIC_PATH_LOCAL = 'src/spotify/.data/external'
        else:
            self.MUSIC_PATH_APPLE = config.ITUNES_PATH / "Apple Music"
            self.MUSIC_PATH_LOCAL = config.ITUNES_PATH / "Music"
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
    def _get_music_metadata(track: Path) -> Dict:
        track_details = {}
        audio = mutagen.File(track)
        text = audio.pprint()
        lines = text.split("\n")

        for line in lines:
            mapping_key, _, value = line.partition("=")
            if mapping_key in DataExtractor.meta_tag_map.keys():
                key = DataExtractor.meta_tag_map[mapping_key]
                track_details[key] = value

        return track_details

    def _get_tags_from_music(self, path: Path) -> List[Dict]:
        """Apple music has more tags (with the xid) than copied music"""
        tracks = []

        for item in path.rglob("*.*"):
            if item.suffix in [".m4p", ".m4a", ".mp3", ".MP3"]:
                track_tags = self._get_music_metadata(item)
                logger.debug(item.name)
                tracks.append(track_tags)

        return tracks

    @staticmethod
    def read_playlists_from_apple_library(filename: str = "Library.xml") -> pd.DataFrame:
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

    @staticmethod
    def read_tracks_from_apple_library(filename: str = "Library.xml") -> pd.DataFrame:
        """Read apple xml file, extract playlists and return as a dataframe"""
        lib = library.parse(config.PLAYLIST_PATH / filename, ignoreRemoteSongs=False)
        tracks = []

        for track in lib.items:
            if not track.remote:
                continue

            try:
                release_date = track.itunesAttributes['Year']
            except KeyError:
                release_date = None

            try:
                track_number = track.itunesAttributes['Track Number']
            except KeyError:
                # Default track number to a valid number as we later remove entries w/out a track number
                track_number = 1

            data = {
                'album': track.album,
                'artist': track.artist,
                'track_name': track.title,
                'release_date': release_date,
                'track_number': track_number
            }

            tracks.append(data)

        return pd.json_normalize(tracks)
