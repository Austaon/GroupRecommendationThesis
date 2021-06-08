from pprint import pprint

from mongoengine import Document, StringField, BooleanField, DateTimeField, DictField, FloatField, IntField

from util.login_spotify import login_spotify


class TrackData(Document):
    """
    Model class for track data stored in the database.
    """

    meta = {"collection": "track_data"}

    track_id = StringField(required=True)

    name = StringField(required=True)
    artist = StringField(required=True)
    artist_id = StringField()

    track_sum = IntField()

    acousticness = FloatField(required=True)
    danceability = FloatField(required=True)
    energy = FloatField(required=True)
    instrumentalness = FloatField(required=True)
    liveness = FloatField(required=True)
    loudness = FloatField(required=True)
    speechiness = FloatField(required=True)
    valence = FloatField(required=True)

    tempo = FloatField(required=True)

    def get_metadata(self):
        return {
            "acousticness": self.acousticness,
            "danceability": self.danceability,
            "energy": self.energy,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "loudness": self.loudness,
            "speechiness": self.speechiness,
            "valence": self.valence,
        }

    def get_array_data(self):
        return [
            self.acousticness, self.danceability, self.energy, self.instrumentalness,
            self.liveness, self.loudness, self.speechiness, self.valence
        ]

    def get_inverse_array_data(self):
        return [
            1-self.acousticness, 1-self.danceability, 1-self.energy, 1-self.instrumentalness,
            1-self.liveness, 1-self.loudness, 1-self.speechiness, 1-self.valence
        ]

    def get_feature(self, feature):
        return self.get_metadata()[feature]

    @staticmethod
    def get_track(track_data):

        if type(track_data) == str:
            track_data = {"id": track_data}

        if TrackData.objects(track_id=track_data["id"]).count() == 0:

            sp = login_spotify()
            audio_features = sp.audio_features([track_data["id"]])[0]

            if audio_features is None:
                if "type" not in track_data or track_data["type"] == "artist":
                    return None

                track_data = TrackData(
                    track_id=track_data["id"],
                    name=track_data["name"],
                    artist=track_data["artists"][0]["name"],
                    artist_id=track_data["artists"][0]["id"],
                    acousticness=-1,
                    danceability=-1,
                    energy=-1,
                    instrumentalness=-1,
                    liveness=-1,
                    loudness=-1,
                    speechiness=-1,
                    valence=-1,
                    tempo=-1,
                )
            else:
                if "name" not in track_data:
                    print(track_data)

                track_data = TrackData(
                    track_id=track_data["id"],
                    name=track_data["name"],
                    artist=track_data["artists"][0]["name"],
                    artist_id=track_data["artists"][0]["id"],
                    acousticness=audio_features["acousticness"],
                    danceability=audio_features["danceability"],
                    energy=audio_features["energy"],
                    instrumentalness=audio_features["instrumentalness"],
                    liveness=audio_features["liveness"],
                    loudness=(audio_features["loudness"] + 60) / 60,
                    speechiness=audio_features["speechiness"],
                    valence=audio_features["valence"],
                    tempo=audio_features["tempo"],
                )
            track_data.save()
        else:
            track_data = TrackData.objects(track_id=track_data["id"])[0]
        return track_data
