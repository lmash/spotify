from dotenv import load_dotenv
import getpass
import os
from pathlib import Path
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import subprocess
from typing import Dict, List


load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

MUSIC_PATH_APPLE = 'Music/Music/Media.localized/Apple Music'
MUSIC_PATH_LOCAL = 'Music/Music/Media.localized/Music'


def search_spotify_by_isrc(isrc_code='GBBND0701743'):
    """
    https://api.spotify.com/v1/search?type=track&q=isrc:USEE10001993
    :return:
    """
    search_str = f'isrc:{isrc_code}'
    result = sp.search(search_str, limit=1, type='track')
    print(result)


def get_users_playlists():
    """
    Endpoint: https://api.spotify.com/v1/users/{user_id}/playlists
    """
    result = sp.current_user_playlists()
    print(result)


def create_spotify_playlist(name, songs):
    pass


def _header_encountered(read_from_here, previous_line):
    """Continue processing if either read_from_here or if the previous line contained our starting text"""
    return read_from_here is True or previous_line.startswith('Track\t')


def _call_mp4info(track: Path) -> Dict:
    """
    Pre-Requisite: brew install mp4v2 (try get it into your pip install!)
    Accepts a track (Path with Full path to track)
    We are only interested in rows after the line with 'Track\t'
    Process the header row (may appear on different row if there were atom issues encountered)
    Process and clean the tag. The tag is a colon (key, value) delimited pair
    """
    result = subprocess.run(["mp4info", str(track)], capture_output=True, text=True, check=True, encoding="latin-1")
    track_details = {}
    read_from_here, previous_line = (False, '')

    lines = result.stdout.split('\n')
    for index, line in enumerate(lines):
        # Start processing tags after the line with 'Track\t'
        if line and _header_encountered(read_from_here, previous_line):
            if previous_line.startswith('Track\t'):
                read_from_here = True
                track_details['Track'] = line.split('\t')[0]
            else:
                key, _, value = line.partition(':')
                key = key.lstrip()
                track_details[key] = value

        previous_line = line

    return track_details


def get_tags_from_music(path: Path) -> List[Dict]:
    """Apple music has more tags (with the xid) than copied music"""
    tracks = []

    for item in path.rglob("*.*"):
        # if item.name.endswith('m4p') or item.name.endswith('m4a'):
        if item.suffix in ['.mp4', '.m4a', 'mp3', '.MP3']:
            track_tags = _call_mp4info(item)
            print(item.name)
            tracks.append(track_tags)

    return tracks


def process_itunes_tracks():
    """
    So you have several problems here,
    1. Apple music (Apple Music folder) has an xid which can be retrieved with mp4, also there is a playlist tag
    2. Locally loaded music (Music folder) has much fewer tags
    suggestion is to load all into dataframes and then see where we go from there!
    """
    user = getpass.getuser()
    path_apple = Path(f"/Users/{user}") / MUSIC_PATH_APPLE
    apple_music_tracks = get_tags_from_music(path_apple)
    df_apple = pd.DataFrame(apple_music_tracks)

    path_local = Path(f"/Users/{user}") / MUSIC_PATH_LOCAL
    local_tracks = get_tags_from_music(path_local)
    df_loaded = pd.DataFrame(local_tracks)

    return df_apple, df_loaded


if __name__ == '__main__':
    df_apple, df_loaded = process_itunes_tracks()

    # get_users_playlists()
    # search_spotify_by_isrc()
