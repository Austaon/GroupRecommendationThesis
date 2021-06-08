<?php


namespace App;


use Jenssegers\Mongodb\Eloquent\Model;

/**
 * Class ConsentForm
 *
 * Model for the consent_forms table in the database.
 *
 * @package App
 */
class ConsentForm extends Model
{
    protected $primaryKey = "email_address";

    protected $fillable = [
        "email_address", "session_id", "consent_form"
    ];
}
