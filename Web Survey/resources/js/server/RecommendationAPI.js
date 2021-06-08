/**
 * Class containing different API calls to the server side of the survey.
 *
 * In general, any function with $.ajax calls are old and likely unused, while axios.<method> calls are used in
 * different components.
 */
export default class RecommendationAPI {
    constructor(routes, userId="", sessionId="") {
        this.sessionExistsUrl = ""
        this.userExistsUrl = ""
        this.createUserUrl = ""
        this.getUserDataUrl = ""
        this.getOtherUserDataUrl = ""
        this.getRecommendationUrl = ""
        this.putRecommendationUrl = ""
        this.generateRecommendationUrl = ""
        this.submitUserUrl = ""

        $.each(routes, r => {
            this[r] = routes[r]
        });

        this.userId = userId;
        this.sessionId = sessionId;
    }

    set setUserId(val) {
        this.userId = val;
    }
    set setSessionId(val) {
        this.sessionId = val;
    }

    /**
     * Checks if a session with the set session id exists.
     * @returns {Promise<AxiosResponse<any> | void>}
     */
    sessionExists() {
        return axios.get(this.sessionExistsUrl, {
            params: {
                "session_id": this.sessionId
            }
        }).catch(err =>console.log(err));
    }

    /**
     * Checks if a user with the set user id exists in the session.
     * @returns {Promise<AxiosResponse<any> | void>}
     */
    userExists() {
        return axios.get(this.userExistsUrl, {
            params: {
                session_id: this.sessionId,
                user_id: this.userId
            }
        }).catch(err => console.log(err));
    }

    /**
     * Returns the user in a session
     * @returns {*}
     */
    getUserData() {
        return $.ajax({
            url: this.getUserDataUrl,
            method: "POST",
            dataType : "json",
            data: {
                session_id: this.sessionId,
                user_id: this.userId,
            }
        }).fail(err => console.log(err));
    }

    /**
     * Puts the generated recommendations to the session
     * @param recommendationArray
     * @returns {Promise<AxiosResponse<any> | void>}
     */
    putRecommendation(recommendationArray) {

        return axios.put(this.putRecommendationUrl, {
            sessionId: this.sessionId,
            userId: this.userId,
            recommendations: recommendationArray
        }).catch(err => console.log(err))
    }

    /**
     * Puts a user with their track information to the session
     * @param tracks
     * @param hoveredUserTracks
     * @param seenUserTracks
     * @returns {Promise<AxiosResponse<any> | void>}
     */
    submitUser(tracks, hoveredUserTracks, seenUserTracks) {

        return axios.put(this.submitUserUrl, {
            sessionId: this.sessionId,
            userData: {
                userId: this.userId,
                tracks: tracks,
                seenTracks: seenUserTracks,
                hoveredTracks: hoveredUserTracks
            },
        }).catch(err => console.log(err))

    }

}
