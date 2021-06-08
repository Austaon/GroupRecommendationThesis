from database.session import Session


def calculate_individual_rating_use():
    """
    Finds the number of times the individual rating in the survey was changed from the default.

    This can be done because the default value of each individual rating is an int, while changed values are strings.
    :return:
    """

    specific_ratings_missed = {
        "like_rating_specific": 0,
        "selection_rating_specific": 0,
        "suitable_rating_specific": 0
    }

    for user, session in Session.get_users_with_surveys():

        for playlist, playlist_string in user.get_playlists_from_survey():

            for specific_rating in specific_ratings_missed.keys():
                individual_ratings = list(playlist[specific_rating].values())

                specific_ratings_missed[specific_rating] += len([x for x in individual_ratings if type(x) == int])

    print(specific_ratings_missed)
    print(f"Totals: {40 * 10 * 3}, {40 * 5 * 3}, {40 * 10 * 3}")
