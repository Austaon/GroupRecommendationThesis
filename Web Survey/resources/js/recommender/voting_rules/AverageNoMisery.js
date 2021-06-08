import AbstractVotingRule from "./AbstractVotingRule";

export default class AverageNoMisery extends AbstractVotingRule {

    constructor(k, threshold=0.95) {
        super(k);
        this.threshold = threshold
    }

    static getRuleName() {
        return "Average No Misery";
    }

    getDescription() {
        return `Averages all ratings for every track, discarding any song that has a rating below ${this.threshold}, and then picks the highest ratings`
    }


    votingRule(song, songRatings) {
        //average = 0
        let average = 0;

        //for user in song_ratings:
        //average += song_ratings[user]
        for(const user in songRatings) {
            if(songRatings.hasOwnProperty(user)) {

                //if song_ratings[user] < self.threshold:
                //  return 0
                if(songRatings[user] < this.threshold) {
                    return 0;
                }

                average += songRatings[user];
            }
        }

        //return average / len(song_ratings)
        return average / Object.keys(songRatings).length;
    }

}