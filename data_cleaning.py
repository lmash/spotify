import logging
from typing import List

import numpy as np
import pandas as pd

from config import (
    SpotifyTrackName,
    SpotifyArtist,
    SpotifyTrackNameByContentId,
    SpotifyAlbum,
)
import config

logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self):
        self.CHARACTERS_REMOVE = "'`´’"
        self.ARTIST_DELIMITERS = [" Feat.", " &", " With"]

    @staticmethod
    def _combine_extracted_dataframes(
        df_apple, df_external
    ) -> pd.DataFrame:
        """Combine dataframes extracted from apple and non apple music folders"""
        df_combined = pd.concat([df_apple, df_external])

        return df_combined

    @staticmethod
    def _get_isrc(xid) -> str:
        try:
            return xid.split(":")[-1]
        except AttributeError:
            return np.nan

    def _set_isrc(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        xid has format: <ReleasedBy>:isrc:<ISRC Code>
        Extract ISRC from xid, add it as a new column and remove xid column
        """
        logger.info("Extract the ISRC from xid")
        df.loc[:, "isrc"] = df.loc[:, "xid"].apply(self._get_isrc)

        df = df.drop(columns=["xid"])
        return df

    @staticmethod
    def _create_spotify_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Create new columns for searching spotify"""
        logger.info("Create new columns for searching spotify")
        df.loc[:, "spotify_search_track_name"] = df.loc[:, "track_name"]
        df.loc[:, "spotify_search_artist"] = df.loc[:, "artist"]
        df.loc[:, "spotify_search_album"] = df.loc[:, "album"]
        df.loc[:, "spotify_track_uri"] = np.nan
        df.loc[:, "spotify_artist_uri"] = np.nan
        df.loc[:, "spotify_album_uri"] = np.nan
        df.loc[:, "spotify_release_year"] = df.loc[:, "release_date"]
        df.loc[:, "spotify_total_tracks"] = 0
        df.loc[:, "isrc"] = np.nan
        return df

    def _remove_characters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Spotify handling. This is a workaround to handle a search issue with
        single quotes https://github.com/spotipy-dev/spotipy/issues/726
        Only apply to records where spotify_search_track_name or spotify_search_artist exist
        """
        logger.info(
            f"Spotify handling - Remove {self.CHARACTERS_REMOVE} from artists & track names"
        )
        track_name_exists = ~df["spotify_search_track_name"].isna()
        artist_exists = ~df["spotify_search_artist"].isna()
        album_exists = ~df["spotify_search_album"].isna()

        for char in self.CHARACTERS_REMOVE:
            df.loc[track_name_exists, "spotify_search_track_name"] = df.loc[
                track_name_exists, "spotify_search_track_name"
            ].apply(lambda x: x.replace(char, ""))

            df.loc[artist_exists, "spotify_search_artist"] = df.loc[
                artist_exists, "spotify_search_artist"
            ].apply(lambda x: x.replace(char, ""))

            df.loc[album_exists, "spotify_search_album"] = df.loc[
                album_exists, "spotify_search_album"
            ].apply(lambda x: x.replace(char, ""))

        return df

    @staticmethod
    def _drop_rows_with_no_track_number(df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Drop rows with no track number")
        df = df.dropna(subset=["track_number"])
        df = df.drop(df[df["track_name"].isna() & df["isrc"].isna()].index)
        df.reset_index()
        return df

    @staticmethod
    def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        logger.info("Remove duplicates")
        df = df.drop_duplicates(
            subset=[
                "track_name",
                "artist",
                "release_date",
                "album",
            ],
            keep="first",
        )
        df = df.set_index(["track_name", "artist", "release_date", "album"])
        df = df.reset_index()
        return df

    @staticmethod
    def _set_artist_where_na(df: pd.DataFrame) -> pd.DataFrame:
        """
        Where artist is na but album_artist is populated use album_artist
        """
        artist_na_mask = df["artist"].isna()
        df.loc[artist_na_mask, "artist"] = df.loc[artist_na_mask, "album_artist"]
        return df

    @staticmethod
    def _set_spotify_release_year(df: pd.DataFrame) -> pd.DataFrame:
        """
        release_date is populated during _create_spotify_columns and contains 2 formats YYYY & YYYY-MM-DDTHH:MM:SSZ
        Clean this field so that spotify_release_year only has YYYY
        """
        logger.info("Set spotify release year")
        release_date_update_mask = (~df.loc[:, "release_date"].isna()) & (
            df.loc[:, "release_date"].str.len() > 4
        )
        df.loc[release_date_update_mask, "spotify_release_year"] = df.loc[
            release_date_update_mask, "release_date"
        ].apply(lambda x: x.split("-")[0])
        return df

    def _split_artists_keep_first_only(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Spotify stores multiple artists against tracks but when searching you can find the track with only one.
        Split on a list of delimiters, keep only the first artist
        """
        logger.info("Spotify handling, split artists keeping only the first")
        df_isrc_na = df[
            ((df.loc[:, "isrc"].isna()) & (~df.loc[:, "spotify_search_artist"].isna()))
        ]

        for delimiter in self.ARTIST_DELIMITERS:
            df_isrc_na.loc[:, "spotify_search_artist"] = df_isrc_na.loc[
                :, "spotify_search_artist"
            ].apply(lambda x: x.split(delimiter)[0])

            df.update(df_isrc_na)

        return df

    @staticmethod
    def _update_spotify_albums(
        df: pd.DataFrame, album_updates: List[SpotifyAlbum]
    ) -> pd.DataFrame:
        """Update value in to_spotify_search_album"""
        for column_map in album_updates:
            df_album = df[
                df.loc[:, "spotify_search_album"]
                == column_map.from_spotify_search_album
            ]
            df_album.loc[:, "spotify_search_album"] = column_map.to_spotify_search_album
            df.update(df_album)

        return df

    @staticmethod
    def _should_add_album(df: pd.DataFrame) -> pd.DataFrame:
        """
        Add a boolean column spotify_add_album to indicate whether the album should be added.
        Set to True if the number of tracks in the library equals the number of tracks
        on the album.
        """
        s_track_count = df.groupby(by="spotify_search_album")["track_name"].count()
        df_track_count = pd.DataFrame(s_track_count)
        df_track_count = df_track_count.rename(
            columns={"track_name": "library_total_tracks"}
        )

        df = pd.merge(
            df,
            df_track_count,
            left_on="spotify_search_album",
            right_on="spotify_search_album",
            how="inner",
        )

        # Set to True where tracks are equal and > 1
        df["spotify_add_album"] = np.where(
            (
                (df["spotify_total_tracks"] == df["library_total_tracks"])
                & (df["spotify_total_tracks"] > 1)
            ),
            True,
            False,
        )

        # Set to True if the number of tracks in the library is greater than 5
        where_tracks_six_or_more = df["library_total_tracks"] >= 6
        df.loc[where_tracks_six_or_more, "spotify_add_album"] = True

        # Set to False if spotify_search_album matches a list of albums to override
        override_mask = df["spotify_search_album"].isin(config.albums_ignore)
        df.loc[override_mask, "spotify_add_album"] = False

        return df

    @staticmethod
    def _update_spotify_artists(
        df: pd.DataFrame, artist_updates: List[SpotifyArtist]
    ) -> pd.DataFrame:
        """Update value in to_spotify_search_artist"""
        for column_map in artist_updates:
            df_artist = df[
                df.loc[:, "spotify_search_artist"]
                == column_map.from_spotify_search_artist
            ]
            df_artist.loc[
                :, "spotify_search_artist"
            ] = column_map.to_spotify_search_artist
            df.update(df_artist)

        return df

    @staticmethod
    def _update_spotify_tracks(
        df: pd.DataFrame, track_updates: List[SpotifyTrackName]
    ) -> pd.DataFrame:
        """Update value in spotify_search_artist. As song names can be shared we also match on artist"""
        for column_map in track_updates:
            df_track = df[
                (
                    (
                        df.loc[:, "spotify_search_track_name"]
                        == column_map.from_spotify_search_track_name
                    )
                    & (df.loc[:, "artist"] == column_map.artist)
                )
            ]
            df_track.loc[
                :, "spotify_search_track_name"
            ] = column_map.to_spotify_search_track_name
            df.update(df_track)

        return df

    @staticmethod
    def _update_spotify_tracks_by_content_id(
        df: pd.DataFrame, track_updates: List[SpotifyTrackNameByContentId]
    ) -> pd.DataFrame:
        """
        Update value in spotify_search_track_name by content_id. Handles case where metadata is missing the
        track_name
        """
        for column_map in track_updates:
            df_track = df[df.loc[:, "content_id"] == column_map.content_id]
            df_track.loc[
                :, "spotify_search_track_name"
            ] = column_map.to_spotify_search_track_name
            df.update(df_track)

        return df

    @staticmethod
    def _clean_brackets_from_spotify_search_fields(df: pd.DataFrame) -> pd.DataFrame:
        """
        Meta data for track names which are missing isrc's appear to have a pattern, where
        spotify does not match the contents inside [] and (). Workaround is to remove the contents.
        Only apply to spotify_search_track_name with missing ISRC
        """
        df_isrc_na = df[df.loc[:, "isrc"].isna()]
        if len(df_isrc_na) == 0:
            return df

        columns = ("spotify_search_track_name",)
        for column in columns:
            df_isrc_na.loc[:, column] = df_isrc_na.loc[:, column].replace(
                r"\s?\[.+\]|\s?\(.+\)", "", regex=True
            )

        df.update(df_isrc_na)

        return df

    @staticmethod
    def _clean_brackets_from_spotify_search_album(df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean brackets contents, square and round from spotify_search_album
        """
        df.loc[:, "spotify_search_album"] = df.loc[:, "spotify_search_album"].replace(
            r"\s?\[.+\]|\s?\(.+\)", "", regex=True
        )
        return df

    @staticmethod
    def _add_spotify_track_uri_to_playlist(
        df_playlist: pd.DataFrame, df_tracks: pd.DataFrame
    ) -> pd.DataFrame:
        """Combine the playlist dataframe with spotify_track_uri"""
        df_tracks = df_tracks.loc[
            :, ["album", "artist", "track_name", "spotify_track_uri"]
        ]

        df_playlist = df_playlist.merge(
            df_tracks,
            left_on=["album", "artist", "track_name"],
            right_on=["album", "artist", "track_name"],
            how="left",
        )

        return df_playlist

    def clean_itunes_extracted(
        self, df_extracted_apple, df_extracted_external
    ) -> pd.DataFrame:
        df_combined = self._combine_extracted_dataframes(
            df_extracted_apple, df_extracted_external
        )

        return df_combined

    def clean_itunes_data_round_1(self, df) -> pd.DataFrame:
        df = self._set_isrc(df)
        df = self._drop_rows_with_no_track_number(df)
        df = self._set_artist_where_na(df)
        df = self._create_spotify_columns(df)
        df = self._set_spotify_release_year(df)
        df = self._clean_brackets_from_spotify_search_fields(df)
        df = self._clean_brackets_from_spotify_search_album(df)
        df = self._remove_characters(df)
        df = self._remove_duplicates(df)
        df = self._split_artists_keep_first_only(df)

        # updates artists and tracks according to the values specified in config.
        df = self._update_spotify_artists(df, config.artist_updates)
        df = self._update_spotify_tracks(df, config.track_updates)
        df = self._update_spotify_tracks_by_content_id(
            df, config.track_updates_by_content_id
        )

        return df

    def clean_itunes_data_round_3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This round of cleaning occurs after the second spotify extraction. This is to ensure artist splitting
        does not unintentionally affect changes made when updating spotify artists.
        """
        df = self._update_spotify_albums(df, config.album_updates)
        df = self._should_add_album(df)

        return df

    def clean_itunes_playlist(
        self, df_playlist: pd.DataFrame, df_tracks: pd.DataFrame
    ) -> pd.DataFrame:
        df_playlist = self._add_spotify_track_uri_to_playlist(df_playlist, df_tracks)
        return df_playlist
