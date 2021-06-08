import AbstractVotingRule from "./AbstractVotingRule";

export default class Median extends AbstractVotingRule {

    static getRuleName() {
        return "Median";
    }

    getDescription() {
        return "Calculates the median of every track's ratings and picks the highest of these."
    }

    median(values) {

        if(values.length === 0) {
            return 0;
        }

        if(values.length === 2) {
            return (values[0][1] + values[1][1]) / 2
        }

        values.sort(function(x, y) {
            return x[1]-y[1];
        });

        const half = Math.floor(values.length / 2);

        if (values.length % 2)
            return values[half][1];

        return (values[half - 1][1] + values[half][1]) / 2.0;
    }

    votingRule(song, songRatings) {
        // return statistics.median(song_ratings.values())
        return this.median(Object.entries(songRatings));
    }

}