from mongoengine.base import BaseDict

from boundary.AbstractBoundary import AbstractBoundary
from recommender.distance_metrics.cosine_similarity import CosineSimilarity


class RatingBoundary(AbstractBoundary):
    """
    The "Similarity Score". Works by calculating the mean distance between the new track and each track in the user profile.
    """

    def __init__(self, user):
        super().__init__(user)
        self.distance_metric = CosineSimilarity()

    def compute_boundaries(self):

        pass

    def get_boundary_score(self, track):

        # The distance metric expects a track id as a string, due to stupid reasons, so change it to a string if a
        # dict is passed to this function.
        if type(track) == BaseDict:
            track = track["id"]

        track_score = self.distance_metric.calculate_ratings(
            self.user_track_ids, [track], exclude_own_tracks=False
        )

        if len(track_score) == 0:
            return 0, False

        return track_score[track], False

    def __repr__(self):
        return_string = ""
        for a in self.boundaries:
            return_string += f"{a} (min: {self.boundaries[a]['min']:.2f}, max: {self.boundaries[a]['max']:.2f})\n"
        return return_string
