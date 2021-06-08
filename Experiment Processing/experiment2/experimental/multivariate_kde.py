import numpy as np
from sklearn.decomposition import PCA
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KernelDensity

from database.session import Session
from database.track_data import TrackData


def get_probability(kde, pca, tracks):
    track_pca = pca.fit_transform(np.array([TrackData.get_track(track).get_array_data() for track in tracks]).T)

    boundary = 0.05
    n = 100

    step = (2 * boundary) / (n - 1)  # Step size

    log_score = kde.score_samples(track_pca)
    score = np.exp(log_score)
    return np.sum(score * step)


def multivariate_kde():
    """
    This file was made while trying to estimate the chance a track belongs in a user profile.
    It was not used more and I'm unsure if it still works.
    :return:
    """

    for session in Session.objects(state="show_playlist"):
        for user in session.get_users():
            if not user.survey:
                continue

            hovered_tracks = np.array([TrackData.get_track(track).get_array_data() for track in user.hovered_tracks])

            pca = PCA(n_components=1, whiten=False)
            data = pca.fit_transform(hovered_tracks)

            params = {'bandwidth': np.logspace(-1, 1, 20)}
            grid = GridSearchCV(KernelDensity(), params)
            grid.fit(data)

            kd = grid.best_estimator_
            print(f"Best estimator: {kd.bandwidth}")

            probability = get_probability(kd, pca, user.tracks)
            print(probability)

            probability = get_probability(kd, pca, session.recommendations[0]["tracks"])
            print(probability)
            probability = get_probability(kd, pca, session.recommendations[1]["tracks"])
            print(probability)
            probability = get_probability(kd, pca, session.recommendations[2]["tracks"])
            print(probability)

            # x = np.array([TrackData.get_track(session.recommendations[0]["tracks"][0]).get_array_data()])
            # x_data = pca.fit_transform(x.T)
            # kd_vals = np.exp(kd.score_samples(x_data))
            # print(kd_vals)

            return

