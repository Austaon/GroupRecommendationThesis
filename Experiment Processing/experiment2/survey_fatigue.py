import statistics

import matplotlib.pyplot as plt
from matplotlib import pyplot

from database.session import Session


def survey_fatigue():
    """
    Analysis to check if survey fatigue was present in the survey.
    The survey key to consider can be changed in the code below.

    Calculates the average survey rating for each playlist (before being put in the "correct" position),
    if survey fatigue did take place, the ratings should go down over time.
    :return:
    """

    key = "like_rating"
    # key = "selection_rating"
    # key = "suitable_rating"

    # key = "like_rating_specific"
    # key = "selection_rating_specific"
    # key = "suitable_rating_specific"

    specific_ratings = {
        "playlist1": {
            "Probability Weighted Sum": [],
            "Fairness": [],
            "Least Misery": []
        },
        "playlist2": {
            "Probability Weighted Sum": [],
            "Fairness": [],
            "Least Misery": []
        },
        "playlist3": {
            "Probability Weighted Sum": [],
            "Fairness": [],
            "Least Misery": []
        }
    }

    overall_ratings = {
        "playlist1": [],
        "playlist2": [],
        "playlist3": []
    }

    for user, session in Session.get_users_with_surveys():
        survey = user.survey

        for playlist_string in [f"playlist{i}" for i in range(1, 4)]:
            voting_rule_name = survey["metaData"][playlist_string]["rule_name"]["ruleName"]

            if "specific" in key:
                specific_ratings[playlist_string][voting_rule_name].extend(
                    [int(x) for _, x in survey[f"{playlist_string}_{key}"].items()]
                )
                overall_ratings[playlist_string].extend(
                    [int(x) for _, x in survey[f"{playlist_string}_{key}"].items()]
                )
            else:
                specific_ratings[playlist_string][voting_rule_name].append(
                    int(survey[f"{playlist_string}_{key}"])
                )
                overall_ratings[playlist_string].append(
                    int(survey[f"{playlist_string}_{key}"])
                )

    boxplot_data = [overall_ratings["playlist1"], overall_ratings["playlist2"], overall_ratings["playlist3"]]
    boxplot_labels = ["Playlist 1", "Playlist 2", "Playlist 3"]

    fig1, ax1 = plt.subplots()

    pyplot.locator_params(axis='y', nbins=5)

    ax1.boxplot(boxplot_data, labels=boxplot_labels,
                boxprops=dict(linestyle='-', linewidth=1.5),
                medianprops=dict(linestyle='-', linewidth=2),
                whiskerprops=dict(linestyle='-', linewidth=1.5),
                capprops=dict(linestyle='-', linewidth=1.5),
                showfliers=True
                )

    ax1.set_ylim((0.8, 5.2))
    ax1.set_ylabel(f"Survey Rating")
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)

    fig1.tight_layout()
    plt.show()

    result = "Specific:\n"
    overall_result = "Overall:\n"

    for playlist in specific_ratings:

        playlist_data = specific_ratings[playlist]
        result += f"{playlist}: "
        overall_result += f"{playlist}: {statistics.mean(overall_ratings[playlist]):.2f}," \
                          f" {statistics.stdev(overall_ratings[playlist]):.2f}, "

        for voting_rule in playlist_data:
            result += f"{voting_rule}: {statistics.mean(playlist_data[voting_rule]):.2f}," \
                      f" {statistics.stdev(playlist_data[voting_rule]):.2f}" \
                      f" (length: {len(playlist_data[voting_rule]): =3d}), "
        result += "\n"
        overall_result += "\n"

    print(result[:-3])
    print(overall_result[:-3])
