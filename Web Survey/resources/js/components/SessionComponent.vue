<template>
    <div class="row">
        <div class="col-sm" style="margin-left: 64px">
            <h3>Search for a song:</h3>
            <!-- Search options block: Text input, dropdown menu for different categories and a search button-->
            <div class="row">
                <b-input-group class="col-lg-10">
                    <b-form-input v-model="searchOptions.query" id="searchQuery"
                                  placeholder="Search"></b-form-input>
                    <b-input-group-append>
                        <b-form-select v-model="searchOptions.selectedType" id="querySelector"
                                       :options="searchOptions.options"></b-form-select>
                        <b-button id="topTrackSearchButton" variant="info" ref="searchButton"
                                  v-on:click="runSearch(false)" :disabled="lockedSession">
                            Go!
                        </b-button>
                        <b-button id="backButton" v-if="searchOptions.showBackButton"
                                  v-on:click="runSearch(false)" :disabled="lockedSession">
                            Back
                        </b-button>
                    </b-input-group-append>
                </b-input-group>
            </div>
            <!-- Displays the search results -->
            <div class="col-lg-16" style='margin-left: -32px;'>
                <ul class="list-group" id="searchResultList">
                    <li v-for="(item, index) in searchResults" :key="`search-result-${item.id}`" class="trackList"
                        v-bind:style="{'background-image': `url(
                        ${item.images.length >= 2 ? item.images[2].url : ''})` }"
                        @mouseenter="addToHoveredTracks([item])">
                        <div v-if="item.type === 'track'">
                            <a :href="item.external_urls.spotify">{{ item.name }} - {{ item.artists[0].name }}</a>
                            <button class="btn btn-primary" v-bind:id="`addButton${index}`"
                                    v-on:click="addToChosenTracks(item)" v-if="!lockedSession"
                                    :disabled="!canAddToChosenTracks(item)">
                                <b-icon-plus></b-icon-plus>
                            </button>
                        </div>

                        <div v-else-if="item.type === 'artist'">
                            <a :href="item.external_urls.spotify" target="_blank">{{ item.name }}</a>
                            <button class="btn btn-secondary" v-bind:id="`artistButton${index}`"
                                    :ref="`artistButton${index}`"
                                    v-on:click="getArtistSongs(item)" v-if="!lockedSession">
                                <b-icon-chevron-right></b-icon-chevron-right>
                            </button>
                        </div>

                        <div v-else-if="item.type === 'album'">
                            <a :href="item.external_urls.spotify">{{ item.name }} - {{ item.artists[0].name }}</a>
                            <button class="btn btn-secondary" v-bind:id="`albumButton${index}`"
                                    v-on:click="getAlbumSongs(item)" v-if="!lockedSession">
                                <b-icon-chevron-right></b-icon-chevron-right>
                            </button>
                        </div>
                    </li>
                </ul>
            </div>
        </div>

        <!-- Shows the currently selected songs and has a submission button -->
        <div class="col-sm" style="margin-left: 64px">
            <h3 id="trackCounter">Chosen Tracks ({{ chosenTracksCounter }}):</h3>
            <b-input-group class="col-lg-10" style='padding-left: 0;'>
                <b-button variant="info" id="lockSongsButton" type="button"
                          v-on:click="submitSongs" :disabled="lockedSession || !hasEnoughSongs()">
                    Submit!
                </b-button>
            </b-input-group>

            <ul class="list-group" id="chosenTrackList">
                <li v-for="(track, index) in chosenTracks" :key="`chosen-tracks-${track.id}`" class="trackList"
                    v-bind:style="{'background-image': `url(
                        ${track.album.images.length >= 2 ? track.album.images[2].url : ''})` }">
                    <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                        {{ track.artists[0].name }}</a>
                    <button class="btn btn-danger" v-bind:id="`removeButton${index}`"
                            v-on:click="removeFromChosenTracks(track)" v-if="!lockedSession">
                        <b-icon-x></b-icon-x>
                    </button>
                </li>
            </ul>
        </div>

        <v-tour name="enterComponentTour" :steps="steps" :callbacks="tourCallbacks"></v-tour>
    </div>

</template>

<script>
import SpotifySearch from "../util/SpotifySearch";

const Spotify = require('spotify-web-api-js')
import RecommendationAPI from "../server/RecommendationAPI";
import {arrayUnique} from "../util/ArrayUtil";
import Recommender from "../recommender/recommender";

/**
 * Component that manages the second stage of the session: data collection.
 *
 * Has a search function, shows the current selection, and retrieves the top five tracks of short_term from Spotify.
 *
 * Also has a tutorial to show people how searching and submitting works.
 * Does the recommendation if the person submitting their tracks is the last to submit in the group.
 */
export default {
    name: "SessionComponent",
    data() {
        return {
            spotify: new Spotify(),
            recommendationAPI: null,
            spotifySearch: new SpotifySearch(),
            chosenTracks: [],
            seenTracks: [],
            hoveredTracks: [],
            searchResults: [],
            searchOptions: {
                selectedType: "track",
                options: [
                    {value: "album", text: "Albums"},
                    {value: "artist", text: "Artists"},
                    {value: "track", text: "Tracks"}
                ],
                query: "bring me the horizon",
                showBackButton: false
            },
            lockedSession: false,
            numberOfRequiredSongs: 5,
            steps: [
                {
                    target: "#sessionId",
                    content: "Thank you for participating in my experiment! Here is a quick tutorial on how to fill in your songs."
                },
                {
                    target: "#trackCounter",
                    content: "Here are the songs that will be submitted, currently it is showing your most listened to songs in the last few weeks."
                },
                {
                    target: "#removeButton0",
                    content: "Click on this button to remove a track from this list.",
                    params: {
                        placement: "left"
                    }
                },
                {
                    target: "#searchQuery",
                    content: "Here you can search for tracks."
                },
                {
                    target: "#addButton0",
                    content: "Press this button to add a song to your submission list.",
                    params: {
                        placement: "left"
                    }
                },
                {
                    target: "#querySelector",
                    content: "You can also search for artists and albums."
                },
                {
                    target: "#searchQuery",
                    content: "When you search for an artist and click on this button, it will show you their top 10 most listened to tracks. " +
                        "Searching for an album will show all tracks in that album."
                },
                {
                    target: "#backButton",
                    content: "Click on this button to go back."
                },
                {
                    target: "#lockSongsButton",
                    content: "Finally, click on this button when you're happy with your chosen songs. Thank you for participating!"
                }
            ],
            tourCallbacks: {
                onPreviousStep: this.onPreviousStep,
                onNextStep: this.onNextStep,
                onSkip: this.onFinishTour,
                onFinish: this.onFinishTour
            }
        };
    },
    props: {
        "accessToken": String, "userId": String, "sessionId": String,
        "routes": Object
    },
    mounted() {
        $(document).ready(() => {
            this.spotify.setAccessToken(this.accessToken);

            this.recommendationAPI = new RecommendationAPI(this.routes, this.userId, this.sessionId);

            this.spotifySearch.spotify = this.spotify;

            // Retrieves the top tracks from Spotify and adds them to the relevant lists.
            this.getTopTracks().then(data => {
                this.chosenTracks = data.items;
                this.addToSeenTracks(data.items);
                this.addToHoveredTracks(data.items);

                if (!this.$cookie.get("finishedTour")) {
                    this.$tours['enterComponentTour'].start()
                }
            });

            // Perform the search when enter is pressed.
            let searchButton = $("#searchQuery");
            if (searchButton.length > 0) {
                searchButton[0].addEventListener("keyup", function (event) {
                    // Number 13 is the "Enter" key on the keyboard
                    if (event.keyCode === 13) {
                        // Cancel the default action, if needed
                        event.preventDefault();
                        // Trigger the button element with a click
                        $("#topTrackSearchButton").click();
                    }
                });
            }
        });
    },
    methods: {
        getTopTracks() {
            return this.getTop("short_term")
        },
        getTop(timeRange) {
            return this.spotify.getMyTopTracks({"limit": 5, "time_range": timeRange})
                .then(data => {
                    return data
                }, error => {
                    console.log(error)
                });
        },
        /**
         * Adds a list of tracks to the seenTracks variable, and makes sure this list only has unique items.
         * @param tracks
         */
        addToSeenTracks(tracks) {
            if (tracks && tracks.length > 0) {
                this.seenTracks = arrayUnique(this.seenTracks.concat(...tracks));
            }
        },
        /**
         * Adds a list of tracks to the hoveredTracks variable, and makes sure this list only has unique items.
         * @param tracks
         */
        addToHoveredTracks(tracks) {
            if (tracks && tracks.length > 0) {
                this.hoveredTracks = arrayUnique(this.hoveredTracks.concat(...tracks));
            }
        },
        /**
         * Performs a search query.
         * @param displayBackButton
         */
        runSearch(displayBackButton = true) {
            this.searchOptions.showBackButton = displayBackButton;
            this.spotifySearch.search(this.searchOptions.query, this.searchOptions.selectedType).then(tracks => {
                this.searchResults = tracks;
                this.addToSeenTracks(tracks);
            })
        },
        /**
         * Retrieves the tracks of an album.
         * @param album
         */
        getAlbumSongs(album) {
            this.spotifySearch.getAlbumSongs(album["id"]).then(tracks => {
                this.searchResults = tracks;
                this.searchOptions.showBackButton = true;
            })
        },
        /**
         * Retrieves the top tracks of an artist.
         * @param artist
         */
        getArtistSongs(artist) {
            this.spotifySearch.getArtistSongs(artist["id"]).then(tracks => {
                this.searchResults = tracks;
                this.searchOptions.showBackButton = true;
            })
        },
        /**
         * Checks if a track can be added to the chosen tracks.
         * Returns true if there are less than five chosen tracks and the given track is not already in the list.
         * @param track
         * @returns {boolean}
         */
        canAddToChosenTracks(track) {
            return this.chosenTracks.length < 5 && !this.chosenTracks.find(item => track.id === item.id)
        },
        /**
         * Returns true if five tracks were selected.
         * @returns {boolean}
         */
        hasEnoughSongs() {
            return this.chosenTracks.length === 5;
        },
        /**
         * Adds to the chosen tracks list.
         * @param track
         */
        addToChosenTracks(track) {
            if (this.canAddToChosenTracks(track)) {
                this.chosenTracks.push(track);
            }
        },
        /**
         * Removes the specific track from the chosen tracks list.
         * @param track
         */
        removeFromChosenTracks(track) {
            const index = this.chosenTracks.findIndex(item => track.id === item.id);
            this.chosenTracks.splice(index, 1);
        },
        /**
         * Handles submission of tracks to the database and performs a recommendation if the current person was the
         * last to submit.
         * If not the last person: Reloads the page to a temporarily "thanks for submission!" page.
         */
        submitSongs() {
            this.lockedSession = true;
            this.recommendationAPI?.submitUser(this.chosenTracks, this.hoveredTracks, this.seenTracks).then(data => {

                if (data.data["all_users_filled_in"]) {
                    const recommender = new Recommender(10);
                    recommender.spotifyApi = this.spotify;
                    recommender.sessionRecommend(data.data.users)
                        .then((recommendationObject) => {
                            return this.recommendationAPI?.putRecommendation(recommendationObject);
                        })
                        .then(data => {
                            window.location.href = data.data.redirect_url;
                        })
                } else {
                    window.location.href = data.data.redirect_url;
                }
            });
        },
        /**
         * Fills in some data if someone goes back in the tutorial.
         * @param currentStep
         */
        onPreviousStep(currentStep) {
            if (currentStep === 3) {
                this.searchOptions.query = ""
                this.searchResults = [];
            } else if (currentStep === 4 || currentStep === 5) {
                this.searchOptions.query = "Sanjake"
                this.searchOptions.selectedType = "track";
                this.$refs.searchButton.click();
            } else if (currentStep === 6) {
                this.searchOptions.query = "Bring Me The Horizon";
                this.searchOptions.selectedType = "artist";
                this.$refs.searchButton.click();
                this.searchOptions.showBackButton = true;
            }
        },
        /**
         * Fills in some data if someone goes forward in the tutorial.
         * @param currentStep
         */
        onNextStep(currentStep) {
            if (currentStep === 0 && this.chosenTracks.length === 0) {
                this.steps[currentStep + 1].content = "Here are the songs that will be submitted."
            } else if (currentStep === 1 && this.chosenTracks.length === 0) {
                this.steps[currentStep + 1] = {
                    content: "You can select a total of five songs.",
                    target: "#trackCounter"
                }
            } else if (currentStep === 2) {
                this.searchOptions.query = "Sanjake"
                this.$refs.searchButton.click();
            } else if (currentStep === 4) {
                this.searchOptions.query = "Bring Me The Horizon";
                this.searchOptions.selectedType = "artist";
                this.$refs.searchButton.click();
                this.searchOptions.showBackButton = true;
            } else if (currentStep === 5) {
                this.$refs.artistButton0[0].click();
            }
        },
        /**
         * Called when the tutorial is finished.
         */
        onFinishTour() {
            this.searchOptions.query = "";
            this.searchOptions.selectedType = "track";
            this.searchResults = [];
            this.searchOptions.showBackButton = false;

            // Sets a cookie for 7 days which prevents the tutorial from showing up.
            this.$cookie.set("finishedTour", true, {
                expires: 7,
                secure: true
            });
        }
    },
    watch: {},
    computed: {
        /**
         * Shows the number of selected tracks.
         */
        chosenTracksCounter() {
            return `${this.chosenTracks.length} / ${this.numberOfRequiredSongs}`;
        }
    }
}
</script>

<style scoped>

</style>
