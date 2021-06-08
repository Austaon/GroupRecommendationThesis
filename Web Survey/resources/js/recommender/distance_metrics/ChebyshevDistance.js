import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class ChebyshevDistance extends AbstractDistanceMetric {

    static getMetricName() {
        return "Chebyshev Distance";
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let maxDistance = 0;

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

            const tempDistance = Math.abs(attributeOwn - attributeOther);
            if(tempDistance > maxDistance) {
                maxDistance = tempDistance;
            }
        });

        return maxDistance;
    }


}