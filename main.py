import logging
import os

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from config import SpotifyArtist, artist_updates
from data_cleaning import DataCleaner
from data_extraction import DataExtractor
from data_linking import DataLinker
from data_loading import DataLoader


logging.basicConfig(
    filename="spotify.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(funcName).40s - %(message)s",
)
logger = logging.getLogger(__name__)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
sp = spotipy.Spotify(auth_manager=auth_manager)


def search_spotify_by_isrc(isrc_code="GBBND0701743"):
    """
    https://api.spotify.com/v1/search?type=track&q=isrc:USEE10001993
    :return:
    """
    search_str = f"isrc:{isrc_code}"
    result = sp.search(search_str, limit=1, type="track")
    print(result)


def get_users_playlists():
    """
    Endpoint: https://api.spotify.com/v1/users/{user_id}/playlists
    """
    result = sp.current_user_playlists()
    print(result)


def create_spotify_playlist(name, songs):
    pass


if __name__ == "__main__":
    data_extractor = DataExtractor()
    data_cleaner = DataCleaner()
    data_loader = DataLoader()
    data_linker = DataLinker()

    df_meta_apple, df_meta_localised = data_extractor.process_itunes_metadata()
    df_combined = data_cleaner.clean_itunes_data_round_1(df_meta_apple, df_meta_localised)
    df_combined = data_linker.extract_all_isrc_with_na(df_combined)

    # Write to Pickle file after initial spotify request
    data_loader.pickle(df_combined, "combined")
    data_loader.pickle(df_combined, "combined_backup")

    # get_users_playlists()
    # search_spotify_by_isrc()

    df_combined = data_loader.read_pickle("combined_backup")
    df_combined = data_cleaner.clean_itunes_data_round_2(df_combined)
    df_combined = data_linker.extract_all_isrc_with_na(df_combined)
    data_loader.pickle(df_combined, "combined")

    # df_playlist = data_extractor.read_playlist('Enjoy the Ride.txt')
    # df_playlist = data_cleaner.clean_itunes_playlist(df_playlist)


