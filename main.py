import logging

import utils
from credentials import spotify_get, spotify_post
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


def add_albums(loader: DataLoader):
    """
    - Unpickle
    - Add Albums
    """
    df = utils.read_pickle_df("3_cleaned")
    loader.add_albums_to_spotify(df)


def remove_albums(loader: DataLoader):
    """
    - Unpickle
    - Add Albums
    """
    df = utils.read_pickle_df("3_cleaned")
    loader.remove_albums_from_spotify(df)


def round_3(cleaner: DataCleaner, linker: DataLinker):
    """
    - Unpickle
    - Clean (round 3)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 3")
    df_combined = utils.read_pickle_df("2_cleaned")
    df_combined = cleaner.clean_itunes_data_round_3(df_combined)
    df_combined = linker.extract_all_isrc_with_na(df_combined)
    df_combined = linker.extract_spotify_album_uri(df_combined)
    utils.to_pickle_df(df_combined, "3_cleaned")


def round_2(cleaner: DataCleaner, linker: DataLinker):
    """
    - Unpickle from the backup
    - Clean (round 2)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 2")
    df_combined = utils.read_pickle_df("1_cleaned")
    df_combined = cleaner.clean_itunes_data_round_2(df_combined)
    df_combined = linker.extract_all_isrc_with_na(df_combined)
    utils.to_pickle_df(df_combined, "2_cleaned")


def round_1(cleaner: DataCleaner, linker: DataLinker):
    """
    - Extract from apple folder (Apple Music) non apple folder (Music)
    - Clean (round 1)
    - Link with ISRC codes
    - Pickle, create 2 files with the same content, one backup
    """
    logging.info("Round 1")
    df = utils.read_pickle_df("1_extracted")
    df = cleaner.clean_itunes_data_round_1(df)
    df = linker.extract_all_isrc_with_na(df)

    # Write to Pickle file after initial spotify request
    utils.to_pickle_df(df, "1_cleaned")


def extract(extractor: DataExtractor, cleaner: DataCleaner):
    logging.info("Extract from apple folder (Apple Music) non apple folder (Music)")
    df_meta_apple, df_meta_localised = extractor.process_itunes_metadata()
    df_combined = cleaner.clean_itunes_extracted(df_meta_apple, df_meta_localised)

    # Write to Pickle file after extraction
    utils.to_pickle_df(df_combined, "1_extracted")


if __name__ == "__main__":
    logging.info("************************** Convert iTunes to Spotify **************************")
    data_extractor = DataExtractor(mode='PROD')
    data_cleaner = DataCleaner()
    data_linker = DataLinker(spotify=spotify_get())
    data_loader = DataLoader(spotify=spotify_post())

    # extract(data_extractor, data_cleaner)
    # round_1(data_cleaner, data_linker)
    # round_2(data_cleaner, data_linker)
    # round_3(data_cleaner, data_linker)

    # Add albums
    add_albums(data_loader)

    # Remove albums
    # remove_albums(data_loader)

    # Good for tracing
    # df = data_extractor.read_pickle("combined")
    # data_linker.extract_isrc(df, "Suede", "The Next Life")

    # Playlists
    # df_playlist = data_extractor.read_playlist('Enjoy the Ride.txt')
    # df_playlist = data_cleaner.clean_itunes_playlist(df_playlist)
    # df_playlist = data_linker.extract_all_isrc_with_na(df_playlist)

    # See if adding tracks works
    # single_album = df_combined[df_combined['album'] == 'Suede']
    # tracks = single_album['spotify_track_uri'].to_list()
    # result = data_loader.add_tracks_to_spotify(tracks=tracks)

