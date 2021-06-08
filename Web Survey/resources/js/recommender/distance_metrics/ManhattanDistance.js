import AbstractDistanceMetric from "./AbstractDistanceMetric";

export default class ManhattanDistance extends AbstractDistanceMetric {

    static getMetricName() {
        return "Manhattan Distance";
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

            tempDistance += Math.abs(attributeOwn - attributeOther);
        });
        let distance;

        try {
            distance = tempDistance / this.attributeKeys.length;
        } catch(err){
            console.log("Zero division");
            return NaN;
        }
        return (1-distance);
    }


}