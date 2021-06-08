from collections import defaultdict
from pprint import pprint

from database.session import Session


def count_matching_artists_per_session():
    """
    Finds the number of times an artist was interacted with multiple times in the same session.
    :return:
    """

    artist_id_name = {}

    for session in Session.get_completed_sessions():

        artists = defaultdict(int)

        for user in session.get_users():

            user_artists = set()

            for track_id, track in user.get_hovered_tracks().items():

                for artist in track["artists"]:
                    user_artists.add(artist["id"])
                    artist_id_name[artist["id"]] = artist["name"]

            for artist in user_artists:
                artists[artist] += 1

        duplicate_artists = {artist: count for artist, count in artists.items() if count >= 2}

        if len(duplicate_artists) > 0:
            print(f"Session: {session.playlist_name}")
            pprint({artist_id_name[artist]: count for artist, count in artists.items() if count >= 2})
