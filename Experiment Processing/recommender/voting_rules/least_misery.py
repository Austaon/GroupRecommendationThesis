from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class LeastMisery(AbstractVotingRule):
    """
    "Least Misery" aggregation rule, returns the minimum rating for each track, which is then sorted in a descending
    order in the abstract class.
    """

    def get_name(self):
        return "Least Misery"

    def voting_rule(self, song, song_ratings):
        return min(song_ratings.values())


