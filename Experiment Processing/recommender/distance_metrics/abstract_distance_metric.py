from abc import ABC, abstractmethod
import numpy as np
from mongoengine.base import BaseDict

from database.track_data import TrackData


class AbstractDistanceMetric(ABC):
    """
    Abstract class for the distance metrics. Only cosine similarity was used in the experiments,
    but others are available too, but the code is not sufficiently tested.

    Implementation of some of these methods is a bit dodgy, beware. :D
    """

    def __init__(self):

        self.attribute_keys = [
            "acousticness", "danceability", "energy", "instrumentalness",
            "liveness", "loudness", "speechiness", "valence"
        ]

        self.own_track_rating = 1.0

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def calculate_distance(self, track_a, track_b):
        pass

    def create_rating_for_person(self, track_ids):
        """
        Generate a ratings dict of tracks in a user profile.
        :param track_ids:
        :return:
        """
        return {k: self.own_track_rating for k in track_ids}

    def calculate_average_distance(self, track, user_profile):
        """
        Calculate the average distance of a track given a user profile
        :param track:
        :param user_profile:
        :return:
        """

        distances = [self.calculate_distance(track, TrackData.get_track(user_track)) for user_track in user_profile]

        return np.nanmean(distances)

    def calculate_ratings(self, user_profile, other_tracks, exclude_own_tracks=False):
        """
        Calculate the ratings of a list of tracks (other_tracks) based on a user profile. Can optionally exclude
        user tracks in the other_tracks variable to be calculated.
        :param user_profile: List of tracks that form a user profile
        :param other_tracks: List of tracks to calculate ratings for
        :param exclude_own_tracks: Prevent calculating ratings for user profile tracks
        :return: Dict consisting of track: rating pairs
        """

        # Fix invalid data ..., in some cases.
        if len(user_profile) > 0 and 0 in user_profile and type(user_profile[0]) == BaseDict:
            user_profile = [track["id"] for track_id, track in user_profile.items()]

        if len(other_tracks) > 0 and 0 in other_tracks and type(other_tracks[0]) == BaseDict:
            other_tracks = [track["id"] for track_id, track in other_tracks.items()]

        resulting_distances = {
            t: self.calculate_average_distance(TrackData.get_track(t), user_profile)
            for t in other_tracks if not exclude_own_tracks or (exclude_own_tracks and t not in user_profile)
        }

        return resulting_distances
