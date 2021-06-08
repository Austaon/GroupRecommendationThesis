from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.session import Session

attributes = [
    "acousticness", "danceability", "energy", "instrumentalness",
    "liveness", "loudness", "speechiness", "valence"
]


def boundary_features_breakdown():
    """
    Checks the breakdown of each score, to see if any audio feature stands out.

    The results are as expected, the features with a non-skewed distribution have lower scores, so the results were not
    interesting enough to mention further.
    :return:
    """

    feature_scores = {
        "binary": {a: 0 for a in attributes},
        "features": {a: 0 for a in attributes},
        "kde": {a: 0 for a in attributes},
        "histogram": {a: 0 for a in attributes},
    }

    for user, session in Session.get_users_with_surveys():

        binary_boundary = BinaryBoundary(user)
        features_boundary = BinaryBoundaryWithFeatures(user)
        kde_boundary = KDEBoundary(user)
        histogram_boundary = HistogramBoundary(user)

        for playlist_index, playlist in enumerate(session.recommendations):

            for track_index, track in enumerate(playlist["tracks"]):

                if track in user.tracks:
                    continue

                score_binary, breakdown_binary = binary_boundary.get_boundary_score(track)
                score_features, breakdown_features = features_boundary.get_boundary_score(track)
                score_kde, breakdown_kde = kde_boundary.get_boundary_score(track)
                score_histogram, breakdown_histogram = histogram_boundary.get_boundary_score(track)

                for a, score in breakdown_binary.items():
                    feature_scores["binary"][a] += score
                for a, score in breakdown_features.items():
                    feature_scores["features"][a] += score
                for a, score in breakdown_kde.items():
                    feature_scores["kde"][a] += score
                for a, score in breakdown_histogram.items():
                    feature_scores["histogram"][a] += score

    for method, scores in feature_scores.items():
        method_string = f"{method}:\n"
        for a, score in scores.items():
            method_string += f"{a}: {score:.2f}, "
        print(method_string[:-2])
