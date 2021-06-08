export default class AbstractVotingRule {

    constructor(k=-1) {
        this.k = k;
        this.ruleName = this.constructor.getRuleName();
    }

    static getRuleName() {
        return "Abstract Voting Rule"
    }

    static get idName() {
        return this.getRuleName().replace(/ /g, "").replace("'", "");
    }

    getDescription() {
        return "Abstract class of the voting rules"
    }

    getUsers(data) {
        return Object.keys(Object.values(data)[0]);
    }

    sort(sortArray) {
        sortArray.sort(function(x, y) {
            if (x[1] < y[1]) {
                return -1;
            }
            if (x[1] > y[1]) {
                return 1;
            }
            return 0;
        }).reverse();
    }

    votingRule(song, songRatings) {
        throw new Error("Calling abstract method");
    }

    *calculateVotes(songRatings) {

        let votingData = [];
        for(const song in songRatings) {
            if(songRatings.hasOwnProperty(song)) {
                votingData.push([song, this.votingRule(song, songRatings[song])]);
            }
        }

        //return sorted(result.items(), key=lambda v: v[1], reverse=True)
        this.sort(votingData);

        let length;
        if(this.k === -1) {
            length = votingData.length;
        } else {
            length = this.k;
        }

        for(const i in [...Array(length).keys()]) {
            yield votingData[i];
        }
    }

}
