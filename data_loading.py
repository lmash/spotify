import logging
from time import sleep
from typing import List

import pandas as pd
import spotipy

from utils import chunked

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, spotify):
        self.spotify = spotify
        self.user_id = self.spotify.me()["id"]
        self.user_name = self.spotify.me()["display_name"]

    def add_tracks_to_spotify(self, df: pd.DataFrame, size=10):
        """Add the tracks in lists broken into chunks"""
        requested_albums = df[((df["spotify_add_album"] == True) & ~df["spotify_album_uri"].isna())]
        tracks_only = pd.concat([df, requested_albums]).drop_duplicates(keep=False)

        exclude_na = ~tracks_only["spotify_track_uri"].isna()
        tracks = tracks_only.loc[exclude_na, "spotify_track_uri"].unique().tolist()
        chunks = chunked(tracks, size)

        for chunk in chunks:
            logger.debug(f"Adding list of album to spotify with uri's: {chunk}")
            self.spotify.current_user_saved_tracks_add(tracks=chunk)

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
                logger.info(
                    f"Adding tracks to playlist {playlist} to spotify with uri's: {chunk}"
                )
                self.spotify.playlist_add_items(response['id'], chunk)

            sleep(2)

    def nuke_playlists(self):
        """Remove ALL users playlists"""
        playlists = self.spotify.user_playlists(self.user_id)

        for playlist in playlists['items']:
            logger.info(f"Deleting playlist {playlist['name']} with id {playlist['id']}")
            self.spotify.current_user_unfollow_playlist(playlist['id'])

    def nuke_albums(self):
        """Remove ALL current users albums"""
        albums = self.spotify.current_user_saved_albums(limit=10)

        while albums:
            logger.debug(f"Deleting list of album to spotify with uri's: {albums}")
            album_uri = [
                item['album']['uri']
                for item in albums['items']
            ]

            if not album_uri:
                return

            self.spotify.current_user_saved_albums_delete(albums=album_uri)
            albums = self.spotify.current_user_saved_albums(limit=10)

    def nuke_tracks(self):
        """Remove ALL current users tracks"""
        tracks = self.spotify.current_user_saved_tracks(limit=10)

        while tracks:
            logger.debug(f"Deleting list of tracks to spotify with uri's: {tracks}")
            track_uri = [
                item['track']['uri']
                for item in tracks['items']
            ]

            if not track_uri:
                return

            self.spotify.current_user_saved_tracks_delete(tracks=track_uri)
            tracks = self.spotify.current_user_saved_tracks(limit=10)
