from database.session import Session


def get_group_purposes():
    """
    Prints the given purposes of each completed group (with Latex syntax).
    :return:
    """

    for session in Session.get_completed_sessions():

        print(f"\\item {session.playlist_name}")
