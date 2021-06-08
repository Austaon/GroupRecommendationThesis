/**
 * Ported from Python code, fixes the surveys to be in the "expected" order, rather than the randomized one.
 */
export default class PlaylistFixer {

    constructor() {
        this.metaDataLink = {
            "Probability Weighted Sum": 1,
                "Fairness": 2,
                "Least Misery": 3
        }
    }

    fixPlaylistOrder(session) {

        const surveysTemp = {};
        session.users.forEach(user => {

            if (!user.survey) {
                return
            }

            const survey = user.survey;
            const metaData = survey["metaData"]
            const resultObject = {
                "playlist1": {},
                "playlist2": {},
                "playlist3": {},
                "feedback": _.get(survey, "general_feedback_input", "")
            }

            for (let i = 1; i < 4; i++) {
                const playlistString = `playlist${i}`
                const actualIndex = this.metaDataLink[metaData[playlistString]["rule_name"]["ruleName"]]
                resultObject[`playlist${actualIndex}`] = this.gatherDataFromPlaylist(survey, i)
                resultObject[`playlist${actualIndex}`]["rule_name"] = metaData[playlistString]["rule_name"]["ruleName"]
            }

            surveysTemp[user.id] = resultObject
        })

        return surveysTemp;
    }
    gatherDataFromPlaylist(survey, playlistIndex) {
        const result = {
            "like_rating": survey[`playlist${playlistIndex}_like_rating`],
            "like_rating_specific": survey[`playlist${playlistIndex}_like_rating_specific`],
            "like_feedback": _.get(survey, `playlist${playlistIndex}_like_feedback`, ""),

            "selection_rating": survey[`playlist${playlistIndex}_selection_rating`],
            "selection_rating_specific": survey[`playlist${playlistIndex}_selection_rating_specific`],
            "selection_feedback": _.get(survey, `playlist${playlistIndex}_selection_feedback`, ""),

            "suitable_rating": survey[`playlist${playlistIndex}_suitable_rating`],
            "suitable_rating_specific": survey[`playlist${playlistIndex}_suitable_rating_specific`],
            "suitable_feedback": _.get(survey, `playlist${playlistIndex}_suitable_feedback`, ""),
        }

        for (let i = 6; i < 11; i++) {
            delete result["selection_rating_specific"][`Song ${i}`]
        }

        if (result["like_feedback"] === "") {
            result["like_feedback"] = _.get(survey, `playlist${playlistIndex}_like_specific`, "");
        }

        return result;
    }
}
