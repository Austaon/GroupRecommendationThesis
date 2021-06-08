import statistics
from math import isnan

import numpy as np

from database.user import SessionUser

import matplotlib.pyplot as plt

from recommender.distance_metrics.cosine_similarity import CosineSimilarity


def compare_tracks(key="real", plot_data=True):
    """
    Calculates the similarity score for each historical track of each user in each category.
    This average and standard deviation of these data points is printed and a boxplot is generated.
    :param key: The dataset to use: "real", "recommended", or "random"
    :param plot_data:
    :return:
    """
    distance_data = {
        "tracks_short_term": [],
        "tracks_medium_term": [],
        "tracks_long_term": []
    }
    boxplot_data = {
        "tracks_short_term": [],
        "tracks_medium_term": [],
        "tracks_long_term": []
    }
    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    distance_metric = CosineSimilarity()
    count = 0

    for user in SessionUser.objects:
        count += 1
        print(f"User {count} out of 88")

        user_tracks = {track['id']: track for track in user.tracks}

        survey = user.survey[key]

        for category in types:
            spotify_songs = {track['id']: track for track in survey[category]}
            mean_distances = list(distance_metric.calculate_ratings(user_tracks, spotify_songs).values())

            distance_data[category].extend(mean_distances)
            if not isnan(np.mean(mean_distances)):
                boxplot_data[category].append(np.mean(mean_distances))

    for category in types:
        print(f"{category:18s}: mean {statistics.mean(distance_data[category]):.4f}, stdev: {statistics.stdev(distance_data[category]):.4f}")

    if plot_data:
        fig, ax = plt.subplots()

        boxplot_data = [
            boxplot_data["tracks_short_term"],
            boxplot_data["tracks_medium_term"],
            boxplot_data["tracks_long_term"]
        ]

        labels = ["Short Term", "Medium Term", "Long Term"]

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

        ax.set_ylim((0.6, 1.0))
        ax.set_ylabel("Similarity Score")

        fig.tight_layout()
        plt.show()
