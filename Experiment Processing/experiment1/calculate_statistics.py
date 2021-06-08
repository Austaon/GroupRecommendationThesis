import statistics

from database.user import SessionUser


def calculate_statistics():
    """
    Calculates the total number of items in each category and overall.
    This is used to find out how complete the historical data is.

    It is expected that some items will be missing since not everyone uses Spotify regularly.
    :return:
    """

    statistic_data = {
        "tracks_short_term": 0,
        "tracks_medium_term": 0,
        "tracks_long_term": 0,
        "artists_short_term": 0,
        "artists_medium_term": 0,
        "artists_long_term": 0,
        "selected_tracks": 0,
        "total": 0
    }

    key = "real"

    selected_numbers_mean = []

    total_number = SessionUser.objects.count() * 10
    total_total_number = total_number * 6

    unique_songs = set()

    for user in SessionUser.objects:

        user_playlist = user.survey[key]

        unique_songs.update([track["id"] for track in user.tracks])
        statistic_data["selected_tracks"] += len(user.tracks)
        selected_numbers_mean.append(len(user.tracks))

        for k in user_playlist.keys():
            statistic_data[k] += len(user_playlist[k])
            statistic_data["total"] += len(user_playlist[k])
            unique_songs.update([track["id"] for track in user_playlist[k]])

    for k in statistic_data:
        if k == "total":
            print(f"{k:19s} -> Total: {statistic_data[k]: =4d}, Percentage: {statistic_data[k] / total_total_number * 100:.2f}%")
        else:
            print(f"{k:19s} -> Total: {statistic_data[k]: =4d}, Percentage: {statistic_data[k] / total_number * 100:.2f}%")

    print(f"Total number: {total_number}, total total: {total_total_number}")

    print(f"Unique songs: {len(unique_songs)}")
    print(f"Mean of selected songs: {statistics.mean(selected_numbers_mean):.2f}")
