import math

import numpy as np

from boundary.BinaryBoundary import BinaryBoundary
from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from database.session import Session

import matplotlib.pyplot as plt

from database.track_data import TrackData


def floor(digit):
    return math.floor(digit * 10) / 10


def plot_boundaries():
    """
    Plots the boundaries of two users and a track selected by them each.
    Can also be used to plot the boundaries of each person by removing the if statement at the top of the loop.
    :return:
    """

    attributes = [
        "acousticness", "danceability", "energy", "instrumentalness",
        "liveness", "loudness", "speechiness", "valence"
    ]

    count = 0

    track_a = {"id": "6j7ShkX2wTd7pXSmRQQtrK"}
    track_b = {"id": "2AVkArcfALVk2X8sfPRzya"}

    example_track_a = TrackData.get_track(track_a).get_metadata()
    example_track_b = TrackData.get_track(track_b).get_metadata()

    for user, session in Session.get_users_with_surveys():

        if not (count == 10 or count == 11):
            count += 1
            continue
        count += 1

        binary_boundary = BinaryBoundary(user)
        features_boundary = BinaryBoundaryWithFeatures(user)
        kde_boundary = KDEBoundary(user)
        histogram_boundary = HistogramBoundary(user)
        print(f"User: {count}")

        fig, axs = plt.subplots(nrows=4, ncols=2, figsize=(13, 13))
        x_index = 0
        y_index = 0

        handles = None
        labels = None

        for feature in attributes:

            histogram_data = histogram_boundary.boundaries[feature]
            kde_data = kde_boundary.boundaries[feature]

            hist_values = np.array(list(histogram_data.values()))
            max_y_value = max(hist_values)

            bins = np.arange(0.1, 1.2, 0.1)

            min_boundary = binary_boundary.boundaries[feature]["min"]
            max_boundary = binary_boundary.boundaries[feature]["max"]

            if max_boundary < min_boundary + 0.02:
                max_boundary = max_boundary + 0.01

            widths = np.array([-0.1 for _ in bins])

            kde_bins = np.linspace(0.0, 1.0, 1000)[: np.newaxis]
            log_score = kde_data.score_samples(kde_bins.reshape(-1, 1))

            ax1 = axs[y_index][x_index]
            ax1.bar(bins, height=hist_values, width=widths, alpha=0.5, label="Histogram", align="edge", color="blue")

            ax1.vlines(
                [min_boundary, max_boundary], ymin=0, ymax=max_y_value,
                linewidth=2, color="#d95f02", label="Boundary"
            )

            ax1.set_xlim(right=1.0)

            ax2 = ax1.twinx()
            ax2.plot(kde_bins, np.exp(log_score), color="#1b9e77", label="KDE", linewidth=2)
            ax2.set_ylim(bottom=0)
            ax2.set_xlim(right=1.0)

            ax1.vlines(
                example_track_a[feature], ymin=0, ymax=max_y_value,
                linewidth=4, color="black", label="Example Track 1", linestyle="dotted"
            )
            ax1.vlines(
                example_track_b[feature], ymin=0, ymax=max_y_value,
                linewidth=4, color="black", label="Example Track 2", linestyle="dashed"
            )

            h1, l1 = ax1.get_legend_handles_labels()
            h2, l2 = ax2.get_legend_handles_labels()

            handles = h1 + h2
            labels = l1 + l2

            ax1.set_xticks(np.arange(0, 1.1, 0.1))
            ax1.tick_params('x', rotation=45)
            ax1.set_title(f"{feature.capitalize()}", fontsize=14)

            x_index += 1
            if x_index >= 2:
                y_index += 1
                x_index = 0

        # 0: Boundary
        # 1: Example Track 1
        # 2: Example Track 2
        # 3: Histogram
        # 4: KDE
        order = [0, 3, 4, 1, 2]

        fig.suptitle(f"Example boundaries, user {'A' if count == 11 else 'B'}", fontsize=20)
        fig.tight_layout()
        fig.legend(
            [handles[idx] for idx in order], [labels[idx] for idx in order],
            loc=9, bbox_to_anchor=(0.5, 0.95), prop={'size': 15}, framealpha=1
        )

        plt.show()
