import statistics

from database.session import Session


def get_experiment_stats():
    """
    Calculates and prints stats of the experiment.
    :return:
    """
    session_count = 0
    filled_in_survey = 0
    user_count = 0
    left_feedback = 0

    number_of_users_in_group = []

    track_set = set()
    chosen_track_set = set()
    hovered_track_set = set()
    seen_track_set = set()

    track_count = 0

    general_feedback_list = []
    like_feedback = []
    selection_feedback = []
    suitable_feedback = []

    for session in Session.get_completed_sessions():
        session_count += 1

        number_of_users_in_group.append(session.get_number_of_users(skip_without_survey=False))

        for user in session.get_users_with_tracks_from_session():
            user_count += 1

            track_set.update(user.get_tracks())
            chosen_track_set.update(user.get_chosen_tracks())
            hovered_track_set.update(user.get_hovered_tracks())
            seen_track_set.update(user.get_seen_tracks())

            track_count += len(user.get_chosen_tracks())

            if not user.survey:
                continue

            filled_in_survey += 1

            survey = user.get_survey()

            has_feedback = False

            if survey["feedback"]:
                has_feedback = True
                general_feedback_list.append(survey["feedback"])

            for playlist, _ in user.get_playlists_from_survey():
                if playlist["like_feedback"]:
                    like_feedback.append(playlist["like_feedback"])
                    has_feedback = True
                if playlist["selection_feedback"]:
                    has_feedback = True
                    selection_feedback.append(playlist["selection_feedback"])
                if playlist["suitable_feedback"]:
                    has_feedback = True
                    suitable_feedback.append(playlist["suitable_feedback"])
            left_feedback += has_feedback

    hovered_track_set = hovered_track_set.union(chosen_track_set)
    seen_track_set = seen_track_set.union(hovered_track_set)

    print(f"Total completed sessions: {session_count}")
    print(f"Total users: {filled_in_survey} / {user_count}")
    print(f"Number of users in a group: {number_of_users_in_group}, mean: {statistics.median(number_of_users_in_group)}")

    print("")
    print(f"Total unique tracks: {len(track_set)}")
    print(f"Total chosen tracks: {len(chosen_track_set)}, non-unique: {track_count}")
    print(f"Total hovered tracks: {len(hovered_track_set)}, is subset: {chosen_track_set.issubset(hovered_track_set)}")
    print(f"Total seen tracks: {len(seen_track_set)}, is subset: {hovered_track_set.issubset(seen_track_set)}")

    print("")
    print(f"Total general feedback: {len(general_feedback_list)}, "
          f"average length: {statistics.mean([len(feedback) for feedback in general_feedback_list]):.2f}")
    print(f"Total like feedback: {len(like_feedback)}, "
          f"average length: {statistics.mean([len(feedback) for feedback in like_feedback]):.2f}")
    print(f"Total selection feedback: {len(selection_feedback)}, "
          f"average length: {statistics.mean([len(feedback) for feedback in selection_feedback]):.2f}")
    print(f"Total suitable feedback: {len(suitable_feedback)}, "
          f"average length: {statistics.mean([len(feedback) for feedback in suitable_feedback]):.2f}")
    print(f"Number of users that left feedback {left_feedback}")
