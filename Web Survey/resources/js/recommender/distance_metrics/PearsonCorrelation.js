import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class PearsonCorrelation extends AbstractDistanceMetric {

    static getMetricName() {
        return "Pearson Correlation";
    }

    calculateMean(track, attributes) {
        const self = this;

        let mean = 0;
        this.attributeKeys.forEach(attribute => {
            if(attribute === "loudness") {
                mean += self.fixLoudness(attributes[track][attribute]);
            } else {
                mean += attributes[track][attribute];
            }
        });
        mean /= this.attributeKeys.length;

        return mean;
    }

    calculateDistance(track, otherTrack, attributes) {
        const self = this;

        let distanceA = 0;
        let distanceB = 0;
        let distanceAB = 0;

        let meanTrack = this.calculateMean(track, attributes);
        let meanOther = this.calculateMean(otherTrack, attributes);

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

            distanceA += (attributeOther - meanOther) ** 2;
            distanceB += (attributeOwn - meanTrack) ** 2;
            distanceAB += (attributeOther - meanOther) * (attributeOwn - meanTrack);
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