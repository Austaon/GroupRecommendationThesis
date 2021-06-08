import math
import numpy as np

from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class EuclideanDistance(AbstractDistanceMetric):
    """
    Euclidean distance metric, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.euclidean.html
    for more information.
    """

    def get_name(self):
        return "Euclidean Distance"

    def calculate_distance(self, track_a, track_b):

        temp_distance = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            temp_distance += (attribute_a - attribute_b) ** 2

        try:
            return 1 - math.sqrt(temp_distance)
        except ZeroDivisionError:
            return np.NaN
