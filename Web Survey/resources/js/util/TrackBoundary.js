/**
 * Similar to the Boundary score from the Python code. Only used for showing results to admins.
 */
export default class TrackBoundary {

    constructor() {
        this.keys = ["acousticness", "danceability", "energy", "instrumentalness",
            "liveness", "loudness", "speechiness", "valence",
        ]
        this.reset();
    }

    reset() {
        this.points = {}
        this.keys.forEach(key => {
            this.points[key] = {
                min: Number.MAX_VALUE,
                max: Number.MIN_VALUE
            }
        })
    }

    addAudioFeature(track) {
        this.keys.forEach(key => {
            const audioFeature = track[key];
            if(this.points[key]["min"] > audioFeature) {
                this.points[key]["min"] = audioFeature
            }
            if(this.points[key]["max"] < audioFeature) {
                this.points[key]["max"] = audioFeature
            }
        })
    }

    getMinSeries() {
        return Object.keys(this.points).map(key => this.points[key]["min"])
    }

    getMaxSeries() {
        return Object.keys(this.points).map(key => this.points[key]["max"])
    }

    getRangeSeries() {
        return Object.keys(this.points).map(key => {
            return {
                x: key,
                y: [this.points[key]["min"], this.points[key]["max"]]
            }
        })
    }

    trackIsInBoundary(track, experimental=false) {
        let correctness = 1
        this.keys.forEach(key => {
            if(track[key] < this.points[key]["min"] || track[key] > this.points[key]["max"]) {
                if(!experimental) {
                    return false;
                } else {
                    correctness -= 0.125
                }
            }
        })

        if(!experimental) {
            return true
        } else {
            return correctness
        }
    }

}
