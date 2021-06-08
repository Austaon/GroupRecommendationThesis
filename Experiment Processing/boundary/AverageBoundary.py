from boundary.AbstractBoundary import AbstractBoundary
from database.track_data import TrackData


class AverageBoundary(AbstractBoundary):
    """
    Experimental "Average" score, which works based on calculating the difference between the audio feature of a track
    and the average of that audio feature in a user profile.

    This score was not used for further analysis.
    """

    def compute_boundaries(self):
        for a in self.attributes:
            self.boundaries[a] = 0

        for spotify_track in self.user_tracks:
            track = TrackData.get_track(spotify_track["id"])

            audio_features = track.get_metadata()

            for a in self.attributes:

                if audio_features[a] < 0:
                    continue

                self.boundaries[a] += audio_features[a] / self.num_items

    def get_boundary_score(self, track):

        track = TrackData.get_track(track["id"])
        audio_features = track.get_metadata()

        breakdown = {a: 0 for a in self.attributes}
        score = 0

        for a in self.attributes:

            score += 1 - abs(audio_features[a] - self.boundaries[a])
            breakdown[a] = 1 - abs(audio_features[a] - self.boundaries[a])

        return score, breakdown

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            return_string += f"{a} (min: {self.boundaries[a]['min']:.2f}, max: {self.boundaries[a]['max']:.2f})\n"
        return return_string
