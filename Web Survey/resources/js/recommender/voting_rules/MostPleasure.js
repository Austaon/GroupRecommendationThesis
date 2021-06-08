import AbstractVotingRule from "./AbstractVotingRule";

export default class MostPleasure extends AbstractVotingRule {

    static getRuleName() {
        return "Most Pleasure";
    }

    getDescription() {
        return "First finds the highest rating for every track, then picks the best of these."
    }

    votingRule(song, songRatings) {
        //return max(song_ratings.values())
        return Math.max(...Object.values(songRatings));
    }

}