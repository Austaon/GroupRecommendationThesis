import pylab

from database.database_util import connect_to_database
from database.session import Session
from experiment2.boundary.boundary_features_breakdown import boundary_features_breakdown
from experiment2.boundary.boundary_playlists import boundary_playlists
from experiment2.boundary.boundary_rating import boundary_rating
from experiment2.boundary.check_user_boundaries import check_user_boundaries
from experiment2.boundary.plot_boundaries import plot_boundaries
from experiment2.calculate_average_ratings import calculate_average_ratings
from experiment2.calculate_individual_rating_use import calculate_individual_rating_use
from experiment2.count_matching_artists_per_session import count_matching_artists_per_session
from experiment2.count_picked_songs_per_playlist import count_picked_songs_per_playlist
from experiment2.feedback_analysis import feedback_analysis
from experiment2.generate_example_one_track_after_selected import generate_example_one_track_after_selected
from experiment2.get_experiment_stats import get_experiment_stats
from experiment2.get_group_purposes import get_group_purposes
from experiment2.hovered_tracks.analyze_playlists_generated_from_hovered_tracks import \
    analyze_playlists_generated_from_hovered_tracks
from experiment2.hovered_tracks.calculate_hovered_track_scores import calculate_hovered_track_scores
from experiment2.hovered_tracks.hovered_rating_over_time import hovered_rating_over_time
from experiment2.hovered_tracks.track_position_analysis import track_position_analysis
from experiment2.compare_selected_tracks_versus_not_selected import compare_selected_tracks_versus_not_selected
from experiment2.periodic_effects import periodic_effects
from experiment2.rating_index_analysis import rating_index_analysis
from experiment2.rating_index_analysis_original_order import rating_index_analysis_original_order
from experiment2.scores_vs_rating import scores_vs_rating
from experiment2.seen_track_analysis import seen_track_analysis
from experiment2.survey_fatigue import survey_fatigue
from recommender.recommender import Recommender
from util.fix_laravel_bug import fix_laravel_bug
from util.get_all_metadata import get_all_metadata

# File used to execute different functions related to the second experiment.
# The functions are roughly grouped in different categories.
# Recommended use is to only execute one at the time,
# each function is explained in the associated file.

# There is a lot of experimental functions in here that were not used in the end. I did my best listing these.

if __name__ == '__main__':

    # Database functions ##########
    # anonymize_database()
    connect_to_database()
    # get_all_metadata()
    # fix_laravel_bug()
    ###############################

    # Set pyplot parameters to keep plots consistent.
    params = {'legend.fontsize': 'xx-large',
              'axes.labelsize': 'xx-large',
              'axes.titlesize': 'xx-large',
              'xtick.labelsize': 'xx-large',
              'ytick.labelsize': 'xx-large'}
    pylab.rcParams.update(params)

    # Interacted items analysis ##########
    # calculate_hovered_track_scores()
    # analyze_playlists_generated_from_hovered_tracks()
    # hovered_rating_over_time()
    # track_position_analysis()
    ######################################

    # Similarity/Boundary/Histogram/Kernel score analysis ##########
    plot_boundaries()
    # boundary_rating()
    # boundary_features_breakdown()
    # boundary_playlists()
    # scores_vs_rating()
    ######################################

    # Experiment result analysis ##########
    # get_experiment_stats()
    # get_group_purposes()
    # calculate_average_ratings()
    # seen_track_analysis()
    # compare_selected_tracks_versus_not_selected()
    # periodic_effects()
    # generate_example_one_track_after_selected()
    # count_picked_songs_per_playlist()
    ######################################

    # Survey fatigue ##########
    # survey_fatigue()
    # rating_index_analysis()
    # rating_index_analysis_original_order()
    # calculate_individual_rating_use()
    ######################################

    # Experimental functions (mostly unused) ##########
    # feedback_analysis()
    # check_user_boundaries()
    # count_matching_artists_per_session()
    ######################################

    # Failed Experiments (unused) ##########
    # audio_feature_density_estimation()
    # audio_feature_density_estimation_bins()
    # random_forest_classifier_test()
    # multivariate_kde()
    ######################################
