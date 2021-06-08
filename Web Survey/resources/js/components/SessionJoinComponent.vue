<template>
    <div>
        <div class="row">
            <div id="surveyContainer">
                <survey :survey="survey"></survey>
            </div>
        </div>
        <div class="row consentForm" style="padding-left: 0 !important;">
            <div class="col" v-if="showButtons">
                <button type="button" class="btn btn-success" @click="joinSession" :disabled="!hasConsented">
                    Join Session
                </button>
            </div>
            <div class="col" v-if="showButtons">
                <button type="button" class="btn btn-danger" @click="withdraw">
                    Withdraw
                </button>
            </div>
        </div>
    </div>
</template>

<script>

import * as SurveyVue from "survey-vue";
import consentForm from "../survey/consent_form.json"

/**
 * Component that manages people joining a session. Loads and shows a consent form from a file.
 * Also offers a way to delete their user data.
 */
export default {
    name: "SessionJoinComponent",
    props: {
        emailAddress: "",
        sessionId: "",
        postConsentFormRoute: "",
        joinSessionRoute: "",
        withdrawRoute: "",
        showButtons: {
            default: true
        }
    },
    data() {
        return {
            survey: null,
            currentDate: new Date().toLocaleDateString()
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
         * Posts the consent form and redirects to the session.
         */
        joinSession() {
            axios.post(this.postConsentFormRoute, {
                    email_address: this.emailAddress,
                    session_id: this.sessionId,
                    consent_form: this.survey.data
                }
            ).then(data => {
                if (data.data.consent_form_accepted) {
                    window.location.href = this.joinSessionRoute;
                }
            })
        },
        /**
         * Withdraws from the session: deletes the user and returns to the index.
         */
        withdraw() {
            window.location.href = this.withdrawRoute;
        },
        async loadSurveyData() {
            return import('../survey/consent_form.json').then(surveyData => {
                return surveyData;
            });
        },
    },
    computed: {
        /**
         * Returns true if all consent form questions have been accepted.
         * @returns {boolean}
         */
        hasConsented() {
            return this.survey.getPlainData()[3].data.length > 0;
        }
    }
}
</script>
