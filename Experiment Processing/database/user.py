from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, ListField, ObjectIdField

from util.parse_survey_meta_data import parse_survey_meta_data


class SessionUser(Document):
    """
    Model class for the users in the database.
    """

    meta = {"collection": "session_users"}

    _id = ObjectIdField()
    spotify_id = StringField(db_field="id")

    tracks = ListField()
    hovered_tracks = ListField()
    seen_tracks = ListField()

    email_address = StringField()
    is_admin = BooleanField()
    has_joined = BooleanField()
    session_id = StringField()

    updated_at = DateTimeField()
    created_at = DateTimeField()

    has_filled_in_tracks = BooleanField()
    has_spotify_account = BooleanField()
    survey = DictField()

    def get_tracks(self):
        """
        Returns all tracks in a user profile. Excludes a track with the name "Sanjake" (it was used in the tutorial)
        and artists or albums that somehow ended up in either of the lists.
        :return:
        """
        track_set = {}
        for track in self.tracks + self.hovered_tracks + self.seen_tracks:

            if track["name"] == "sanjake" or track["type"] in ["artist", "album"]:
                continue
            track_set[track["id"]] = track
        return track_set

    def get_chosen_tracks(self):
        """
        Returns the tracks selected by the user. Excludes the aforementioned cases.
        :return:
        """
        track_set = {}
        for track in self.tracks:

            if track["name"] == "sanjake" or track["type"] in ["artist", "album"]:
                continue
            track_set[track["id"]] = track

        return track_set

    def get_hovered_tracks(self):
        """
        Returns the tracks that the user interacted with. Excludes the aforementioned cases.
        :return:
        """
        track_set = {}
        for track in self.hovered_tracks:

            if track["name"] == "sanjake" or track["type"] in ["artist", "album"]:
                continue
            track_set[track["id"]] = track
        return track_set

    def get_seen_tracks(self):
        """
        Returns the tracks that the user saw. Excludes the aforementioned cases.
        :return:
        """
        track_set = {}
        for track in self.seen_tracks:

            if track["name"] == "sanjake" or track["type"] in ["artist", "album"]:
                continue
            track_set[track["id"]] = track
        return track_set

    def get_experiment_1_tracks(self):
        """
        Used to return all tracks of a user profile from experiment 1. The earlier methods cannot be used due to the
        tracks being stored in a different way.
        :return:
        """

        types = ["tracks_short_term", "tracks_medium_term", "tracks_long_term"]
        categories = ["real", "recommended", "random"]

        track_set = {}
        for track in self.tracks:
            if track["type"] in ["artist", "album"]:
                continue
            track_set[track["id"]] = track

        for c in categories:
            for t in types:
                for track in self.survey[c][t]:

                    if type(track) == str:
                        print(f"{c}, {t}, {track}, {self.spotify_id}")

                    if track["name"] == "sanjake" or track["type"] in ["artist", "album"]:
                        continue
                    track_set[track["id"]] = track

        return track_set

    def get_survey(self):
        """
        Returns the survey, with the playlists in the correct order.
        :return:
        """
        return parse_survey_meta_data(self.survey)

    def get_playlists_from_survey(self):
        """
        Yields the ratings of each playlist separately together with a string listing the current playlist.
        :return:
        """
        survey = self.get_survey()

        for playlist_string in [f"playlist{i}" for i in range(1, 4)]:
            yield survey[playlist_string], playlist_string
