import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class CorrelationDistance extends AbstractDistanceMetric {

    static getMetricName() {
        return "Correlation Similarity"
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

        let distanceU = 0;
        let distanceV = 0;
        let distanceUV = 0;

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

            distanceU += (attributeOwn - meanTrack) ** 2;
            distanceV += (attributeOther - meanOther) ** 2;
            distanceUV += (attributeOwn - meanTrack) * (attributeOther - meanOther);
        });
        let distance;

        try {
            distanceUV /= this.attributeKeys.length;
            distanceU /= this.attributeKeys.length;
            distanceV /= this.attributeKeys.length;
            distance = 1 - (distanceUV / Math.sqrt(distanceU * distanceV));
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return 1 - distance;
    }

}