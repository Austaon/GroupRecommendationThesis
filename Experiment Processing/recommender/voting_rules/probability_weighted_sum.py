import copy
import random

from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class ProbabilityWeightedSum(AbstractVotingRule):
    """
    "Probability Weighted Sum" aggregation strategy. Calculates a pdf based on the squared averages of the ratings and
    picks a random item using the pdf as weights. The pdf is recalculated every time an item gets removed.
    """

    def get_name(self):
        return "Probability Weighted Sum"

    @staticmethod
    def calculate_sums(song_ratings):
        combined_sum = {s: sum(song_ratings[s].values()) ** 2 for s in song_ratings}
        max_sum = sum(combined_sum.values())
        combined_sum = {s: combined_sum[s] / max_sum for s in combined_sum}
        return combined_sum

    def voting_rule(self, song, song_ratings):
        return random.choices(list(song_ratings.keys()), weights=song_ratings.values())[0]

    def calculate_votes(self, data):
        result = {}

        data_copy = copy.deepcopy(data)

        while len(data_copy) > 0:
            combined_sum = self.calculate_sums(data)
            chosen_song = self.voting_rule(None, combined_sum)

            result[chosen_song] = combined_sum[chosen_song]
            data_copy.pop(chosen_song, None)

        return list(result.items())
