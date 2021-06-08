from database.database_util import connect_to_skip_database
from skip_dataset.generate_histogram import generate_histogram
from skip_dataset.generate_track_data import generate_track_data
from skip_dataset.plot_track_sum import import_track_sum

# File used to execute different functions related to Spotify Sequential Skip Prediction Challenge dataset.
# The functions are roughly grouped in different categories.
# Recommended use is to only execute one at the time,
# each function is explained in the associated file.
if __name__ == '__main__':
    # Establish a database connection.
    connect_to_skip_database()

    # generate_track_data()

    # import_track_sum()

    generate_histogram()
