import pandas as pd
import matplotlib.pyplot as plt


def import_track_sum():
    """
    Plots the amount of times each track appears in the Spotify Sequential Skip Prediction Challenge dataset.
    The datafile is provided in the skip_dataset/data folder and was pre-generated using the full data.
    :return:
    """

    file_name = "skip_dataset/data/track_sum.csv"

    df = pd.read_csv(file_name)

    sums = df["sum"].to_list()
    sums.sort(reverse=True)

    plt.plot(sums)
    ax = plt.gca()
    ax.set_yscale("log")
    plt.show()
