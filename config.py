from dataclasses import dataclass
import os
from pathlib import Path

DATA_PATH = Path('.data/')
CHECKPOINTS_PATH = DATA_PATH / 'checkpoints'
HISTORY_PATH = DATA_PATH / 'history'
PLAYLIST_PATH = DATA_PATH / 'playlist'

if os.name == 'nt':
    ITUNES_PATH = Path('Music/iTunes/iTunes Media')
else:
    ITUNES_PATH = Path('Music/Music/Media.localized')

playlists_exclude = (
    "Library", "Downloaded", "Music", "All Music", "90’s Music", "Classical Music", "Music Videos",
    "Playlist", "Recently Played", "Top 25 Most Played", "Album Artwork Screen Saver", "Repeats"
)

playlist_columns_to_drop = [
    "Grouping", "Work", "Movement Number", "Movement Count", "Movement Name", "Size", "Time",
    "Date Modified", "Date Added", "Bit Rate", "Sample Rate", "Volume Adjustment", "Kind",
    "Equaliser", "Comments", "Plays", "Last Played", "Skips", "Last Skipped", "My Rating",
    "Location", "Disc Count", "Track Count"
]


playlist_columns = {
    "Name": "track_name",
    "Artist": "artist",
    "Composer": "composer",
    "Album": "album",
    "Genre": "genre",
    "Disc Number": "disk",
    "Track Number": "track_number",
    "Year": "release_date",
}


@dataclass
class SpotifyTrackName:
    """
    Updating a column from a value to a value always needs to contain a field which does not change.
    artist remains constant.
    content_id added to handle special cases where track_name is na
    """

    artist: str
    from_spotify_search_track_name: str
    to_spotify_search_track_name: str


track_updates = [
    SpotifyTrackName(
        artist="Faithless",
        from_spotify_search_track_name="Miss You Less, See You More",
        to_spotify_search_track_name="Miss U Less, See U More",
    ),
    SpotifyTrackName(
        artist="Faithless",
        from_spotify_search_track_name="Muhammed Ali",
        to_spotify_search_track_name="Muhammad Ali",
    ),
]


@dataclass
class SpotifyTrackNameByContentId:
    """
    Some of the metadata is missing a track name. Manually check iTunes to find the missing track. Use the
    content_id to update as it's unique
    """
    content_id: str
    to_spotify_search_track_name: str


track_updates_by_content_id = [
    SpotifyTrackNameByContentId(
        content_id='1485137457',
        to_spotify_search_track_name="The Last Time",
    ),
]


@dataclass
class SpotifyAlbum:
    from_spotify_search_album: str
    to_spotify_search_album: str


album_updates = [
    SpotifyAlbum(
        from_spotify_search_album='Coco Part 1',
        to_spotify_search_album='Coco, Pt. 1'
    ),
    SpotifyAlbum(
        from_spotify_search_album='Coco Part 2',
        to_spotify_search_album='Coco, Pt. 2'
    ),
    SpotifyAlbum(
        from_spotify_search_album='The Princess: The Vinyl Collection 2010 - 2012',
        to_spotify_search_album='The Princess, Pt. Two'
    ),
    SpotifyAlbum(
        from_spotify_search_album="Live At St. Annes Warehouse",
        to_spotify_search_album="Live At St. Anns Warehouse"
    ),
    SpotifyAlbum(
        from_spotify_search_album="Paint The Sky With Stars: The Best Of Enya",
        to_spotify_search_album="Paint The Sky With Stars"
    ),
    SpotifyAlbum(
        from_spotify_search_album="Superior You Are Inferior",
        to_spotify_search_album="Superioryouareinferior"
    ),
    SpotifyAlbum(
        from_spotify_search_album=" Morning Glory?",
        to_spotify_search_album="(Whats The Story) Morning Glory?"
    ),
    SpotifyAlbum(
        from_spotify_search_album="Keren Ann 2007",
        to_spotify_search_album="Keren Ann"
    ),
    SpotifyAlbum(
        from_spotify_search_album="Songs in the Key of Life - Disc 2",
        to_spotify_search_album="Songs in the Key of Life"
    ),
]


# A set of albums to ignore (as they're being incorrectly requested, many soundtracks)
albums_ignore = {'Folk Tunes, Vol. 2', 'Virus', 'Woman II', 'Chilled Euphoria',
                 'Pump Up The Volume', 'In The Name Of The Father', 'Reality Bites',
                 'City Of Angels', 'Stealing Beauty', 'Point Of No Return','Pulp Fiction'
                 }


@dataclass
class SpotifyArtist:
    """
    Updating a column from a value to a value always needs to contain a field which does not change.
    meta_track_name remains constant
    """

    from_spotify_search_artist: str
    to_spotify_search_artist: str


artist_updates = [
    SpotifyArtist(
        from_spotify_search_artist="The London Suede", to_spotify_search_artist="Suede",
    ),
]
