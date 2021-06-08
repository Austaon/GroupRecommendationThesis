import copy
import random

from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class Fairness(AbstractVotingRule):
    """
    "Fairness" aggregation strategy. Ensures that all group members have the same, or nearly the same,
     amount of items in a recommendation.
    """

    def __init__(self, users):
        super().__init__(users)
        self.current_user = random.randint(0, len(self.users)-1)

    def get_name(self):
        return "Fairness"

    def next_user(self):
        self.current_user = (self.current_user + 1) % len(self.users)

    def voting_rule(self, song, song_ratings):

        user_ratings = {k: v[self.users[self.current_user]] for k, v in song_ratings.items()}

        max_rating = max(user_ratings.items(), key=lambda k: k[1])

        return max_rating

    def calculate_votes(self, data):
        result = {}

        data_copy = copy.deepcopy(data)

        while len(data_copy) > 0:
            song_item = self.voting_rule(song=None, song_ratings=data_copy)
            result[song_item[0]] = song_item[1]

            data_copy.pop(song_item[0], None)
            self.next_user()

        return list(result.items())
