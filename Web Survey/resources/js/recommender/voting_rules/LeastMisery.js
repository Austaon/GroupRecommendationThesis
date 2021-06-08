import AbstractVotingRule from "./AbstractVotingRule";

export default class LeastMisery extends AbstractVotingRule {

    static getRuleName() {
        return "Least Misery";
    }

    getDescription() {
        return `First finds the lowest rating for every track, then picks the best of these.
        This option is a "safe" option, in that it will pick tracks that everyone at least kind of likes.
        However, this can also lead to boring results.`
    }

    votingRule(song, songRatings) {
        //return min(song_ratings.values())
        return Math.min(...Object.values(songRatings));
    }

}
