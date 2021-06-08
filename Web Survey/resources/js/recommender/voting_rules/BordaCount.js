import AbstractVotingRule from "./AbstractVotingRule";

export default class BordaCount extends AbstractVotingRule {

    constructor(k, numberOfPoints=5) {
        super(k);
        this.numberOfPoints = numberOfPoints;
    }

    static getRuleName() {
        return "Borda Count";
    }

    getDescription() {
        return `Each user (automatically) votes for their favourites, awarding ${this.numberOfPoints} to their top track,
         ${this.numberOfPoints - 1} to the next and so on. After awarding points to five tracks, the rest will be given 0 points.
        These votes are then added together, and the highest awarded tracks are picked. 
        NOTE: Since everyone will vote for their own tracks first, this voting method is kind of useless at the moment.
        `
    }

    calculateBordaRatings(songRatings, user) {

        //user_ratings = {k: v[user] for k, v in song_ratings.items()}
        let userRatings = [];
        Object.keys(songRatings).forEach(track => {
            userRatings.push([track, songRatings[track][user]]);
        });

        //sorted_ratings = sorted(user_ratings.items(), key=lambda v: v[1], reverse=True)
        this.sort(userRatings);

        // max_points = self.number_of_points
        // borda_ratings = []
        let maxPoints = this.numberOfPoints;
        let bordaRatings = [];

        // for song in sorted_ratings:
        //  borda_ratings.append((song[0], max_points))
        //  max_points = max_points - 1 if max_points > 0 else 0
        userRatings.forEach(track => {
           bordaRatings.push([track[0], maxPoints]);
           maxPoints = Math.max(0, maxPoints - 1);
        });

        // return borda_ratings
        return bordaRatings;
    }

    *calculateVotes(data) {

        const users = this.getUsers(data);

        // result = {}
        let tempVotingData = {};

        // for song in data:
        //  result[song] = 0
        for(const song in data) {
            if(data.hasOwnProperty(song)) {
                tempVotingData[song] = 0;
            }
        }

        // for user in self.users:
        //  user_ratings = self.calculate_borda_ratings(data, user)
        let userRatings = {};
        for(const user in users) {
            userRatings = this.calculateBordaRatings(data, users[user]);

            // for song in user_ratings:
            // result[song[0]] += song[1]
            for(const song in userRatings) {
                if(userRatings.hasOwnProperty(song)) {
                    const track = userRatings[song];
                    tempVotingData[track[0]] += track[1];
                }
            }
        }

        let votingData = [];
        for(const song in tempVotingData) {
            if(tempVotingData.hasOwnProperty(song)) {
                votingData.push([song, tempVotingData[song]]);
            }
        }

        // return sorted(result.items(), key=lambda v: v[1], reverse=True)
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

    /*
        def calculate_borda_ratings(self, song_ratings, user):
        user_ratings = {k: v[user] for k, v in song_ratings.items()}
        sorted_ratings = sorted(user_ratings.items(), key=lambda v: v[1], reverse=True)

        max_points = self.number_of_points

        borda_ratings = []

        for song in sorted_ratings:
            borda_ratings.append((song[0], max_points))
            max_points = max_points - 1 if max_points > 0 else 0

        return borda_ratings

     */

}