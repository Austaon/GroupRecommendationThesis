from recommender.distance_metrics.abstract_distance_metric import AbstractDistanceMetric


class CanberraDistance(AbstractDistanceMetric):
    """
    Canberra distance, see https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.canberra.html
    for more information.
    """

    def get_name(self):
        return "Canberra Distance"

    def calculate_distance(self, track_a, track_b):

        distance_sum = 0

        track_a_features = track_a.get_metadata()
        track_b_features = track_b.get_metadata()

        for attribute in self.attribute_keys:
            attribute_own = track_a_features[attribute]
            attribute_other = track_b_features[attribute]

            if attribute_own == 0 and attribute_other == 0:
                distance_sum += 0
            else:
                distance_sum += abs(attribute_own - attribute_other) / (abs(attribute_own) + abs(attribute_other))

        return distance_sum
