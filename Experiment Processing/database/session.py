from typing import Tuple

from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, ReferenceField, ListField, \
    ObjectIdField

from database.user import SessionUser


class Session(Document):
    """
    Model class for the sessions in the database.
    """

    meta = {"collection": "sessions"}

    _id = ObjectIdField(required=True)
    session_id = StringField(required=True, db_field="id")

    playlist_name = StringField(required=True)
    has_started = BooleanField(required=True)
    state = StringField(required=True)

    updated_at = DateTimeField(required=True)
    created_at = DateTimeField(required=True)

    recommendations = ListField()

    def get_users(self):
        """
        Return all users in a session that have a survey filled in
        :return:
        """
        for user in SessionUser.objects(session_id=self.session_id):
            if not user.survey:
                continue
            yield user

    def get_number_of_users(self, skip_without_survey=True):
        """
        Returns the number of users with a completed survey in the current session
        :return:
        """
        count = 0
        for user in SessionUser.objects(session_id=self.session_id):
            if skip_without_survey and not user.survey:
                continue
            count += 1
        return count

    def get_users_with_tracks_from_session(self):
        """
        Returns all users that have tracks in the current sessions
        :return:
        """
        for user in SessionUser.objects(session_id=self.session_id):
            if not user.tracks:
                continue
            yield user

    @staticmethod
    def get_number_completed_sessions():
        """
        Returns the number of completed sessions (aka sessions that are on the survey step)
        :return:
        """
        return Session.objects(state="show_playlist").count()

    @staticmethod
    def get_completed_sessions():
        """
        Returns all completed sessions.
        :return:
        """
        for session in Session.objects(state="show_playlist"):
            yield session

    @staticmethod
    def get_users_with_surveys() -> Tuple[SessionUser, 'Session']:
        """
        Returns all users that have surveys.
        :return:
        """
        for session in Session.objects(state="show_playlist"):
            for user in session.get_users():
                yield user, session

    @staticmethod
    def get_users_with_tracks():
        """
        Returns all users that have filled in tracks.
        :return:
        """
        for session in Session.objects():
            for user in session.get_users():
                if not user.tracks:
                    continue
                yield user
