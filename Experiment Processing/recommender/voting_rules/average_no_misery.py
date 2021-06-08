from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class AverageNoMisery(AbstractVotingRule):
    """
    "Average without Misery" aggregation strategy. Works by calculating the averages of each song, but discarding any
    song that has _any_ rating below a certain threshold.
    """

    def __init__(self, users, threshold):
        super().__init__(users)
        self.threshold = threshold

    def get_name(self):
        return "Average No Misery"

    def voting_rule(self, song, song_ratings):

        average = 0
        for user in song_ratings:

            if song_ratings[user] < self.threshold:
                return 0

            average += song_ratings[user]

        return average / len(song_ratings)
