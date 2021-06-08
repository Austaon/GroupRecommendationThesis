import random
import string
from collections import defaultdict
from pprint import pprint

from spotipy import SpotifyException

from database.user import SessionUser
from util.login_spotify import login_spotify


def random_search(spotify_api, item_type="track"):
    """
    Uses the Spotify Search API to return a list of random tracks.

    The query it executes consists of:
    - A random lower bound between 1950 and 2019
    - A random upper bound between the lower bound and 2019
    - A single random (ASCII) letter as query

    The first query is used to collect the number of items that are available for this query (max. 1000)
    It is then executed again with a random offset between 0 and 950 (or 0 if less than 50 items are available)

    If this results in a list of tracks, it is returned, else up to 5 retries are done.
    If these retries do not result in any success, execution is stopped.

    :param spotify_api:
    :param item_type:
    :return: List of tracks
    """
    tracks = []

    counter = 0

    while len(tracks) == 0:

        if counter > 5:
            print("Could not find enough items")
            exit()

        lower_bound = random.randrange(1950, 2019)
        upper_bound = random.randrange(lower_bound, 2020)
        query = random.choice(string.ascii_letters)

        search_data = spotify_api.search(f"{query} year:{lower_bound}-{upper_bound}",
                                         type=item_type, limit=50)

        total = search_data[f"{item_type}s"]["total"]
        if total < 50:
            offset = 0
        else:
            offset = random.randrange(0, min(950, total))

        try:
            tracks = spotify_api.search(
                f"{query} year:{lower_bound}-{upper_bound}",
                type=item_type, limit=50, offset=offset
            )[f"{item_type}s"]["items"]
        except SpotifyException as _:
            print(total)
            print(offset)
            exit()

        counter += 1

    return tracks


def generate_random_data():
    """
    Generates random track lists and stores it for each user.
    An explanation of the random algorithm can be found in the `random_search` function.
    :return:
    """
    sp = login_spotify()

    track_count = defaultdict(int)

    count = 0

    for user in SessionUser.objects:

        count += 1

        print(f"{count} / 88")

        track_object = {
            "tracks_short_term": [],
            "tracks_medium_term": [],
            "tracks_long_term": [],
            "artists_short_term": [],
            "artists_medium_term": [],
            "artists_long_term": []
        }

        for t in ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]:

            chosen_track_ids = []

            for _ in range(len(user.survey["real"][t])):
                searched_tracks = random_search(sp, "track")

                searched_tracks = [t for t in searched_tracks if t["id"] not in chosen_track_ids]

                chosen_track = random.choices(searched_tracks, k=1)[0]

                track_count[chosen_track["id"]] += 1
                track_object[t].append(chosen_track)
                chosen_track_ids.append(chosen_track["id"])

        user.survey["random"] = track_object
        user.save()

    print(len({k: v for k, v in track_count.items() if v >= 2}))
    print(f"{len(track_count)}")
    print(len({k: v for k, v in track_count.items() if v >= 2}) / len(track_count))
