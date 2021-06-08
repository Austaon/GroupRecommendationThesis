<template>
    <div class="container">
        <div class="row">
            <div class="col consentForm" style="padding-left: 0 !important;">
                <b-form>
                    <b-form-group
                        id="input-group-1"
                        label="Email address:"
                        label-for="input-1">
                        <b-form-input
                            id="input-1"
                            v-model="form.email"
                            type="email"
                            required
                            placeholder="Enter email"></b-form-input>
                    </b-form-group>

                    <b-form-group id="input-group-2" label="Session Name:" label-for="input-2">
                        <b-form-input
                            id="input-2"
                            v-model="form.sessionName"
                            required
                            placeholder="Enter name"></b-form-input>
                    </b-form-group>

                </b-form>
            </div>

            <div class="row">
                <div id="surveyContainer">
                    <survey :survey="survey"></survey>
                </div>
            </div>
            <div class="col consentForm" style="padding-left: 0 !important;">
                <button type="button" class="btn btn-success" @click="createSession" :disabled="!hasConsented">
                    Create Session
                </button>
            </div>
        </div>

    </div>

</template>

<script>
import * as SurveyVue from "survey-vue";
import consentForm from "../survey/consent_form.json"

/**
 * Component that manages creating a session. Requires a person to fill in a consent form, their email address, and
 * a purpose for the group.
 */
export default {
    name: "CreateSessionComponent",
    props: {
        postConsentFormRoute: "",
        joinSessionRoute: "",
    },
    data() {
        return {
            survey: null,
            currentDate: new Date().toLocaleDateString(),
            form: {
                email: "",
                sessionName: ""
            }
        }
    },
    created() {

        // Replaces the date template with the actual current date.
        consentForm.pages[0].elements[0].rows[0].text =
            consentForm.pages[0].elements[0].rows[0].text.replace("${this.currentDate}", this.currentDate);

        // Loads the consent form.
        this.survey = new SurveyVue.Model(consentForm);
        this.survey.showNavigationButtons = false;
    },
    methods: {
        /**
         * Posts the consent form and then creates a session with the given data.
         */
        createSession() {
            axios.post(this.postConsentFormRoute, {
                    email_address: this.form.email,
                    session_id: "",
                    consent_form: this.survey.data
                }
            ).then(data => {
                if (data.data.consent_form_accepted) {
                    return axios.post(this.joinSessionRoute, {
                        email_address: this.form.email,
                        session_name: this.form.sessionName
                    })
                }
            }).then(redirectUrl => {
                window.location.href = redirectUrl.data;
            });
        },
        /**
         * Checks if a string is a valid email address.
         * @param email
         * @returns {boolean}
         */
        validEmail: function (email) {
            const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
    },
    computed: {
        /**
         * Returns true if a person has done all steps to consent and prepare the session.
         */
        hasConsented() {
            return this.survey.getPlainData()[3].data.length > 0
                && this.form.email && this.validEmail(this.form.email)
                && this.form.sessionName;
        }
    }

}
</script>

<style scoped>

</style>
