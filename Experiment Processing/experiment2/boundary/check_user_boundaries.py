import statistics

from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.RatingBoundary import RatingBoundary
from database.session import Session
from database.track_data import TrackData
from database.user import SessionUser


def __compute_boundary(user, track_function):
    boundaries = BinaryBoundaryWithFeatures(user, track_function)

    return boundaries


def __compute_ratings(user, track_list):
    rating_object = RatingBoundary(user)

    ratings = []

    for t in track_list:
        rating, _ = rating_object.get_boundary_score(t)
        ratings.append(rating)
    return statistics.mean(ratings)


def check_user_boundaries():
    """
    First experiment comparing boundary score with similarity score with different aggregation strategies and
    different sets of tracks as user profiles.
    :return:
    """
    average_boundary = []
    average_ratings = []
    total_users = 0

    track_functions = {
        "tracks": lambda u: u.get_chosen_tracks(),
        "hovered_tracks": lambda u: u.get_hovered_tracks(),
        "seen_tracks": lambda u: u.get_seen_tracks(),
    }

    for playlist in [0, 1, 2]:
        print(f"Playlist {playlist + 1}")
        for key in ["tracks", "hovered_tracks", "seen_tracks"]:
            for user, session in Session.get_users_with_surveys():
                total_users += 1
                user_boundary = __compute_boundary(user, track_functions[key])
                in_boundary_counter = 0

                average_rating = __compute_ratings(
                    user, session.recommendations[playlist]["tracks"]
                )

                for track in session.recommendations[playlist]["tracks"]:
                    boundary_score, _ = user_boundary.get_boundary_score(track)
                    in_boundary_counter += 1 if boundary_score == 8 else 0
                average_boundary.append(in_boundary_counter)
                average_ratings.append(average_rating)
                # print(f"boundary: {in_boundary_counter:.2f}/10, rating: {average_rating:.2f}")

            print(f"{key:14s}: boundary {statistics.mean(average_boundary):.2f}, rating {statistics.mean(average_ratings):.2f}")
