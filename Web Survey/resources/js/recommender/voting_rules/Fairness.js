import AbstractVotingRule from "./AbstractVotingRule";

export default class Fairness extends AbstractVotingRule {

    static getRuleName() {
        return "Fairness";
    }

    getDescription() {
        return `A random person gets to pick their favourite track first. Then the next user gets to pick.
        Repeat until all tracks have been chosen.`
    }

    getNextUser(currentUser, users) {
        //self.current_user = (self.current_user + 1) % users.length
        return (currentUser + 1) % users.length;
    }

    getRandomUser(users) {
        //self.current_user = random.randint(0, len(self.users)-1)
        return Math.floor(Math.random() * users.length);
    }

    votingRule(song, songRatings, currentUser) {

        //user_ratings = {k: v[self.users[self.current_user]] for k, v in song_ratings.items()}
        let userRatings = [];
        Object.keys(songRatings).forEach(track => {
            userRatings.push([track, songRatings[track][currentUser]]);
        });

        //max_rating = max(user_ratings.items(), key=lambda k: k[1])
        //return max_rating
        this.sort(userRatings);
        return userRatings[0];
    }

    * calculateVotes(songRatings) {
        let users = this.getUsers(songRatings);
        let currentUser = this.getRandomUser(users);

        let length;
        if(this.k === -1) {
            length = Object.keys(songRatings).length;
        } else {
            length = this.k;
        }

        //while len(data_copy) > 0:
        for(const _ in [...Array(length).keys()]) {
            //song_item = self.voting_rule(song=None, song_ratings=data_copy)
            const songItem = this.votingRule(null, songRatings, users[currentUser]);

            //data_copy.pop(song_item[0], None)
            delete songRatings[songItem[0]];

            //self.next_user()
            currentUser = this.getNextUser(currentUser, users);

            //return list(result.items())
            yield songItem;
        }
    }

}
