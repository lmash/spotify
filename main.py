import argparse
import logging


from credentials import spotify_get, spotify_post
from data_cleaning import DataCleaner
from data_extraction import DataExtractor
from data_linking import DataLinker
from data_loading import DataLoader
from data_reporting import DataReporter
import log  # Do not remove
import utils

logger = logging.getLogger(__name__)


def load_albums(loader: DataLoader):
    """
    - Unpickle
    - Add Albums
    """
    logging.info("Load albums into Spotify Library")
    df = utils.read_pickle_df("2_cleaned")
    loader.add_albums_to_spotify(df)


def remove_albums(loader: DataLoader):
    """
    - Unpickle
    - Remove Albums
    """
    df = utils.read_pickle_df("2_cleaned")
    loader.remove_albums_from_spotify(df)


def round_2(cleaner: DataCleaner, linker: DataLinker):
    """
    - Unpickle
    - Clean (round 2)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 3")
    df_combined = utils.read_pickle_df("1_cleaned")
    df_combined = cleaner.clean_itunes_data_round_2(df_combined)
    df_combined = linker.extract_spotify_album_uri(df_combined)

    utils.to_pickle_df(df_combined, "2_cleaned")


def round_1(cleaner: DataCleaner, linker: DataLinker):
    """
    - Unpickle
    - Clean (round 1)
    - Link with ISRC codes
    - Pickle
    """
    logging.info("Round 1")
    df = utils.read_pickle_df("1_extracted")
    df = cleaner.clean_itunes_data_round_1(df)
    df = linker.extract_all_isrc_with_na(df)

    utils.to_pickle_df(df, "1_cleaned")


def extract(extractor: DataExtractor, cleaner: DataCleaner):
    logging.info("Extract from apple folder (Apple Music) non apple folder (Music)")
    df_meta_apple, df_meta_localised = extractor.process_itunes_metadata()
    df_combined = cleaner.clean_itunes_extracted(df_meta_apple, df_meta_localised)

    utils.to_pickle_df(df_combined, "1_extracted")


def extract_from_library_xml(extractor: DataExtractor):
    logging.info("Extract from Apple Library XML")
    df = extractor.read_tracks_from_apple_library()

    utils.to_pickle_df(df, "1_extracted")


def extract_playlists(extractor: DataExtractor):
    logging.info("Extract playlists from Library.xml")
    df = extractor.read_playlists_from_apple_library()

    utils.to_pickle_df(df, "playlist_extracted")


def clean_playlists(cleaner: DataCleaner):
    logging.info("Clean playlists ")
    df_playlist = utils.read_pickle_df("playlist_extracted")
    df_tracks = utils.read_pickle_df("2_cleaned")
    df_playlist = cleaner.clean_itunes_playlist(df_playlist, df_tracks)

    utils.to_pickle_df(df_playlist, "playlist_cleaned")


def load_playlists(loader: DataLoader):
    logging.info("Add playlists to Spotify Library")
    df_playlist = utils.read_pickle_df("playlist_cleaned")
    loader.add_playlists(df_playlist)


def remove_playlists(loader: DataLoader):
    # TODO
    logging.info("Remove playlists NOT IMPLEMENTED")
    pass


def load_tracks(loader: DataLoader):
    logging.info("Add tracks to Spotify Library")
    df = utils.read_pickle_df("2_cleaned")
    loader.add_tracks_to_spotify(df)


def nuke(loader: DataLoader):
    """Remove current users tracks, albums, playlists from Spotify"""
    logging.info("Nuke current users spotify tracks, albums and playlists... OUCH!")
    loader.nuke_playlists()
    loader.nuke_albums()
    loader.nuke_tracks()


def report(reporter: DataReporter):
    logging.info("Report")
    df = utils.read_pickle_df("2_cleaned")
    df_playlists = utils.read_pickle_df("playlist_cleaned")
    reporter.albums(df)
    reporter.playlists(df_playlists)
    reporter.tracks(df)


def loading_into_spotify(args) -> bool:
    """Return True if runtime argument selected will load data into spotify"""
    if any((args.run, args.playlist == "load", args.playlist == "remove", args.nuke)):
        return True
    return False


def verify_user(loader: DataLoader, skip_verification: bool) -> bool:
    """
    Display username and id to console and wait for confirmation before continuing
    This is to prevent inadvertently loading data against another user
    """
    if skip_verification:
        return True

    print(f"Loading for user_name {loader.user_name} user_id: {loader.user_id}")
    proceed = input(f"Enter 'Y' or 'y' to continue ...\n")
    return True if proceed in ("Y", "y") else False


def get_parser():
    parser = argparse.ArgumentParser(description="Convert iTunes files to Spotify")
    parser.add_argument(
        "-r",
        "--run",
        help="Extract, clean, load tracks, albums & playlists from Library.xml",
        action="store_true",
    )

    parser.add_argument(
        "-e",
        "--extract",
        help="extract from Apple Media Music folders",
        action="store_true",
    )
    parser.add_argument(
        "-efl",
        "--extract-from-library",
        help="extract from Apple Library XML",
        action="store_true",
    )
    parser.add_argument("-c", "--clean", help="clean data", action="store_true")
    parser.add_argument(
        "-la", "--load-albums", help="load albums into spotify", action="store_true"
    )
    parser.add_argument(
        "-ra", "--remove-albums", help="remove albums from spotify", action="store_true"
    )
    parser.add_argument(
        "-lt", "--load-tracks", help="load tracks into spotify", action="store_true"
    )

    parser.add_argument(
        "-p",
        "--playlist",
        help="Playlist choices",
        choices=["extract", "clean", "load", "remove", "ecl"],
    )

    parser.add_argument(
        "--nuke",
        help="Spotify nuke current users tracks, albums & playlists! Warning!!!! This will remove ALL items selected "
        "(Not only those in Library.XML)",
        action="store_true",
    )

    parser.add_argument(
        "--skip-verify", help="Skip user verification", action="store_true"
    )

    return parser


def command_line_runner(
    data_extractor, data_cleaner, data_linker, data_loader, data_reporter
):
    parser = get_parser()
    args = parser.parse_args()

    if loading_into_spotify(args) and not verify_user(data_loader, args.skip_verify):
        print("Processing aborted")
        return

    logging.info(
        "************************** Convert iTunes to Spotify **************************"
    )
    logging.info("See spotify.log for debug logging")

    if args.run:
        # Extract and clean albums and tracks
        extract_from_library_xml(data_extractor)
        round_1(data_cleaner, data_linker)
        round_2(data_cleaner, data_linker)

        # Extract and clean playlists
        extract_playlists(data_extractor)
        clean_playlists(data_cleaner)

        # Load
        load_albums(data_loader)
        load_playlists(data_loader)
        load_tracks(data_loader)
        report(data_reporter)
        return

    if args.nuke:
        nuke(data_loader)
        return

    if args.extract:
        extract(data_extractor, data_cleaner)
        return

    if args.extract_from_library:
        # Workaround when cannot be run from users PC, use Library.xml to get albums, tracks and playlists.
        # This method doesn't get xid's
        extract_from_library_xml(data_extractor)
        return

    if args.clean:
        round_1(data_cleaner, data_linker)
        round_2(data_cleaner, data_linker)

    if args.load_albums:
        load_albums(data_loader)

    if args.remove_albums:
        remove_albums(data_loader)

    if args.load_tracks:
        load_tracks(data_loader)

    if args.playlist:
        if args.playlist == "extract":
            extract_playlists(data_extractor)
        elif args.playlist == "clean":
            clean_playlists(data_cleaner)
        elif args.playlist == "load":
            load_playlists(data_loader)
        elif args.playlist == "remove":
            remove_playlists(data_loader)
        else:
            extract_playlists(data_extractor)
            clean_playlists(data_cleaner)
            load_playlists(data_loader)


if __name__ == "__main__":
    data_cleaner = DataCleaner()
    data_linker = DataLinker(spotify=spotify_get())
    data_loader = DataLoader(spotify=spotify_post())
    data_extractor = DataExtractor(mode="PROD")
    data_reporter = DataReporter()

    command_line_runner(
        data_extractor, data_cleaner, data_linker, data_loader, data_reporter
    )
