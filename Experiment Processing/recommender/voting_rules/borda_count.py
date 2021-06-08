from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class BordaCount(AbstractVotingRule):
    """
    "Borda Count" aggregation strategy. See https://en.wikipedia.org/wiki/Borda_count for more information.
    """

    def __init__(self, users, number_of_points=5):
        super().__init__(users)
        self.number_of_points = number_of_points

    def get_name(self):
        return "Borda Count"

    def calculate_borda_ratings(self, song_ratings, user):
        user_ratings = {k: v[user] for k, v in song_ratings.items()}
        sorted_ratings = sorted(user_ratings.items(), key=lambda v: v[1], reverse=True)

        max_points = self.number_of_points

        borda_ratings = []

        for song in sorted_ratings:
            borda_ratings.append((song[0], max_points))
            max_points = max_points - 1 if max_points > 0 else 0

        return borda_ratings

    def voting_rule(self, song, song_ratings):
        pass

    def calculate_votes(self, data):
        result = {}

        for song in data:
            result[song] = 0

        for user in self.users:
            user_ratings = self.calculate_borda_ratings(data, user)

            for song in user_ratings:
                result[song[0]] += song[1]

        return sorted(result.items(), key=lambda v: v[1], reverse=True)
