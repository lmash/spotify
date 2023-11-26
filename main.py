from dotenv import load_dotenv
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from extract import Extractor


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
    extractor = Extractor()
    df_apple, df_loaded = extractor.process_itunes_tracks()

    # get_users_playlists()
    # search_spotify_by_isrc()
