import logging
from typing import List

import numpy as np
import pandas as pd

from config import SpotifyTrackName, SpotifyArtist, SpotifyTrackNameByContentId
import config

logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self):
        self.CHARACTERS_REMOVE = "'`´’"
        self.ARTIST_DELIMITERS = [' Feat.', ' &', ' With']

    @staticmethod
    def _drop_columns(df: pd.DataFrame, columns: List) -> pd.DataFrame:
        df = df.drop(columns=columns, errors="ignore")
        return df

    @staticmethod
    def _combine_extracted_dataframes(
        df_extracted_apple, df_extracted_external
    ) -> pd.DataFrame:
        """Combine dataframes extracted from apple and non apple music folders"""
        df_apple = df_extracted_apple.copy()
        df_external = df_extracted_external.copy()

        # Drop columns
        df_apple = df_apple.drop(
            columns=[
                "Copyright",
                "Content Rating",
                "Media Type",
                "iTunes Account",
                "Cover Art pieces",
                "ReadAtom",
            ],
            errors="ignore",
        )
        df_external = df_external.drop(
            columns=[
                "Encoded with",
                "BPM",
                "Part of Gapless Album",
                "Cover Art pieces",
                "Copyright",
                "Content Rating",
                "Media Type",
                'CRî" 1184108314 vs 7910639',
                "CRî is suspect",
                "iTunes Account",
                "Purchase Date",
                "ReadAtom",
                "iTunes Account Type",
                "Comments",
                "TV Episode",
                "TV Season",
                "Sort Composer",
                "TV Show",
                "Sort Name",
                "Sort Artist",
                "Sort Album",
            ],
            errors="ignore",
        )

        df_external = df_external.rename(
            columns={
                "Name": "Sort Name",
                "Artist": "Sort Artist",
                "Album": "Sort Album",
            }
        )

        # Combine into a single dataframe
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
        logger.debug("Extract the ISRC from xid")
        df.loc[:, "isrc"] = df.loc[:, "xid"].apply(self._get_isrc)

        df = df.drop(columns=["xid"])
        return df

    @staticmethod
    def _rename_columns(df: pd.DataFrame, columns) -> pd.DataFrame:
        """Renames columns & set column names to lowercase and make them python friendly"""
        df = df.rename(columns=columns)
        return df

    @staticmethod
    def _create_spotify_columns(df: pd.DataFrame) -> pd.DataFrame:
        """Create new columns for searching spotify."""
        df.loc[:, "spotify_search_track_name"] = df.loc[:, "track_name"]
        df.loc[:, "spotify_search_artist"] = df.loc[:, "artist"]
        df.loc[:, "spotify_search_album"] = df.loc[:, "album"]
        df.loc[:, "spotify_track_uri"] = np.nan
        df.loc[:, "spotify_artist_uri"] = np.nan
        df.loc[:, "spotify_album_uri"] = np.nan
        df.loc[:, "isrc"] = np.nan
        return df

    def _remove_characters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Spotify handling. This is a workaround to handle a search issue with
        single quotes https://github.com/spotipy-dev/spotipy/issues/726
        Only apply to records where spotify_search_track_name or spotify_search_artist exist
        """
        logger.info(f"Spotify handling - Remove {self.CHARACTERS_REMOVE} from artists & track names")
        track_name_exists = ~df["spotify_search_track_name"].isna()
        artist_exists = ~df["spotify_search_artist"].isna()

        for char in self.CHARACTERS_REMOVE:
            df.loc[track_name_exists, "spotify_search_track_name"] = df.loc[
                track_name_exists, "spotify_search_track_name"
            ].apply(lambda x: x.replace(char, ""))

            df.loc[artist_exists, "spotify_search_artist"] = df.loc[artist_exists, "spotify_search_artist"].apply(
                lambda x: x.replace(char, "")
            )

        return df

    @staticmethod
    def _drop_rows_with_no_track_number(df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna(subset=["track_number"])
        df = df.drop(df[df["track_name"].isna() & df["isrc"].isna()].index)
        df.reset_index()
        return df

    @staticmethod
    def _remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
        df = df.drop_duplicates(
            subset=[
                "track_name",
                "artist",
                "release_date",
                "album",
            ],
            keep="first",
        )
        df = df.set_index(
            ["track_name", "artist", "release_date", "album"]
        )
        df = df.reset_index()
        return df

    @staticmethod
    def set_spotify_track_name(
        df: pd.DataFrame, column_map: SpotifyTrackName
    ) -> pd.DataFrame:
        """Update value in spotify_search_track_name"""
        df_single_track = df[
            (
                (df.loc[:, "artist"] == column_map.artist)
                & (
                    df.loc[:, "spotify_search_track_name"]
                    == column_map.from_spotify_search_track_name
                )
            )
        ]
        df_single_track.loc[
            :, "spotify_search_track_name"
        ] = column_map.to_spotify_search_track_name
        df.update(df_single_track)

        return df

    def _split_artists_keep_first_only(self, df:pd.DataFrame) -> pd.DataFrame:
        """
        Spotify stores multiple artists against tracks but when searching you can find the track with only one.
        Split on a list of delimiters, keep only the first artist
        """
        logger.info("Spotify handling, split artists keeping only the first")
        df_isrc_na = df[(
            (df.loc[:, "isrc"].isna()) & (~df.loc[:, "spotify_search_artist"].isna())
        )
        ]

        for delimiter in self.ARTIST_DELIMITERS:
            df_isrc_na.loc[:, "spotify_search_artist"] = df_isrc_na.loc[
                :, "spotify_search_artist"
            ].apply(lambda x: x.split(delimiter)[0])

            df.update(df_isrc_na)

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
            df_track = df[(
                (df.loc[:, "spotify_search_track_name"] == column_map.from_spotify_search_track_name) &
                (df.loc[:, "artist"] == column_map.artist)
            )]
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
    def _clean_brackets_from_spotify_track_names(df: pd.DataFrame) -> pd.DataFrame:
        """
        Meta data for track names which are missing isrc's appear to have a pattern, where
        spotify does not match the contents inside [] and (). Workaround is to remove the contents.
        Only apply to spotify_search_track_name with missing ISRC
        """
        df_isrc_na = df[df.loc[:, "isrc"].isna()]
        df_isrc_na.loc[:, "spotify_search_track_name"] = df_isrc_na.loc[
            :, "spotify_search_track_name"
        ].replace(r"\s?\[.+\]", "", regex=True)
        df_isrc_na.loc[:, "spotify_search_track_name"] = df_isrc_na.loc[
            :, "spotify_search_track_name"
        ].replace(r"\s?\(.+\)", "", regex=True)

        df.update(df_isrc_na)

        return df

    def clean_itunes_data_round_1(
        self, df_extracted_apple, df_extracted_external
    ) -> pd.DataFrame:
        df_combined = self._combine_extracted_dataframes(
            df_extracted_apple, df_extracted_external
        )
        df_combined = self._set_isrc(df_combined)
        df_combined = self._rename_columns(df_combined, columns=config.meta_columns)
        df_combined = self._drop_rows_with_no_track_number(df_combined)
        df_combined = self._create_spotify_columns(df_combined)
        df_combined = self._remove_characters(df_combined)
        df_combined = self._remove_duplicates(df_combined)

        return df_combined

    def clean_itunes_data_round_2(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This round of cleaning occurs after the first spotify extraction
        """
        df = self._clean_brackets_from_spotify_track_names(df)
        df = self._remove_characters(df)
        df = self._update_spotify_artists(df, config.artist_updates)
        df = self._update_spotify_tracks(df, config.track_updates)
        df = self._update_spotify_tracks_by_content_id(df, config.track_updates_by_content_id)

        return df

    def clean_itunes_data_round_3(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        This round of cleaning occurs after the second spotify extraction. This is to ensure artist splitting
        does not unintentionally affect changes made when updating spotify artists.
        """
        df = self._split_artists_keep_first_only(df)

        return df

    def clean_itunes_playlist(self, df) -> pd.DataFrame:
        df = self._drop_columns(df, config.playlist_columns_to_drop)
        df = self._rename_columns(df, columns=config.playlist_columns)
        df = self._create_spotify_columns(df)
        df = self._clean_brackets_from_spotify_track_names(df)
        df = self._remove_characters(df)
        df = self._update_spotify_artists(df, config.artist_updates)
        df = self._update_spotify_tracks(df, config.track_updates)
        return df
