from abc import ABC, abstractmethod


class AbstractVotingRule(ABC):
    """
    Abstract class for the different aggregation strategies (called voting rules at an early stage).
    The voting rules can be used by first initialising with a list of user ids.
    Then, the calculate_votes function can be called to retrieve a generator which will yield all items in descending
    order based on the calculated score.

    Note: only PWS, Fairness, and Least Misery were used for the experiments, but more strategies were implemented.
    """

    def __init__(self, users):
        self.users = users

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def voting_rule(self, song, song_ratings):
        pass

    def calculate_votes(self, data):
        result = {}

        for song in data:
            result[song] = self.voting_rule(song, data[song])

        sorted_list = sorted(result.items(), key=lambda v: v[1], reverse=True)
        for track in sorted_list:
            yield track
