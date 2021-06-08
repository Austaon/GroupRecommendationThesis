import statistics

import numpy as np

from database.user import SessionUser

import matplotlib.pyplot as plt

from recommender.distance_metrics.cosine_similarity import CosineSimilarity


def compare_datasets(key_1, key_2):
    """
    Compares the distances of the tracks in two different datasets for each users and prints/boxplots them.

    The resulting data from this function is not used for further analysis.
    :param key_1:
    :param key_2:
    :return:
    """
    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    differences = {
        "tracks_short_term": [],
        "tracks_medium_term": [],
        "tracks_long_term": []
    }

    distance_metric = CosineSimilarity()
    count = 0

    for user in SessionUser.objects:
        count += 1
        print(f"User {count} out of 88")

        user_tracks = [track["id"] for track in user.tracks]

        for category in types:

            tracks_1 = [track["id"] for track in user.survey[key_1][category]]
            tracks_2 = [track["id"] for track in user.survey[key_2][category]]

            distances_1 = distance_metric.calculate_ratings(
                user_tracks, tracks_1
            )
            distances_2 = distance_metric.calculate_ratings(
                user_tracks, tracks_2
            )

            differences[category] += [score_1 - score_2 for score_1, score_2 in
                                      zip(distances_1.values(), distances_2.values())
                                      ]

    for category in types:
        print(
            f"{category:18s}: mean {statistics.mean(differences[category]):.4f}, stdev: {statistics.stdev(differences[category]):.4f}")

    fig, ax = plt.subplots()

    boxplot_data = [
        differences["tracks_short_term"],
        differences["tracks_medium_term"],
        differences["tracks_long_term"]
    ]

    labels = ["Short term", "Medium term", "Long term"]

    ax.boxplot(boxplot_data, labels=labels,
               boxprops=dict(linestyle='-', linewidth=1.5),
               medianprops=dict(linestyle='-', linewidth=2),
               whiskerprops=dict(linestyle='-', linewidth=1.5),
               capprops=dict(linestyle='-', linewidth=1.5),
               showfliers=False
               )

    ax.set_xticklabels(labels)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.locator_params(axis='y', nbins=5)

    ax.set_ylabel("Similarity Score")

    fig.tight_layout()
    plt.show()
