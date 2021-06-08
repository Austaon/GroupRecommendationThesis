<template>
    <div>
        <b-row>
            <b-col>
                <b-form-select v-model="activeSession" :options="sessionOptions" @change="sessionChanged">
                </b-form-select>
            </b-col>
        </b-row>
        <b-row v-if="activeSession">
            <b-col>
                <b-form-select v-model="selectedUser" :options="userNames" @change="stateChanged">
                </b-form-select>
                <b-form-select v-model="selectedPlaylist" :options="playlistNames" @change="stateChanged">
                </b-form-select>
                <b-form-select v-model="selectedRating" :options="ratingNames" @change="stateChanged">
                </b-form-select>
                <apexchart type="bar" height="350" :options="chartOptions" :series="chartSeries"></apexchart>

            </b-col>
            <b-col>
                <table class="table table-striped adminTable">
                    <thead>
                    <tr>
                        <th>Playlist 1 ({{ activeSession.recommendations[0].metadata.rule_name.ruleName }})</th>
                        <th>Playlist 2 ({{ activeSession.recommendations[1].metadata.rule_name.ruleName }})</th>
                        <th>Playlist 3 ({{ activeSession.recommendations[2].metadata.rule_name.ruleName }})</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="index in 10" :key="`${activeSession.id}-recommendation-${index}`">
                        <td :set="track = activeSession.recommendations[0].tracks[index-1]">
                            <img :src="`${track.album.images.length >= 2 ? track.album.images[2].url : ''}`"
                                 alt="" width="50" height="50">
                            <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                                {{ track.artists[0].name }}</a>
                        </td>
                        <td :set="track = activeSession.recommendations[1].tracks[index-1]">
                            <img :src="`${track.album.images.length >= 2 ? track.album.images[2].url : ''}`"
                                 alt="" width="50" height="50">
                            <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                                {{ track.artists[0].name }}</a>
                        </td>
                        <td :set="track = activeSession.recommendations[2].tracks[index-1]">
                            <img :src="`${track.album.images.length >= 2 ? track.album.images[2].url : ''}`"
                                 alt="" width="50" height="50">
                            <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                                {{ track.artists[0].name }}</a>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </b-col>
        </b-row>

    </div>
</template>

<script>
import PlaylistFixer from "../../util/PlaylistFixer";

/**
 * Component showing the survey ratings of a specific person for a playlist and category.
 * Also highlights the tracks that same person selected, in order to see if periodic effects are present.
 *
 * In a slight ironic circumstance, this component uncovered the "laravel bug", where some people had their data
 * overwritten, since this component showed some people had none of their tracks selected, even in the Fairness playlist.
 */
export default {
    name: "PeriodicEffectsComponent",
    data() {
        return {
            sessions: [],
            sessionOptions: [],
            activeSession: null,
            surveys: {},
            userNames: [],
            selectedUser: {},
            playlistNames: [
                "Probability Weighted Sum", "Fairness", "Least Misery"
            ],
            selectedPlaylist: "Probability Weighted Sum",
            ratingNames: [
                "like_rating", "selection_rating", "suitable_rating"
            ],
            selectedRating: "like_rating",
            playlistFixer: new PlaylistFixer(),
            chartSeries: [],
            chartIndex: 0,
            chartOptions: {
                chart: {
                    height: 700,
                    type: 'radar',
                    captionAlignment: "right",
                    toolbar: {
                        show: false
                    },
                },
                colors: [({value, seriesIndex, w}) => {
                    let returnColor;
                    if(this.trackIsChosenByUser()) {
                        returnColor = "#006E22";
                    } else {
                        returnColor = "#E91E63";
                    }
                    this.chartIndex++;
                    return returnColor;
                }],
                dataLabels: {
                    formatter: (val) => `${val.toFixed(2)}`
                },
                stroke: {
                    width: 0.5,
                    curve: 'stepline',
                },
                yaxis: {
                    tickAmount: 10,
                    min: 0,
                    max: 5,
                    labels: {
                        formatter: (val) => val
                    }
                }
            },

        }
    },
    props: {
        sessionsInitial: {},
        getTrackDataRoute: "",
        spotifyId: "",
    },
    mounted() {
        // Only shows sessions that are in the survey stage.
        this.sessionsInitial.filter(session => session.state === "show_playlist").forEach(session => {
            this.sessions.push(session)
            this.sessionOptions.push({text: session.playlist_name, value: session})
        })
        this.activeSession = this.sessionsInitial[0];
        this.sessionChanged();
    },
    methods: {
        /**
         * Handles changing a session.
         */
        sessionChanged() {
            this.surveys = this.playlistFixer.fixPlaylistOrder(this.activeSession);
            this.userNames = [];
            this.activeUsers.forEach(user => {
                this.userNames.push({text: user.email_address, value: user});
            })
            this.selectedUser = this.activeSession.users[0];
            this.stateChanged();
        },
        /**
         * Handles changing any of the other parameters.
         */
        stateChanged() {
            this.chartIndex = 0;

            const playlistIndex = this.playlistNames.indexOf(this.selectedPlaylist);
            const survey = this.surveys[this.selectedUser.id];
            const surveyData = survey[`playlist${playlistIndex+1}`][`${this.selectedRating}_specific`];
            const resultSeries = [];

            Object.keys(surveyData).forEach(key => {
                const track = this.getTrack(key, playlistIndex);
                resultSeries.push({
                    x: track.name,
                    y: Number.parseInt(surveyData[key])
                })
            });

            this.chartSeries = [
                {
                    name: "Selected Tracks",
                    data: resultSeries
                }
            ]
        },
        /**
         * Gets the rating of a specific track.
         * @param songIndex
         * @param playlistIndex
         * @returns {*}
         */
        getTrack(songIndex, playlistIndex) {
            const index = songIndex.slice(4) - 1;

            if (this.selectedRating === "selection_rating") {
                return this.selectedUser.tracks[index];
            } else {
                return this.activeSession.recommendations[playlistIndex].tracks[index];
            }
        },
        /**
         * Checks if a track was selected by the current user.
         * @returns {boolean}
         */
        trackIsChosenByUser() {

            if(this.chartIndex > this.chartSeries[0].data.length || this.chartIndex === 0) {
                return false;
            }
            const trackIndex = _.clone(this.chartIndex);
            const userTracks = this.selectedUser.tracks.map(track => track.id);
            const playlistIndex = this.playlistNames.indexOf(this.selectedPlaylist);

            const track = this.getTrack(`Song${trackIndex}`, playlistIndex);

            return userTracks.includes(track.id);
        }
    },
    computed: {
        activeUsers() {
            return this.activeSession.users.filter(user => user.survey);
        }
    }
}
</script>

<style scoped>

</style>
