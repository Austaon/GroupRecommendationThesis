from pprint import pprint

from database.session import Session
from database.user import SessionUser
from util.login_spotify import login_spotify


def fix_laravel_bug():
    """
    A bug occurred while storing users that participated more than twice, which caused their track data to be overwritten.
    This function restores the selected track data using session metadata. The interacted and seen items cannot be restored.
    :return:
    """

    user_set = {}

    sp = login_spotify()

    for user in SessionUser.objects():
        if user.spotify_id not in user_set:
            user_set[user.spotify_id] = 0

        user_set[user.spotify_id] += 1

    duplicate_users = [user for user, amount in user_set.items() if amount > 1]

    for user in duplicate_users:
        for session in Session.objects:
            if user in [u.spotify_id for u in session.get_users()]:
                distance_magic = session.recommendations[0]["metadata"]["distances"][user]
                user_tracks = [track for track, rating in distance_magic.items() if rating == 1]
                track_data = sp.tracks(user_tracks)["tracks"]

                print(session.session_id)
                print(user)

                replace_user = SessionUser.objects.get(spotify_id=user, session_id=session.session_id)
                print([track["id"] for track in track_data])
                print(user_tracks)
                print([track["id"] for track in replace_user.tracks])
                replace_user.tracks = track_data
                replace_user.save()
                print([track["id"] for track in replace_user.tracks])
                print("===================")
