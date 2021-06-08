import statistics

from database.session import Session

import matplotlib.pyplot as plt


def track_position_analysis():
    """
    Analysis on the positions of the selected items in the list of interacted items.

    No temporal logs are available of when a person selected their tracks, but the interacted item list is ordered by
    time and can be used as a substitute.
    :return:
    """

    found_positions = []
    found_positions_per_track = {
        1: [], 2: [], 3: [], 4: [], 5: []
    }

    found_in_initial_tracks = {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0
    }

    for user in Session.get_users_with_tracks():

        chosen_track_ids = [track_id for track_id in user.get_chosen_tracks()]
        hovered_tracks = user.get_hovered_tracks()

        found_tracks = 0
        index = 0

        found_positions_temp = []

        for track_id, track in hovered_tracks.items():

            index += 1

            if track_id in chosen_track_ids:
                found_tracks += 1

                found_positions_temp.append(index / len(hovered_tracks))
                found_positions_per_track[found_tracks].append(index / len(hovered_tracks))

                if index <= 5:
                    found_in_initial_tracks[found_tracks] += 1

        if found_tracks != 5:
            continue

        found_positions.extend(found_positions_temp)

    print(f"Found position: {statistics.mean(found_positions):.2f}, {statistics.stdev(found_positions):.2f}")

    print("Positions per index: ", end="")
    for key, position_list in found_positions_per_track.items():
        print(f"{key}: {statistics.mean(position_list):.2f}, {statistics.stdev(position_list):.2f}; ", end="")
    print("")

    print("Number of items found in initial selection: ", end="")
    for key, position_list in found_in_initial_tracks.items():
        print(f"{key}: {position_list}; ", end="")
    print("")

    boxplot_data = [found_positions_per_track[1], found_positions_per_track[2], found_positions_per_track[3],
                    found_positions_per_track[4], found_positions_per_track[5]]

    fig1, ax1 = plt.subplots()
    ax1.boxplot(boxplot_data, vert=False,
                boxprops=dict(linestyle='-', linewidth=1.5),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='-', linewidth=1.5),
                capprops=dict(linestyle='-', linewidth=1.5),
                showfliers=True
                )
    ax1.set_xlabel("Relative Position")
    ax1.set_ylabel("Number of Selected Tracks")
    ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
    ax1.set_xlim((0, 1))

    fig1.tight_layout()

    plt.show()
