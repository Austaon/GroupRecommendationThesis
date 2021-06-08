import math
import numpy as np

from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class CosineSimilarity(AbstractDistanceMetric):
    """
    Cosine similarity, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cosine.html
    for more information.
    """

    def get_name(self):
        return "Cosine Similarity"

    def calculate_distance(self, track_a, track_b):

        distance_a = 0
        distance_b = 0
        distance_a_b = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            distance_a += attribute_a ** 2
            distance_b += attribute_b ** 2
            distance_a_b += attribute_a * attribute_b

        try:
            return distance_a_b / (math.sqrt(distance_a) * math.sqrt(distance_b))
        except ZeroDivisionError:
            return np.NaN
