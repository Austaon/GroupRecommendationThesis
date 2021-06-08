import statistics

from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.session import Session


def boundary_rating():
    """
    Calculates the different scores separated for each survey rating and prints the mean / standard deviation per rating.

    Also attempts to see if a score can be a predictor for a survey rating (spoiler: doesn't seem like it), but
    this was not used further.
    :return:
    """

    scores = {
        "binary": [],
        "features": [],
        "kde": [],
        "histogram": [],
    }

    rating_comparison = {
        "binary": {1: [], 2: [], 3: [], 4: [], 5: []},
        "features": {1: [], 2: [], 3: [], 4: [], 5: []},
        "kde": {1: [], 2: [], 3: [], 4: [], 5: []},
        "histogram": {1: [], 2: [], 3: [], 4: [], 5: []},
    }

    rating_key = "like_rating_specific"

    reverse_object = {
        "binary": [],
        "features": [],
        "kde": [],
        "histogram": []
    }

    rating_histogram = {
        0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0
    }

    for user, session in Session.get_users_with_surveys():

        binary_boundary = BinaryBoundary(user)
        features_boundary = BinaryBoundaryWithFeatures(user)
        kde_boundary = KDEBoundary(user)
        histogram_boundary = HistogramBoundary(user)

        survey = user.get_survey()

        for playlist_index, playlist in enumerate(session.recommendations):
            ratings = survey[f"playlist{playlist_index + 1}"][rating_key]

            for track_index, track in enumerate(playlist["tracks"]):

                score_binary, _ = binary_boundary.get_boundary_score(track)
                score_features, _ = features_boundary.get_boundary_score(track)
                score_kde, _ = kde_boundary.get_boundary_score(track)
                score_histogram, _ = histogram_boundary.get_boundary_score(track)

                scores["binary"].append(score_binary)
                scores["features"].append(score_features)
                scores["kde"].append(score_kde)
                scores["histogram"].append(score_histogram)

                rating = int(ratings[f'Song{track_index + 1}'])

                rating_histogram[rating] += 1
                rating_histogram[6] += 1

                rating_comparison["binary"][rating].append(score_binary)
                rating_comparison["features"][rating].append(score_features)
                rating_comparison["kde"][rating].append(score_kde)
                rating_comparison["histogram"][rating].append(score_histogram)

                reverse_object["binary"].append({
                    "boundary": score_binary,
                    "rating": rating
                })
                reverse_object["features"].append({
                    "boundary": score_features,
                    "rating": rating
                })
                reverse_object["kde"].append({
                    "boundary": score_kde,
                    "rating": rating
                })
                reverse_object["histogram"].append({
                    "boundary": score_histogram,
                    "rating": rating
                })

    for method, bins in rating_comparison.items():
        method_string = f"{method:9s} -> "
        for rating_bin, scores in bins.items():
            method_string += f"{rating_bin}: {statistics.mean(scores):.3f}, {statistics.stdev(scores):.3f}, "
        method_string = method_string[:-2]
        print(method_string)

    print(rating_histogram)

    reverse_object["features"].sort(key=lambda x: x["boundary"])
    reverse_object["histogram"].sort(key=lambda x: x["boundary"])
    reverse_object["kde"].sort(key=lambda x: x["boundary"])

    steps = []
    previous_value = 0

    for i in range(1, 6):
        steps.append((
            previous_value, rating_histogram[i] + previous_value
        ))
        previous_value += rating_histogram[i]

    for i in range(5):

        lower_bound = steps[i][0]
        upper_bound = steps[i][1]

        slice_features = reverse_object["features"][lower_bound:upper_bound]
        slice_histogram = reverse_object["histogram"][lower_bound:upper_bound]
        slice_kernel = reverse_object["kde"][lower_bound:upper_bound]

        print([x['rating'] for x in slice_features])

        ratings_features = [t["rating"] for t in slice_features]
        ratings_histogram = [t["rating"] for t in slice_histogram]
        ratings_kernel = [t["rating"] for t in slice_kernel]

        amount_correct_features = [x for x in ratings_features if x == (i+1)]
        amount_correct_histogram = [x for x in ratings_histogram if x == (i+1)]
        amount_correct_kernel = [x for x in ratings_kernel if x == (i+1)]

        print(f"{lower_bound} - {upper_bound} -> "
              f"({statistics.mean(ratings_features):.2f}, {statistics.mean(ratings_histogram):.2f}, {statistics.mean(ratings_kernel):.2f}) "
              f"{sum(amount_correct_features) / (upper_bound - lower_bound):.2f} "
              f"{sum(amount_correct_histogram) / (upper_bound - lower_bound):.2f} "
              f"{sum(amount_correct_kernel) / (upper_bound - lower_bound):.2f}")
