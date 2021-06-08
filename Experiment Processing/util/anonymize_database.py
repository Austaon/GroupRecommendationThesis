import hashlib

from database.consent_form import ConsentForm
from database.database_util import connect_to_database, connect_to_anonymous_database, close_database_connection
from database.session import Session


def anonymize_database():
    """
    Anonymises the currently connected database to the 'anonymous' database.
    Intended to be used with the 'laravel' dataset, which is data collected from the second experiment.
    :return:
    """
    connect_to_database()

    # First collect the important parts of the database.
    sessions = []
    users = []
    consent_forms = []

    for session in Session.get_completed_sessions():
        sessions.append(session)

    for user in Session.get_users_with_tracks():
        users.append(user)

    email_addresses = [user.email_address for user in users]

    for consent_form in ConsentForm.objects():
        if consent_form.email_address in email_addresses and \
                consent_form.email_address not in [consent_form_temp.email_address for consent_form_temp in consent_forms]:
            consent_forms.append(consent_form)

    close_database_connection()
    connect_to_anonymous_database()

    # Sessions don't need to be anonymised, so just store them.
    for session in sessions:
        print(f"Storing: {session.playlist_name}")
        session.save()

    # The email address and spotify user id need to be anonymised before storing them.
    print("\n====================\n")
    user_dict = {}
    for user in users:
        user_dict[user.email_address] = user
        user.email_address = hashlib.sha224(user.email_address.encode()).hexdigest()
        user.spotify_id = hashlib.sha224(user.spotify_id.encode()).hexdigest()
        print(f"Storing: {user.email_address}")
        user.save()

    # The consent forms similarly need to be anonymised as well,
    #  but make sure that the email address remains consistent.
    print("\n====================\n")
    for consent_form in consent_forms:
        print(f"Storing: {consent_form.email_address}")

        associated_user = user_dict[consent_form.email_address]

        consent_form.email_address = associated_user.email_address
        consent_form.save()
        if consent_form.session_id is None:
            consent_form.session_id = associated_user.session_id
            consent_form.save()

    close_database_connection()
