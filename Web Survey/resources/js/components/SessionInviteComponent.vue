<template>
    <div class="row">
        <div class="col-sm" style="margin-left: 64px">

            <table class="table table-striped">
                <thead>
                <tr>
                    <th>User</th>
                    <th>Ready?</th>
                    <th>Delete</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(user, index) in this.userList" :key="user.id">
                    <th scope="row" :id="'table-row-' + index">{{ user.email_address }}</th>
                    <td>
                        <b-icon :icon="user.has_joined ? 'check2' : 'x' "></b-icon>
                    </td>
                    <td v-if="(currentUser.is_admin && !user.is_admin) ||
                     (!currentUser.is_admin && currentUser.id === user.id)">
                        <b-button
                            id="deleteUserAdmin"
                            variant="danger"
                            v-on:click="deleteUser(user)">
                            Delete User
                        </b-button>
                    </td>
                </tr>
                </tbody>

                <div v-if="currentUser.is_admin">
                    <b-form @submit="onSubmit" inline>
                        <b-input-group prepend="Add new user: ">
                            <b-input
                                v-model="newUserEmailAddress"
                                id="emailAddressInput"
                                placeholder="Email Address"
                                type="email"
                                required
                            ></b-input>
                        </b-input-group>
                        <b-button
                            id="addNewUserAdmin"
                            variant="primary"
                            type="submit">
                            Invite user
                        </b-button>
                        <b-tooltip target="addNewUserAdmin" :show.sync="showErrorTooltip" triggers="manual">
                            User already exists
                        </b-tooltip>
                    </b-form>
                    <b-button
                        id="lockSession"
                        variant="primary"
                        :disabled="numberOfJoinedUsers <= 1"
                        v-on:click="startSession">
                        Start Session
                    </b-button>
                </div>

            </table>
        </div>
    </div>
</template>

<script>
/**
 * Component that manages the first stage of the session: inviting people and starting the session.
 * There's two "variants" of this component, which change depending on if the current user is an admin to this
 * session or not.
 *
 * If the user is not: it just shows the users that are in a session and nothing else.
 * If the user is: it lets them delete and invite people, and start the session.
 */
export default {
    name: "SessionInviteComponent",
    props: {
        "originalSession": {},
        "currentUser": {},
        "getSessionUpdate": "",
        "addNewUserRoute": "",
        "deleteUserRoute": "",
        "startSessionRoute": ""
    },
    data() {
        return {
            "newUserEmailAddress": "",
            "session": this.originalSession,
            "showErrorTooltip": false
        }
    },
    created() {
        /**
         * Retrieves the session every 5 seconds and checks if the state has changed.
         * If the state has changed, loads a new url (effectively preforms a reload since the url is the same)
         *
         * Regardless of the state, it updates the session and user data to show new people.
         */
        setInterval(() => {
            axios.get(this.getSessionUpdate, {
                params: {
                    "sessionId": this.session.id
                }
            }).then(data => {

                if (data.data["new_state"]) {
                    window.location.href = data.data["new_state"];
                    return;
                }

                this.session = data.data.session;
                this.session.users = data.data.users;
            }).catch(() => {
            });

        }, 5000);
    },
    methods: {
        /**
         * Called when a new person is invited.
         * @param evt
         * @returns {boolean}
         */
        onSubmit(evt) {
            evt.preventDefault();

            // Checks if the user already exists and shows an error message for 1 second if it does.
            const userExists = this.session.users.find(user => user.email_address === this.newUserEmailAddress);
            if (userExists) {
                this.showErrorTooltip = true;
                setTimeout(() => this.showErrorTooltip = false, 1000);
                return false;
            }

            // Pre-emptively pushes a "user" to the session so the UI gets updated. This gets overwritten after
            // the web call returns, but this causes the UI to be more responsive.
            this.session.users.push({
                "email_address": this.newUserEmailAddress
            });

            axios.post(this.addNewUserRoute, {
                sessionId: this.session.id,
                emailAddress: this.newUserEmailAddress
            }).then(data => {
                    this.session = data.data.session;
                }
            )
        },
        /**
         * Handles deleting a user.
         * @param user
         */
        deleteUser(user) {

            axios.delete(this.deleteUserRoute, {
                data: {
                    sessionId: this.session.id,
                    emailAddress: user.email_address
                }
            }).then(data => {
                this.session = data.data.session;
                this.session.users = data.data.users;
            })
        },

        /**
         * Handles starting a session.
         */
        startSession() {
            // Creates a list of people who actually joined the session.
            const joinedUsersString = this.session.users.map(user => {
                if (user.has_joined) {
                    return `<li>${user.email_address}</li>`;
                }
            }).filter(Boolean).join("")

            // Shows a dialog with the currently joined users as confirmation.
            this.$dialog
                .confirm(`Do you want to start the session with the following users:<br />
                    <ul>${joinedUsersString}</ul>
                    Note: You won't be able to invite more people after this step`, {html: true})
                .then(dialog => {
                    axios.post(this.startSessionRoute, {
                        "session": this.session.id
                    }).then(data => {
                        window.location.href = data.data.redirect_url;
                    }).catch(err => {
                        console.log(err);
                    })
                })
                .catch(err => {
                    console.log(err);
                });
        }
    },
    computed: {
        /**
         * Computes the number of users who have currently joined the session.
         * @returns {number}
         */
        numberOfJoinedUsers() {
            let totalJoined = 0;
            this.session.users.forEach(user => {
                if (user.has_joined) {
                    totalJoined++;
                }
            });

            return totalJoined;
        },
        /**
         * Returns a list of users, but making sure the admin is at the top of the list.
         * @returns {*[]}
         */
        userList() {

            let admin;
            let otherUsers = [];

            this.session.users.forEach(user => {
                if (user.is_admin) {
                    admin = user;
                } else {
                    otherUsers.push(user);
                }
            });

            otherUsers.unshift(admin);
            return otherUsers;

        }
    }
}
</script>

<style scoped>

</style>
