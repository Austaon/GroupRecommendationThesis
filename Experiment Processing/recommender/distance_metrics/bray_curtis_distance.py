import numpy as np

from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class BrayCurtisDistance(AbstractDistanceMetric):
    """
    "Bray-Curtis Distance": Calculated by doing 1 - Bray-Curtis Dissimilarity.
    See https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.braycurtis.html for more information.
    """

    def get_name(self):
        return "Bray-Curtis Distance"

    def calculate_distance(self, track_a, track_b):

        distance_sum = 0
        distance_subtraction = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            distance_sum += abs(attribute_a + attribute_b)
            distance_subtraction += abs(attribute_a - attribute_b)

        try:
            return 1 - distance_subtraction / distance_sum
        except ZeroDivisionError:
            return np.NaN
