<template>
    <div>
        <div class="row justify-content-center">
            <div class="col-sm">
                <h3 id="trackCounter" v-if="headerMessage">{{ headerMessage }}:</h3>
            </div>
            <div class="col-sm">
                <button type="button" class="btn btn-success" v-if="showStorePlaylistButton"
                        v-on:click="showStorePlaylistButton">
                    Store Playlist
                </button>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col">
                <ul class="list-group" id="chosenTrackList">
                    <li v-for="track in playlistTracks.slice(0, this.maxItems ? this.maxItems : playlistTracks.length+1)"
                        :key="`chosen-tracks-${track.id}`" class="trackList"
                        v-bind:style="{'background-image': `url(
                            ${track.album.images.length >= 2 ? track.album.images[2].url : ''})` }">
                        <a :href="track.external_urls.spotify" target="_blank">{{ track.name }} -
                            {{ track.artists[0].name }}</a>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script>
/**
 * Sub-component which displays a list of tracks in a neat playlist. Separated as component because it is used in
 * multiple places.
 */
export default {
    name: "DisplayPlaylist",
    props: {
        "playlistTracks": {},
        "headerMessage": "",
        "sessionId": "",
        "liveRefresh": {
            type: Boolean,
            value: false
        },
        "showPlaylistRoute": {
            type: String,
            value: ""
        },
        "showStorePlaylistButton": {
            value: false
        },
        "maxItems": {
            value: 0
        }
    },
    mounted() {

        // If liveRefresh is true, periodically retrieves the session.
        if (this.liveRefresh) {
            setInterval(() => {
                axios.get(this.showPlaylistRoute, {
                    params: {
                        "sessionId": this.sessionId
                    }
                }).then(data => {
                    if (data.data["new_state"]) {
                        window.location.href = data.data["new_state"];
                    }
                }).catch(() => {
                });

            }, 5000);
        }

    }
}
</script>

<style scoped>

</style>
