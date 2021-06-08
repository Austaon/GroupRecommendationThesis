import {
    LeastMisery, ProbabilityWeightedSum, Fairness
} from "./voting_rules";
import {
    CosineSimilarity
} from "./distance_metrics"

/**
 * Class that handles recommending a playlist. This is partly ported from old (deleted) Python code which was then later
 * ported back to Python.
 *
 * This recommender was also made for allowing any aggregation strategy or distance metric to be used dynamically,
 * so there is code left over to accommodate for this.
 *
 * The code for the distance metrics and aggregation strategies is ported directly from Python, the previous code is
 * often still commented to show how lines were changed around.
 *
 * The classes won't be commented individually due to this.
 */
export default class Recommender {
    constructor(kValues, useSpotifyRecommender = false, votingRule = ProbabilityWeightedSum, distanceMetric = CosineSimilarity) {
        this.k = kValues;
        this.useSpotifyRecommender = useSpotifyRecommender;
        this.songData = {};
        this.songFeatures = {};
        this.distances = {};
        this.generatorList = {};

        this.votingRule = new votingRule();
        this.votingRuleMap = {};

        this.distanceMetric = new distanceMetric();
        this.distanceMetricMap = {};

        this.safeVotingRules = [];

        const self = this;

        // Loads all voting rules and stores it into a map so they can be accessed by name.
        const votingRules = require("./voting_rules");
        Object.keys(votingRules).forEach(rule => {
            if (votingRules[rule].getRuleName() !== "Abstract Voting Rule") {
                self.votingRuleMap[votingRules[rule].getRuleName()] = votingRules[rule];
            }

            if(!["Abstract Voting Rule", "Probability Weighted Sum", "Fairness", "Random"].includes(
                votingRules[rule].getRuleName())) {
                this.safeVotingRules.push(votingRules[rule]);
            }
        });

        // Same with the distance metrics.
        const distanceMetrics = require("./distance_metrics");
        Object.keys(distanceMetrics).forEach(metric => {
            if (distanceMetrics[metric].getMetricName() !== "Abstract Distance Metric") {
                self.distanceMetricMap[distanceMetrics[metric].getMetricName()] = distanceMetrics[metric];
            }
        });
    }

    set spotifyApi(val) {
        this.spotify = val;
    }

    get votingRules() {
        return Object.values(this.votingRuleMap);
    }

    get distanceMetrics() {
        return Object.values(this.distanceMetricMap);
    }

    /**
     * Sets a new aggregation strategy and returns if a new strategy was set
     * @param val
     * @returns {boolean}
     */
    setVotingRule(val) {
        if (val !== this.votingRule.constructor.getRuleName() && val.length > 0) {
            this.votingRule = new this.votingRuleMap[val]();
            return true;
        }
        return false;
    }

    setRandomVotingRule() {
        const keys = Object.keys(this.votingRuleMap);
        this.votingRule = new this.votingRuleMap[keys [keys.length * Math.random() << 0]]();
        return true;
    }

    getRandomVotingRule() {
        const keys = Object.keys(this.safeVotingRules);
        return new this.safeVotingRules[keys[keys.length * Math.random() << 0]]();
    }

    /**
     * Sets a new aggregation strategy and returns if a new strategy was set
     * @param val
     * @returns {boolean}
     */
    setDistanceMetric(val) {
        if (val !== this.distanceMetric.constructor.getMetricName() && val.length > 0) {
            this.distanceMetric = new this.distanceMetricMap[val]();
            return true;
        }
        return false;
    }

    setRandomDistanceMetric() {
        const keys = Object.keys(this.distanceMetricMap);
        this.distanceMetric = new this.distanceMetricMap[keys [keys.length * Math.random() << 0]]();
        return true;
    }

    /**
     * Gets the audio features of a list of tracks.
     * @param userObject
     * @returns {Promise<SpotifyApi.MultipleAudioFeaturesResponse>}
     */
    getSongAttributes(userObject) {

        const trackList = userObject.tracks.map(track => track.id);

        return this.spotify.getAudioFeaturesForTracks(trackList)
            .then(data => {
                data["audio_features"].forEach(track => {
                    this.songFeatures[track["id"]] = track
                });
            }, function (error) {
                console.log(error);
            }
        )
    }

    /**
     * Experimental feature that uses the recommended tracks as seeds for the Spotify recommender.
     * @param tracks
     * @returns {Promise<never>|Promise<*[]>}
     */
    recommendTracks(tracks) {
        const self = this;
        let playlist = [];
        let promises = [];

        if (tracks.length === 0) {
            return Promise.reject();
        }

        tracks.forEach(track => {
            promises.push(self.spotify.getRecommendations({
                "seed_tracks": [track[0]],
                "limit": 3
            }).then(function (data) {
                playlist.push(...data["tracks"])
            }, function (err) {
                console.log(`error: ${err}`)
            }));
        });

        return Promise.all(promises).then(_ => {
            return playlist;
        });
    }

    /**
     * Used to generate three different playlists with the aggregation strategies used for the survey.
     * @param trackObject
     * @returns {Promise<unknown[]>}
     */
    sessionRecommend(trackObject) {

        const promises = [];

        promises.push(this.recommend(trackObject, new ProbabilityWeightedSum(), new CosineSimilarity()))
        promises.push(this.recommend(trackObject, new Fairness(), new CosineSimilarity()))
        promises.push(this.recommend(trackObject, new LeastMisery(), new CosineSimilarity()))

        return Promise.all(promises);
    }

    /**
     * Main function that handles the recommendation. Expects an object with users and their tracks, and optionally
     * allows for an aggregation strategy and distance metric as parameters.
     *
     * Returns a promise since a lot of API calls are done in this process.
     * @param trackObject
     * @param votingRule
     * @param distanceMetric
     * @returns {Promise<{metadata: {distances: {}, rule_name: ProbabilityWeightedSum, generator_list: *[], distance_metric: CosineSimilarity}, tracks: *[]}>}
     */
    recommend(trackObject, votingRule = this.votingRule, distanceMetric = this.distanceMetric) {

        const songData = {};

        trackObject.forEach(person => {
            person.tracks.forEach(track => {
                songData[track.id] = track;
            })
        })
        this.songData = songData;

        let selfRatings = {};
        let promises = [];
        let distances = {};
        let generatorList = [];

        // Creates ratings per person and retrieves the audio features for each track.
        Object.keys(trackObject).forEach(person => {
            selfRatings[trackObject[person].id] = distanceMetric.createRatingForPerson(trackObject[person]);
            promises.push(this.getSongAttributes(trackObject[person]));
        });

        return Promise.all(promises).then(_ => {
            // Estimates the ratings of all tracks for each user and combines it with the ratings of the selected tracks.
            const dotProductRatings = this.calculateDotProductRatings(trackObject, selfRatings, distanceMetric);
            distances = dotProductRatings;
            return this.formRatingsObject(dotProductRatings);
        }).then(ratings => {
            // Creates the playlists
            let result = this.createPlaylist(ratings, votingRule);
            generatorList = result;
            return result.slice(0, this.k);
        }).then(useForRecommendingTracks => {
            // Optionally: add more recommendation.
            if(this.useSpotifyRecommender) {
                return this.recommendTracks(useForRecommendingTracks)
            } else {
                const resultingTrackArray = [];
                useForRecommendingTracks.forEach(track => {
                    resultingTrackArray.push(songData[track[0]])
                });
                return resultingTrackArray
            }
        }).then(tracks => {
            return {
                tracks: tracks,
                metadata: {
                    "distances": distances,
                    "generator_list": generatorList,
                    "rule_name": votingRule,
                    "distance_metric": distanceMetric
                }
            }
        }, error => {
            console.log(error);
            return Promise.reject(votingRule)
        });
    }

    /**
     * Estimates ratings for each track and person and combines it with the own ratings.
     * @param trackObject
     * @param selfRatings
     * @param distanceMetric
     * @returns {{trackList: *[]}}
     */
    calculateDotProductRatings(trackObject, selfRatings, distanceMetric) {

        let result = {
            "trackList": []
        };

        //Create a track list (for storing data later)
        for (const person in selfRatings) {
            if (selfRatings.hasOwnProperty(person)) {
                result["trackList"].push(...Object.keys(selfRatings[person]));
            }
        }

        //Loop over every person
        Object.keys(trackObject).forEach(person => {

            let trackList = [];

            //Create a list with all tracks except the current selected person's tracks
            Object.keys(trackObject).forEach(otherPerson => {
                if (otherPerson !== person) {
                    trackList.push(...trackObject[otherPerson].tracks.map(track => track.id));
                }
            });

            const selectedPersonTracks = trackObject[person].tracks.map(track => track.id);

            //Calculate distances for every track of the selected person
            const calculatedRatings = distanceMetric.calculateRatings(
                selectedPersonTracks, trackList, this.songFeatures
            );

            //Combine the fixed ratings and the calculate ones.
            result[trackObject[person].id] = Object.assign(
                {},
                selfRatings[trackObject[person].id],
                calculatedRatings
            );
        });

        return result;
    }

    /**
     * Swaps the ratings from user -> track to track -> user
     * @param fullRatings
     * @returns {{}}
     */
    formRatingsObject(fullRatings) {
        let result = {};

        fullRatings["trackList"].forEach(track => {
            result[track] = {};
            Object.keys(fullRatings).forEach(person => {
                if (person !== "trackList") {
                    result[track][person] = fullRatings[person][track];
                }
            })
        });

        return result;
    }

    /**
     * Generates the playlist.
     * @param ratings
     * @param votingRule
     * @returns {*[]}
     */
    createPlaylist(ratings, votingRule) {

        const recommendGenerator = votingRule.calculateVotes(ratings);

        let track = recommendGenerator.next();

        const result = [];
        while (!track.done) {
            result.push(track["value"]);
            track = recommendGenerator.next();
        }

        return result;
    }
}
