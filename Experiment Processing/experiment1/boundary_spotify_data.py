import statistics

from boundary.AverageBoundary import AverageBoundary
from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.session import Session
from database.user import SessionUser

attributes = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "loudness", "speechiness", "valence"
]


def boundary_spotify_data(key="real"):
    """
    Uses the different scores introduced in the second experiment and calculates a score for each user.
    The considered dataset can be set with the key parameter.

    The data from this function was not used for further analysis.

    :param key: The dataset to use: "real", "recommended", or "random"
    :return:
    """

    playlist_scores = {
        "binary": {"tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
        "features": {"tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
        "kde": {"tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
        "histogram": {"tracks_short_term": [], "tracks_medium_term": [], "tracks_long_term": []},
    }

    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    count = 0

    for user in SessionUser.objects:

        count += 1
        print(f"User {count} out of 88")

        # The default tracks_function collects the "hovered_tracks" field, which does not exist in the first experiment.
        binary_boundary = BinaryBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())
        features_boundary = BinaryBoundaryWithFeatures(user, tracks_function=lambda u: u.get_chosen_tracks())
        kde_boundary = KDEBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())
        histogram_boundary = HistogramBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())

        for category in types:
            if len(user.survey[key][category]) < 5:
                continue

            playlist = user.survey[key][category]

            for track_index, track in enumerate(playlist):

                score_binary, breakdown_binary = binary_boundary.get_boundary_score(track)
                score_features, breakdown_features = features_boundary.get_boundary_score(track)
                score_kde, breakdown_kde = kde_boundary.get_boundary_score(track)
                score_histogram, breakdown_histogram = histogram_boundary.get_boundary_score(track)

                playlist_scores["binary"][category].append(score_binary)
                playlist_scores["features"][category].append(score_features)
                playlist_scores["kde"][category].append(score_kde)
                playlist_scores["histogram"][category].append(score_histogram)

    for method, playlists in playlist_scores.items():
        method_string = f"{method}:\n"
        for playlist, scores in playlists.items():
            method_string += f"{playlist}: {statistics.mean(scores):.2f}, "
        print(method_string[:-2])

# Real
# binary:
# tracks_short_term: 2.66, tracks_medium_term: 2.55, tracks_long_term: 2.21
# features:
# tracks_short_term: 6.46, tracks_medium_term: 6.43, tracks_long_term: 6.31
# kde:
# tracks_short_term: 3.10, tracks_medium_term: 3.07, tracks_long_term: 3.07
# histogram:
# tracks_short_term: 3.08, tracks_medium_term: 3.06, tracks_long_term: 3.01


# Recommended
# binary:
# tracks_short_term: 1.43, tracks_medium_term: 1.65, tracks_long_term: 1.57
# features:
# tracks_short_term: 6.16, tracks_medium_term: 6.11, tracks_long_term: 6.12
# kde:
# tracks_short_term: 3.04, tracks_medium_term: 3.04, tracks_long_term: 3.03
# histogram:
# tracks_short_term: 2.93, tracks_medium_term: 2.93, tracks_long_term: 2.95

# Random
# binary:
# tracks_short_term: 0.79, tracks_medium_term: 0.86, tracks_long_term: 0.88
# features:
# tracks_short_term: 5.50, tracks_medium_term: 5.48, tracks_long_term: 5.46
# kde:
# tracks_short_term: 2.83, tracks_medium_term: 2.82, tracks_long_term: 2.85
# histogram:
# tracks_short_term: 2.65, tracks_medium_term: 2.63, tracks_long_term: 2.65
