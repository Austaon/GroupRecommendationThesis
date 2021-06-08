from recommender.voting_rules.abstract_voting_rule import AbstractVotingRule


class CopelandRule(AbstractVotingRule):
    """
    "Copeland's Method" aggregation strategy. See https://en.wikipedia.org/wiki/Copeland%27s_method for more information.
    """

    def get_name(self):
        return "Copeland's Rule"

    @staticmethod
    def calculate_copeland_ratings(song_ratings, debug=False):

        result = {}
        test_array = []
        index = 0

        for song in song_ratings:
            result[song] = 0
            rating = song_ratings[song]
            rating_sum = sum(rating.values())

            test_array.append([])

            for competing_song in song_ratings:
                if song == competing_song:
                    test_array[index].append(0)
                    continue

                competing_rating = song_ratings[competing_song]
                competing_sum = sum(competing_rating.values())

                if rating_sum > competing_sum:
                    score = 1
                elif rating_sum == competing_sum:
                    score = 0.5
                else:
                    score = -1

                result[song] += score
                test_array[index].append(score)

            index += 1

        if debug:
            col_width = max(len(str(word)) for row in test_array for word in row) + 2  # padding
            for row in test_array:
                print("".join(str(word).ljust(col_width) for word in row))
        return result

    def normalize(self, ratings):
        min_rating = abs(min(ratings.values()))
        ratings = dict(map(lambda r: (r, ratings[r] + min_rating), ratings))
        max_rating = max(ratings.values())
        ratings = dict(map(lambda r: (r, ratings[r] * 10 / max_rating), ratings))

        return ratings

    def voting_rule(self, song, song_ratings):
        pass

    def calculate_votes(self, data):
        result = CopelandRule.calculate_copeland_ratings(data)

        result = self.normalize(result)

        return sorted(result.items(), key=lambda v: v[1], reverse=True)
