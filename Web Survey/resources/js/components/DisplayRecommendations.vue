<template>
    <div class="row" v-if="!showSurvey">
        <div class="col-lg text-center" id="preSurveyState">
            Here are the generated playlists. Feel free to look through them and listen to them.
            You can click on the button next to the playlist to store it on Spotify.
            Once you are ready to fill in the survey, press the button below.
            <br/>
            <br/>
            Please note that the three playlists will be shuffled every time you refresh this page.
            <br/>
            <button type="button" class="btn btn-success" v-on:click="startSurvey">Start survey</button>
        </div>
        <div class="col-lg justify-content-center">
            <carousel :per-page="1" class="col-lg" ref="carousel"
                      pagination-position="top" pagination-color="#999999" pagination-active-color="#218838">
                <slide v-for="(recommendation, index) in recommendations" :key="`recommendation-initial-${index}`">
                    <display-playlist
                        :playlist-tracks="recommendation.tracks"
                        :header-message="`Playlist ${index + 1}`"
                        :show-store-playlist-button="() => storePlaylist(recommendation, index)">
                    </display-playlist>
                </slide>
            </carousel>
        </div>
    </div>
    <div class="row" v-else>
        <div class="col-lg">
            <div id="surveyContainer">
                <survey :survey="survey"></survey>
            </div>
        </div>
        <div class="col-lg">
            <carousel :per-page="1" class="col-lg" ref="carousel"
                      pagination-position="top" pagination-color="#999999" pagination-active-color="#218838"
                      :touch-drag="navigationEnabled" :mouse-drag="navigationEnabled">
                <slide v-for="(recommendation, index) in recommendations" :key="`recommendation-survey-${index}`">
                    <display-playlist
                        :playlist-tracks="recommendation.tracks"
                        :header-message="`Playlist ${index + 1}`"
                        :show-store-playlist-button="() => storePlaylist(recommendation, index)">
                    </display-playlist>
                </slide>
            </carousel>
        </div>
    </div>

</template>

<script>

const Spotify = require('spotify-web-api-js')
import * as SurveyVue from 'survey-vue'

SurveyVue.Survey.cssType = "bootstrap";

/**
 * Component that manages showing the recommendations and the survey.
 *
 * Survey.js is kind of a pain in the ass and breaks randomly sometimes. No clue why :(
 */
export default {
    name: "DisplayRecommendations",
    data() {
        return {
            spotify: new Spotify(),
            carousel: this.$refs.carousel,
            showSurvey: false,
            survey: null,
            surveyModel: {
                "pages": [
                    {
                        "name": "playlist1_like",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist1_like_rating",
                                "title": "How much did you enjoy this playlist?",
                                "description": "1: Not at all, 5: A lot. The same scale will be used in the other questions.",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist1_like_rating_specific",
                                "title": "How much did you enjoy each specific song",
                                "description": "Here you can fill in songs you have a specific like/dislike for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist1_like_feedback",
                                "title": "Any other feedback for how much you enjoyed this playlist?"
                            }
                        ],
                        "title": "Playlist 1",
                        "description": "This page contains questions about your enjoyment of the first playlist."
                    },
                    {
                        "name": "playlist1_selection",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist1_selection_rating",
                                "title": "Are you satisfied with the position of your chosen tracks in this playlist?",
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist1_selection_rating_specific",
                                "title": "How happy are you with each of your chosen tracks.",
                                "description": "Here you can fill in songs you have a strong feeling for. In case a song you chose is not in the playlist, you can express your (dis)satisfaction here.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist1_selection_feedback",
                                "title": "Any other feedback about your chosen tracks?"
                            }
                        ],
                        "title": "Playlist 1",
                        "description": "This page contains questions about the first playlist"
                    },
                    {
                        "name": "playlist1_suitable",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist1_suitable_rating",
                                "title": `Do you think this playlist fits the purpose of the group session "${this.sessionPurpose}"?`,
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist1_suitable_rating_specific",
                                "title": "Do any of the songs fit this purpose especially well or poorly.",
                                "description": "Here you can fill in songs you have a strong feeling for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist1_suitable_feedback",
                                "title": "Any other feedback about how well this playlist fits the purpose?"
                            }
                        ],
                        "title": "Playlist 1",
                        "description": "This page contains questions about the first playlist"
                    },
                    {
                        "name": "playlist2_like",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist2_like_rating",
                                "title": "How much did you enjoy this playlist?",
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist2_like_rating_specific",
                                "title": "How much did you enjoy each specific song",
                                "description": "Here you can fill in songs you have a specific like/dislike for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist2_like_feedback",
                                "title": "Any other feedback for how much you enjoyed this playlist?"
                            }
                        ],
                        "title": "Playlist 2",
                        "description": "This page contains questions about your enjoyment of the second playlist."
                    },
                    {
                        "name": "playlist2_selection",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist2_selection_rating",
                                "title": "Are you satisfied with the position of your chosen tracks in this playlist?",
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist2_selection_rating_specific",
                                "title": "How happy are you with each of your chosen tracks.",
                                "description": "Here you can fill in songs you have a strong feeling for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist2_selection_feedback",
                                "title": "Any other feedback about your chosen tracks?"
                            }
                        ],
                        "title": "Playlist 2",
                        "description": "This page contains questions about the second playlist"
                    },
                    {
                        "name": "playlist2_suitable",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist2_suitable_rating",
                                "title": `Do you think this playlist fits the purpose of the group session "${this.sessionPurpose}"?`,
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist2_suitable_rating_specific",
                                "title": "Do any of the songs fit this purpose especially well or poorly.",
                                "description": "Here you can fill in songs you have a strong feeling for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist2_suitable_feedback",
                                "title": "Any other feedback about how well this playlist fits the purpose?"
                            }
                        ],
                        "title": "Playlist 2",
                        "description": "This page contains questions about the second playlist"
                    },
                    {
                        "name": "playlist3_like",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist3_like_rating",
                                "title": "How much did you enjoy this playlist?",
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist3_like_rating_specific",
                                "title": "How much did you enjoy each specific song",
                                "description": "Here you can fill in songs you have a specific like/dislike for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist3_like_specific",
                                "title": "Any other feedback for how much you enjoyed this playlist?"
                            }
                        ],
                        "title": "Playlist 3",
                        "description": "This page contains questions about your enjoyment of the third playlist."
                    },
                    {
                        "name": "playlist3_selection",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist3_selection_rating",
                                "title": "Are you satisfied with the position of your chosen tracks in this playlist?",
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist3_selection_rating_specific",
                                "title": "How happy are you with each of your chosen tracks.",
                                "description": "Here you can fill in songs you have a strong feeling for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist3_selection_feedback",
                                "title": "Any other feedback about your chosen tracks?"
                            }
                        ],
                        "title": "Playlist 3",
                        "description": "This page contains questions about the third playlist"
                    },
                    {
                        "name": "playlist3_suitable",
                        "elements": [
                            {
                                "type": "rating",
                                "name": "playlist3_suitable_rating",
                                "title": `Do you think this playlist fits the purpose of the group session "${this.sessionPurpose}"?`,
                                "description": "(1: Not at all, 5: A lot)",
                                "isRequired": true
                            },
                            {
                                "type": "matrix",
                                "name": "playlist3_suitable_rating_specific",
                                "title": "Do any of the songs fit this purpose especially well or poorly.",
                                "description": "Here you can fill in songs you have a strong feeling for.",
                                "defaultValue": {
                                    "Song 1": "3",
                                    "Song 2": "3",
                                    "Song 3": "3",
                                    "Song 4": "3",
                                    "Song 5": "3",
                                    "Song 6": "3",
                                    "Song 7": "3",
                                    "Song 8": "3",
                                    "Song 9": "3",
                                    "Song 10": "3"
                                },
                                "isRequired": true,
                                "columns": [
                                    "1",
                                    "2",
                                    "3",
                                    "4",
                                    "5"
                                ],
                                "rows": [
                                    "Song 1",
                                    "Song 2",
                                    "Song 3",
                                    "Song 4",
                                    "Song 5",
                                    "Song 6",
                                    "Song 7",
                                    "Song 8",
                                    "Song 9",
                                    "Song 10"
                                ]
                            },
                            {
                                "type": "text",
                                "name": "playlist3_suitable_feedback",
                                "title": "Any other feedback about how well this playlist fits the purpose?"
                            }
                        ],
                        "title": "Playlist 3",
                        "description": "This page contains questions about the third playlist"
                    },
                    {
                        "name": "general_feedback",
                        "elements": [
                            {
                                "type": "text",
                                "name": "general_feedback_input",
                                "title": "Do you have any other feedback?"
                            }
                        ]
                    }
                ]
            }
        }
    },
    props: {
        recommendations: Array,
        user: Object,
        accessToken: String,
        sessionId: String,
        sessionPurpose: String,
        putSurveyRoute: String
    },
    created() {

        // Shuffle the recommendations to combat survey fatigue.
        this.shuffleRecommendations(this.recommendations);

        this.spotify.setAccessToken(this.accessToken);

        // Get the survey ready to show later
        this.prepareSurvey();
        this.survey = new SurveyVue.Model(this.surveyModel);
        this.survey.css = {
            navigationButton: "btn btn-success"
        };
        this.survey.showPrevButton = true;
        this.survey.render();

        // Submit the survey to the database.
        this.survey.onComplete.add((result, options) => {

            options.showDataSaving()

            // Make sure the order can be reconstructed later.
            const shuffledMetadata = {
                metaData: {
                    playlist1: this.recommendations[0].metadata,
                    playlist2: this.recommendations[1].metadata,
                    playlist3: this.recommendations[2].metadata,
                }
            }
            let resultData = {...this.revertSurveyChanges(this.survey), ...shuffledMetadata};
            axios.put(this.putSurveyRoute, {
                "sessionId": this.sessionId,
                "userId": this.user.id,
                "survey": resultData
            }).then(data => {
                options.showDataSavingSuccess();
            }).catch(error => {
                options.showDataSavingError("Error saving the data, please report at A.H.J.Bansagi@student.tudelft.nl")
            })
        });

        // Sometimes a new survey page does not render, so force the survey to render if needed.
        this.survey.onCurrentPageChanged.add(() => {
            this.survey.render();
        })
    },
    mounted() {
        this.carousel = this.$refs.carousel;
        this.survey.onCurrentPageChanged.add((sender, options) => {
            this.controlCarousel()
        })
    },
    computed: {
        navigationEnabled() {
            return this.survey.currentPageNo === 9
        },
    },
    methods: {
        /**
         * Enables the survey
         */
        startSurvey() {
            this.showSurvey = true;
        },
        /**
         * Randomizer for the order of the playlists. Is not perfect since there is a clear bias to elements appearing
         * in their original order. However, does a good enough job.
         * @param shuffleArray
         */
        shuffleRecommendations(shuffleArray) {
            for (let i = shuffleArray.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [shuffleArray[i], shuffleArray[j]] = [shuffleArray[j], shuffleArray[i]];
            }
        },
        /**
         * Stores a playlist to Spotify as "Group Survey Playlist <index>". Does not check if the playlist was already
         * stored.
         * @param recommendation
         * @param index
         */
        storePlaylist(recommendation, index) {
            this.spotify.createPlaylist(this.user.id, {
                "name": `Group Survey Playlist ${index + 1}`
            }).then(data => {
                const uriArray = recommendation.tracks.map(track => track.uri);
                return this.spotify.replaceTracksInPlaylist(data.id, uriArray);
            }, error => {
                console.error(error);
                return Promise.reject()
            }).then(_ => {
                return this.$dialog
                    .alert(`Playlist added successfully! <br /> Look in Spotify for "Group Survey Playlist ${index + 1}"`,
                        {html: true})
            })
        },
        /**
         * Replaces some text in the survey to be more user friendly. Also replaces any periods in the track names, since
         * they cause errors later on when storing in mongo.
         */
        prepareSurvey() {
            this.recommendations.forEach((recommendation, indexRecommendation) => {
                recommendation.tracks.forEach((track, index) => {
                    let trackName = track.name.replaceAll(".", "");

                    this.surveyModel.pages[indexRecommendation * 3].elements[1].defaultValue[trackName] = 3
                    this.surveyModel.pages[indexRecommendation * 3].elements[1].rows[index] = trackName;
                    delete this.surveyModel.pages[indexRecommendation * 3].elements[1].defaultValue[`Song ${index + 1}`];

                    this.surveyModel.pages[indexRecommendation * 3 + 2].elements[1].defaultValue[trackName] = 3
                    this.surveyModel.pages[indexRecommendation * 3 + 2].elements[1].rows[index] = trackName;
                    delete this.surveyModel.pages[indexRecommendation * 3 + 2].elements[1].defaultValue[`Song ${index + 1}`];
                })

                this.user.tracks.forEach((track, index) => {
                    let trackName = track.name.replaceAll(".", "");

                    this.surveyModel.pages[indexRecommendation * 3 + 1].elements[1].defaultValue[trackName] = 3
                    this.surveyModel.pages[indexRecommendation * 3 + 1].elements[1].rows[index] = trackName;
                    delete this.surveyModel.pages[indexRecommendation * 3 + 1].elements[1].defaultValue[`Song ${index + 1}`];
                })
            });
        },
        /**
         * Reverts the changes done to the survey so the data can be stored.
         * @param survey
         * @returns {*}
         */
        revertSurveyChanges(survey) {
            this.recommendations.forEach((recommendation, indexRecommendation) => {
                recommendation.tracks.forEach((track, index) => {
                    let trackName = track.name.replaceAll(".", "");

                    survey.data[`playlist${indexRecommendation + 1}_like_rating_specific`][`Song${index + 1}`] =
                        survey.data[`playlist${indexRecommendation + 1}_like_rating_specific`][trackName];
                    delete survey.data[`playlist${indexRecommendation + 1}_like_rating_specific`][trackName];


                    survey.data[`playlist${indexRecommendation + 1}_suitable_rating_specific`][`Song${index + 1}`] =
                        survey.data[`playlist${indexRecommendation + 1}_suitable_rating_specific`][trackName];
                    delete survey.data[`playlist${indexRecommendation + 1}_suitable_rating_specific`][trackName];
                });

                this.user.tracks.forEach((track, index) => {
                    let trackName = track.name.replaceAll(".", "");

                    survey.data[`playlist${indexRecommendation + 1}_selection_rating_specific`][`Song${index + 1}`] =
                        survey.data[`playlist${indexRecommendation + 1}_selection_rating_specific`][trackName];
                    delete survey.data[`playlist${indexRecommendation + 1}_selection_rating_specific`][trackName];
                })
            });

            return survey.data;
        },
        /**
         * Changes which playlist is shown based on the page of the survey that is currently shown.
         */
        controlCarousel() {
            const pageNumber = this.survey.currentPageNo;
            if (pageNumber >= 0 && pageNumber <= 2) {
                this.carousel.goToPage(0);
            } else if (pageNumber >= 3 && pageNumber <= 5) {
                this.carousel.goToPage(1);
            } else if (pageNumber >= 6 && pageNumber <= 8) {
                this.carousel.goToPage(2);
            } else if (pageNumber >= 9) {
                this.carousel.goToPage(0)
            }
        }
    },
}
</script>

<style scoped>

</style>
