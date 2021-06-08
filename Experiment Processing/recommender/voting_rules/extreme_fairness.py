import copy
import random

from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class ExtremeFairness(AbstractVotingRule):
    """
    Experimental adaptation of the "Fairness" strategy, instead of passing the turn to the next user in the list,
    it instead gives the user with the lowest rating for the previously selected item a turn.
    """

    def __init__(self, users):
        super().__init__(users)
        self.user_map = {}

        count = 0
        for user in self.users:
            self.user_map[user] = count
            count += 1

        self.current_user = random.randint(0, len(self.users)-1)

    def get_name(self):
        return "Extreme Fairness"

    def next_user(self, song_data, chosen_song):
        ratings = song_data[chosen_song[0]]
        max_rating = min(ratings.items(), key=lambda k: k[1])

        self.current_user = self.user_map[max_rating[0]]

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

            self.next_user(data_copy, song_item)
            data_copy.pop(song_item[0], None)

        return list(result.items())
