import math
import numpy as np

from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class CorrelationDistance(AbstractDistanceMetric):
    """
    Correlation distance metric. See https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.correlation.html
    for more information.
    """

    def get_name(self):
        return "Correlation Distance"

    def calculate_mean(self, track_features):

        mean = 0

        for attribute in self.attribute_keys:
            mean += track_features[attribute]

        return mean / len(self.attribute_keys)

    def calculate_distance(self, track_a, track_b):
        distance_u = 0
        distance_v = 0
        distance_u_v = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        mean_a = self.calculate_mean(track_a_features)
        mean_b = self.calculate_mean(track_b_features)

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            distance_u += (attribute_a - mean_a) ** 2
            distance_v += (attribute_b - mean_b) ** 2
            distance_u_v += (attribute_a - mean_a) * (attribute_b - mean_b)

        try:
            distance_u /= len(self.attribute_keys)
            distance_v /= len(self.attribute_keys)
            distance_u_v /= len(self.attribute_keys)
            return 1 - (distance_u_v / math.sqrt(distance_u * distance_v))
        except ZeroDivisionError:
            return np.NaN
