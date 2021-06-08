import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity

from boundary.AbstractBoundary import AbstractBoundary
from database.track_data import TrackData


class KDEBoundary(AbstractBoundary):
    """
    The "Kernel Score". Uses scikit-learn to train a Kernel Density Estimator for each user profile.
    The score is calculated by estimating the chance that each audio feature "fits" in the user profile and summing
    these together.
    """

    def compute_boundaries(self):

        params = {'bandwidth': np.logspace(-1, 1, 20)}

        track_data = {track["id"]: TrackData.get_track(track) for track in self.user_tracks}

        for a in self.attributes:
            grid = GridSearchCV(KernelDensity(), params)

            self.boundaries[a] = grid.fit(np.array([
                0 if track is None else
                track.get_feature(a)
                for (_, track) in track_data.items()
            ]).reshape(-1, 1)).best_estimator_

    def get_boundary_score(self, track):

        track_data = TrackData.get_track(track)
        track_features = track_data.get_metadata()

        breakdown = {a: 0 for a in self.attributes}

        track_score = 0
        boundary = 0.1
        n = 100
        step = boundary / (n - 1)  # Step size

        for track_feature in track_features:

            start = track_features[track_feature] - boundary / 2
            end = track_features[track_feature] + boundary / 2

            x = np.linspace(start, end, n)[: np.newaxis]
            log_score = self.boundaries[track_feature].score_samples(x.reshape(-1, 1))

            score = np.exp(log_score)
            probability = np.sum(score * step)
            track_score += probability

            breakdown[track_feature] = probability

        return track_score, breakdown

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            return_string += f"{a} (bandwidth: {self.boundaries[a].bandwidth:.2f})\n"
        return return_string
