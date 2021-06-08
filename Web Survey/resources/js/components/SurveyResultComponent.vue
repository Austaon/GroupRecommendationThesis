<template>
    <div id="resultDiv">
        <hooper :vertical="true" style="height: 100%" :centerMode="true" ref="hooperCarousel">
            <slide ref="slide1">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row h-100 justify-content-center align-items-center text-center">
                    <h1>
                        Comparing a person's favourite songs according to Spotify and their own choices
                    </h1>
                </div>
            </slide>
            <slide ref="slide2">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row h-100 justify-content-center align-items-center text-center">
                    <div class="col-lg">
                        Slide 2
                    </div>
                    <div class="col-lg text-left" v-if="this.examplePerson.chosenTracks.length > 1">
                        <display-playlist
                            :playlist-tracks="this.examplePerson.chosenTracks"
                            header-message="Example playlist"
                            :show-store-playlist-button="false"
                            max-items="5">
                        </display-playlist>
                    </div>
                </div>
            </slide>
            <slide ref="slide3">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row h-100 justify-content-center align-items-center text-center">
                    <div class="col-lg text-left">
                        <div class="embed-responsive embed-responsive-21by9" id="spotifyEmbedId">
                            <iframe class="embed-responsive-item"
                                    :src="`https://open.spotify.com/embed/track/${this.examplePerson.chosenTracks[0].id}`"
                                    width="300" height="380" frameborder="0" allowtransparency="true"
                                    allow="encrypted-media"></iframe>
                        </div>
                    </div>
                    <div class="col-lg">
                        <apexchart type="radar" height="350" :options="chartOptions" ref="exampleRadar"
                                   :series="exampleSeries"></apexchart>
                    </div>
                </div>
            </slide>
            <slide ref="slide4">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row justify-content-center align-items-center text-center slide-title">
                    <h1>
                        Audio Features?
                    </h1>
                </div>
                <div class="row justify-content-center align-items-center text-center slide-body">

                    <div class="col-lg text-center">
                        <ul class="card-list feature-list" ref="audioFeatureList">
                            <li v-for="feature in audioFeatures" :key="`acoustic-feature-${feature}`"
                                @mouseenter="featureHover(feature)"
                                class="list-group-item border rounded-lg unselectable"
                                :class="activeAudioFeatureDescription === feature ? 'activeAudioFeatureCard' : ''">
                                {{ feature }}
                            </li>
                        </ul>
                    </div>
                    <div class="col-lg" id="audioFeatureDescriptions">
                        <div class="card" ref="audioFeatureDescriptionCard">
                            <div class="card-body">
                                <h5 class="card-title">{{ activeAudioFeatureDescription }}</h5>
                                <p class="card-text">{{ audioFeatureDescriptions[activeAudioFeatureDescription] }}</p>
                                <a target="_blank"
                                   href="https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/"
                                   class="card-link">Source</a>
                            </div>
                        </div>
                    </div>
                </div>
            </slide>
            <slide ref="slide5">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row justify-content-center align-items-center text-center slide-title">
                    <h1>
                        Average features of all songs in the survey
                    </h1>
                </div>
                <div class="row justify-content-center align-items-center text-center slide-body">
                    <div class="col-lg">
                        Hello world!
                    </div>
                    <div class="col-lg">
                        <apexchart type="radar" height="350" :options="chartOptions"
                                   :series="averageSeries"></apexchart>
                    </div>
                </div>
            </slide>
            <slide ref="slide6">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row justify-content-center align-items-center text-center slide-title">
                    <h1>
                        Calculate average distance
                    </h1>
                </div>
                <div class="row justify-content-center align-items-center text-center slide-body">
                    <div class="col-lg">
                        <ul class="card-list track-list" ref="retrievedTracksList">
                            <li v-for="track in examplePerson.retrievedTracks" :key="`retrieved-tracks-${track.id}`"
                                @mouseenter="retrievedTrackHover(track)"
                                class="list-group-item border rounded-lg unselectable"
                                :class="activeRetrievedTrack === track ? 'activeAudioFeatureCard' : ''">
                                {{ track.name }}
                            </li>
                        </ul>
                    </div>
                    <div class="col-lg">
                        <ul class="card-list track-list" ref="retrievedTracksList">
                            <li v-for="track in examplePerson.chosenTracks" :key="`chosen-tracks-${track.id}`"
                                class="list-group-item border rounded-lg unselectable">
                                {{ track.name }}
                            </li>
                        </ul>
                    </div>
                    <div class="col-lg">
                        {{ examplePerson.calculatedDistance }}
                    </div>
                </div>
            </slide>
            <slide ref="slide7">
                <canvas class="trianglifyCanvas">

                </canvas>
                <div class="row justify-content-center align-items-center text-center slide-title">
                    <h1>
                        Two additional datasets
                    </h1>
                </div>
                <div class="row justify-content-center align-items-center text-center slide-body">
                    <div class="col">
                        <div class="card mx-auto playlist-card">
                            <b-iconstack class="card-img-top" font-scale="7.5">
                                <b-icon-music-player-fill stacked shift-v="3"></b-icon-music-player-fill>
                                <b-icon-circle stacked scale="0.3"></b-icon-circle>
                                <b-icon-dot stacked scale="0.3" shift-v="2.3" animation="spin"></b-icon-dot>
                            </b-iconstack>
                            <div class="card-body">
                                <h5 class="card-title">Recommended tracks</h5>
                                <p class="card-text">Some quick example text to build on the card title and make up the
                                    bulk of the card's content.</p>
                            </div>
                        </div>
                    </div>
                    <div class="col">
                        <div class="card mx-auto playlist-card" style="width: 18rem;">
                            <b-icon :icon="diceIconString" class="card-img-top" font-scale="7.5" shift-v="3"></b-icon>
                            <div class="card-body">
                                <h5 class="card-title">Randomly generated</h5>
                                <p class="card-text">Some quick example text to build on the card title and make up the
                                    bulk of the card's content.</p>
                            </div>
                        </div>
                    </div>
                </div>
            </slide>
            <slide ref="slide8">
                <canvas class="trianglifyCanvas">
                </canvas>
                <div class="row h-100 justify-content-center align-items-center text-center">
                    <div class="col-lg">
                        <vue-word-cloud
                            id="wordCloudFeedback"
                            :words="wordCloudData"
                            :color="([, weight]) => weight > 10 ? 'DeepPink' : weight > 5 ? 'RoyalBlue' : 'Indigo'"
                            font-family="Life Savers"
                        />
                    </div>
                    <div class="col-lg">
                        hello world!
                    </div>
                </div>
            </slide>
            <hooper-navigation slot="hooper-addons"></hooper-navigation>
        </hooper>
    </div>
</template>

<script>
import {Hooper, Slide, Navigation as HooperNavigation} from 'hooper';
import trianglify from 'trianglify';

import audioFeatureDescriptions from '../data/audio_feature_descriptions.json'
import {CosineSimilarity} from "../recommender/distance_metrics";

/**
 * Experimental component that would've shown the results in a fancy presentation-like web page.
 * Never got around to finishing this and likely has a memory leak somewhere.
 */
export default {
    name: "SurveyResultComponent",
    components: {
        Hooper,
        Slide,
        HooperNavigation
    },
    data() {
        return {
            patterns: [
                this.hashCode("0"),
                `${this.hashCode("This")}`,
                `${this.hashCode("is")}`,
                `${this.hashCode("the")}`,
                `${this.hashCode("results")}`,
                `${this.hashCode('moar')}`,
                `${this.hashCode("of")}`,
                `${this.hashCode("the")}`,
                `${this.hashCode("survey")}`,
            ],
            audioFeatures: ['Acousticness', 'Danceability', 'Energy', "Instrumentalness",
                "Liveness", "Loudness", "Speechiness", "Valence"],
            audioFeatureDescriptions: audioFeatureDescriptions,
            activeAudioFeatureDescription: "Acousticness",
            examplePerson: {
                retrievedTracks: [],
                chosenTracks: [{
                    id: "4uLU6hMCjMI75M1A2tKUQC"
                }],
                calculatedDistance: 0,
            },
            activeRetrievedTrack: {},
            surveyData: {},
            songMetaData: {},
            exampleSeries: [],
            averageSeries: [],
            diceIconNumber: 1,
            wordCloudData: [],
            chartOptions: {
                chart: {
                    height: 700,
                    type: 'radar',
                    captionAlignment: "right",
                    toolbar: {
                        show: false
                    },
                },
                tooltip: {
                    y: {
                        formatter: (val) => `${val.toFixed(2)}`,
                        title: {
                            formatter: (_, seriesObject) => this.audioFeatures[seriesObject.dataPointIndex]
                        }
                    },
                    x: {
                        formatter: (_) => "Audio Features"
                    }
                },
                plotOptions: {
                    radar: {
                        polygons: {
                            strokeColor: '#e8e8e8',
                            fill: {
                                colors: ['#f8f8f8', '#fff']
                            }
                        }
                    }
                },
                xaxis: {
                    categories: ['Acousticness', 'Danceability', 'Energy', "Instrumentalness",
                        "Liveness", "Loudness", "Speechiness", "Valence"],
                    labels: {
                        style: {
                            colors: ["#212529", "#212529", "#212529", "#212529",
                                "#212529", "#212529", "#212529", "#212529"]
                        }
                    }
                },
                yaxis: {
                    tickAmount: 8,
                    min: 0,
                    max: 1,
                    labels: {
                        formatter: function (val, i) {
                            if (i % 2 === 0) {
                                return val
                            } else {
                                return ''
                            }
                        }
                    }
                }
            },
        }
    },
    created() {
        window.addEventListener("resize", this.windowResized);
    },
    mounted() {

        this.$refs.hooperCarousel.slideTo(2);
        this.generateCanvas();
        this.loadSongMetaData().then(_ => {

        }).then(this.loadSurveyData).then(_ => {
            this.generateWordCloudData();
            this.generateRandomPerson();
            this.prepareExampleRadar();
        });

        const diceLoop = () => {
            const rand = Math.round(Math.random() * (1000 - 500)) + 500;
            setTimeout(() => {
                this.diceIconNumber = Math.floor(Math.random() * 6) + 1
                diceLoop();
            }, rand);
        };
        diceLoop();

    },
    destroyed() {
        window.removeEventListener("resize", this.windowResized);
    },
    methods: {
        generateCanvas() {
            for (let i = 1; i < this.patterns.length; i++) {
                const pattern = trianglify({
                    width: this.$refs[`slide${i}`].$el.clientWidth,
                    height: window.innerHeight,
                    cellSize: 75,
                    variance: 0.75,
                    seed: this.patterns[i]
                })
                const canvas = this.$refs[`slide${i}`].$el.children[0]
                canvas.width = this.$refs[`slide${i}`].$el.clientWidth
                canvas.height = window.innerHeight

                const ctx = canvas.getContext('2d');
                ctx.drawImage(pattern.toCanvas(), 0, 0);
            }
        },
        windowResized() {
            this.generateCanvas();
        },
        async loadSongMetaData() {
            if (Object.keys(this.songMetaData).length !== 0) {
                return this.songMetaData;
            }

            return import('../data/song_meta_data.json').then(songMetaData => {
                this.songMetaData = songMetaData.default;
                return songMetaData;
            });
        },
        async loadSurveyData() {
            if (Object.keys(this.surveyData).length !== 0) {
                return this.surveyData;
            }

            return import('../data/all_survey_data.json').then(surveyData => {
                this.surveyData = surveyData.default;
                return surveyData;
            });
        },
        prepareExampleRadar() {
            const audioFeatureAverages = this.calculateAverages();
            this.averageSeries = [
                {
                    name: 'Series 1',
                    data: audioFeatureAverages,
                }
            ]
            const exampleTrack = this.examplePerson.chosenTracks[0];
            this.exampleSeries = [
                {
                    data: [exampleTrack["acousticness"], exampleTrack["danceability"],
                        exampleTrack["energy"], exampleTrack["instrumentalness"],
                        exampleTrack["liveness"], exampleTrack["loudness"],
                        exampleTrack["speechiness"], exampleTrack["valence"]]
                }
            ]
            this.$refs.exampleRadar.updateOptions({
                title: {
                    text: `Audio features for "${exampleTrack.name}"`,
                    align: "center"
                }
            })
        },
        calculateAverages() {
            const averages = {
                "acousticness": 0,
                "danceability": 0,
                "energy": 0,
                "instrumentalness": 0,
                "liveness": 0,
                "loudness": 0,
                "speechiness": 0,
                "valence": 0
            }

            Object.keys(this.songMetaData).forEach(trackUri => {
                const track = this.songMetaData[trackUri];
                Object.keys(averages).forEach(average => {
                    averages[average] += track[average]
                })
            })

            Object.keys(averages).forEach(average => {
                averages[average] /= Object.keys(this.songMetaData).length
            })
            return Object.values(averages);
        },
        generateExamplePlaylist() {
            const playlistArray = [];
            const songKeys = Object.keys(this.songMetaData);
            for (let i = 0; i < 5; i++) {
                playlistArray.push(
                    this.songMetaData[songKeys[Math.floor(Math.random() * songKeys.length)]]
                );
            }

            this.examplePlaylist = playlistArray;
        },
        generateWordCloudData() {
            const words = {};
            let count = 0;
            this.surveyData.forEach(person => {
                if (person.feedback.length > 0) {
                    count++;
                    person.feedback.split(" ").forEach(word => {
                        if (!(word in words)) {
                            words[word] = 1
                        } else {
                            words[word]++;
                        }
                    })
                }
            })
            console.log(count);

            this.wordCloudData = Object.entries(words).sort(([, a], [, b]) => b - a).filter(([, a]) => a > 1);
        },
        generateRandomPerson() {
            const randomPerson = this.surveyData[Math.floor(Math.random() * this.surveyData.length)];
            const retrievedTracks = randomPerson.top_tracks.tracks_long_term;
            const chosenTracks = randomPerson.chosen_tracks;

            retrievedTracks.forEach(track => {
                if (this.examplePerson.retrievedTracks.length < 5) {
                    this.examplePerson.retrievedTracks.push(this.songMetaData[track])
                }
            })
            this.examplePerson.chosenTracks = [];
            chosenTracks.forEach(track => {
                if (this.examplePerson.chosenTracks.length < 5) {
                    this.examplePerson.chosenTracks.push(this.songMetaData[track])
                }
            })
        },
        featureHover(feature) {
            this.activeAudioFeatureDescription = feature;
        },
        retrievedTrackHover(track) {
            this.activeRetrievedTrack = track;
            this.calculateDistanceForHoveredTrack(track);
        },
        calculateDistanceForHoveredTrack(track) {
            this.examplePerson.calculatedDistance = new CosineSimilarity().calculateAverageDistance(
                track.uri,
                this.examplePerson.chosenTracks.map(track => track.uri),
                this.songMetaData
            );
        },
        hashCode(hashString) {
            let hash = 0;
            if (hashString.length === 0) {
                return hash;
            }
            for (let i = 0; i < hashString.length; i++) {
                const char = hashString.charCodeAt(i);
                hash = ((hash << 5) - hash) + char;
                hash = hash & hash; // Convert to 32bit integer
            }
            return hash;
        },
    },
    computed: {
        diceIconString() {
            return `dice${this.diceIconNumber}-fill`
        }
    }
}
</script>

<style scoped>

</style>
