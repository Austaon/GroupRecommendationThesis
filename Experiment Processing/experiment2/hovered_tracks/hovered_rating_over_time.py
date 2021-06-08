import statistics

import numpy as np
from scipy.stats import ttest_ind

from database.session import Session
from recommender.distance_metrics.cosine_similarity import CosineSimilarity

import matplotlib.pyplot as plt


def hovered_rating_over_time():
    """
    Calculates, plots, and prints the similarity scores of the interacted items, the tracks considered as the user
    profile can be changed by modifying the `chosen_tracks` and `chosen_track_ids` variables.

    The selected items are highlighted in red in the plots.
    :return:
    """

    distance_metric = CosineSimilarity()

    found_positions = []
    found_positions_per_track = {
        1: [], 2: [], 3: [], 4: [], 5: []
    }
    average_ratings = []
    average_rating_chosen = []

    hovered_items_higher_than_chosen = []

    for user in Session.get_users_with_tracks():

        own_track_indices = np.empty([0])
        ratings = []

        chosen_tracks = [track_id for track_id in user.get_chosen_tracks()]
        chosen_track_ids = [track_id for track_id in user.get_chosen_tracks()]
        hovered_tracks = user.get_hovered_tracks()

        found_tracks = 0
        index = 0

        found_positions_temp = []

        average_rating_chosen_temp = []
        average_ratings_temp = []

        for track_id, track in hovered_tracks.items():

            index += 1

            if track_id in chosen_track_ids:
                found_tracks += 1

                found_positions_temp.append(index / len(hovered_tracks))
                track_rating = distance_metric.calculate_ratings(chosen_tracks, [track["id"]])
                average_rating_chosen_temp.append(list(track_rating.values())[0])
                ratings.append(list(track_rating.values())[0])

                own_track_indices = np.append(own_track_indices, True)

                found_positions_per_track[found_tracks].append(index / len(hovered_tracks))

            else:
                track_rating = distance_metric.calculate_ratings(chosen_tracks, [track["id"]])
                ratings.append(list(track_rating.values())[0])
                average_ratings_temp.append(list(track_rating.values())[0])

                own_track_indices = np.append(own_track_indices, False)

        if found_tracks != 5:
            continue

        average_rating_chosen.extend(average_rating_chosen_temp)
        average_ratings.extend(average_ratings_temp)

        found_positions.extend(found_positions_temp)

        max_chosen_score = max(average_rating_chosen_temp)

        better_tracks = [track_score for track_score in average_ratings_temp if track_score > max_chosen_score]

        hovered_items_higher_than_chosen.append(len(better_tracks))

        x_values = np.array(range(0, len(hovered_tracks)))
        ratings = np.array(ratings)

        own_mask = own_track_indices == 1
        other_mask = own_track_indices != 1

        plt.bar(x_values[own_mask], ratings[own_mask], color='red')
        plt.bar(x_values[other_mask], ratings[other_mask], color='blue')
        plt.ylim((0.5, 1))
        plt.title(user.email_address)
        plt.show()

    print(f"Average rating: {statistics.mean(average_ratings):.2f}, {statistics.stdev(average_ratings):.2f}")
    print(f"Average rating chosen: {statistics.mean(average_rating_chosen):.2f}, {statistics.stdev(average_rating_chosen):.2f}")
    print(f"Average better scoring items: {statistics.mean(hovered_items_higher_than_chosen):.2f}, {statistics.stdev(hovered_items_higher_than_chosen):.2f}")
    print(f"Found position: {statistics.mean(found_positions):.2f}, {statistics.stdev(found_positions):.2f}")

    print("Positions per index: ", end="")
    for key, position_list in found_positions_per_track.items():
        print(f"{key}: {statistics.mean(position_list):.2f}, {statistics.stdev(position_list):.2f}; ", end="")
    print("")

    print(f"t-test (df={len(average_ratings)}, {len(average_rating_chosen)}): "
          f"{ttest_ind(average_ratings, average_rating_chosen, equal_var=False)}")

    # Chosen tracks as user profile:
    # Average rating: 0.87, 0.09
    # Average rating chosen: 0.92, 0.06
    # Average better scoring items: 1.00, 1.83
    # t-test: statistic=-9.30, pvalue=8.54e-19)

    # Hovered tracks as user profile:
    # Average rating: 0.87, 0.07
    # Average rating chosen: 0.89, 0.06
    # t-test: statistic=-4.48, pvalue=1.00e-05)

    # Same as Hovered, but temporarily remove selected track from distance metric if that track is being calculated
    # Average rating: 0.87, 0.09
    # Average rating chosen: 0.90, 0.08
    # Average better scoring items: 4.00, 5.28
    # t-test (df=642, 185): statistic=-5.05, pvalue=6.90e-07)

    # Seen tracks as user profile
    # Average rating: 0.85, 0.07
    # Average rating chosen: 0.87, 0.06
    # t-test: statistic=-4.07, pvalue=5.77e-05)

    # Positions of chosen tracks (@hovered tracks):
    # Found position: 0.67, 0.27
    # Positions per index: 1: 0.33, 0.20; 2: 0.52, 0.17; 3: 0.69, 0.14; 4: 0.82, 0.14; 5: 0.99, 0.03

    # Positions of chosen tracks (@seen tracks):
    # Found position: 0.51, 0.29
    # Positions per index: 1: 0.22, 0.19; 2: 0.35, 0.19; 3: 0.52, 0.17; 4: 0.67, 0.16; 5: 0.86, 0.12

