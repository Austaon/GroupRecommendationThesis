export default class AbstractDistanceMetric {

    constructor() {
        this.attributeKeys = [
            "acousticness", "danceability", "energy", "instrumentalness",
            "liveness", "loudness", "speechiness", "valence"
        ];
        this.ownTrackRating = 1.0
        this.metricName = this.constructor.getMetricName();
    }

    static getMetricName() {
        return "Abstract Distance Metric"
    }

    static get idName() {
        return this.getMetricName().replace(/ /g, "").replace("'", "");
    }

    getDescription() {
        return "Abstract class of the distance metrics"
    }

    fixLoudness(loudness){
        return (loudness + 60) / 60
    }

    createRatingForPerson(userObject) {
        let result = {};
        const tracks = userObject.tracks;
        tracks.forEach(track => {
            result[track.id] = this.ownTrackRating;
        })

        return result;
    }

    calculateDistance(track, otherTrack, attributes) {
        throw new Error("Calling abstract method");
    }

    calculateAverageDistance(track, selectedUserTracks, attributes) {
        if(!(track in attributes)) {
            return NaN;
        }
        let distances = [];

        selectedUserTracks.forEach(otherTrack => {
            if (!(otherTrack in attributes)) {
                return;
            }
            const trackDistance = this.calculateDistance(track, otherTrack, attributes);

            distances.push(trackDistance);
        });


        const sum = distances.reduce((previous, current) => current += previous);
        return sum / distances.length;
    }

    calculateRatings(selectedPersonTracks, otherUsersTracks, attributes) {
        const self = this;
        let resultingDistances = {};

        //Loop over every track from the other users.
        otherUsersTracks.forEach(track => {

            //If the selected person does not already have this rack
            if(!selectedPersonTracks.includes(track)) {

                //Calculate the average distance between the selected user tracks and the other track.
                resultingDistances[track] = self.calculateAverageDistance(
                    track, selectedPersonTracks, attributes
                );
            }
        });

        return resultingDistances;
    }

}
