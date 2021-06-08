from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class Average(AbstractVotingRule):
    """
    "Average" aggregation strategy, works by calculating the average rating for each song.
    """

    def get_name(self):
        return "Average"

    def voting_rule(self, song, song_ratings):

        average = 0
        for user in song_ratings:
            average += song_ratings[user]

        return average / len(song_ratings)
