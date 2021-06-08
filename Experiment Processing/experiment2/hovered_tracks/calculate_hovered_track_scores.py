import statistics

from boundary.RatingBoundary import RatingBoundary
from database.session import Session


def calculate_hovered_track_scores():
    """
    Compares the similarity score for the interacted items with those of the three playlists generated for the sessions.

    Not used for further analysis.
    :return:
    """

    playlist_keys = ["PWS", "Fairness", "LM"]

    overall_means = {
            "hovered": [],
            "PWS": [],
            "Fairness": [],
            "LM": []
        }

    for user, session in Session.get_users_with_surveys():

        rating_boundary = RatingBoundary(user)

        user_scores = {
            "hovered": [],
            "PWS": [],
            "Fairness": [],
            "LM": []
        }

        for track_id, track in user.get_hovered_tracks().items():
            score, _ = rating_boundary.get_boundary_score(track_id)
            user_scores["hovered"].append(score)

        for index, playlist in enumerate(session.recommendations):

            playlist_key = playlist_keys[index]

            tracks = playlist["tracks"]
            for track in tracks:
                score, _ = rating_boundary.get_boundary_score(track)
                user_scores[playlist_key].append(score)

        for key, item in user_scores.items():
            overall_means[key].extend(item)

    for key, item in overall_means.items():
        print(f"{key}: {statistics.mean(item):.2f}")
