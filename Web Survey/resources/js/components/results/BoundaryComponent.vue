<template>
    <div>
        <b-row>
            <b-col>
                <b-form-group>
                    <b-form-radio-group v-model="selectedOption" name="playlist-selection" @input="playlistSelected">
                        <b-form-radio value="0">Playlist 1</b-form-radio>
                        <b-form-radio value="1">Playlist 2</b-form-radio>
                        <b-form-radio value="2">Playlist 3</b-form-radio>
                        <b-form-radio value="other">Specific Song</b-form-radio>
                    </b-form-radio-group>
                    <b-form-select v-model="selectedTrack" :options="trackOptions" @change="trackSelected"
                                   v-if="selectedOption === 'other'">
                    </b-form-select>
                    <b-form-select v-model="histogram.selectedAudioFeature"
                                   :options="userBoundary.keys" @change="playlistSelected">
                    </b-form-select>
                </b-form-group>

                <apexchart type="bar" height="350" :options="chartOptions" ref="exampleRadar"
                           :series="chartSeries"></apexchart>
                <p v-if="Object.keys(selectedTrack).length > 0">
                    The selected {{ selectedOption === 'other' ? 'track' : 'playlist' }} has a score of: {{
                        trackScore
                    }}
                </p>
            </b-col>
            <b-col>
                <b-form-select v-model="selectedUser" :options="userOptions" @change="userSelected">
                </b-form-select>
                <display-playlist style="margin-top: 3%"
                                  :playlist-tracks="selectedUser.tracks"
                                  :header-message="selectedUser.email_address"
                                  :show-store-playlist-button="false">
                </display-playlist>
            </b-col>

        </b-row>
    </div>

</template>

<script>
import TrackBoundary from "../../util/TrackBoundary";

/**
 * Computes and shows the boundaries for a specific user. Kind of a mix between boundary score and histogram score.
 * Mostly just used for some visualisations, not much more.
 */
export default {
    name: "BoundaryComponent",
    data() {
        return {
            users: [],
            tracks: [],
            userOptions: [],
            trackOptions: [],
            selectedOption: "other",
            selectedUser: {tracks: [], email_address: ""},
            selectedTrack: {},
            selectedUserFeatures: [],
            histogram: {
                selectedAudioFeature: "acousticness",
                bins: 10,
                x: [],
                y: []
            },
            trackScore: 0,
            userBoundary: new TrackBoundary(),
            boundarySeries: [],
            chartSeries: [],
            chartOptions: {
                chart: {
                    height: 700,
                    // type: 'radar',
                    captionAlignment: "right",
                    toolbar: {
                        show: false
                    },
                    stacked: true
                },
                colors: [({value, seriesIndex, w}) => {
                    if (seriesIndex === 0) {
                        return "#003388"
                    } else {
                        return "#666666"
                    }
                }],
                dataLabels: {
                    formatter: (val, {seriesIndex, dataPointIndex, w}) => {
                        if (seriesIndex === 0) {
                            return val
                        } else {
                            return ""
                        }
                    }
                },
                yaxis: {
                    labels: {
                        formatter: (val) => val.toFixed(0)
                    }
                }
            },
        }
    },
    props: {
        sessionsInitial: {},
        trackList: {},
        getTrackDataRoute: "",
        getUserDataRoute: "",
        spotifyId: "",
    },
    mounted() {
        this.sessionsInitial.forEach(session => {
            this.users.push(...session.users.filter(user => user.tracks.length > 0));
        })
        // Sorts the list of tracks on artist name.
        this.tracks = _.uniq(this.trackList.sort((a, b) => a.artist.localeCompare(b.artist)));
        this.userOptions = this.users.map(user => {
            return {value: user, text: user.email_address}
        })
        this.trackOptions = this.tracks.map(track => {
            return {value: track, text: `${track.name} - ${track.artist}`}
        })

        this.selectedUser = this.users[0];
        this.selectedTrack = this.tracks[0];

        this.userSelected()
    },
    methods: {
        /**
         * Gets the required data when a new user is selected.
         */
        userSelected() {
            axios.get(this.getUserDataRoute, {
                params: {
                    user_id: this.selectedUser.id,
                    spotify_id: this.spotifyId
                }
            }).then(data => {
                return axios.get(this.getTrackDataRoute, {
                    params: {
                        track_ids: data.data.user.hovered_tracks.map(track => track.id),
                        spotify_id: this.spotifyId
                    }
                });
            }).then(data => {
                // this.computeUserBoundaries(data.data.tracks)
                this.selectedUserFeatures = data.data.tracks;

                this.createHistogram();
                this.playlistSelected();
            })
        },
        /**
         * Gets the session from a selected user
         * @param selectedUser
         * @returns {*}
         */
        findSession(selectedUser) {

            let foundSession

            this.sessionsInitial.forEach(session => {
                session.users.forEach(user => {
                    if (user.id === selectedUser.id) {
                        foundSession = session;
                    }
                })
            })
            return foundSession
        },
        /**
         * Creates the histogram of the user and selected song/playlist.
         */
        createHistogram() {
            const retrievedFeatures = this.selectedUserFeatures.map(track => track[this.histogram.selectedAudioFeature])
            const stepSize = 1 / this.histogram.bins;
            this.histogram.x = [];
            this.histogram.y = [];

            for (let i = 0; i < this.histogram.bins + 1; i++) {
                this.histogram.x.push(stepSize * i);
                this.histogram.y.push(0);
            }

            retrievedFeatures.forEach(track => {
                for (let i = 0; i < this.histogram.bins; i++) {
                    if (track >= this.histogram.x[i] && track < this.histogram.x[i + 1]) {
                        this.histogram.y[i]++;
                    }
                }
            })

            const data = [];
            for (let i = 0; i < this.histogram.bins; i++) {
                data.push({x: this.histogram.x[i] * 10, y: this.histogram.y[i]})
            }

            this.boundarySeries = [
                {
                    name: `${this.histogram.selectedAudioFeature} histogram`,
                    data: data
                }
            ];
            this.chartSeries = _.cloneDeep(this.boundarySeries);

        },
        /**
         * Finds the bin an audio feature value belongs to.
         * @param audioFeature
         * @returns {boolean|number}
         */
        findBin(audioFeature) {
            for (let i = 0; i < this.histogram.bins; i++) {
                if (audioFeature >= this.histogram.x[i] && audioFeature < this.histogram.x[i + 1]) {
                    return i;
                }
            }
            return false;
        },
        /**
         * ¯\_(ツ)_/¯
         * @param trackFeatures
         */
        computeUserBoundaries(trackFeatures) {
            this.userBoundary.reset();
            trackFeatures.forEach(track => {
                this.userBoundary.addAudioFeature(track)
            })
            this.selectedUserFeatures = trackFeatures

            this.boundarySeries = [
                {name: "Boundary", data: this.userBoundary.getRangeSeries()}
            ]
            this.chartSeries = _.cloneDeep(this.boundarySeries);
        },
        /**
         * Gets the track data of a selected playlist. (Redirects to trackSelected() is a specific track was selected.)
         */
        playlistSelected() {
            this.createHistogram();
            if (this.selectedOption === "other") {
                return this.trackSelected();
            }

            const session = this.findSession(this.selectedUser)
            const recommendedSongs = session.recommendations[this.selectedOption].tracks.map(track => track.id);

            axios.get(this.getTrackDataRoute, {
                params: {
                    track_ids: recommendedSongs,
                    spotify_id: this.spotifyId
                }
            }).then(data => {
                if (data.data.tracks.length === 0) {
                    console.log(`Missing track: ${this.selectedTrack}`);
                    return;
                }
                const trackData = data.data.tracks;
                this.processTracks(trackData);
            })
        },
        /**
         * Gets the track data of a selected track.
         */
        trackSelected() {
            axios.get(this.getTrackDataRoute, {
                params: {
                    track_ids: [this.selectedTrack.track_id],
                    spotify_id: this.spotifyId
                }
            }).then(data => {
                if (data.data.tracks.length === 0) {
                    console.log(`Missing track: ${this.selectedTrack}`);
                    return;
                }
                const trackData = data.data.tracks;
                this.processTracks(trackData);
            })
        },
        /**
         * Processes the tracks and fills in the histogram.
         * @param tracks
         */
        processTracks(tracks) {
            this.chartSeries = _.cloneDeep(this.boundarySeries);
            this.trackScore = 0

            tracks.forEach(trackData => {

                const x = this.findBin(trackData[this.histogram.selectedAudioFeature]);
                const data = [];
                for (let i = 0; i < this.histogram.bins; i++) {
                    if (i === x) {
                        data.push({x: i, y: 1})
                    } else {
                        data.push({x: i, y: 0});
                    }
                }

                this.chartSeries.push({
                    name: trackData.name,
                    data: data
                })
                this.trackScore += this.userBoundary.trackIsInBoundary(trackData, true);
            })
            // tracks.forEach(trackData => {
            //     this.chartSeries.push({
            //         name: trackData.name,
            //         data: this.userBoundary.keys.map(key => {
            //             return {x: key, y: [trackData[key] - 0.01, trackData[key] + 0.01]}
            //         })
            //     })
            //     this.trackScore += this.userBoundary.trackIsInBoundary(trackData, true);
            // })
        }
    }
}
</script>

<style scoped>

</style>
