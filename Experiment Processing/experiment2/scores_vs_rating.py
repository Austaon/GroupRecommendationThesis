import statistics
from pprint import pprint

from scipy.stats import ttest_rel, ttest_ind

from boundary.HistogramBoundary import HistogramBoundary
from database.session import Session

import matplotlib.pyplot as plt


def scores_vs_rating():
    """
    Does a t-test between the scores calculated for each survey rating.

    Also plots a histogram of each rating to check the distribution of the scores
    :return:
    """

    rating_comparison = {
        1: [], 2: [], 3: [], 4: [], 5: []
    }

    rating_key = "like_rating_specific"

    for user, session in Session.get_users_with_surveys():

        boundary = HistogramBoundary(user)

        survey = user.get_survey()

        for playlist_index, playlist in enumerate(session.recommendations):
            survey_ratings = survey[f"playlist{playlist_index+1}"][rating_key]

            for track_index, track in enumerate(playlist["tracks"]):

                track_rating, _ = boundary.get_boundary_score(track)

                survey_rating = int(survey_ratings[f'Song{track_index + 1}'])

                rating_comparison[survey_rating].append(track_rating)

    result_string = ""

    for rating_bin, scores in rating_comparison.items():
        result_string += f"{rating_bin}: {statistics.mean(scores):.3f}, "
    result_string = result_string[:-2]
    print(result_string)

    for rating_bin, scores in rating_comparison.items():

        plt.hist(scores, bins=20)
        plt.title(f"Rating: {rating_bin} (total: {len(scores)})")
        plt.xlim((0.0, 8.0))
        plt.show()

    t_tests = {}
    for i in range(1, 6):
        t_tests[i] = {}
        for j in range(1, 6):
            if i != j:

                t_test_score = ttest_ind(
                    rating_comparison[i],  # [:min_amount],
                    rating_comparison[j],  # [:min_amount],
                    equal_var=False
                )
                t_tests[i][j] = t_test_score[1]

    pprint(t_tests)
