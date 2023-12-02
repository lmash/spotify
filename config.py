from dataclasses import dataclass


@dataclass
class ColumnMap:
    artist_name: str
    from_column: str
    to_column: str


meta_columns = {
    "Track": "meta_track_number",
    "Sort Name": "meta_track_name",
    "Sort Artist": "meta_artist",
    "Release Date": "meta_release_date",
    "Sort Album": "meta_album",
    "Content ID ": "meta_content_id",
    "Artist ID": "meta_artist_id",
    "Playlist ID": "meta_playlist_id",
    "Genre ID": "meta_genre_id",
    "Composer ID": "meta_composer_id",
    "iTunes Store Country": "meta_itunes_stores_country",
    "Part of Compilation": "meta_part_of_compilation",
    "Composer": "meta_composer",
    "Disk": "meta_disk",
    "GenreType": "meta_genre_type",
    "Album Artist": "meta_album_artist",
    "Genre": "meta_genre",
}


@dataclass
class SpotifyTrackName:
    """
    Updating a column from a value to a value always needs to contain a field which does not change.
    meta_artist remains constant
    """

    meta_artist: str
    from_spotify_search_track_name: str
    to_spotify_search_track_name: str


track_updates = [
    SpotifyTrackName(
        meta_artist="Chikinki",
        from_spotify_search_track_name="Like A See-Saw",
        to_spotify_search_track_name="Like A Seesaw",
    ),
    SpotifyTrackName(
        meta_artist="Skin",
        from_spotify_search_track_name="Til Morning Comes",
        to_spotify_search_track_name="Til Morning",
    ),
    SpotifyTrackName(
        meta_artist="Suede",
        from_spotify_search_track_name="Pantomine Horse",
        to_spotify_search_track_name="Pantomime Horse",
    ),
    SpotifyTrackName(
        meta_artist="Parov Stelar",
        from_spotify_search_track_name="True Romance Part 2",
        to_spotify_search_track_name="True Romance, Pt.2",
    ),
    SpotifyTrackName(
        meta_artist="Heather Nova",
        from_spotify_search_track_name="When Somebody Turns You On",
        to_spotify_search_track_name="When Someone Turns You On",
    ),
    SpotifyTrackName(
        meta_artist="Enigma",
        from_spotify_search_track_name="I Love You ... Ill Kill You",
        to_spotify_search_track_name="I Love You... Ill Kill You",
    ),
    SpotifyTrackName(
        meta_artist="Faithless",
        from_spotify_search_track_name="Miss You Less, See You More",
        to_spotify_search_track_name="Miss U Less, See U More",
    ),
    SpotifyTrackName(
        meta_artist="Faithless",
        from_spotify_search_track_name="Muhammed Ali",
        to_spotify_search_track_name="Muhammad Ali",
    ),
    SpotifyTrackName(
        meta_artist="Nirvana",
        from_spotify_search_track_name="Something In The Way / Endless, Nameless",
        to_spotify_search_track_name="Something In The Way",
    ),
    SpotifyTrackName(
        meta_artist="Madonna",
        from_spotify_search_track_name="The Power Of Goodbye",
        to_spotify_search_track_name="The Power Of Good-Bye",
    ),
    SpotifyTrackName(
        meta_artist="George Michael",
        from_spotify_search_track_name="A Moment With You",
        to_spotify_search_track_name="Moment With You",
    ),
    SpotifyTrackName(
        meta_artist="George Michael",
        from_spotify_search_track_name="Killer / Papa Was A Rolling Stone",
        to_spotify_search_track_name="Killer / Papa Was A Rollin Stone",
    ),
    SpotifyTrackName(
        meta_artist="Rae Spoon",
        from_spotify_search_track_name="My Heart Is a Piece of Garbage. Fight Segulls!...",
        to_spotify_search_track_name="My Heart Is a Piece of Garbage. Fight Seagulls! Fight!",
    ),
    SpotifyTrackName(
        meta_artist="The Cure",
        from_spotify_search_track_name="The Caterpiller",
        to_spotify_search_track_name="The Caterpillar",
    ),
    SpotifyTrackName(
        meta_artist="Sia",
        from_spotify_search_track_name="The Girl You Lost To Cocaine",
        to_spotify_search_track_name="The Girl You Lost",
    ),
    SpotifyTrackName(
        meta_artist="Lenny Kravitz",
        from_spotify_search_track_name="What The Fuck Are We Saying?",
        to_spotify_search_track_name="What The .... Are We Saying?",
    ),
    SpotifyTrackName(
        meta_artist="Jamiroquai",
        from_spotify_search_track_name="Love Blind",
        to_spotify_search_track_name="Loveblind",
    ),
    SpotifyTrackName(
        meta_artist="Ennio Morricone",
        from_spotify_search_track_name="Once Upon A Time In American",
        to_spotify_search_track_name="Once Upon A Time in America (Deborah's Theme)",
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
]
