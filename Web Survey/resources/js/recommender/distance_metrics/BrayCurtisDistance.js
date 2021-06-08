import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class BrayCurtisDistance extends AbstractDistanceMetric {

    static getMetricName() {
        return "Bray-Curtis Distance"
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let distanceSum = 0;
        let distanceSubtraction = 0;

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

            distanceSum += Math.abs(attributeOwn + attributeOther);
            distanceSubtraction += Math.abs(attributeOwn - attributeOther);
        });
        let distance;

        try {
            distance = distanceSubtraction / distanceSum;
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return distance;
    }

}