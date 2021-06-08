import statistics

from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.session import Session

attributes = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "loudness", "speechiness", "valence"
]


def boundary_playlists():
    """
    Compares the scores calculated for specific aggregation strategies with each other and with survey ratings.

    Not really used much.
    :return:
    """

    playlist_names = {
        "playlist1": "PWS",
        "playlist2": "Fairness",
        "playlist3": "LM"
    }

    playlist_scores = {
        "binary": {"PWS": [], "Fairness": [], "LM": []},
        "features": {"PWS": [], "Fairness": [], "LM": []},
        "kde": {"PWS": [], "Fairness": [], "LM": []},
        "histogram": {"PWS": [], "Fairness": [], "LM": []},
    }

    rating_comparison = {
        "binary": {"PWS": {1: [], 2: [], 3: [], 4: [], 5: []},
                   "Fairness": {1: [], 2: [], 3: [], 4: [], 5: []},
                   "LM": {1: [], 2: [], 3: [], 4: [], 5: []}},
        "features": {"PWS": {1: [], 2: [], 3: [], 4: [], 5: []},
                     "Fairness": {1: [], 2: [], 3: [], 4: [], 5: []},
                     "LM": {1: [], 2: [], 3: [], 4: [], 5: []}},
        "kde": {"PWS": {1: [], 2: [], 3: [], 4: [], 5: []},
                "Fairness": {1: [], 2: [], 3: [], 4: [], 5: []},
                "LM": {1: [], 2: [], 3: [], 4: [], 5: []}},
        "histogram": {"PWS": {1: [], 2: [], 3: [], 4: [], 5: []},
                      "Fairness": {1: [], 2: [], 3: [], 4: [], 5: []},
                      "LM": {1: [], 2: [], 3: [], 4: [], 5: []}},
    }

    rating_key = "like_rating_specific"

    for user, session in Session.get_users_with_surveys():

        binary_boundary = BinaryBoundary(user)
        features_boundary = BinaryBoundaryWithFeatures(user)
        kde_boundary = KDEBoundary(user)
        histogram_boundary = HistogramBoundary(user)

        survey = user.get_survey()

        for playlist_index, playlist in enumerate(session.recommendations):
            ratings = survey[f"playlist{playlist_index+1}"][rating_key]
            playlist_string = playlist_names[f"playlist{playlist_index + 1}"]

            for track_index, track in enumerate(playlist["tracks"]):
                if track in user.tracks:
                    continue

                score_binary, breakdown_binary = binary_boundary.get_boundary_score(track)
                score_features, breakdown_features = features_boundary.get_boundary_score(track)
                score_kde, breakdown_kde = kde_boundary.get_boundary_score(track)
                score_histogram, breakdown_histogram = histogram_boundary.get_boundary_score(track)

                playlist_scores["binary"][playlist_string].append(score_binary)
                playlist_scores["features"][playlist_string].append(score_features)
                playlist_scores["kde"][playlist_string].append(score_kde)
                playlist_scores["histogram"][playlist_string].append(score_histogram)

                rating = int(ratings[f'Song{track_index + 1}'])

                rating_comparison["binary"][playlist_string][rating].append(score_binary)
                rating_comparison["features"][playlist_string][rating].append(score_features)
                rating_comparison["kde"][playlist_string][rating].append(score_kde)
                rating_comparison["histogram"][playlist_string][rating].append(score_histogram)

    for method, playlists in playlist_scores.items():
        method_string = f"{method}:\n"
        for playlist, scores in playlists.items():
            method_string += f"{playlist}: {statistics.mean(scores):.2f}, "
        print(method_string[:-2])

    for method, playlists in rating_comparison.items():
        method_string = f"{method:9s} -> \n"
        for playlist, bins in playlists.items():
            method_string += f"{'':13s}{playlist}: "
            for rating_bin, scores in bins.items():
                method_string += f"{rating_bin}: {statistics.mean(scores):.2f}, "
            method_string += "\n"
        print(method_string)
