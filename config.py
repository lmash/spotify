from dataclasses import dataclass

playlist_columns_to_drop = [
    "Grouping", "Work", "Movement Number", "Movement Count", "Movement Name", "Size", "Time",
    "Date Modified", "Date Added", "Bit Rate", "Sample Rate", "Volume Adjustment", "Kind",
    "Equaliser", "Comments", "Plays", "Last Played", "Skips", "Last Skipped", "My Rating",
    "Location", "Disc Count", "Track Count"
]


meta_columns = {
    "Track": "track_number",
    "Sort Name": "track_name",
    "Sort Artist": "artist",
    "Release Date": "release_date",
    "Sort Album": "album",
    "Content ID ": "content_id",
    "Artist ID": "artist_id",
    "Playlist ID": "playlist_id",
    "Genre ID": "genre_id",
    "Composer ID": "composer_id",
    "iTunes Store Country": "itunes_stores_country",
    "Part of Compilation": "part_of_compilation",
    "Composer": "composer",
    "Disk": "disk",
    "GenreType": "genre_type",
    "Album Artist": "album_artist",
    "Genre": "genre",
}

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
    artist remains constant
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
]


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
    SpotifyArtist(
        from_spotify_search_artist="Moby Feat. Azure Ray", to_spotify_search_artist="Moby",
    ),
    SpotifyArtist(
        from_spotify_search_artist="Moby Feat. MC Lyte & Angie Stone", to_spotify_search_artist="Moby",
    ),
    SpotifyArtist(
        from_spotify_search_artist="R.E.M. Feat. KRS-One", to_spotify_search_artist="R.E.M.",
    ),
    SpotifyArtist(
        from_spotify_search_artist="R.E.M. Feat. Kate Pearson", to_spotify_search_artist="R.E.M.",
    ),
    SpotifyArtist(
        from_spotify_search_artist="Aretha Franklin & George Michael", to_spotify_search_artist="George Michael",
    ),
    SpotifyArtist(
        from_spotify_search_artist="George Michael With Queen", to_spotify_search_artist="George Michael",
    ),
]
