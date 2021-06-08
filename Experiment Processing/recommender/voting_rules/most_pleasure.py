from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class MostPleasure(AbstractVotingRule):
    """
    "Most Pleasure" aggregation strategy. Basically the opposite of Least Misery: returns that maximum rating of each track.
    """

    def get_name(self):
        return "Most Pleasure"

    def voting_rule(self, song, song_ratings):
        return max(song_ratings.values())


