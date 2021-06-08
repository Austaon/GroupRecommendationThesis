import random
import statistics

from scipy.stats import ttest_rel, ttest_ind

from boundary.BinaryBoundaryWithFeatures import BinaryBoundaryWithFeatures
from boundary.HistogramBoundary import HistogramBoundary
from boundary.KDEBoundary import KDEBoundary
from boundary.RatingBoundary import RatingBoundary
from database.session import Session
from recommender.recommender import Recommender
from recommender.voting_rules.fairness import Fairness
from recommender.voting_rules.least_misery import LeastMisery
from recommender.voting_rules.probability_weighted_sum import ProbabilityWeightedSum


def analyze_playlists_generated_from_hovered_tracks():
    """
    Recommends a new playlist based on different track and limit functions.
    The limit function was only experimented with and not used further.

    These new playlists are then analysis with the different scores to see if they give different results.

    There are several track functions available in this file.
    :return:
    """
    random.seed(a=42)  # For consistent results (especially from PWS)

    results_user_profiles = {
        "PWS": {
            "similarity": [], "boundary": [], "histogram": [], "kernel": [],
            "chosen_similarity": [], "chosen_boundary": [], "chosen_histogram": [], "chosen_kernel": []
        },
        "Fairness": {
            "similarity": [], "boundary": [], "histogram": [], "kernel": [],
            "chosen_similarity": [], "chosen_boundary": [], "chosen_histogram": [], "chosen_kernel": []
        },
        "LM": {
            "similarity": [], "boundary": [], "histogram": [], "kernel": [],
            "chosen_similarity": [], "chosen_boundary": [], "chosen_histogram": [], "chosen_kernel": []
        },
    }

    metadata = {
        "PWS": {
            "voting_rule": ProbabilityWeightedSum,
            "index": 0
        },
        "Fairness": {
            "voting_rule": Fairness,
            "index": 1
        },
        "LM": {
            "voting_rule": LeastMisery,
            "index": 2
        }
    }

    # This track function returns the interacted items minus the selected items (except if those are the same, then
    # it just returns the same five items)

    # def get_tracks_function(user):
    #     hovered_tracks = user.get_hovered_tracks()
    #     chosen_tracks = user.get_chosen_tracks()
    #     for chosen_track in chosen_tracks:
    #         if chosen_track in hovered_tracks:
    #             del hovered_tracks[chosen_track]
    #
    #     if len(hovered_tracks) == 0:
    #         return user.get_hovered_tracks()
    #
    #     return hovered_tracks

    # def get_tracks_function(user):
    #     return user.get_chosen_tracks()

    def get_tracks_function(user):
        return user.get_hovered_tracks()

    # Example of a limit function that re-ranks items based on the kernel score and then returns the top five items.
    def limit_function(tracks, user):
        boundary = KDEBoundary(user)
        track_ratings = {}
        for track in tracks:
            score, _ = boundary.get_boundary_score(track)
            track_ratings[track] = score

        sorted_tracks = [k for k, v in sorted(track_ratings.items(), key=lambda item: item[1], reverse=True)][:5]
        return {track: tracks[track] for track in sorted_tracks}

    count = 0
    total_count = Session.get_number_completed_sessions()

    for session in Session.get_completed_sessions():

        print(f"{count + 1} / {total_count} ", end="")
        count += 1

        for voting_rule_key in metadata.keys():

            print(f"{voting_rule_key}, ", end="")

            voting_rule = metadata[voting_rule_key]["voting_rule"]
            voting_rule_index = metadata[voting_rule_key]["index"]

            users = [user.spotify_id for user in session.get_users()]

            recommender = Recommender()

            playlist, ratings = recommender.recommend(
                session,
                voting_rule(users),
                get_tracks_function  # , limit_function
            )

            similarity_scores = []
            boundary_scores = []
            histogram_scores = []
            kernel_scores = []

            session_tracks = [track["id"] for track in session.recommendations[voting_rule_index]["tracks"]]
            session_distances = session.recommendations[voting_rule_index]["metadata"]["distances"]

            scores_chosen_similarity = []
            scores_chosen_boundary = []
            scores_chosen_histogram = []
            scores_chosen_kernel = []

            for user in session.get_users():
                features_boundary = BinaryBoundaryWithFeatures(user)
                histogram_boundary = HistogramBoundary(user)
                kde_boundary = KDEBoundary(user)

                for track in playlist:
                    boundary_score, _ = features_boundary.get_boundary_score({"id": track})
                    histogram_score, _ = histogram_boundary.get_boundary_score({"id": track})
                    kernel_score, _ = kde_boundary.get_boundary_score({"id": track})

                    similarity_scores.append(ratings[track][user.spotify_id])
                    boundary_scores.append(boundary_score)
                    histogram_scores.append(histogram_score)
                    kernel_scores.append(kernel_score)

                for track_id in session_distances[user.spotify_id]:
                    if track_id in session_tracks:
                        scores_chosen_similarity.append(session_distances[user.spotify_id][track_id])

                        boundary_score, _ = features_boundary.get_boundary_score({"id": track_id})
                        histogram_score, _ = histogram_boundary.get_boundary_score({"id": track_id})
                        kernel_score, _ = kde_boundary.get_boundary_score({"id": track_id})

                        scores_chosen_boundary.append(boundary_score)
                        scores_chosen_histogram.append(histogram_score)
                        scores_chosen_kernel.append(kernel_score)

            results_user_profiles[voting_rule_key]["similarity"].extend(similarity_scores)
            results_user_profiles[voting_rule_key]["boundary"].extend(boundary_scores)
            results_user_profiles[voting_rule_key]["histogram"].extend(histogram_scores)
            results_user_profiles[voting_rule_key]["kernel"].extend(kernel_scores)

            results_user_profiles[voting_rule_key]["chosen_similarity"].extend(scores_chosen_similarity)
            results_user_profiles[voting_rule_key]["chosen_boundary"].extend(scores_chosen_boundary)
            results_user_profiles[voting_rule_key]["chosen_histogram"].extend(scores_chosen_histogram)
            results_user_profiles[voting_rule_key]["chosen_kernel"].extend(scores_chosen_kernel)

        print("")

    r_u = results_user_profiles

    for key in results_user_profiles:
        print(f"{key:8s}:\n"
              f"Chosen  Similarity: {statistics.mean(r_u[key]['chosen_similarity']):.2f}, {statistics.stdev(r_u[key]['chosen_similarity']):.2f}; "
              f"Boundary: {statistics.mean(r_u[key]['chosen_boundary']):.2f}, {statistics.stdev(r_u[key]['chosen_boundary']):.2f}; "
              f"Histogram: {statistics.mean(r_u[key]['chosen_histogram']):.2f}, {statistics.stdev(r_u[key]['chosen_histogram']):.2f}; "
              f"Kernel: {statistics.mean(r_u[key]['chosen_kernel']):.2f}, {statistics.stdev(r_u[key]['chosen_kernel']):.2f}\n"
              f"New     Similarity: {statistics.mean(r_u[key]['similarity']):.2f}, {statistics.stdev(r_u[key]['similarity']):.2f}; "
              f"Boundary: {statistics.mean(r_u[key]['boundary']):.2f}, {statistics.stdev(r_u[key]['boundary']):.2f}; "
              f"Histogram: {statistics.mean(r_u[key]['histogram']):.2f}, {statistics.stdev(r_u[key]['histogram']):.2f}; "
              f"Kernel: {statistics.mean(r_u[key]['kernel']):.2f}, {statistics.stdev(r_u[key]['kernel']):.2f}\n"
              f"t_test, similarity (df={len(r_u[key]['chosen_similarity'])}, {len(r_u[key]['similarity'])}): "
              f"{ttest_ind(r_u[key]['chosen_similarity'], r_u[key]['similarity'], equal_var=False)}\n"
              f"t_test, boundary   (df={len(r_u[key]['chosen_boundary'])}, {len(r_u[key]['boundary'])}): "
              f"{ttest_ind(r_u[key]['chosen_boundary'], r_u[key]['boundary'], equal_var=False)}\n"
              f"t_test, histogram  (df={len(r_u[key]['chosen_histogram'])}, {len(r_u[key]['histogram'])}): "
              f"{ttest_ind(r_u[key]['chosen_histogram'], r_u[key]['histogram'], equal_var=False)}\n"
              f"t_test, kernel     (df={len(r_u[key]['chosen_kernel'])}, {len(r_u[key]['kernel'])}): "
              f"{ttest_ind(r_u[key]['chosen_kernel'], r_u[key]['kernel'], equal_var=False)}\n")


# Results

# NO LIMIT
# CHOSEN
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.92, 0.09; Boundary: 7.12, 1.29; Histogram: 2.98, 0.59; Kernel: 1.65, 0.23
# t_test (df=400, 400): Ttest_indResult(statistic=-1.3973556934782363, pvalue=0.16269620282889452)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.6492247584263782, pvalue=0.5163799978625025)
# t_test (df=400, 400): Ttest_indResult(statistic=-2.0899645947754837, pvalue=0.03694304704940378)
# t_test (df=400, 400): Ttest_indResult(statistic=-1.6769440815010155, pvalue=0.0939478685190991)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.91, 0.10; Boundary: 6.96, 1.42; Histogram: 2.92, 0.61; Kernel: 1.62, 0.26
# t_test (df=400, 400): Ttest_indResult(statistic=0.7321446483001859, pvalue=0.46429768115592596)
# t_test (df=400, 400): Ttest_indResult(statistic=1.4756731392356481, pvalue=0.14042666335752105)
# t_test (df=400, 400): Ttest_indResult(statistic=0.13572168301123194, pvalue=0.8920755833665549)
# t_test (df=400, 400): Ttest_indResult(statistic=1.3692429105257287, pvalue=0.17131082606418493)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.93, 0.07; Boundary: 7.26, 1.16; Histogram: 2.98, 0.60; Kernel: 1.68, 0.22
# t_test (df=400, 400): Ttest_indResult(statistic=-0.3252486359026212, pvalue=0.7450781785695852)
# t_test (df=400, 400): Ttest_indResult(statistic=0.09192554869588833, pvalue=0.9267802677078205)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.686147918593145, pvalue=0.49281946372535634)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.09538024107357988, pvalue=0.9240367555664086)
#
# INTERACTED:
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.91, 0.09; Boundary: 7.07, 1.40; Histogram: 2.82, 0.66; Kernel: 1.61, 0.26
# t_test (df=400, 400): Ttest_indResult(statistic=-0.18226574402232898, pvalue=0.8554204969857491)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.1297309957169672, pvalue=0.896812072646979)
# t_test (df=400, 400): Ttest_indResult(statistic=1.3821088225742728, pvalue=0.16732523211395411)
# t_test (df=400, 400): Ttest_indResult(statistic=0.7014504676905425, pvalue=0.4832265241018159)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.91, 0.11; Boundary: 7.02, 1.46; Histogram: 2.78, 0.68; Kernel: 1.59, 0.27
# t_test (df=400, 400): Ttest_indResult(statistic=0.2353965638414779, pvalue=0.8139646352818788)
# t_test (df=400, 400): Ttest_indResult(statistic=0.8765205387601963, pvalue=0.38101209300822014)
# t_test (df=400, 400): Ttest_indResult(statistic=3.177061249228485, pvalue=0.0015452876070216471)
# t_test (df=400, 400): Ttest_indResult(statistic=2.8822678198811005, pvalue=0.004055603004105211)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.94, 0.05; Boundary: 7.36, 1.10; Histogram: 2.94, 0.58; Kernel: 1.69, 0.20
# t_test (df=400, 400): Ttest_indResult(statistic=-3.9903782026821273, pvalue=7.246598335124974e-05)
# t_test (df=400, 400): Ttest_indResult(statistic=-1.1663725351389158, pvalue=0.2438129826564188)
# t_test (df=400, 400): Ttest_indResult(statistic=0.36236809800971437, pvalue=0.7171736360913349)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.4069345718501755, pvalue=0.6841657186404777)
#
# INTERACTED - SELECTED
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.89, 0.12; Boundary: 6.85, 1.55; Histogram: 2.70, 0.69; Kernel: 1.57, 0.28
# t_test (df=400, 400): Ttest_indResult(statistic=1.9689122344540955, pvalue=0.04934078357144461)
# t_test (df=400, 400): Ttest_indResult(statistic=2.0101086426040795, pvalue=0.044764585693345)
# t_test (df=400, 400): Ttest_indResult(statistic=3.7765009523783637, pvalue=0.00017086610356198192)
# t_test (df=400, 400): Ttest_indResult(statistic=3.1794424868580857, pvalue=0.001533117399764945)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.91, 0.12; Boundary: 7.06, 1.44; Histogram: 2.78, 0.66; Kernel: 1.59, 0.26
# t_test (df=400, 400): Ttest_indResult(statistic=0.08075540732753915, pvalue=0.9356581931216359)
# t_test (df=400, 400): Ttest_indResult(statistic=0.4784193839624211, pvalue=0.6324832121363999)
# t_test (df=400, 400): Ttest_indResult(statistic=3.282312885877729, pvalue=0.0010744790023246736)
# t_test (df=400, 400): Ttest_indResult(statistic=2.7159812564468218, pvalue=0.006752456985366699)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.93, 0.08; Boundary: 7.26, 1.23; Histogram: 2.86, 0.62; Kernel: 1.66, 0.23
# t_test (df=400, 400): Ttest_indResult(statistic=-1.1750969829142432, pvalue=0.24031390898223565)
# t_test (df=400, 400): Ttest_indResult(statistic=0.029745929831719923, pvalue=0.9762771559364403)
# t_test (df=400, 400): Ttest_indResult(statistic=2.12791532163012, pvalue=0.033650031934587134)
# t_test (df=400, 400): Ttest_indResult(statistic=1.4628500033594365, pvalue=0.14390318054985646)

# FIVE TRACK LIMIT (Histogram)
# CHOSEN
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.91, 0.09; Boundary: 7.08, 1.30; Histogram: 2.94, 0.61; Kernel: 1.64, 0.24
# t_test (df=400, 400): Ttest_indResult(statistic=-1.1998175659393524, pvalue=0.23056681677172003)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.24257448082523161, pvalue=0.808397394300927)
# t_test (df=400, 400): Ttest_indResult(statistic=-1.0614292224649815, pvalue=0.28881902993657327)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.6698347094123226, pvalue=0.5031571231171477)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.91, 0.09; Boundary: 7.07, 1.34; Histogram: 3.11, 0.57; Kernel: 1.68, 0.23
# t_test (df=400, 400): Ttest_indResult(statistic=-0.5038666223743568, pvalue=0.6144941905853201)
# t_test (df=400, 400): Ttest_indResult(statistic=0.34020948977333865, pvalue=0.7337883345486012)
# t_test (df=400, 400): Ttest_indResult(statistic=-4.308992862806778, pvalue=1.847033566152875e-05)
# t_test (df=400, 400): Ttest_indResult(statistic=-2.038368374645507, pvalue=0.04184270908213692)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.93, 0.07; Boundary: 7.26, 1.16; Histogram: 2.98, 0.60; Kernel: 1.68, 0.22
# t_test (df=400, 400): Ttest_indResult(statistic=-0.3252486359026684, pvalue=0.7450781785695497)
# t_test (df=400, 400): Ttest_indResult(statistic=0.09192554869588833, pvalue=0.9267802677078205)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.686147918593145, pvalue=0.49281946372535634)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.09538024107357988, pvalue=0.9240367555664086)
#
# INTERACTED
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.92, 0.11; Boundary: 7.16, 1.29; Histogram: 3.21, 0.59; Kernel: 1.72, 0.25
# t_test (df=400, 400): Ttest_indResult(statistic=-2.4908865165125316, pvalue=0.012952718218285529)
# t_test (df=400, 400): Ttest_indResult(statistic=-1.1122452520116655, pvalue=0.2663679062306583)
# t_test (df=400, 400): Ttest_indResult(statistic=-7.288646023299842, pvalue=7.662993948489623e-13)
# t_test (df=400, 400): Ttest_indResult(statistic=-5.226968838806225, pvalue=2.202047841087715e-07)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.93, 0.11; Boundary: 7.19, 1.25; Histogram: 3.30, 0.58; Kernel: 1.75, 0.24
# t_test (df=400, 400): Ttest_indResult(statistic=-2.71534004276241, pvalue=0.0067693151023742355)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.9177192760384477, pvalue=0.3590450536115174)
# t_test (df=400, 400): Ttest_indResult(statistic=-8.683749724289772, pvalue=2.1632139067158217e-17)
# t_test (df=400, 400): Ttest_indResult(statistic=-6.141726253031106, pvalue=1.2869631601614056e-09)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.94, 0.10; Boundary: 7.32, 1.13; Histogram: 3.27, 0.57; Kernel: 1.77, 0.23
# t_test (df=400, 400): Ttest_indResult(statistic=-2.1646389707307527, pvalue=0.03075263984251333)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.6823390477000503, pvalue=0.4952226192267619)
# t_test (df=400, 400): Ttest_indResult(statistic=-7.359352767412329, pvalue=4.63550028295561e-13)
# t_test (df=400, 400): Ttest_indResult(statistic=-5.587443987829305, pvalue=3.1636888451246855e-08)
#
# INTERACTED - SELECTED
# PWS     :
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.06, 1.32; Histogram: 2.89, 0.67; Kernel: 1.63, 0.25
# New     Similarity: 0.91, 0.13; Boundary: 7.07, 1.38; Histogram: 3.09, 0.62; Kernel: 1.69, 0.27
# t_test (df=400, 400): Ttest_indResult(statistic=-0.5374302424204874, pvalue=0.5911391127309524)
# t_test (df=400, 400): Ttest_indResult(statistic=-0.15712295673340015, pvalue=0.8751877651033474)
# t_test (df=400, 400): Ttest_indResult(statistic=-4.5161774897645035, pvalue=7.253834779245485e-06)
# t_test (df=400, 400): Ttest_indResult(statistic=-3.6103972837228606, pvalue=0.00032490363778550245)
#
# Fairness:
# Chosen  Similarity: 0.91, 0.09; Boundary: 7.11, 1.36; Histogram: 2.93, 0.63; Kernel: 1.64, 0.24
# New     Similarity: 0.91, 0.13; Boundary: 7.08, 1.39; Histogram: 3.18, 0.64; Kernel: 1.71, 0.27
# t_test (df=400, 400): Ttest_indResult(statistic=-0.5929713668624964, pvalue=0.5533922543172136)
# t_test (df=400, 400): Ttest_indResult(statistic=0.3080842115848144, pvalue=0.7580986842274395)
# t_test (df=400, 400): Ttest_indResult(statistic=-5.6655270420683514, pvalue=2.046666448394408e-08)
# t_test (df=400, 400): Ttest_indResult(statistic=-3.9434698565511335, pvalue=8.750684009018268e-05)
#
# LM      :
# Chosen  Similarity: 0.93, 0.07; Boundary: 7.26, 1.15; Histogram: 2.95, 0.63; Kernel: 1.68, 0.22
# New     Similarity: 0.92, 0.13; Boundary: 7.21, 1.29; Histogram: 3.15, 0.62; Kernel: 1.73, 0.26
# t_test (df=400, 400): Ttest_indResult(statistic=0.8335602891455909, pvalue=0.40485771757692735)
# t_test (df=400, 400): Ttest_indResult(statistic=0.5791870319669511, pvalue=0.562628748588077)
# t_test (df=400, 400): Ttest_indResult(statistic=-4.558818863011932, pvalue=5.951018659433864e-06)
# t_test (df=400, 400): Ttest_indResult(statistic=-2.8869506615530183, pvalue=0.003997869730323633)
