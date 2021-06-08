from tqdm import tqdm

from database.track_data import TrackData

import matplotlib.pyplot as plt


def generate_histogram():
    """
    Generates audio feature histograms based on the Spotify Sequential Skip Prediction Challenge dataset.
    :return:
    """

    keys = ["acousticness", "danceability", "energy", "instrumentalness",
            "liveness", "loudness", "speechiness", "valence", "tempo"]

    histogram_values = {
            "acousticness": [],
            "danceability": [],
            "energy": [],
            "instrumentalness": [],
            "liveness": [],
            "loudness": [],
            "speechiness": [],
            "valence": [],
            "tempo": []
        }

    for track in tqdm(TrackData.objects, total=TrackData.objects.count()):
        audio_features = track.get_metadata()
        for key in keys:
            if key == "tempo":
                histogram_values[key].append(track.tempo)
            else:
                histogram_values[key].append(audio_features[key])

    for key in keys:
        plt.hist(histogram_values[key], bins=50)
        plt.show()
