import statistics

from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class Median(AbstractVotingRule):
    """
    "Median" aggregation strategy. Returns the median rating of all tracks, as the name implies.
    """

    def get_name(self):
        return "Median"

    def voting_rule(self, song, song_ratings):
        return statistics.median(song_ratings.values())


