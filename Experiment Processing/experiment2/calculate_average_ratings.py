import statistics

from matplotlib import pyplot

from database.session import Session
import matplotlib.pyplot as plt


def calculate_average_ratings():
    """
    Calculates the average rating for each playlist and prints/plots it.
    The key can be specified in the code below.
    :return:
    """
    key = "like_rating"
    # key = "selection_rating"
    # key = "suitable_rating"

    overall_ratings = {
        "playlist1": [],
        "playlist2": [],
        "playlist3": []
    }

    for user, _ in Session.get_users_with_surveys():

        average_ratings = {
            "playlist1": [],
            "playlist2": [],
            "playlist3": []
        }

        for playlist, playlist_string in user.get_playlists_from_survey():

            average_ratings[playlist_string].append(int(playlist[key]))
            overall_ratings[playlist_string].append(int(playlist[key]))

    labels = ["PWS", "Fairness", "Least Misery"]

    result = f"Overall ({key}):\n"
    for index, playlist in enumerate(overall_ratings):
        result += f"{labels[index]}: {statistics.mean(overall_ratings[playlist]):.2f}, {statistics.stdev(overall_ratings[playlist]):.2f}, "
    print(result[:-2])

    fig, ax = plt.subplots()
    boxplot_data = [overall_ratings[playlist] for playlist in overall_ratings]

    ax.boxplot(boxplot_data, labels=labels,
                boxprops=dict(linestyle='-', linewidth=1.5),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='-', linewidth=1.5),
                capprops=dict(linestyle='-', linewidth=1.5),
                showfliers=True
                )

    pyplot.locator_params(nbins=5)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    ax.set_ylim((0.8, 5.2))
    ax.set_xticklabels(labels)
    ax.set_ylabel("Survey Rating")
    fig.tight_layout()
    plt.show()
