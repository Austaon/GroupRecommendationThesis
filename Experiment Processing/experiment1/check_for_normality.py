import datetime

import numpy as np
from matplotlib import pylab
import matplotlib.pyplot as plt
from scipy.stats import normaltest

from database.user import SessionUser
from recommender.distance_metrics.cosine_similarity import CosineSimilarity


def check_for_normality(key="real", plot_data=True):
    """
    Plots a histogram of the distances calculated by a distance metric.
    This can be used to check if the distribution of the distances follows a normal distribution.
    :param key:
    :param plot_data:
    :return:
    """
    distance_data = {
        "tracks_short_term": [],
        "tracks_medium_term": [],
        "tracks_long_term": []
    }

    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    distance_metric = CosineSimilarity()

    for user in SessionUser.objects:
        user_tracks = [track["id"] for track in user.tracks]

        user_survey = user.survey[key]

        for category in types:
            spotify_songs = [track["id"] for track in user_survey[category]]
            mean_distances = list(distance_metric.calculate_ratings(user_tracks, spotify_songs).values())

            distance_data[category].extend(mean_distances)

    if plot_data:
        params = {'legend.fontsize': 'xx-large',
                  'figure.figsize': (15, 5),
                  'axes.labelsize': 'xx-large',
                  'axes.titlesize': 'xx-large',
                  'xtick.labelsize': 'xx-large',
                  'ytick.labelsize': 'xx-large'}
        pylab.rcParams.update(params)

        histogram_data = (
            distance_data["tracks_short_term"],
            distance_data["tracks_medium_term"],
            distance_data["tracks_long_term"]
        )

        plt.hist(histogram_data, label=("short", "medium", "long"))

        plt.legend(loc="upper left")
        plt.title(f"{key}: {datetime.datetime.now()}")
        plt.show()

    print(f"Short: {normaltest(distance_data['tracks_short_term'])}")
    print(f"Medium: {normaltest(distance_data['tracks_medium_term'])}")
    print(f"Long: {normaltest(distance_data['tracks_long_term'])}")