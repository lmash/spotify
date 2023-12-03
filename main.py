import logging

from credentials import spotify
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


if __name__ == "__main__":
    data_extractor = DataExtractor()
    data_cleaner = DataCleaner()
    data_linker = DataLinker(spotify=spotify)
    data_loader = DataLoader(spotify=spotify)

    # df_meta_apple, df_meta_localised = data_extractor.process_itunes_metadata()
    # df_combined = data_cleaner.clean_itunes_data_round_1(df_meta_apple, df_meta_localised)
    # df_combined = data_linker.extract_all_isrc_with_na(df_combined)
    #
    # # Write to Pickle file after initial spotify request
    # data_loader.pickle(df_combined, "combined")
    # data_loader.pickle(df_combined, "combined_backup")
    #
    # df_combined = data_extractor.read_pickle("combined_backup")
    # df_combined = data_cleaner.clean_itunes_data_round_2(df_combined)
    # df_combined = data_linker.extract_all_isrc_with_na(df_combined)
    # data_loader.pickle(df_combined, "combined")
    #
    df_combined = data_extractor.read_pickle("combined")
    # df_combined = data_cleaner.clean_itunes_data_round_3(df_combined)
    # df_combined = data_linker.extract_all_isrc_with_na(df_combined)
    # data_loader.pickle(df_combined, "combined")

    # Playlists
    # df_playlist = data_extractor.read_playlist('Enjoy the Ride.txt')
    # df_playlist = data_cleaner.clean_itunes_playlist(df_playlist)
    # df_playlist = data_linker.extract_all_isrc_with_na(df_playlist)

    # See if adding tracks works
    single_album = df_combined[df_combined['album'] == 'Suede']
    tracks = single_album['spotify_track_uri'].to_list()
    print('here')

    result = data_loader.add_tracks_to_spotify(tracks=tracks)
