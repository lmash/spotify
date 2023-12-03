import logging
import os

from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

scope = 'user-library-modify'

logger = logging.getLogger(__name__)
load_dotenv()
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret
)
spotify = spotipy.Spotify(auth_manager=auth_manager)
