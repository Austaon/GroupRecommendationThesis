from os import listdir
from os.path import isfile, join

import pandas as pd
from tabulate import tabulate
from tqdm import tqdm

from database.track_data import TrackData


def generate_track_data():
    """
    Converts the data from the Spotify Sequential Skip Prediction Challenge dataset to the database format.
    The data needs to be downloaded manually and put in the skip_dataset/data/ folder.
    :return:
    """

    folder_name = "skip_dataset/data/"

    all_files = [f for f in listdir(folder_name) if isfile(join(folder_name, f)) and f.endswith("csv")]

    df1 = pd.read_csv(folder_name + all_files[0])
    df2 = pd.read_csv(folder_name + all_files[1])

    df = pd.concat([df1, df2])

    for index, track in tqdm(df.iterrows(), total=df.shape[0]):

        track_data = TrackData(
            track_id=track["track_id"],
            name=track["track_id"],
            artist="N/A",
            artist_id="N/A",
            acousticness=track["acousticness"],
            danceability=track["danceability"],
            energy=track["energy"],
            instrumentalness=track["instrumentalness"],
            liveness=track["liveness"],
            loudness=(track["loudness"] + 60) / 60,
            speechiness=track["speechiness"],
            valence=track["valence"],
            tempo=track["tempo"],
        )

        track_data.save()

