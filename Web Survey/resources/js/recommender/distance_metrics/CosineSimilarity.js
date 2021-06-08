import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class CosineSimilarity extends AbstractDistanceMetric {

    static getMetricName() {
        return "Cosine Similarity"
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let distanceA = 0;
        let distanceB = 0;
        let distanceAB = 0;

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

            distanceA += attributeOther ** 2;
            distanceB += attributeOwn ** 2;
            distanceAB += attributeOther * attributeOwn;
        });
        let distance;

        try {
            distance = distanceAB / Math.sqrt(distanceA * distanceB)
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return distance;
    }

}