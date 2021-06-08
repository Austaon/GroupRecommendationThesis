from abc import ABC, abstractmethod


class AbstractBoundary(ABC):
    """
    Abstract class that calculates the different scores (called 'boundaries' at an earlier stage)
    """

    def __init__(self, user, tracks_function=lambda user: user.get_hovered_tracks()):
        """
        Constructor of the Boundary class. The track_function variable expects a lambda returning the tracks that
        should be considered as user profile.
        :param user:
        :param tracks_function:
        """
        self.user = user
        self.attributes = [
            "acousticness", "danceability", "energy", "instrumentalness",
            "liveness", "loudness", "speechiness", "valence"
        ]

        self.user_tracks = [track for _, track in tracks_function(self.user).items()]
        self.user_track_ids = [track_id for track_id, _ in tracks_function(self.user).items()]
        self.num_items = len(self.user_tracks)

        self.boundaries = {}
        self.compute_boundaries()

    @abstractmethod
    def compute_boundaries(self):
        """
        Calculates the user profile.
        :return:
        """
        pass

    @abstractmethod
    def get_boundary_score(self, track):
        """
        Returns the score of a track.
        :param track:
        :return:
        """
        pass
