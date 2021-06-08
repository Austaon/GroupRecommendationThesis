from collections import defaultdict

from database.user import SessionUser


def count_duplicates(key="real"):
    """
    Counts the number of duplicate tracks in a given dataset.
    :param key: The dataset to use: "real", "recommended", or "random"
    :return:
    """

    count_tracks = defaultdict(int)
    total_count = 0

    for user in SessionUser.objects:

        survey = user.survey

        for category in survey[key]:
            for track in survey[key][category]:
                count_tracks[track["id"]] += 1
                total_count += 1

        for track in user.tracks:
            count_tracks[track["id"]] += 1
            total_count += 1

    print(f"Duplicate tracks: {len({k: v for k, v in count_tracks.items() if v >= 2})}")
    print(f"Unique vs total tracks: {len(count_tracks)} / {total_count}")
    print(f"Percentage duplicate tracks: {len({k: v for k, v in count_tracks.items() if v >= 2}) / len(count_tracks) * 100:.2f}%")
