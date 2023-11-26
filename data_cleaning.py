import logging
import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    def __init__(self):
        pass

    @staticmethod
    def _combine_extracted_dataframes(df_extracted_apple, df_extracted_external) -> pd.DataFrame:
        """Combine dataframes extracted from apple and non apple music folders"""
        df_apple = df_extracted_apple.copy()
        df_external = df_extracted_external.copy()

        # Drop columns
        df_apple = df_apple.drop(columns=[
            "Copyright", "Content Rating", "Media Type", "iTunes Account", "Cover Art pieces", "ReadAtom"
        ])
        df_external = df_external.drop(columns=[
            "Encoded with", "BPM", "Part of Gapless Album", "Cover Art pieces", "Copyright", "Content Rating",
            "Media Type", 'CRî" 1184108314 vs 7910639', "CRî is suspect", "iTunes Account", "Purchase Date", "ReadAtom",
            "iTunes Account Type", "Comments", "TV Episode", "TV Season", "Sort Composer", "TV Show", "Sort Name",
            "Sort Artist", "Sort Album"
        ])

        df_external = df_external.rename(
            columns={"Name": "Sort Name", "Artist": "Sort Artist", "Album": "Sort Album"})

        # Combine into a single dataframe
        df_combined = pd.concat([df_apple, df_external])

        return df_combined

    @staticmethod
    def _set_isrc(df: pd.DataFrame) -> pd.DataFrame:
        """
        xid has format: <ReleasedBy>:isrc:<ISRC Code>
        Extract ISRC from xid, add it as a new column and remove xid column
        """
        logger.debug("Extract the ISRC from xid")
        try:
            df.loc[:, "isrc"] = df.loc[:, "xid"].apply(lambda x: x.split(":")[-1])
        except AttributeError:
            df.loc[:, "isrc"] = np.nan

        df = df.drop(columns=["xid"])

        return df

    @staticmethod
    def _rename_columns(df:pd.DataFrame) -> pd.DataFrame:
        """Renames columns & set column names to lowercase and make them python friendly"""
        df = df.rename(
            columns={"Track": "track", "Sort Name": "name", "Sort Artist": "artist", "Release Date": "release_date",
                     "Sort Album": "album", "Content ID ": "content_id", "Artist ID": "artist_id",
                     "Playlist ID": "playlist_id", "Genre ID": "genre_id", "Composer ID": "composer_id",
                     "iTunes Store Country": "itunes_stores_country", "Part of Compilation": "part_of_compilation",
                     "Composer": "composer", "Disk": "disk", "GenreType": "genre_type", "Album Artist": "album_artist",
                     "Genre": "genre"})

        return df

    def clean_itunes_data(self, df_extracted_apple, df_extracted_external) -> pd.DataFrame:
        df_combined = self._combine_extracted_dataframes(df_extracted_apple, df_extracted_external)
        df_combined = self._set_isrc(df_combined)
        df_combined = self._rename_columns(df_combined)

        return df_combined
