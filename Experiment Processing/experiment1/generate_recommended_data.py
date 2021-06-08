from database.user import SessionUser
from util.login_spotify import login_spotify


def generate_recommended_data():
    """
    Generates a new data set based on the Spotify Recommendation API and stores it for each user.
    The first five tracks of the historical data are used as seed and the same number of items as the historical data
    is obtained.
    :return:
    """

    sp = login_spotify()

    types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]
    count = 0

    for user in SessionUser.objects():

        count += 1
        print(f"{count} / 88")

        for t in types:

            if len(user.survey["real"][t]) == 0:
                continue

            top_songs = [t["id"] for t in user.survey["real"][t][:5]]

            num_songs = len(user.survey["real"][t])

            recommendations = sp.recommendations(seed_tracks=top_songs, limit=num_songs)
            user.survey["recommended"][t] = recommendations["tracks"]

        user.save()
