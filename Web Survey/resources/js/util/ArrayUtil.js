/**
 * Removes duplicate items from an array.
 * @param array
 * @returns {*}
 */
export function arrayUnique(array) {

    array.forEach(track => {

        const filteredTracks = array.filter(item => track.id === item.id);

        if(filteredTracks.length > 1) {
            const index = array.findIndex(item => track.id === item.id);
            array.splice(index, 1);
        }

    });

    return array;
}
