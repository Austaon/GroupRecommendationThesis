import AbstractVotingRule from "./AbstractVotingRule";

export default class ExtremeFairness extends AbstractVotingRule {

    static getRuleName() {
        return "Extreme Fairness";
    }

    getDescription() {
        return `A random person gets to pick their favourite track first. The person for who this track is the lowest rated gets to pick next.
        Repeat until all tracks have been chosen.`
    }

    createUserMap(users) {
        let result = {};
        //  for user in self.users:
        //  self.user_map[user] = count
        for(const user in users) {
            if(users.hasOwnProperty(user)) {
                result[users[user]] = parseInt(user);
            }
        }
        return result;
    }

    getNextUser(users, chosenSong, songData, userMap) {
        // ratings = song_data[chosen_song[0]]
        const ratings = songData[chosenSong[0]];

        // max_rating = min(ratings.items(), key=lambda k: k[1])
        const resultArray = Object.entries(ratings);
        this.sort(resultArray);
        resultArray.reverse();

        // self.current_user = self.user_map[max_rating[0]]
        return userMap[resultArray[0]];
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
        const userMap = this.createUserMap(users);

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

            //self.next_user()
            currentUser = this.getNextUser(users, songItem, songRatings, userMap);

            //data_copy.pop(song_item[0], None)
            delete songRatings[songItem[0]];

            //return list(result.items())
            yield songItem;
        }
    }

}