import math
import numpy as np

from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class PearsonCorrelation(AbstractDistanceMetric):
    """
    Pearson correlation, see https://en.wikipedia.org/wiki/Pearson_correlation_coefficient for more information.
    Roughly mirrors the correlation distance.
    """

    def get_name(self):
        return "Pearson Correlation"

    def calculate_mean(self, track_features):

        mean = 0

        for attribute in self.attribute_keys:
            mean += track_features[attribute]

        return mean / len(self.attribute_keys)

    def calculate_distance(self, track_a, track_b):
        distance_a = 0
        distance_b = 0
        distance_a_b = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        mean_a = self.calculate_mean(track_a_features)
        mean_b = self.calculate_mean(track_b_features)

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            distance_a += (attribute_a - mean_a) ** 2
            distance_b += (attribute_b - mean_b) ** 2
            distance_a_b += (attribute_b - mean_b) * (mean_a - mean_a)

        try:
            return distance_a_b / (math.sqrt(distance_a * distance_b))
        except ZeroDivisionError:
            return np.NaN
