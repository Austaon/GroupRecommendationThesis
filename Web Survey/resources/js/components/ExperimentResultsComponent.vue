<template>
    <div>
        <b-tabs content-class="mt-3">
            <b-tab title="Ratings">
                <ratings-component
                    :sessions-initial="sessionsInitial"
                    :get-track-data-route="getTrackDataRoute"
                    :spotify-id="spotifyId">
                </ratings-component>
            </b-tab>
            <b-tab title="Boundary">
                <p>
                    <boundary-component
                        :sessions-initial="sessionsInitial"
                        :track-list="trackList"
                        :get-track-data-route="getTrackDataRoute"
                        :get-user-data-route="getUserDataRoute"
                        :spotify-id="spotifyId">
                    </boundary-component>
                </p>
            </b-tab>
            <b-tab title="Periodic Effects" active>
                <periodic-effects-component
                    :sessions-initial="sessionsInitial"
                    :get-track-data-route="getTrackDataRoute"
                    :spotify-id="spotifyId">
                </periodic-effects-component>
            </b-tab>
        </b-tabs>
    </div>
</template>

<script>

import BoundaryComponent from "./results/BoundaryComponent";
import RatingsComponent from "./results/RatingsComponent";
import PeriodicEffectsComponent from "./results/PeriodicEffectsComponent";

/**
 * Admin component which shows the results of the surveys in three different views.
 */
export default {
    name: "ExperimentResultsComponent",
    components: {PeriodicEffectsComponent, RatingsComponent, BoundaryComponent},
    data() {
        return {
            sessions: []
        }
    },
    props: {
        sessionsInitial: {},
        getTrackDataRoute: "",
        getUserDataRoute: "",
        spotifyId: "",
        trackList: {}
    },
    mounted() {
        this.sessionsInitial.forEach(session => {
            this.sessions.push(session)
        })
    },
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
