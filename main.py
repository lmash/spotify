import logging

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


def add_albums(extractor: DataExtractor, loader: DataLoader):
    """
    - Unpickle
    - Add Albums
    """
    df = extractor.read_pickle("checkpoint_3")
    loader.add_albums_to_spotify(df)


def remove_albums(extractor: DataExtractor, loader: DataLoader):
    """
    - Unpickle
    - Add Albums
    """
    df = extractor.read_pickle("checkpoint_3")
    loader.remove_albums_from_spotify(df)


def round_3(extractor: DataExtractor, cleaner: DataCleaner, linker: DataLinker, loader: DataLoader):
    """
    - Unpickle
    - Clean (round 3)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 3")
    df_combined = extractor.read_pickle("checkpoint_2")
    df_combined = cleaner.clean_itunes_data_round_3(df_combined)
    df_combined = linker.extract_all_isrc_with_na(df_combined)
    df_combined = linker.extract_spotify_album_uri(df_combined)
    loader.pickle(df_combined, "checkpoint_3")


def round_2(extractor: DataExtractor, cleaner: DataCleaner, linker: DataLinker, loader: DataLoader):
    """
    - Unpickle from the backup
    - Clean (round 2)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 2")
    df_combined = extractor.read_pickle("checkpoint_1_backup")
    df_combined = cleaner.clean_itunes_data_round_2(df_combined)
    df_combined = linker.extract_all_isrc_with_na(df_combined)
    loader.pickle(df_combined, "checkpoint_2")


def round_1(extractor: DataExtractor, cleaner: DataCleaner, linker: DataLinker, loader: DataLoader):
    """
    - Extract from apple folder (Apple Music) non apple folder (Music)
    - Clean (round 1)
    - Link with ISRC codes
    - Pickle, create 2 files with the same content, one backup
    """
    logging.info("Round 1")
    df_meta_apple, df_meta_localised = extractor.process_itunes_metadata()
    df_combined = cleaner.clean_itunes_data_round_1(df_meta_apple, df_meta_localised)
    df_combined = linker.extract_all_isrc_with_na(df_combined)

    # Write to Pickle file after initial spotify request
    loader.pickle(df_combined, "checkpoint_1")
    loader.pickle(df_combined, "checkpoint_1_backup")


if __name__ == "__main__":
    logging.info("************************** Convert iTunes to Spotify **************************")
    data_extractor = DataExtractor(mode='TEST')
    data_cleaner = DataCleaner()
    data_linker = DataLinker(spotify=spotify_get())
    data_loader = DataLoader(spotify=spotify_post())

    round_1(data_extractor, data_cleaner, data_linker, data_loader)
    round_2(data_extractor, data_cleaner, data_linker, data_loader)
    round_3(data_extractor, data_cleaner, data_linker, data_loader)

    # Add albums
    # add_albums(data_extractor, data_loader)

    # Remove albums
    # remove_albums(data_extractor, data_loader)

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

