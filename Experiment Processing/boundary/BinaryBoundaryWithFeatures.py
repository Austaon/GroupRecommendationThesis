from boundary.AbstractBoundary import AbstractBoundary
from database.track_data import TrackData


class BinaryBoundaryWithFeatures(AbstractBoundary):
    """
    The "Boundary Score". Finds the minimum and maximum value of each audio feature and checks if the audio feature
    of a track falls within these values. The score increases by 1/8 (0.125) for each audio feature that does.
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

        track = TrackData.get_track(track)
        audio_features = track.get_metadata()

        breakdown = {a: 0 for a in self.attributes}
        score = 0

        for a in self.attributes:
            if self.boundaries[a]["min"] <= audio_features[a] <= self.boundaries[a]["max"]:
                score += 1
                breakdown[a] = 1

        return score, breakdown

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            return_string += f"{a} (min: {self.boundaries[a]['min']:.2f}, max: {self.boundaries[a]['max']:.2f})\n"
        return return_string
