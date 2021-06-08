import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class CanberraDistance extends AbstractDistanceMetric {
    //TODO: Figure out typical values


    static getMetricName() {
        return "Canberra Distance"
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let distanceSum = 0;

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

            if(attributeOwn === 0 && attributeOther === 0) {
                distanceSum += 0
            } else {
                distanceSum += Math.abs(attributeOwn - attributeOther) /
                    (Math.abs(attributeOwn) + Math.abs(attributeOther));
            }

        });
        let distance;

        try {
            distance = distanceSum;
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return distance;
    }

}