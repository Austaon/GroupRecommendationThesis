import math
import random

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from database.session import Session
from database.track_data import TrackData


def random_forest_classifier_test():
    """
    This file was made while trying to estimate the chance a track belongs in a user profile.
    It was not used more and I'm unsure if it still works.
    :return:
    """

    for session in Session.objects(state="show_playlist"):
        for user in session.get_users():
            if not user.survey:
                continue

            hovered_tracks = [TrackData.get_track(track).get_array_data() for track in user.hovered_tracks]
            hovered_track_ids = [TrackData.get_track(track)["id"] for track in user.hovered_tracks]

            other_users = [new_user for new_user in session.get_users() if new_user.id != user.id]
            all_other_tracks = [TrackData.get_track(track).get_array_data()
                             for new_user in other_users
                             for track in new_user.hovered_tracks]

            all_other_tracks = [TrackData.get_track(track).get_inverse_array_data() for track in user.hovered_tracks]

            # all_other_tracks = [track.get_array_data()
            #                     for track in TrackData.objects()
            #                     if track.id not in hovered_track_ids]

            random.shuffle(all_other_tracks)

            false_label_length = len(all_other_tracks)  # math.floor(len(all_other_tracks) / 10)

            x_train = np.concatenate((hovered_tracks, all_other_tracks[:false_label_length]))
            labels = [1] * len(hovered_tracks) + [0] * false_label_length

            model = RandomForestClassifier(n_estimators=200)
            model.fit(x_train, labels)

            # y_test = np.array([0.221, 0.7, 0.722, 0, 0.272, 0.9407, 0.0369, 0.756])
            # y_hat = model.predict_proba(y_test.reshape(1, -1))
            # print(y_hat)
            #
            # y_test = np.array([0.849, 0.05, 0.05, 0.9952, 0.755, 0.173, 0.9285, 0.084])
            # y_hat = model.predict_proba(y_test.reshape(1, -1))
            # print(y_hat)

            recommended_tracks = session.recommendations[0]["tracks"]
            track_data = [TrackData.get_track(track).get_array_data() for track in recommended_tracks]

            for track in track_data:
                y_hat = model.predict_proba(np.array(track).reshape(1, -1))
                print(y_hat)

            return
