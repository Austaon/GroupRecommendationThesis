import datetime
import statistics

import numpy as np
from matplotlib import pylab

from database.track_data import TrackData
from database.user import SessionUser

import matplotlib.pyplot as plt
import pandas as pd


def calculate_mutual_artists(key="real", plot_data=True):
    """
    Finds the number of artists that are in both the selected data and the given dataset in each time range.
    The average and standard deviation are printed and a boxplot is generated.
    :param key: The dataset to use: "real", "recommended", or "random"
    :param plot_data:
    :return:
    """

    types = ["artists_short_term", "artists_medium_term", "artists_long_term"]

    result = {
        "artists_short_term": [],
        "artists_medium_term": [],
        "artists_long_term": []
    }

    count = 0
    for user in SessionUser.objects:

        count += 1
        print(f"User {count} out of 88")

        chosen_artists = []
        for track in user.tracks:
            track_data = TrackData.objects(track_id=track["id"])[0]
            chosen_artists.append(track_data.artist_id)

        for category in types:
            top_artists = user.survey[key][category]
            result[category].append(len([a for a in top_artists if a["id"] in chosen_artists]))

    for category in types:
        print(
            f"{category}: mean {statistics.mean(result[category]):.2f}, stdev: {statistics.stdev(result[category]):.2f}")

    if plot_data:
        fig, ax = plt.subplots()

        boxplot_data = [result["artists_short_term"], result["artists_medium_term"], result["artists_long_term"]]

        labels = ["Short Term", "Medium Term", "Long Term"]

        ax.boxplot(boxplot_data, labels=labels,
                   boxprops=dict(linestyle='-', linewidth=1.5),
                   medianprops=dict(linestyle='-', linewidth=2),
                   whiskerprops=dict(linestyle='-', linewidth=1.5),
                   capprops=dict(linestyle='-', linewidth=1.5),
                   showfliers=True
                   )

        ax.set_xticklabels(labels)
        ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

        ax.set_ylim((0, 10))
        ax.set_ylabel("Matching Items")

        fig.tight_layout()
        plt.show()
