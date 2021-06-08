import statistics

from database.session import Session
import matplotlib.pyplot as plt


def album_detection(user):
    """
    Attempts to detect if a user searched for an album by checking if all tracks of an album appeared in the seen items.
    :param user:
    :return:
    """
    seen_tracks = user.seen_tracks

    list_of_albums = {}
    album_number_of_tracks = {}
    for track in seen_tracks:
        if "album" not in track:
            continue

        if track["name"] == "sanjake":
            continue

        album_name = track["album"]["name"]
        if album_name not in list_of_albums:
            list_of_albums[album_name] = 0
            album_number_of_tracks[album_name] = track["album"]["total_tracks"]
        list_of_albums[album_name] += 1

        if list_of_albums[album_name] > 1 and list_of_albums[album_name] == album_number_of_tracks[album_name]:
            print(f"Album search detected: {album_name}, number of tracks: {album_number_of_tracks[album_name]}")
            print(f"User: {user.email_address}")


def seen_track_analysis():
    """
    Performs an analysis on the number of tracks that were interacted with or seen and prints/plots it.
    Also checks if albums were searched.
    :return:
    """

    average_track_length = {
        "tracks": [],
        "hovered_tracks": [],
        "seen_tracks": []
    }

    for user in Session.get_users_with_tracks():
        average_track_length["tracks"].append(len(user.tracks))
        average_track_length["hovered_tracks"].append(len(user.hovered_tracks))
        average_track_length["seen_tracks"].append(len(user.seen_tracks))

        album_detection(user)

    result = "Overall:\n"
    for category in average_track_length:
        result += f"{category}: ({statistics.mean(average_track_length[category]):.2f}," \
                  f" {statistics.mode(average_track_length[category])}), "
    print(result[:-2])

    fig, ax = plt.subplots()

    boxplot_data = [average_track_length['hovered_tracks'], average_track_length['seen_tracks']]

    labels = ["Interacted Items", "Seen Items"]

    ax.boxplot(boxplot_data, labels=labels,
               boxprops=dict(linestyle='-', linewidth=1.5),
               medianprops=dict(linestyle='-', linewidth=2),
               whiskerprops=dict(linestyle='-', linewidth=1.5),
               capprops=dict(linestyle='-', linewidth=1.5),
               showfliers=True
               )

    ax.set_xticklabels(labels)
    ax.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax.set_ylabel("Number of Tracks")
    ax.set_ylim((0, 220))

    fig.tight_layout()
    plt.show()
