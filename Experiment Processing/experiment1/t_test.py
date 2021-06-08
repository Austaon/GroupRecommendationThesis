import json
from scipy.stats import *

from database.user import SessionUser
from recommender.distance_metrics.cosine_similarity import CosineSimilarity


def perform_t_test():
    """
    Performs Welch's unequal variances t-test pairwise on each pair of datasets, for each category, and for each score method.
    The data is stored in the results/t_test.json file.
    :return:
    """

    # T-Test:
    # data vs random vs recommended (pair-wise)
    # distance metric (separately)
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

    distance_metric = CosineSimilarity()

    distances_dict = {}
    for playlist_type in playlist_types:
        distances_dict[playlist_type] = {}
        for category in ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]:
            distances_dict[playlist_type][category] = []

    count = 0
    for user in SessionUser.objects:

        count += 1
        print(f"User {count} out of 88")

        user_chosen_tracks = [track["id"] for track in user.tracks]
        for playlist_type in playlist_types:

            for category in ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]:
                user_playlist = [track["id"] for track in user.survey[playlist_type][category]]

                distances = list(distance_metric.calculate_ratings(user_chosen_tracks, user_playlist).values())

                if len(distances) != len(user.survey["real"][category]):
                    print(user.spotify_id)
                    print(distances)
                    print(category)
                    print(playlist_type)
                    exit()

                distances_dict[playlist_type][category].extend(distances)

    results = {}

    for category in ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]:
        temp_result = []
        for steps in order:

            step_1 = steps[0]
            step_2 = steps[1]

            dict_name = f"{step_1} <-> {step_2}"
            distances_1 = distances_dict[step_1][category]
            distances_2 = distances_dict[step_2][category]

            temp_result.append({
                "type": dict_name,
                "result": str(ttest_ind(distances_1, distances_2, equal_var=False)),
                "time_span": category,
            })

        results[category] = temp_result

    with open("experiment1/results/t_test_results.json", "w") as out_file:
        json.dump(results, out_file, indent=4)
