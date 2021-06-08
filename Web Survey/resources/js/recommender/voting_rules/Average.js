import AbstractVotingRule from "./AbstractVotingRule";

export default class Average extends AbstractVotingRule {

    static getRuleName() {
        return "Average";
    }

    getDescription() {
        return "Averages all ratings for every track and picks the highest ratings"
    }

    votingRule(song, songRatings) {
        //average = 0
        let average = 0;

        //for user in song_ratings:
        //average += song_ratings[user]
        for(const user in songRatings) {
            if(songRatings.hasOwnProperty(user)) {
                average += songRatings[user];
            }
        }

        //return average / len(song_ratings)
        return average / Object.keys(songRatings).length;
    }

}