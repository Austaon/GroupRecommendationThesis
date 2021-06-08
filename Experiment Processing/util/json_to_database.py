import json
import os
from os import listdir
from os.path import isfile, join
from pprint import pprint

from database.user import SessionUser
from util.login_spotify import login_spotify


def json_to_database():
    """
    Loads the json files from the first experiment into a database, the folder can be specified by changing the
    folder_name variable.
    The SessionUser class is hijacked, which means some code can be re-used. This also means that some variable names
    are unintuitive.
    Specifically: the "survey" field is used to store historical data, since MongoDB accepts any JSON object.
    The "tracks" field is used to store the selected tracks and the "email_address" field is used to store the feedback.

    :return:
    """
    sp = login_spotify()

    count = 0

    folder_name = "experiment1/json_files"

    all_json_files = [f for f in listdir(folder_name) if isfile(join(folder_name, f))]

    for file_name in all_json_files:

        count += 1
        print(f"{count} / 88")

        with open(f"{folder_name}/{file_name}") as file:
            json_data = json.load(file)

            chosen_tracks = json_data["chosen_tracks"]

            track_data = sp.tracks(chosen_tracks)["tracks"]

            fake_survey = {
                "real": {"artists_short_term": [], "artists_medium_term": [], "artists_long_term": [],
                         "tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
                "recommended": {"artists_short_term": [], "artists_medium_term": [], "artists_long_term": [],
                                "tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
                "random": {"artists_short_term": [], "artists_medium_term": [], "artists_long_term": [],
                           "tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []}
            }

            if "tracks_short_term" in json_data["top_tracks"]:
                fake_survey["real"]["tracks_short_term"] = sp.tracks(
                    json_data["top_tracks"]["tracks_short_term"]
                )["tracks"]
            else:
                fake_survey["real"]["tracks_short_term"] = []

            if "tracks_medium_term" in json_data["top_tracks"]:
                fake_survey["real"]["tracks_medium_term"] = sp.tracks(
                    json_data["top_tracks"]["tracks_medium_term"]
                )["tracks"]
            else:
                fake_survey["real"]["tracks_medium_term"] = []

            if "tracks_long_term" in json_data["top_tracks"]:
                fake_survey["real"]["tracks_long_term"] = sp.tracks(
                    json_data["top_tracks"]["tracks_long_term"]
                )["tracks"]
            else:
                fake_survey["real"]["tracks_long_term"] = []

            if "artists_short_term" in json_data["top_tracks"]:
                fake_survey["real"]["artists_short_term"] = sp.artists(
                    json_data["top_tracks"]["artists_short_term"]
                )["artists"]
            else:
                fake_survey["real"]["artists_short_term"] = []

            if "artists_medium_term" in json_data["top_tracks"]:
                fake_survey["real"]["artists_medium_term"] = sp.artists(
                    json_data["top_tracks"]["artists_medium_term"]
                )["artists"]
            else:
                fake_survey["real"]["artists_medium_term"] = []

            if "artists_long_term" in json_data["top_tracks"]:
                fake_survey["real"]["artists_long_term"] = sp.artists(
                    json_data["top_tracks"]["artists_long_term"]
                )["artists"]
            else:
                fake_survey["real"]["artists_long_term"] = []

            new_user = SessionUser(
                spotify_id=json_data["user_id"],
                tracks=track_data,
                survey=fake_survey,
                email_address=json_data["feedback"]
            )
            new_user.save()
