import statistics as st
from pprint import pprint

from matplotlib import pyplot
from scipy import stats

import numpy as np
import matplotlib.pyplot as plt

from database.session import Session


def parse_int(playlist_string):
    return int(''.join(filter(str.isdigit, playlist_string)))


abbreviations = {
    "Probability Weighted Sum": "PWS",
    "Fairness": "F",
    "Least Misery": "LM"
}


def plot_results_own_other(data, range_object, labels, figure_title):
    result = f"Overall ({figure_title}):\n"

    boxplot_data = []
    boxplot_labels = []

    for index, playlist, in enumerate(data):
        if playlist == "global":
            continue

        boxplot_data.append(data[playlist][labels[0]])
        boxplot_data.append(data[playlist][labels[1]])

        boxplot_labels.append(f"{abbreviations[playlist]} - next") # {labels[0]}")
        boxplot_labels.append(f"{abbreviations[playlist]} - others") # {labels[1]}")

    fig1, ax1 = plt.subplots()

    pyplot.locator_params(axis='y', nbins=5)

    ax1.boxplot(boxplot_data, labels=boxplot_labels,
                boxprops=dict(linestyle='-', linewidth=1.5),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='-', linewidth=1.5),
                capprops=dict(linestyle='-', linewidth=1.5),
                showfliers=True)
    ax1.set_ylim((0.8, 5.2))
    ax1.set_ylabel("Survey Rating")
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    plt.xticks(rotation=-45, ha="left", rotation_mode="anchor")

    fig1.tight_layout()

    fig, axs = plt.subplots(ncols=2, nrows=3)
    label_range = range(range_object[0], range_object[1])
    for index, playlist, in enumerate(data):

        playlist_data = data[playlist]
        ow_data = playlist_data[labels[0]]
        ot_data = playlist_data[labels[1]]
        result += f"{playlist:24}: " \
                  f"{labels[0]}: {st.mean(ow_data):.2f} ({st.stdev(ow_data):.2f}), " \
                  f"{labels[1]}: {st.mean(ot_data):.2f} ({st.stdev(ot_data):.2f}), \n"

        if playlist == "global":
            continue

        own_labels, own_data = np.unique(playlist_data[labels[0]], return_counts=True)
        other_labels, other_data = np.unique(playlist_data[labels[1]], return_counts=True)

        for label in label_range:
            if label not in own_labels:
                if label <= len(label_range) / 2:
                    own_data = np.insert(own_data, 0, 0)
                else:
                    own_data = np.append(own_data, 0)

            if label not in other_labels:
                if label < len(label_range) / 2:
                    other_data = np.insert(other_data, 0, 0)
                else:
                    other_data = np.append(other_data, 0)

        axs[index, 0].bar(label_range, own_data)
        axs[index, 1].bar(label_range, other_data, color="orange")

    pad = 5  # in points

    for ax, col in zip(axs[0], labels):
        ax.annotate(col, xy=(0.5, 1), xytext=(0, pad),
                    xycoords='axes fraction', textcoords='offset points',
                    size='large', ha='center', va='baseline')
    for ax, row in zip(axs[:, 0], ["PWS", "Fairness", "LM"]):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')

    for ax in axs.reshape(-1):
        ax.set_xticks(label_range)

    fig.suptitle(figure_title, fontsize=16)
    fig.tight_layout()
    plt.show()

    print(result[:-3])


def periodic_effects():
    """
    Compares multiple different combinations of survey ratings to see if any periodic effects occurred in the playlists.

    (This code is a bit of a mess, and very similar to `compare_selected_versus_not_selected`.)

    The survey key can be modified in the code below.
    :return:
    """

    key = "like_rating_specific"
    # key = "suitable_rating_specific"

    ratings = {
        "Probability Weighted Sum": {"own": [], "other": []},
        "Fairness": {"own": [], "other": []},
        "Least Misery": {"own": [], "other": []},
        "global": {"own": [], "other": []}
    }

    rating_after_own_track = {
        "Probability Weighted Sum": {"one": [], "two": []},
        "Fairness": {"one": [], "two": []},
        "Least Misery": {"one": [], "two": []},
        "global": {"one": [], "two": []}
    }

    rating_after_own_track_not_own = {
        "Probability Weighted Sum": {"one": [], "two": []},
        "Fairness": {"one": [], "two": []},
        "Least Misery": {"one": [], "two": []},
        "global": {"one": [], "two": []}
    }

    rating_one_and_all_others = {
        "Probability Weighted Sum": {"one": [], "two": []},
        "Fairness": {"one": [], "two": []},
        "Least Misery": {"one": [], "two": []},
        "global": {"one": [], "two": []}
    }

    for user, session in Session.get_users_with_surveys():

        user_tracks = [track["id"] for track in user.tracks]

        for playlist, playlist_string in user.get_playlists_from_survey():
            playlist_index = parse_int(playlist_string)

            recommended_playlist = session.recommendations[playlist_index - 1]["tracks"]
            playlist_rule = playlist["rule_name"]

            user_tracks_vector = [
                1 if recommended_playlist[parse_int(song) - 1]["id"] in user_tracks else 0
                for song, rating in playlist[key].items()
            ]

            specific_ratings = [
                int(rating)
                for song, rating in playlist[key].items()
            ]

            ratings[playlist_rule]["own"].extend([
                rating for index, rating in enumerate(specific_ratings)
                if user_tracks_vector[index]
            ])
            ratings[playlist_rule]["other"].extend([
                rating for index, rating in enumerate(specific_ratings)
                if not user_tracks_vector[index]
            ])
            ratings["global"]["own"].extend([
                rating for index, rating in enumerate(specific_ratings)
                if user_tracks_vector[index]
            ])
            ratings["global"]["other"].extend([
                rating for index, rating in enumerate(specific_ratings)
                if not user_tracks_vector[index]
            ])

            rating_after_own_track[playlist_rule]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1]
            ])
            rating_after_own_track[playlist_rule]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 1 and user_tracks_vector[index - 2]
            ])
            rating_after_own_track["global"]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1]
            ])
            rating_after_own_track["global"]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 1 and user_tracks_vector[index - 2]
            ])

            rating_after_own_track_not_own[playlist_rule]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1] and not user_tracks_vector[index]
            ])
            rating_after_own_track_not_own[playlist_rule]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 1 and user_tracks_vector[index - 2] and not user_tracks_vector[index]
            ])

            rating_after_own_track_not_own["global"]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1] and not user_tracks_vector[index]
            ])
            rating_after_own_track_not_own["global"]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 1 and user_tracks_vector[index - 2] and not user_tracks_vector[index]
            ])

            rating_one_and_all_others[playlist_rule]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1] and not user_tracks_vector[index]
            ])
            rating_one_and_all_others[playlist_rule]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if (index == 0 and not user_tracks_vector[index]) or
                   (index > 0 and not user_tracks_vector[index - 1] and not user_tracks_vector[index])
            ])
            rating_one_and_all_others["global"]["one"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if index > 0 and user_tracks_vector[index - 1] and not user_tracks_vector[index]
            ])
            rating_one_and_all_others["global"]["two"].extend([
                specific_ratings[index]
                for index, rating in enumerate(specific_ratings)
                if (index == 0 and not user_tracks_vector[index]) or
                   (index > 0 and not user_tracks_vector[index - 1] and not user_tracks_vector[index])
            ])

    plot_results_own_other(ratings, (1, 6), ["own", "other"], "Absolute ratings")
    plot_results_own_other(rating_after_own_track, (1, 6), ["one", "two"], "Rating of tracks 1 and 2 after own track")
    plot_results_own_other(rating_after_own_track_not_own, (1, 6), ["one", "two"],
                           "Rating of tracks 1 and 2 after own track (no own songs)")
    plot_results_own_other(rating_one_and_all_others, (1, 6), ["one", "two"],
                           "Ratings of items following a selected item and the other non-selected items")

    for playlist in rating_one_and_all_others:
        print(f"{playlist} ->")
        print(
            f"One track after (df = {len(rating_one_and_all_others[playlist]['one'])}): "
            f"{stats.ttest_ind(rating_one_and_all_others[playlist]['one'], ratings[playlist]['other'], equal_var=False)}")
        print(
            f"Two tracks after (df = {len(rating_one_and_all_others[playlist]['two'])}): "
            f"{stats.ttest_ind(rating_one_and_all_others[playlist]['two'], ratings[playlist]['other'], equal_var=False)}")
