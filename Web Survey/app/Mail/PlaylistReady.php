<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

/**
 * Class PlaylistReady
 *
 * Model class for the mail that is sent to all group members once the playlists have been generated and the survey
 * can be filled in.
 * @package App\Mail
 */
class PlaylistReady extends Mailable
{
    use Queueable, SerializesModels;

    public string $sessionId;
    public string $sessionName;
    public string $sessionObject;

    /**
     * Create a new message instance.
     *
     * @param string $sessionString
     * @param string $sessionName
     * @param string $sessionObject
     */
    public function __construct(string $sessionString, string $sessionName, string $sessionObject)
    {
        $this->sessionId = $sessionString;
        $this->sessionName = $sessionName;
        $this->sessionObject = $sessionObject;
    }

    /**
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        return $this
            ->subject("Session " . $this->sessionName . " is ready to be evaluated")
            ->view('emails.playlist_ready');
    }
}
