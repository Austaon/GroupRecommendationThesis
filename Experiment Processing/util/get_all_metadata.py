
from database.session import Session
from database.track_data import TrackData
from database.user import SessionUser


def get_all_metadata():
    """
    Collects all unique tracks available in the database and retrieves their metadata.
    Intended to be used with the data from the first experiment.
    :return:
    """
    track_set = set()
    tracks = {}

    for session in Session.get_completed_sessions():
        for user in session.get_users_with_tracks_from_session():
            user_tracks = user.get_tracks()
            track_set.update([track_id for track_id, track in user_tracks.items()])
            tracks = {**tracks, **user_tracks}

    track_counter = 0
    total_tracks = len(track_set)

    for track in track_set:
        TrackData.get_track(tracks[track])
        track_counter += 1
        print(f"Track {track_counter} out of {total_tracks}")


def get_all_metadata_from_users():
    """
    Collects all unique tracks available in the database and retrieves their metadata.
    Intended to be used with the data from the first experiment.
    :return:
    """
    track_set = set()
    tracks = {}

    for user in SessionUser.objects:
        user_tracks = user.get_experiment_1_tracks()
        track_set.update([track_id for track_id, track in user_tracks.items()])
        tracks = {**tracks, **user_tracks}

    track_counter = 0
    total_tracks = len(track_set)

    for track in track_set:
        TrackData.get_track(tracks[track])
        track_counter += 1
        print(f"Track {track_counter} out of {total_tracks}")
