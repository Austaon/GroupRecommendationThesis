import statistics
import matplotlib.pyplot as plt

from database.session import Session


def parse_int(playlist_string):
    return int(''.join(filter(str.isdigit, playlist_string)))


def count_picked_songs_per_playlist():
    """
    Finds the number of tracks that were selected by a person that were recommended to a playlist.
    Additionally, does a normalization on these numbers, as the chance of a person having more tracks goes down
    when the group has more members.

    The result is printed and plotted.

    :return:
    """

    number_of_used_tracks = {
        "Probability Weighted Sum": [],
        "Fairness": [],
        "Least Misery": []
    }
    normalized_to_group_members = {
        "Probability Weighted Sum": [],
        "Fairness": [],
        "Least Misery": []
    }

    for user, session in Session.get_users_with_surveys():

        user_tracks = [track["id"] for track in user.tracks]

        for playlist, playlist_string in user.get_playlists_from_survey():

            playlist_index = parse_int(playlist_string)

            recommended_playlist = session.recommendations[playlist_index - 1]["tracks"]
            playlist_rule = playlist["rule_name"]

            user_tracks_vector = [
                1 if recommended_playlist[parse_int(song) - 1]["id"] in user_tracks else 0
                for song, rating in playlist["like_rating_specific"].items()
            ]
            number_of_used_tracks[playlist_rule].append(sum(user_tracks_vector))
            normalized_to_group_members[playlist_rule].append(sum(user_tracks_vector) / session.get_number_of_users())

    result = "Result:\n"
    for playlist in number_of_used_tracks:
        playlist_data = number_of_used_tracks[playlist]
        result += f"{playlist}: {statistics.mean(playlist_data):.2f} (stdev: {statistics.stdev(playlist_data):.2f}), "
    print(result[:-2])

    result = "Normalised result:\n"
    for playlist in normalized_to_group_members:
        playlist_data = normalized_to_group_members[playlist]
        result += f"{playlist}: {statistics.mean(playlist_data):.2f} (stdev: {statistics.stdev(playlist_data):.2f}), "
    print(result[:-2])

    labels = ["PWS", "F", "LM"]
    boxplot_data = [
        number_of_used_tracks["Probability Weighted Sum"],
        number_of_used_tracks["Fairness"],
        number_of_used_tracks["Least Misery"],
    ]

    fig, ax = plt.subplots()
    ax.boxplot(boxplot_data, labels=labels)

    ax.set_xticklabels(labels)

    fig.tight_layout()
    plt.show()

    boxplot_data = [
        normalized_to_group_members["Probability Weighted Sum"],
        normalized_to_group_members["Fairness"],
        normalized_to_group_members["Least Misery"],
    ]

    fig, ax = plt.subplots()
    ax.boxplot(boxplot_data, labels=labels)

    ax.set_xticklabels(labels)

    fig.tight_layout()
    plt.show()
