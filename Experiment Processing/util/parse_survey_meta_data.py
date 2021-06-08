def __gather_data_from_playlist(survey, playlist_index):
    """
    Gathers the data from the survey. Fixes some inconsistencies that are present in the survey.
    :param survey:
    :param playlist_index:
    :return:
    """

    result = {
        "like_rating": survey[f"playlist{playlist_index}_like_rating"],
        "like_rating_specific": survey[f"playlist{playlist_index}_like_rating_specific"],
        "like_feedback": survey.get(f"playlist{playlist_index}_like_feedback", ""),

        "selection_rating": survey[f"playlist{playlist_index}_selection_rating"],
        "selection_rating_specific": survey[f"playlist{playlist_index}_selection_rating_specific"],
        "selection_feedback": survey.get(f"playlist{playlist_index}_selection_feedback", ""),

        "suitable_rating": survey[f"playlist{playlist_index}_suitable_rating"],
        "suitable_rating_specific": survey[f"playlist{playlist_index}_suitable_rating_specific"],
        "suitable_feedback": survey.get(f"playlist{playlist_index}_suitable_feedback", ""),
    }
    for i in range(6, 11):
        if f"Song {i}" in result["selection_rating_specific"]:
            del result["selection_rating_specific"][f"Song {i}"]

    if result["like_feedback"] == "":
        result["like_feedback"] = survey.get(f"playlist{playlist_index}_like_specific", "")

    return result


def parse_survey_meta_data(survey):
    """
    Changes the order of the playlists from the survey, which were shuffled to prevent survey fatigue.
    This function makes sure that the order is always PWS -> Fairness -> LM.
    :param survey:
    :return:
    """

    meta_data_link = {
        "Probability Weighted Sum": 1,
        "Fairness": 2,
        "Least Misery": 3
    }

    meta_data = survey["metaData"]
    result_object = {
        "playlist1": {},
        "playlist2": {},
        "playlist3": {},
        "feedback": survey.get("general_feedback_input", "")
    }

    index = 1

    for playlist_string in [f"playlist{i}" for i in range(1, 4)]:
        actual_index = meta_data_link[meta_data[playlist_string]["rule_name"]["ruleName"]]
        result_object[f"playlist{actual_index}"] = __gather_data_from_playlist(survey, index)
        result_object[f"playlist{actual_index}"]["rule_name"] = meta_data[playlist_string]["rule_name"]["ruleName"]
        index += 1

    return result_object
