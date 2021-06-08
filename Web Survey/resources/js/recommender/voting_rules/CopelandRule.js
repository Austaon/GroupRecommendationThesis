import AbstractVotingRule from "./AbstractVotingRule";

export default class CopelandRule extends AbstractVotingRule {

    static getRuleName() {
        return "Copeland's Rule";
    }

    getDescription() {
        return `Sums all ratings for every track. Then, links every song to all other songs and creates a competition. 
        If a track is rated higher than the other track, it gets a point, else it loses a point. 
        The tracks with the highest points are then picked.`
    }

    votingRule(song, songRatings) {

        //  result = {}
        let result = {};

        //for song in song_ratings:
        Object.keys(songRatings).forEach(track => {
            //result[song] = 0
            //rating = song_ratings[song]
            //rating_sum = sum(rating.values())
            result[track] = 0;
            const ratings = songRatings[track];
            const ratingSum = Object.values(ratings).reduce((previous, current) => current += previous);

            //for competing_song in song_ratings:
            Object.keys(songRatings).forEach(otherTrack => {
                //if song == competing_song:
                if(track === otherTrack) {
                    //continue
                    return;
                }

                //competing_rating = song_ratings[competing_song]
                //competing_sum = sum(competing_rating.values())
                const competingRatings = songRatings[otherTrack];
                const competingSum = Object.values(competingRatings).reduce((previous, current) => current += previous);

                //  if rating_sum > competing_sum: score = 1
                //  elif rating_sum == competing_sum: score = 0.5
                //  else: score = -1
                let score;
                if(ratingSum > competingSum) {
                    score = 1;
                } else if(ratingSum === competingSum) {
                    score = 0.5;
                } else {
                    score = -1;
                }

                //  result[song] += score
                result[track] += score;
            });
        });

        //  return result
        return Object.entries(result);
    }

    normalize(songRatings) {
        // min_rating = abs(min(ratings.values()))
        const minRating = Math.abs(
            Math.min(
                ...Object.values(songRatings).map(track => track[1])
            )
        );

        // ratings = dict(map(lambda r: (r, ratings[r] + min_rating), ratings))
        songRatings = Object.values(songRatings).map(track => {
            return [track[0], track[1] + minRating]
        });

        // max_rating = max(ratings.values())
        const maxRating = Math.abs(
            Math.max(
                ...Object.values(songRatings).map(track => track[1])
            )
        );

        // ratings = dict(map(lambda r: (r, ratings[r] * 10 / max_rating), ratings))
        songRatings = Object.values(songRatings).map(track => {
            return [track[0], track[1] / maxRating]
        });

        // return ratings
        return songRatings;
    }

    * calculateVotes(songRatings) {
        // result = CopelandRule.calculate_copeland_ratings(data)
        const copelandResult = this.votingRule(null, songRatings);

        // result = self.normalize(result)
        const votingData = this.normalize(copelandResult);

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
}