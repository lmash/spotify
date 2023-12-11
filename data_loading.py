import logging
from typing import List

import pandas as pd

from utils import chunked

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, spotify):
        self.spotify = spotify
        self.user_id = self.spotify.me()["id"]

    def add_tracks_to_spotify(self, tracks: List):
        self.spotify.current_user_saved_tracks_add(tracks=tracks)

    def add_albums_to_spotify(self, df: pd.DataFrame, size=10):
        """Add the albums in lists broken into chunks"""
        exclude_na = ~df["spotify_album_uri"].isna()
        albums = df.loc[exclude_na, "spotify_album_uri"].unique().tolist()
        chunks = chunked(albums, size)

        for chunk in chunks:
            logger.debug(f"Adding list of album to spotify with uri's: {chunk}")
            self.spotify.current_user_saved_albums_add(albums=chunk)

    def remove_albums_from_spotify(self, df: pd.DataFrame, size=10):
        exclude_na = ~df["spotify_album_uri"].isna()
        albums = df.loc[exclude_na, "spotify_album_uri"].unique().tolist()
        chunks = chunked(albums, size)

        for chunk in chunks:
            logger.debug(f"Deleting list of album to spotify with uri's: {chunk}")
            self.spotify.current_user_saved_albums_delete(albums=chunk)

    def add_playlists(self, df: pd.DataFrame, size=5):
        """ Add Users playlists. Note: If re-run will add once again """
        exclude_na = ~df["spotify_track_uri"].isna()
        playlists = df.loc[exclude_na, "playlist_name"].unique().tolist()

        for playlist in playlists:
            # Create the Playlist
            response = self.spotify.user_playlist_create(self.user_id, playlist)

            tracks_mask = (~df["spotify_track_uri"].isna()) & (
                df["playlist_name"] == playlist
            )
            tracks = df.loc[tracks_mask, "spotify_track_uri"].unique().tolist()
            chunks = chunked(tracks, size)

            # Add tracks to the Playlist
            for chunk in chunks:
                logger.debug(
                    f"Adding tracks to playlist {playlist} to spotify with uri's: {chunk}"
                )
                self.spotify.playlist_add_items(response['id'], chunk)

    def remove_playlists(self):
        """Remove ALL users playlists"""
        playlists = self.spotify.user_playlists(self.user_id)

        for playlist in playlists['items']:
            logger.info(f"Deleting playlist {playlist['name']} with id {playlist['id']}")
            self.spotify.current_user_unfollow_playlist(playlist['id'])