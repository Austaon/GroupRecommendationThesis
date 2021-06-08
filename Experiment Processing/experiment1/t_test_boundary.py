import json

from scipy.stats import *

from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.user import SessionUser


def perform_t_test_boundary():
    """
    Performs Welch's unequal variances t-test pairwise on each pair of datasets, for each category, and for each score method.
    The data is stored in the results/t_test_boundaries.json file.

    Like with the `boundary_spotify_data` function, this data was not used for further analysis.
    :return:
    """
    # T-Test:
    # data vs random vs recommended (pair-wise)
    # time span

    # https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_rel.html
    # "This is a two-sided test for the null hypothesis that
    # 2 related or repeated samples have identical average (expected) values."

    # https://blog.minitab.com/blog/adventures-in-statistics-2/understanding-t-tests-t-values-and-t-distributions

    order = [
        ("real", "recommended"),
        ("real", "random"),
        ("recommended", "random")
    ]

    playlist_types = ["real", "recommended", "random"]
    boundary_types = ["binary", "features", "kde", "histogram"]
    categories = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    boundaries_dict = {}
    for playlist_type in playlist_types:
        boundaries_dict[playlist_type] = {}
        for category in categories:
            boundaries_dict[playlist_type][category] = {}
            for boundary in boundary_types:
                boundaries_dict[playlist_type][category][boundary] = []

    count = 0

    for user in SessionUser.objects:

        count += 1
        print(f"User {count} out of 88")

        # The default tracks_function collects the "hovered_tracks" field, which does not exist in the first experiment.
        binary_boundary = BinaryBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())
        features_boundary = BinaryBoundaryWithFeatures(user, tracks_function=lambda u: u.get_chosen_tracks())
        kde_boundary = KDEBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())
        histogram_boundary = HistogramBoundary(user, tracks_function=lambda u: u.get_chosen_tracks())

        for playlist_type in playlist_types:

            for category in categories:
                user_playlist = user.survey[playlist_type][category]

                for track in user_playlist:
                    score_binary, breakdown_binary = binary_boundary.get_boundary_score(track)
                    score_features, breakdown_features = features_boundary.get_boundary_score(track)
                    score_kde, breakdown_kde = kde_boundary.get_boundary_score(track)
                    score_histogram, breakdown_histogram = histogram_boundary.get_boundary_score(track)

                    boundaries_dict[playlist_type][category]["binary"].append(score_binary)
                    boundaries_dict[playlist_type][category]["features"].append(score_features)
                    boundaries_dict[playlist_type][category]["kde"].append(score_kde)
                    boundaries_dict[playlist_type][category]["histogram"].append(score_histogram)

    results = {}

    for boundary_type in boundary_types:
        results[boundary_type] = {}
        for category in ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]:
            temp_result = {}
            for steps in order:
                step_1 = steps[0]
                step_2 = steps[1]

                dict_name = f"{step_1} <-> {step_2}"
                distances_1 = boundaries_dict[step_1][category][boundary_type]
                distances_2 = boundaries_dict[step_2][category][boundary_type]

                temp_result[dict_name] = {
                    "result": str(ttest_ind(distances_1, distances_2, equal_var=False)),
                    "time_span": category,
                    "boundary": boundary_type
                }

            results[boundary_type][category] = temp_result

    with open("experiment1/results/t_test_boundaries.json", "w") as out_file:
        json.dump(results, out_file, indent=4)
