from boundary.AbstractBoundary import AbstractBoundary
from database.track_data import TrackData


class BinaryBoundary(AbstractBoundary):
    """
    Score that "accepts" a track if it falls within the minimum and maximum value of _each_ audio feature.
    That is, it returns 1.0 if it does and else returns 0.0 .
    """

    def compute_boundaries(self):
        for a in self.attributes:
            self.boundaries[a] = {
                "min": float("inf"),
                "max": float("-inf")
            }

        for spotify_track in self.user_tracks:
            track = TrackData.get_track(spotify_track["id"])

            audio_features = track.get_metadata()

            for a in self.attributes:

                if audio_features[a] < 0:
                    continue

                if audio_features[a] > self.boundaries[a]["max"]:
                    self.boundaries[a]["max"] = audio_features[a]
                if audio_features[a] < self.boundaries[a]["min"]:
                    self.boundaries[a]["min"] = audio_features[a]

    def get_boundary_score(self, track):

        track = TrackData.get_track(track["id"])
        audio_features = track.get_metadata()

        breakdown = {a: 1 for a in self.attributes}
        score = 8

        for a in self.attributes:
            if not (self.boundaries[a]["min"] <= audio_features[a] <= self.boundaries[a]["max"]):
                score = 0
                breakdown[a] = 0

        return score, breakdown

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            return_string += f"{a} (min: {self.boundaries[a]['min']:.2f}, max: {self.boundaries[a]['max']:.2f})\n"
        return return_string
