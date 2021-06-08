import itertools
import statistics

import matplotlib.pyplot as plt
from matplotlib import pyplot

from database.session import Session


def parse_int(playlist_string):
    return int(''.join(filter(str.isdigit, playlist_string)))


def compare_selected_tracks_versus_not_selected():
    """
    Compares survey ratings of songs chosen by a user versus chosen by others and prints/plots it.

    The survey key can be modified in the code below.
    :return:
    """
    key = "like_rating_specific"
    # key = "suitable_rating_specific"

    specific_ratings = {
        "Probability Weighted Sum": {"own": [], "other": []},
        "Fairness": {"own": [], "other": []},
        "Least Misery": {"own": [], "other": []}
    }

    global_ratings = {
        "own": [], "other": []
    }

    for user, session in Session.get_users_with_surveys():

        user_tracks = [track["id"] for track in user.tracks]

        for playlist, playlist_string in user.get_playlists_from_survey():
            playlist_index = parse_int(playlist_string)

            recommended_playlist = session.recommendations[playlist_index - 1]["tracks"]

            playlist_rule = playlist["rule_name"]

            specific_ratings[playlist_rule]["own"].extend(
                [
                    int(rating)
                    for song, rating in playlist[key].items()
                    if recommended_playlist[parse_int(song) - 1]["id"] in user_tracks
                ]
            )
            global_ratings["own"].extend(
                [
                    int(rating)
                    for song, rating in playlist[key].items()
                    if recommended_playlist[parse_int(song) - 1]["id"] in user_tracks
                ]
            )
            specific_ratings[playlist_rule]["other"].extend(
                [
                    int(rating)
                    for song, rating in playlist[key].items()
                    if recommended_playlist[parse_int(song) - 1]["id"] not in user_tracks
                ]
            )
            global_ratings["other"].extend(
                [
                    int(rating)
                    for song, rating in playlist[key].items()
                    if recommended_playlist[parse_int(song) - 1]["id"] not in user_tracks
                ]
            )

    result = "Overall:\n"

    boxplot_data_own = {
        f"own-{playlist}": specific_ratings[playlist]['own'] for playlist in specific_ratings
    }
    boxplot_data_other = {
        f"other-{playlist}": specific_ratings[playlist]['other'] for playlist in specific_ratings
    }
    boxplot_data = [
        boxplot_data_own["own-Probability Weighted Sum"],
        boxplot_data_other["other-Probability Weighted Sum"],
        boxplot_data_own["own-Fairness"],
        boxplot_data_other["other-Fairness"],
        boxplot_data_own["own-Least Misery"],
        boxplot_data_other["other-Least Misery"],
    ]

    for playlist in specific_ratings:
        playlist_data = specific_ratings[playlist]
        result += f"{playlist:24s}: own: {statistics.mean(playlist_data['own']):.2f}," \
                  f" other: {statistics.mean(playlist_data['other']):.2f}, \n"

    result += f"{'Global':24s}: own: {statistics.mean(global_ratings['own']):.2f}, "
    result += f"other: {statistics.mean(global_ratings['other']):.2f}"

    print(result)

    labels = ["PWS", "F", "LM"]
    labels = [f"{rule} - {own_other}" for rule, own_other in itertools.product(labels, ["own", "other"])]

    fig, ax = plt.subplots()

    ax.boxplot(boxplot_data, labels=labels,
               boxprops=dict(linestyle='-', linewidth=1.5),
               medianprops=dict(linestyle='-', linewidth=2),
               whiskerprops=dict(linestyle='-', linewidth=1.5),
               capprops=dict(linestyle='-', linewidth=1.5),
               showfliers=True
               )

    pyplot.locator_params(axis='y', nbins=5)

    ax.set_xticklabels(labels)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    ax.set_ylim((0.8, 5.2))
    ax.set_ylabel("Survey Rating")

    plt.xticks(rotation=-45, ha="left", rotation_mode="anchor")

    fig.tight_layout()
    plt.show()
