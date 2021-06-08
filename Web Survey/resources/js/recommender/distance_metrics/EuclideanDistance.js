import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class EuclideanDistance extends AbstractDistanceMetric {

    constructor(props) {
        super(props);
        this.ownTrackRating = 1.0;
    }


    static getMetricName() {
        return "Euclidean Distance";
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let tempDistance = 0;

        this.attributeKeys.forEach(attribute => {

            let attributeOwn;
            let attributeOther;

            if(attribute === "loudness") {
                attributeOwn = self.fixLoudness(attributes[track][attribute]);
                attributeOther = self.fixLoudness(attributes[otherTrack][attribute])
            } else {
                attributeOwn = attributes[track][attribute];
                attributeOther = attributes[otherTrack][attribute];
            }

            tempDistance += (attributeOwn - attributeOther) ** 2;
        });
        let distance;

        try {
            distance = Math.sqrt(tempDistance);
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return (1 - distance);
    }

}