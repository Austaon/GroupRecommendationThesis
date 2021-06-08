from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class ChebyshevDistance(AbstractDistanceMetric):
    """
    Chebyshev distance, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.chebyshev.html
    for more information.
    """

    def get_name(self):
        return "Chebyshev Distance"

    def calculate_distance(self, track_a, track_b):
        max_distance = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_own = track_a_features[attribute]
            attribute_other = track_b_features[attribute]

            temp_distance = abs(attribute_own - attribute_other)
            if temp_distance > max_distance:
                max_distance = temp_distance

        return max_distance
