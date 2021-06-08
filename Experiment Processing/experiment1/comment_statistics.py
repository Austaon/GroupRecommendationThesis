import json
from pprint import pprint

from database.user import SessionUser


def get_comment_statistics():
    """
    Collects and prints all feedback together with the associated user id.
    Additionally, shows how many users left feedback and the average length of a feedback message.
    :return:
    """

    comments = {}
    non_empty_count = 0
    comment_length = 0

    number_of_users = SessionUser.objects.count()

    for user in SessionUser.objects:

        feedback = user.email_address

        if len(feedback) > 0:
            comments[user.spotify_id] = feedback
            non_empty_count += 1
            comment_length += len(feedback)

            comments[user.spotify_id] = feedback

    pprint(comments)
    print(f"{non_empty_count} out of {number_of_users} left feedback ({non_empty_count / number_of_users * 100:.2f}%)")
    print(f"Average comment length: {comment_length / number_of_users:.2f}")

    with open("experiment1/results/feedback_given.json", "w") as out_file:
        json.dump(comments, out_file, indent=4)

