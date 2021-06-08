import AbstractVotingRule from "./AbstractVotingRule";

export default class ProbabilityWeightedSum extends AbstractVotingRule{

    static getRuleName() {
        return "Probability Weighted Sum"
    }

    getDescription() {
        return `Randomized method with weights: higher rated songs have a higher chance to being picked, but any song can be chosen.`
    }

    calculateSums(songRatings) {

        let combinedSum = {};

        //combined_sum = {s: sum(song_ratings[s].values()) ** 2 for s in song_ratings}
        Object.keys(songRatings).forEach(track => {
            for(const person in songRatings[track]) {
                const personRating = songRatings[track][person];
                if (!(track in combinedSum)) {
                    combinedSum[track] = personRating ** 2;
                } else {
                    combinedSum[track] += personRating ** 2;
                }
            }
        });

        //max_sum = sum(combined_sum.values())
        const values = Object.values(combinedSum);
        const sum = values.reduce((previous, current) => current += previous);

        //combined_sum = {s: combined_sum[s] / max_sum for s in combined_sum}
        let result = {};
        Object.entries(combinedSum).forEach(([key, value]) => {
            result[key] = value / sum;
        });

        return result;
    }

    createdWeightedPdf(songRatings) {
        let weightedPdf = [];
        let previousValue = 0;

        Object.entries(songRatings).forEach(([track, chance]) => {
            weightedPdf.push([track, previousValue]);
            previousValue += chance;
        });
        weightedPdf.push([null, 1]);
        return weightedPdf;
    }

    votingRule(song, songRatings) {
        //return random.choices(list(song_ratings.keys()), weights=song_ratings.values())[0]
        //Javascript pls
        const randomValue = Math.random();
        for(const key in songRatings) {

            if(!songRatings.hasOwnProperty(key)) {
                continue;
            }
            const trackData = songRatings[key];

            if (trackData[1] < randomValue && songRatings[parseInt(key)+1][1] > randomValue) {
                return trackData;
            }
        }
    }

    *calculateVotes(songRatings) {
        const self = this;

        //data_copy = copy.deepcopy(data)
        let normalizedPdf = this.calculateSums(songRatings);
        let weightedPdf = this.createdWeightedPdf(normalizedPdf);

        let length;

        this.k = -1;

        if(this.k === -1) {
            length = weightedPdf.length - 1;
        } else {
            length = this.k;
        }

        //while len(data_copy) > 0:
        for(const _ in [...Array(length).keys()]) {
            //chosen_song = self.voting_rule(None, combined_sum)
            let chosenSong = self.votingRule(_, weightedPdf);

            //data_copy.pop(chosen_song, None)
            delete normalizedPdf[chosenSong[0]];

            //combined_sum = self.calculate_sums(data)
            weightedPdf = self.createdWeightedPdf(normalizedPdf);
            yield chosenSong;
        }
    }
}