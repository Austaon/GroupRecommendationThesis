from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric
import numpy as np


class ManhattanDistance(AbstractDistanceMetric):
    """
    Manhattan distance, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.cityblock.html
    for more information.
    """

    def get_name(self):
        return "Manhattan Distance"

    def calculate_distance(self, track_a, track_b):

        temp_distance = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_a = track_a_features[attribute]
            attribute_b = track_b_features[attribute]

            temp_distance += abs(attribute_a - attribute_b)

        try:
            return 1 - temp_distance / len(self.attribute_keys)
        except ZeroDivisionError:
            return np.NaN
