<?php


namespace App;

use Jenssegers\Mongodb\Eloquent\Model;

/**
 * Class TrackData
 *
 * Model class for the track_data table in the database.
 *
 * @package App
 */
class TrackData extends Model
{
    protected $primaryKey = "track_id";

    protected $fillable = [
        "track_id", "name", "artist", "acousticness", "danceability",
        "energy", "instrumentalness", "liveness", "loudness", "speechiness",
        "valence", "tempo"
    ];
}
