<?php


namespace App;


use Jenssegers\Mongodb\Eloquent\Model as Eloquent;
use Jenssegers\Mongodb\Relations\HasMany;

/**
 * Class Session
 *
 * Model for the sessions table in the database.
 *
 * @package App
 */
class Session extends Eloquent
{
    // Constant variables for the states a session can be in
    const NEW_SESSION = "new_session";
    const ENTER_PLAYLIST = "enter_playlist";
    const SHOW_PLAYLIST = "show_playlist";

    protected
        $primaryKey = "id";

    protected
        $fillable = [
        'id',
        'playlist_name',
        "has_started",
        "state",
        "recommendations",
    ];

    // Used to make sure users get deleted if the associated session gets deleted.
    public static function boot()
    {
        parent::boot();

        static::deleting(
            function ($user) { // before delete() method call this
                $user->users()->delete();
            }
        );
    }

    /**
     * Sessions have a one-to-many relation with session users.
     * @return HasMany
     */
    public function users(): HasMany
    {
        return $this->hasMany(SessionUser::class);
    }

}
