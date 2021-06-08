import AbstractVotingRule from "./AbstractVotingRule";

export default class RandomOrder extends AbstractVotingRule {

    static getRuleName() {
        return "Random Order"
    }

    getDescription() {
        return "Randomly picks tracks."
    }

    votingRule(song, songRatings) {
        return Math.random();
    }

}