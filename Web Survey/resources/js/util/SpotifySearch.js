/**
 * Class that manages searching in Spotify. Because we allow different types of searching, some parsing needs to be
 * done when the result of a query is returned. This class handles all of that and returns the right data.
 *
 * This is some of the earliest code so it's a bit of a mess. Initially this was also handling modifying HTML/CSS, before
 * using Vue.
 */
export default class SpotifySearch {
    constructor(maxSize = 10) {
        this.maxSize = maxSize;
    }

    set spotifyApi(val) {
        this.spotify = val;
    }

    /**
     * Executes a search query to Spotify.
     * @param query
     * @param type Type of the data that should be returned (artist, album, or track)
     * @returns {*}
     */
    search(query, type) {
        const self = this;

        if (query.length === 0) {
            return;
        }

        return this.spotify.search(query, [type], {
            "limit": 10
        }).then(function (data) {
            return self.parseSearchResults(data, type);
        }, function (error) {
            console.log(error);
        });
    }

    /**
     *
     * @param trackIds
     * @returns {Promise<*>}
     */
    getTracks(trackIds) {

        return this.spotify.getTracks(trackIds).then(data => {
            const tracks = data["tracks"];
            data["tracks"] = {};
            data["tracks"]["items"] = tracks;
            return this.parseSearchResults(data, "track");
        }, function (error) {
            console.log(error);
        });
    }

    /**
     * Parses the search result so all types return consistent-ish data.
     * @param data
     * @param type
     * @returns {*}
     */
    parseSearchResults(data, type) {

        if (type === "album") {
            return this.parseAlbumResults(data);
        } else if (type === "artist") {
            return this.parseArtistResults(data);
        }

        data["tracks"]["items"].forEach(track => {
            track["type"] = "track";
            track["images"] = track["album"]["images"];
        })

        return data["tracks"]["items"];
    }

    /**
     * Parses results when albums were searched for
     * @param data
     * @returns {*}
     */
    parseAlbumResults(data) {

        data["albums"]["items"].forEach(album => {
            album["type"] = "album"
        })
        return data["albums"]["items"]
    }

    /**
     * Parses results when artists were searched for
     * @param data
     * @returns {*}
     */
    parseArtistResults(data) {

        data["artists"]["items"].forEach(artist => {
            artist["type"] = "artist"
        })
        return data["artists"]["items"];
    }

    /**
     * Retrieves the tracks that are in an album. Tries to retrieve all, but limits it to 30..., for some reason.
     * @param albumUri
     * @returns {Promise<*>}
     */
    getAlbumSongs(albumUri) {

        return this.spotify.getAlbumTracks(albumUri, {"limit": 30}).then(data => {
            let trackIds = [];
            data.items.forEach(track => {
                trackIds.push(track["id"]);
            })
            return this.getTracks(trackIds)
        }, function (error) {
            console.log(error);
        })
    }

    /**
     * Retrieves the top ten most popular tracks of an artist.
     * @param artistUri
     * @returns {Promise<*>}
     */
    getArtistSongs(artistUri) {

        return this.spotify.getArtistTopTracks(artistUri,
            "from_token", {"limit": 10}).then(data => {
                let trackIds = [];
                data.tracks.forEach(track => {
                    trackIds.push(track["id"]);
                })

                return this.getTracks(trackIds);
            }, function (error) {
                console.log(error);
            }
        )
    }
}
