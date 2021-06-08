<template>
    <div>
        <b-row>
            <b-col>
                <b-form-select v-model="session" :options="sessionOptions" @change="sessionSelected">
                </b-form-select>
            </b-col>
        </b-row>
        <b-row v-if="session">
            <b-col>
                <b-form-select v-model="selectedRating" :options="ratingNames" @change="ratingSelected">
                </b-form-select>
                <apexchart type="bar" height="350" :options="chartOptions" ref="exampleRadar"
                           :series="chartSeries"></apexchart>
                <table class="table table-striped adminTable">
                    <caption>{{activeUser.id}}</caption>
                    <thead>
                    <tr>
                        <th>Song</th>
                        <th>Rating</th>
                    </tr>
                    </thead>
                    <tr v-for="(value, key) in surveys[activeUser.id][activePlaylist][`${selectedRating}_specific`]">
                        <td>
                            {{getSongTitle(key)}}
                        </td>
                        <td>
                            {{value}}
                        </td>
                    </tr>
                    <tr v-if="surveys[activeUser.id][activePlaylist][`${selectedRating.split('_')[0]}_feedback`].length > 0">
                        <td>Feedback: </td>
                        <td>
                            {{ surveys[activeUser.id][activePlaylist][`${selectedRating.split('_')[0]}_feedback`] }}
                        </td>
                    </tr>
                </table>
            </b-col>
            <b-col>
                <table class="table table-striped adminTable">
                    <thead>
                    <tr>
                        <th>Playlist 1 ({{ session.recommendations[0].metadata.rule_name.ruleName }})</th>
                        <th>Playlist 2 ({{ session.recommendations[1].metadata.rule_name.ruleName }})</th>
                        <th>Playlist 3 ({{ session.recommendations[2].metadata.rule_name.ruleName }})</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="index in 10" :key="`${session.id}-recommendation-${index}`">
                        <td :set="track = session.recommendations[0].tracks[index-1]">
                            <img :src="`${track.album.images.length >= 2 ? track.album.images[2].url : ''}`"
                                 alt="" width="50" height="50">
                            <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                                {{ track.artists[0].name }}</a>
                        </td>
                        <td :set="track = session.recommendations[1].tracks[index-1]">
                            <img :src="`${track.album.images.length >= 2 ? track.album.images[2].url : ''}`"
                                 alt="" width="50" height="50">
                            <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                                {{ track.artists[0].name }}</a>
                        </td>
                        <td :set="track = session.recommendations[2].tracks[index-1]">
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
 * Component that shows the survey rating for each person in a group per playlist. Also shows the average rating
 * for each playlist. Clicking on a person shows their specific ratings for each track.
 */
export default {
    name: "RatingsComponent",
    data() {
        return {
            session: null,
            activeUser: {},
            activePlaylist: "playlist1",
            sessionOptions: [],
            surveys: {},
            playlistFixer: new PlaylistFixer(),
            playlistStrings: [
                "playlist1", "playlist2", "playlist3"
            ],
            ratingNames: [
                "like_rating", "selection_rating", "suitable_rating"
            ],
            selectedRating: "like_rating",
            chartSeries: [],
            chartOptions: {
                chart: {
                    height: 700,
                    type: 'radar',
                    captionAlignment: "right",
                    toolbar: {
                        show: false
                    },
                    events: {
                        dataPointSelection: (event, chartContext, config) => {
                            this.activePlaylist = `playlist${config.dataPointIndex+1}`
                            if(config.seriesIndex < 4) {
                                this.activeUser = this.session.users[config.seriesIndex];
                            }
                        }
                    }
                },
                tooltip: {
                    y: {
                        formatter: (val) => `${val.toFixed(2)}`,
                    },
                },
                dataLabels: {
                    formatter: (val) => `${val.toFixed(2)}`
                },
                stroke: {
                    width: 0.5,
                    curve: 'stepline',
                },
                xaxis: {
                    categories: ["Probability Weighted Sum", "Fairness", "Least Misery"],
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
        // Only shows sessions that are in the survey state.
        this.sessionsInitial.filter(session => session.state === "show_playlist").forEach(session => {
            this.sessionOptions.push({text: session.playlist_name, value: session})
        })
        this.session = this.sessionsInitial[0];
        this.activeUser = this.session.users[0];
        this.sessionSelected();
    },
    methods: {
        /**
         * Called when a new session is selected
         */
        sessionSelected() {
            this.surveys = this.playlistFixer.fixPlaylistOrder(this.session);
            this.activeUser = this.session.users[0];
            this.renderChart();
        },
        ratingSelected() {
            this.renderChart();
        },
        /**
         * Handles all the rendering for the graph in the component.
         */
        renderChart() {
            this.chartSeries = [];

            const resultObject = {}
            this.session.users.forEach(user => resultObject[user.id] = []);
            resultObject["Average"] = [];

            this.activeUsers.forEach(user => {
                this.playlistStrings.forEach(playlist => {
                    resultObject[user.id].push(this.surveys[user.id][playlist][this.selectedRating])
                })
            })

            this.playlistStrings.forEach(playlist => {
                resultObject["Average"].push(this.getAverageForRating(playlist, this.selectedRating))
            });

            Object.keys(resultObject).forEach(key => {
                this.chartSeries.push({
                    name: key, data: resultObject[key]
                })
            })
        },
        /**
         * Calculates the average rating for a playlist and category.
         * @param playlist
         * @param ratingType
         * @returns {number}
         */
        getAverageForRating(playlist, ratingType) {
            let average = 0;

            Object.keys(this.surveys).forEach(userId => {
                const survey = this.surveys[userId]
                average += Number.parseFloat(survey[playlist][ratingType])
            });

            return average / Object.keys(this.surveys).length;
        },
        /**
         * Gets the title of a track.
         * @param songIndex
         * @returns {*}
         */
        getSongTitle(songIndex) {
            const index = songIndex.slice(4) - 1;
            const playlistIndex = this.activePlaylist.slice(-1) - 1;

            if(this.selectedRating === "selection_rating") {
                return this.activeUser.tracks[index].name;
            } else {
                return this.session.recommendations[playlistIndex].tracks[index].name;
            }
        }
    },
    computed: {
        activeUsers() {
            return this.session.users.filter(user => user.survey);
        }
    }
}
</script>

<style scoped>
.truncate {
    max-width: 1px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
</style>
