<?php


namespace App;


use Jenssegers\Mongodb\Eloquent\Model;
use Jenssegers\Mongodb\Relations\BelongsTo;

/**
 * Class SessionUser
 *
 * Model for the session_users table in the database.
 *
 * @package App
 */
class SessionUser extends Model
{
    protected $primaryKey = "id";

    protected $fillable = [
        'id', 'tracks', 'hovered_tracks', 'seen_tracks', "email_address",
        "is_admin", "has_joined", "has_filled_in_tracks", "survey", "has_spotify_account"
    ];

    /**
     * Session users belong to one session.
     * @return BelongsTo
     */
    public function session(): BelongsTo
    {
        return $this->belongsTo(Session::class);
    }

}
