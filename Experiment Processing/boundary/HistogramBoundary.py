import math

import numpy as np

from boundary.AbstractBoundary import AbstractBoundary
from database.track_data import TrackData


class HistogramBoundary(AbstractBoundary):
    """
    The "Histogram Score". Puts the values of each audio feature of each track in one of ten bins.
    The score is calculated by finding the bin an audio feature of a track belongs to and dividing the respective
    number by the total number of tracks in the user profile.
    """

    @staticmethod
    def floor(digit):
        return math.floor(digit*10)/10

    def compute_boundaries(self):

        for a in self.attributes:
            self.boundaries[a] = {
                round(index, 1): 0 for index in np.linspace(0.0, 1.0, 11, endpoint=True)
            }

        for spotify_track in self.user_tracks:
            track = TrackData.get_track(spotify_track["id"])

            audio_features = track.get_metadata()

            for a in self.attributes:
                rounded_attribute = self.floor(audio_features[a])

                if rounded_attribute < 0:
                    continue

                self.boundaries[a][rounded_attribute] += 1

    def get_boundary_score(self, track):

        track_data = TrackData.get_track(track)

        if track_data is None:
            return 0

        track_features = track_data.get_metadata()

        track_score = 0
        breakdown = {a: 0 for a in self.attributes}

        for a in self.attributes:
            rounded_down_attribute = self.floor(track_features[a])
            score = self.boundaries[a][rounded_down_attribute] / self.num_items
            track_score += score
            breakdown[a] = score

        return track_score, breakdown

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            bins = ', '.join([
                f"{current_bin}: {amount}" for current_bin, amount in
                self.boundaries[a].items() if amount > 0
            ])
            return_string += f"{a} ({bins})\n"
        return return_string
