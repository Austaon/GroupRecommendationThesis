import statistics
import matplotlib.pyplot as plt

from database.session import Session


def parse_int(playlist_string):
    return int(''.join(filter(str.isdigit, playlist_string)))


def rating_index_analysis():
    """
    This function checks for the average rating per index of tracks in the playlists.
    If the rating goes down over time, this could be an indication of survey fatigue.
    :return:
    """

    rating_indices = {
        "Probability Weighted Sum": {},
        "Fairness": {},
        "Least Misery": {}
    }

    key = "like_rating"
    # key = "suitable_rating"

    for user, session in Session.get_users_with_surveys():

        for playlist, playlist_string in user.get_playlists_from_survey():
            rule_name = playlist["rule_name"]
            playlist_ratings = playlist[f"{key}_specific"]
            for song, rating in playlist_ratings.items():
                if song not in rating_indices[rule_name]:
                    rating_indices[rule_name][song] = []
                rating_indices[rule_name][song].append(int(rating))

    fig, axs = plt.subplots(ncols=1, nrows=4)
    label_range = range(1, 11)
    index = 0

    min_y = float("+inf")
    max_y = float("-inf")

    for rule_name, playlist in rating_indices.items():
        print(rule_name)
        playlist_averages = [statistics.mean(song_ratings) for _, song_ratings in playlist.items()]
        print([f"{average:.2f}" for average in playlist_averages])
        axs[index].bar(label_range, playlist_averages)
        index += 1

        max_y = max(max_y, *playlist_averages)
        min_y = min(min_y, *playlist_averages)

        print(f"Max difference: {max(playlist_averages) - min(playlist_averages):.2f}")
        print("")

    playlist_averages = [
        (statistics.mean(rating_indices["Probability Weighted Sum"][f"Song{index}"]) +
         statistics.mean(rating_indices["Fairness"][f"Song{index}"]) +
         statistics.mean(rating_indices["Least Misery"][f"Song{index}"])) / 3
        for index in label_range
    ]
    print("Averages:")
    print([f"{average:.2f}" for average in playlist_averages])
    print(f"Max difference: {max(playlist_averages) - min(playlist_averages):.2f}")
    axs[3].bar(label_range, playlist_averages)

    for ax in axs.reshape(-1):
        ax.set_xticks(label_range)
        ax.set_ylim([3, 4.5])

    for ax, row in zip(axs.reshape(-1), ["PWS", "Fairness", "LM", "Average"]):
        ax.annotate(row, xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
                    xycoords=ax.yaxis.label, textcoords='offset points',
                    size='large', ha='right', va='center')

    fig.tight_layout()
    plt.show()
