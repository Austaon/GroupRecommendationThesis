import BordaCount from "./BordaCount";

export default class DowdallSystem extends BordaCount {

    constructor(k) {
        super(k);
    }

    static getRuleName() {
        return "Dowdall System";
    }

    getDescription() {
        return `A variant of the Borda Count voting rule. In this variant, each user still (automatically) votes for
        their favourite tracks. However, in this case, the top pick gets 1 point, the next 1/2, then 1/3, and so on.
        The key difference from the Borda Count is that in this rule, all tracks will be awarded some points.
        Additionally, each user will always vote a 1 for their own tracks. This method does not depend on the number of
        tracks that can be voted on.`;
    }

    calculateBordaRatings(songRatings, user) {

        //user_ratings = {k: v[user] for k, v in song_ratings.items()}
        let userRatings = [];
        Object.keys(songRatings).forEach(track => {
            userRatings.push([track, songRatings[track][user]]);
        });

        //sorted_ratings = sorted(user_ratings.items(), key=lambda v: v[1], reverse=True)
        this.sort(userRatings);

        // index = 1
        // borda_ratings = []
        let index = 1;
        let bordaRatings = [];

        // for song in sorted_ratings:
        //  borda_ratings.append((song[0], 1 / index))
        //  index = index + 1
        userRatings.forEach(track => {
            if (track[1] !== 1) {
                index++;
            }
            bordaRatings.push([track[0], 1 / index]);

        });

        // return borda_ratings
        return bordaRatings;
    }
}
