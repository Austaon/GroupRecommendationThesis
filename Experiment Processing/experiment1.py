import pylab

from database.database_util import connect_to_first_experiment_database
from experiment1.boundary_spotify_data import boundary_spotify_data
from experiment1.calculate_mutual_artists import calculate_mutual_artists
from experiment1.calculate_mutual_tracks import calculate_mutual_tracks
from experiment1.calculate_statistics import calculate_statistics
from experiment1.check_for_normality import check_for_normality
from experiment1.comment_statistics import get_comment_statistics
from experiment1.compare_datasets import compare_datasets
from experiment1.compare_tracks import compare_tracks
from experiment1.count_duplicates import count_duplicates
from experiment1.generate_random_data import generate_random_data
from experiment1.generate_recommended_data import generate_recommended_data
from experiment1.t_test import perform_t_test
from experiment1.t_test_boundary import perform_t_test_boundary
from util.get_all_metadata import get_all_metadata_from_users
from util.json_to_database import json_to_database

# File used to execute different functions related to the first experiment.
# The functions are roughly grouped in different categories.
# Recommended use is to only execute one at the time,
# each function is explained in the associated file.

if __name__ == '__main__':
    # Establish a database connection.
    connect_to_first_experiment_database()

    # Database functions ##########
    # json_to_database()
    # generate_random_data()
    # generate_recommended_data()
    get_all_metadata_from_users()
    ###############################

    # Set pyplot parameters to keep plots consistent.
    params = {'legend.fontsize': 'xx-large',
              'axes.labelsize': 'xx-large',
              'axes.titlesize': 'xx-large',
              'xtick.labelsize': 'xx-large',
              'ytick.labelsize': 'xx-large'}
    pylab.rcParams.update(params)

    # Statistics ##################
    # calculate_statistics()
    # get_comment_statistics()
    # count_duplicates("real")
    ###############################

    # Analysis ####################
    # perform_t_test()
    # compare_tracks("real")
    # compare_datasets("real", "random")
    # calculate_mutual_tracks("real")
    # calculate_mutual_artists("real")
    # check_for_normality()
    ################################

    # Experimental #################
    # boundary_spotify_data("real")
    # perform_t_test_boundary()
    ################################
