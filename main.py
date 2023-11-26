from dotenv import load_dotenv
import logging
import os

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from data_cleaning import DataCleaner
from data_extraction import DataExtractor

logging.basicConfig(
    filename='spotify.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format=
    "%(asctime)s [%(levelname)s] %(name)s - %(funcName).40s - %(message)s",
)
logger = logging.getLogger(__name__)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


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


if __name__ == '__main__':
    data_extractor = DataExtractor()
    df_apple, df_other = data_extractor.process_itunes_tracks()

    data_cleaner = DataCleaner()
    df_combined = data_cleaner.clean_itunes_data(df_apple, df_other)

    # get_users_playlists()
    # search_spotify_by_isrc()
