import logging

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

logger = logging.getLogger(__name__)
# Load the Spotify env variables from .env
load_dotenv()


def spotify_get() -> spotipy.Spotify:
    """
    Spotify's Client Credentials Flow - used when we search.
    https://spotipy.readthedocs.io/en/2.22.1/#authorization-code-flow
    Only endpoints that do not access user information can be accessed.
    The advantage here in comparison with requests to the Web API made without an access token,
    is that a higher rate limit is applied
    """
    auth_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp


def spotify_put() -> spotipy.Spotify:
    """
    Spotify's Client Credentials Flow - used when we search.
    https://spotipy.readthedocs.io/en/2.22.1/#authorization-code-flow
    Only endpoints that do not access user information can be accessed.
    The advantage here in comparison with requests to the Web API made without an access token,
    is that a higher rate limit is applied
    """
    scope = "user-library-read"

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))
    return sp
