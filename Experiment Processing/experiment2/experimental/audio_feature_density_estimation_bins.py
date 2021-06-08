import math
from pprint import pprint

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from scipy.integrate import simps, trapz
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity

from database.session import Session
from database.track_data import TrackData

# https://stackoverflow.com/questions/38711541/how-to-compute-the-probability-of-a-value-given-a-list-of-samples-from-a-distrib


def audio_feature_density_estimation_bins():
    """
    This file was made while trying to estimate the chance a track belongs in a user profile.
    It was not used more and I'm unsure if it still works.
    :return:
    """

    audio_features = {
        "acousticness": [[], [], []],
        "danceability": [[], [], []],
        "energy": [[], [], []],
        "instrumentalness": [[], [], []],
        "liveness": [[], [], []],
        "loudness": [[], [], []],
        "speechiness": [[], [], []],
        "valence": [[], [], []],
    }

    track_scores = [[], [], []]

    for user, session in Session.get_users_with_surveys():
        track_data = {track["id"]: TrackData.get_track(track) for track in user.seen_tracks}

        kd_dict = {}
        params = {'bandwidth': np.logspace(-1, 1, 20)}

        for audio_feature in audio_features:
            grid = GridSearchCV(KernelDensity(), params)

            kd_dict[audio_feature] = grid.fit(np.array([
                0 if track is None else
                track.get_feature(audio_feature)
                for (_, track) in track_data.items()
            ]).reshape(-1, 1)).best_estimator_

        for i in range(0, 3):

            for track in session.recommendations[i]["tracks"]:
                track_data = TrackData.get_track(track)

                if track_data is None:
                    continue

                track_features = track_data.get_metadata()

                track_score = 0
                boundary = 0.1
                n = 100
                step = (2 * boundary) / (n - 1)  # Step size
                # print(f"{track_data['name']} - {track_data['artist']}")

                for track_feature in track_features:

                    start = math.floor(track_features[track_feature]*10)/10
                    end = math.floor(track_features[track_feature]*10)/10 + boundary

                    x = np.linspace(start, end, n)[: np.newaxis]
                    log_score = kd_dict[track_feature].score_samples(x.reshape(-1, 1))

                    score = np.exp(log_score)
                    probability = np.sum(score * step)
                    # print(f"{track_feature} -> {probability}")
                    audio_features[track_feature][i].append(probability)

                    track_score += probability ** 0.5
                print(track_score)
                track_scores[i].append(1 if track_score > 4 else 0)

    # pprint(audio_features)
    for audio_feature in audio_features:
        print(f"{audio_feature}: {[f'{feature:.4f}' for feature in np.mean(audio_features[audio_feature], axis=1)]}")

    print(f"Track scores: {[f'{feature:.4f}' for feature in np.mean(track_scores, axis=1)]}")
