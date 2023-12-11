from dataclasses import dataclass
from pathlib import Path

DATA_PATH = Path('.data/')
CHECKPOINTS_PATH = DATA_PATH / 'checkpoints'
HISTORY_PATH = DATA_PATH / 'history'
PLAYLIST_PATH = DATA_PATH / 'playlist'

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


# meta_columns = {
#     "Track": "track_number",
#     "Sort Name": "track_name",
#     "Sort Artist": "artist",
#     "Release Date": "release_date",
#     "Sort Album": "album",
#     "Content ID": "content_id",
#     "Artist ID": "artist_id",
#     "Playlist ID": "playlist_id",
#     "Genre ID": "genre_id",
#     "Composer ID": "composer_id",
#     "iTunes Store Country": "itunes_stores_country",
#     "Part of Compilation": "part_of_compilation",
#     "Composer": "composer",
#     "Disk": "disk",
#     "GenreType": "genre_type",
#     "Album Artist": "album_artist",
#     "Genre": "genre",
# }

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
        artist="Chikinki",
        from_spotify_search_track_name="Like A See-Saw",
        to_spotify_search_track_name="Like A Seesaw",
    ),
    SpotifyTrackName(
        artist="Skin",
        from_spotify_search_track_name="Til Morning Comes",
        to_spotify_search_track_name="Til Morning",
    ),
    SpotifyTrackName(
        artist="Suede",
        from_spotify_search_track_name="Pantomine Horse",
        to_spotify_search_track_name="Pantomime Horse",
    ),
    SpotifyTrackName(
        artist="Parov Stelar",
        from_spotify_search_track_name="True Romance Part 2",
        to_spotify_search_track_name="True Romance, Pt.2",
    ),
    SpotifyTrackName(
        artist="Heather Nova",
        from_spotify_search_track_name="When Somebody Turns You On",
        to_spotify_search_track_name="When Someone Turns You On",
    ),
    SpotifyTrackName(
        artist="Enigma",
        from_spotify_search_track_name="I Love You ... Ill Kill You",
        to_spotify_search_track_name="I Love You... Ill Kill You",
    ),
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
    SpotifyTrackName(
        artist="Nirvana",
        from_spotify_search_track_name="Something In The Way / Endless, Nameless",
        to_spotify_search_track_name="Something In The Way",
    ),
    SpotifyTrackName(
        artist="Madonna",
        from_spotify_search_track_name="The Power Of Goodbye",
        to_spotify_search_track_name="The Power Of Good-Bye",
    ),
    SpotifyTrackName(
        artist="George Michael",
        from_spotify_search_track_name="A Moment With You",
        to_spotify_search_track_name="Moment With You",
    ),
    SpotifyTrackName(
        artist="George Michael",
        from_spotify_search_track_name="Killer / Papa Was A Rolling Stone",
        to_spotify_search_track_name="Killer / Papa Was A Rollin Stone",
    ),
    SpotifyTrackName(
        artist="Rae Spoon",
        from_spotify_search_track_name="My Heart Is a Piece of Garbage. Fight Segulls!...",
        to_spotify_search_track_name="My Heart Is a Piece of Garbage. Fight Seagulls! Fight!",
    ),
    SpotifyTrackName(
        artist="The Cure",
        from_spotify_search_track_name="The Caterpiller",
        to_spotify_search_track_name="The Caterpillar",
    ),
    SpotifyTrackName(
        artist="Sia",
        from_spotify_search_track_name="The Girl You Lost To Cocaine",
        to_spotify_search_track_name="The Girl You Lost",
    ),
    SpotifyTrackName(
        artist="Lenny Kravitz",
        from_spotify_search_track_name="What The Fuck Are We Saying?",
        to_spotify_search_track_name="What The .... Are We Saying?",
    ),
    SpotifyTrackName(
        artist="Jamiroquai",
        from_spotify_search_track_name="Love Blind",
        to_spotify_search_track_name="Loveblind",
    ),
    SpotifyTrackName(
        artist="Ennio Morricone",
        from_spotify_search_track_name="Once Upon A Time In American",
        to_spotify_search_track_name="Once Upon A Time in America (Deborah's Theme)",
    ),
    SpotifyTrackName(
        artist="Soap&Skin",
        from_spotify_search_track_name="DDMMYYYY",
        to_spotify_search_track_name="Ddmmyy",
    ),
    SpotifyTrackName(
        artist="Hayley Williams",
        from_spotify_search_track_name="Roses / Lotus / Violet / Iris",
        to_spotify_search_track_name="Roses/Lotus/Violet/Iris",
    ),
    SpotifyTrackName(
        artist="Brian Eno",
        from_spotify_search_track_name="Zawinul / Lava",
        to_spotify_search_track_name="Zawinul/Lava - 2004 Remaster",
    ),
    SpotifyTrackName(
        artist="LSD",
        from_spotify_search_track_name="Genius",
        to_spotify_search_track_name="Genius (feat. Sia, Diplo, and Labrinth) - Lil Wayne Remix",
    ),
    SpotifyTrackName(
        artist="Scary Mansion",
        from_spotify_search_track_name="Over The Weekend",
        to_spotify_search_track_name="Over The Week End",
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
    SpotifyTrackNameByContentId(
        content_id='724357853',
        to_spotify_search_track_name="The Big Ship",
    ),
    SpotifyTrackNameByContentId(
        content_id='250112772',
        to_spotify_search_track_name="The Story",
    ),
    SpotifyTrackNameByContentId(
        content_id='1440951234',
        to_spotify_search_track_name="The Wake-Up Bomb",
    ),
    SpotifyTrackNameByContentId(
        content_id='1571671153',
        to_spotify_search_track_name="The Sidewinder Sleeps Tonite",
    ),
    SpotifyTrackNameByContentId(
        content_id='1440713987',
        to_spotify_search_track_name="The Mans Too Strong",
    ),
    SpotifyTrackNameByContentId(
        content_id='1458625982',
        to_spotify_search_track_name="The Moth",
    ),
    SpotifyTrackNameByContentId(
        content_id='1458625613',
        to_spotify_search_track_name="The Sandman",
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
        from_spotify_search_album="Schubert: The Complete Impromptus - Moments Musicaux",
        to_spotify_search_album="Schubert: The Complete Impromptus/Moments Musicaux"
    ),
    SpotifyAlbum(
        from_spotify_search_album="The Beach Boys 20 Golden Greats",
        to_spotify_search_album="The Beach Boys: 20 Golden Greats"
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
