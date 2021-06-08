import statistics

from database.user import SessionUser

import matplotlib.pyplot as plt


def calculate_mutual_tracks(key="real", plot_data=True):
    """
    Finds the number of tracks that are in both the selected data and the given dataset in each time range.
    The average and standard deviation are printed and a boxplot is generated.
    :param key: The dataset to use: "real", "recommended", or "random"
    :param plot_data:
    :return:
    """
    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]

    result = {
        "tracks_short_term": [],
        "tracks_medium_term": [],
        "tracks_long_term": []
    }

    count = 0
    for user in SessionUser.objects:

        count += 1
        print(f"User {count} out of 88")
        chosen_tracks = user.tracks

        for category in types:
            top_tracks = user.survey[key][category]
            result[category].append(len([t for t in top_tracks if t in chosen_tracks]))

    for category in types:
        print(
            f"{category:18s}: mean {statistics.mean(result[category]):.2f}, stdev: {statistics.stdev(result[category]):.2f}")

    if plot_data:
        fig, ax = plt.subplots()

        boxplot_data = [
            result["tracks_short_term"],
            result["tracks_medium_term"],
            result["tracks_long_term"]
        ]

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
