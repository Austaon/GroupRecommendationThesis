from textblob import TextBlob

from database.session import Session


def __collect_feedback_data():
    feedback_object = {}

    for user, session in Session.get_users_with_surveys():
        survey = user.get_survey()

        feedback_list = [
            [survey["feedback"], 0],
        ]

        for playlist in [f"playlist{i}" for i in range(1, 4)]:
            survey_playlist = survey[playlist]
            feedback_list.append([survey_playlist["like_feedback"], survey_playlist["like_rating"]])
            feedback_list.append([survey_playlist["selection_feedback"], survey_playlist["selection_rating"]])
            feedback_list.append([survey_playlist["suitable_feedback"], survey_playlist["suitable_rating"]])

        feedback_object[user.spotify_id] = feedback_list

    return feedback_object


def get_all_feedback_strings(feedback_object):
    feedback_array = []

    for person in feedback_object:
        for feedback_pair in feedback_object[person]:
            feedback = feedback_pair[0]
            if feedback != "":
                feedback_array.append(feedback_pair)

    return feedback_array


def feedback_analysis():
    """
    Attempted to match sentiment to survey ratings, but no easy to find link appeared.

    Now just prints all feedback and the rating associated with that feedback. (Prints 0 if the feedback was given at the end)
    :return:
    """
    feedback_object = __collect_feedback_data()
    feedback_array = get_all_feedback_strings(feedback_object)

    for feedback in feedback_array:
        blob = TextBlob(feedback[0])
        for sentence in blob.sentences:
            print(
                f"{feedback[1]}: {sentence}"
                # f"{sentence}: ({sentence.sentiment.polarity:.2f}, {sentence.sentiment.subjectivity:.2f}), {feedback[1]}"
            )
