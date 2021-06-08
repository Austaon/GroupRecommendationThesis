<template>
    <div id="adminComponentDiv">
        <div v-for="session in sessions" :key="session.id">
            <div class="row adminCenter">
                <h2>
                    Session {{ session.playlist_name }} / <a target="_blank" @click="copyLink(session)">
                    {{ session.id }}</a>
                </h2>
                <b-button
                    id="changeSessionName"
                    variant="info"
                    v-on:click="changeSessionName(session)">
                    Change Session Name
                </b-button>
            </div>
            <div class="row adminCenter">
                <h3>
                    State:
                    <b-form-select :options="states" :value="session.state"
                                   @change="value => changeSessionState(session, value)"></b-form-select>
                </h3>
            </div>
            <div class="row adminCenter">
                <div class="col-sm-8">
                    <h4>
                        Created at: {{ session.created_at }} by {{ session | getAdminUser }}
                    </h4>
                </div>
                <div class="col-sm-2">
                    <button class="btn btn-info" @click="copySession(session)">
                        Copy session
                    </button>
                </div>
                <div class="col-sm-2">
                    <button class="btn btn-danger" @click="deleteSession(session)"
                            :disabled="!shouldShowDeleteButton(session)">
                        Delete Session
                    </button>
                </div>
            </div>
            <div class="row">
                <div class="col-sm">
                    <table class="table table-striped adminTable">
                        <thead>
                        <tr>
                            <th>User</th>
                            <th>Ready?</th>
                            <th>Filled in songs?</th>
                            <th>Filled in survey?</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="(user, index) in session.users" :key="user.id">
                            <th scope="row" :id="'table-row-' + index">{{ user.email_address }}</th>
                            <td>
                                <b-icon :icon="user.has_joined ? 'check2' : 'x' "></b-icon>
                            </td>
                            <td>
                                <b-icon :icon="user.has_filled_in_tracks ? 'check2' : 'x' "></b-icon>
                            </td>
                            <td>
                                <b-icon @click="user.survey ? handleSurveyClick(user) : {}"
                                        :icon="user.survey ? 'check2' : 'x' "
                                        :class="user.survey ? 'clickable-icon' : ''"></b-icon>
                            <td/>
                        </tr>
                        </tbody>

                    </table>
                </div>
            </div>
            <div class="row" v-if="session.state === 'show_playlist'">
                <div class="col-sm">
                    <table class="table table-striped adminTable">
                        <thead>
                        <tr>
                            <th>Playlist 1 ({{ session.recommendations[0].metadata.rule_name.ruleName }})</th>
                            <th>Playlist 2 ({{ session.recommendations[1].metadata.rule_name.ruleName }})</th>
                            <th>Playlist 3 ({{ session.recommendations[2].metadata.rule_name.ruleName }})</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr v-for="index in 10" :key="session.id + 'recommendation' + index">
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
                </div>
            </div>
            <hr style="border-top: 5px solid rgba(0, 0, 0, 0.1)">
        </div>
    </div>

</template>

<script>
/**
 * Component that manages an admin panel which shows sessions and allows some modifications.
 * Usually the server craps out when loading this component the first time, but a refresh should fix it.
 */
export default {
    name: "AdminComponent",
    props: {
        sessionsInitial: {
            type: Array
        },
        deleteSessionRoute: "",
        updateSessionNameRoute: "",
        updateSessionStateRoute: "",
        templateLink: "",
        spotifyId: ""
    },
    data() {
        return {
            sessions: this.sessionsInitial,
            states: [
                {
                    value: "new_session", text: "New Session",
                },
                {
                    value: "enter_playlist", text: "Enter Playlist",
                },
                {
                    value: "show_playlist", text: "Show Playlist",
                }
            ]
        }
    },
    methods: {
        shouldShowDeleteButton(session) {
            return true
        },
        /**
         * Deletes a session.
         * @param session
         */
        deleteSession(session) {
            this.$dialog
                .confirm(`Are you sure you want to delete session ${session.id}?`)
                .then(dialog => {
                    return axios.delete(this.deleteSessionRoute, {
                        data: {
                            "spotify_id": this.spotifyId,
                            "session_id": session.id
                        }
                    })
                })
                .then(data => {
                    this.sessions = data.data.sessions;
                })
                .catch(err => {
                });
        },
        /**
         * Changes the name of a session.
         * @param session
         */
        changeSessionName(session) {
            this.$dialog.prompt({
                title: "Change session name",
                body: `Current title is: ${session.playlist_name}`
            }).then(dialog => {
                return axios.post(this.updateSessionNameRoute, {
                    "spotify_id": this.spotifyId,
                    "session_id": session.id,
                    "session_name": dialog.data || session.playlist_name
                })
            }).then(data => {
                this.sessions = data.data.sessions;
            }).catch(data => {
            });
        },
        /**
         * Changes the state of a session.
         * @param session
         * @param value
         */
        changeSessionState(session, value) {
            this.$dialog.confirm(`Are you sure you want to change the state of session ${session.id} to ${value}?`)
                .then(dialog => {
                    return axios.post(this.updateSessionStateRoute, {
                            "spotify_id": this.spotifyId,
                            "session_id": session.id,
                            "session_state": value
                        }
                    )
                })
                .then(data => {
                    this.sessions = data.data.sessions;
                }).catch(data => {
            });
        },
        /**
         * Copies a JSON representation of the session to the clipboard.
         * @param session
         */
        copySession(session) {
            const text = JSON.stringify(session);
            this.copy(text);
        },
        /**
         * Copies the link to a session to the clipboard.
         * @param session
         */
        copyLink(session) {
            const text = `${this.templateLink}/${session.id}`
            this.copy(text);
        },
        /**
         * Copies a JSON representation of a survey to the clipboard.
         * @param user
         */
        handleSurveyClick(user) {
            const text = JSON.stringify(user.survey);
            this.copy(text)
        },
        /**
         * Handles copying to the clipboard.
         * @param text
         */
        copy(text) {
            if (typeof (navigator.clipboard) === "undefined") {
                return this.oldCopy(text);
            }
            navigator.clipboard.writeText(text).then(function () {
                console.log('Async: Copying to clipboard was successful!');
            }, function (err) {
                console.error('Async: Could not copy: ', err);
            });
        },
        /**
         * Handles copying to a clipboard on web browsers that do not have access to navigator.clipboard.
         * @param text
         */
        oldCopy(text) {
            const textArea = document.createElement("textarea");
            textArea.value = text;
            textArea.style.position = "fixed";  //avoid scrolling to bottom
            document.body.appendChild(textArea);
            textArea.focus();
            textArea.select();

            try {
                document.execCommand('copy');
            } catch (err) {
                console.log(`Failed to copy: ${err}`);
            }

            document.body.removeChild(textArea)
        }
    },
    filters: {
        /**
         * Gets the admin of a session.
         * @param session
         * @returns {string}
         */
        getAdminUser(session) {
            let admin = {
                "email_address": "<no admin>"
            };
            session.users.forEach(user => {
                if (user.is_admin) {
                    admin = user;
                }
            })
            return admin["email_address"];
        }
    }
}
</script>

<style scoped>

</style>
