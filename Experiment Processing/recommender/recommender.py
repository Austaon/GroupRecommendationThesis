from database.track_data import TrackData
from recommender.distance_metrics.cosine_similarity import CosineSimilarity


class Recommender:
    """
    Class that handles recommending a new playlist for a group.
    This code was directly ported from Javascript, so some code might be awkward from a Python PoV.
    """

    def __init__(self):
        self.distance_metric = CosineSimilarity()

    def recommend(self, session, voting_rule, track_function, limit_function=lambda tracks, user: tracks):
        """
        Call this function to generate a new recommendation
        :param session: Dict with users and their selected tracks
        :param voting_rule:
        :param track_function: Lambda function returning the tracks that should be used from a user profile.
        :param limit_function: Optional lambda function that can be used to limit or re-rank the user tracks.
        :return: A list of tracks and a dict containing the ratings for each track and user.
        """

        tracks = {}
        song_data = {}
        self_ratings = {}

        for user in session.get_users():
            user_tracks = track_function(user)
            user_tracks = limit_function(user_tracks, user)

            song_data = {
                **song_data,
                **{track_id: TrackData.objects(track_id=track_id)[0] for track_id in user_tracks}
            }
            tracks = {**tracks, **{track_id: track for track_id, track in user_tracks.items()}}
            self_ratings[user.spotify_id] = self.distance_metric.create_rating_for_person(user_tracks)

        distances = self.dot_product_ratings(session, song_data, self_ratings, track_function, limit_function)
        ratings = self.form_ratings_object(session, song_data, distances)
        playlist_scores = self.create_playlist(ratings, voting_rule)[:10]

        playlist = {track_id: tracks[track_id] for track_id, _ in playlist_scores}

        return playlist, ratings

    def dot_product_ratings(self, session, song_data, self_ratings, track_function, limit_function):
        """
        Estimates the ratings of all tracks for each user and combines this with the rating of the tracks selected
        by a user.
        :param session: Same session variable as in the recommend function
        :param song_data: Dict containing all tracks in the session
        :param self_ratings: Dict containing the ratings of tracks selected by a specific user.
        :param track_function: Same track_function as in the recommend function
        :param limit_function: Same limit_function as in the recommend function
        :return:
        """

        distances = {}
        session_songs = [track_id for track_id in song_data]

        for user in session.get_users():

            chosen_tracks = [track_id for track_id in limit_function(track_function(user), user)]

            calculated_ratings = self.distance_metric.calculate_ratings(
                chosen_tracks,
                session_songs,
                exclude_own_tracks=True
            )

            distances[user.spotify_id] = {
                **calculated_ratings,
                **self_ratings[user.spotify_id]
            }

        return distances

    @staticmethod
    def form_ratings_object(session, song_data, distances):
        """
        Transforms the ratings object from user -> track to track -> user
        :param session:
        :param song_data:
        :param distances:
        :return:
        """
        result = {}

        for track_id, track in song_data.items():

            result[track_id] = {}
            for user in session.get_users():
                result[track_id][user.spotify_id] = distances[user.spotify_id][track_id]

        return result

    @staticmethod
    def create_playlist(ratings, voting_rule):
        """
        Creates a playlist generator and calls this while there are new tracks to generate.
        :param ratings:
        :param voting_rule:
        :return:
        """

        recommender_generator = voting_rule.calculate_votes(ratings)
        result = []
        for track in recommender_generator:
            result.append(track)
        return result
