<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

/**
 * Class SessionStarted
 *
 * Model class for the mail that is sent to all group members once they can fill in their track selection.
 * @package App\Mail
 */
class SessionStarted extends Mailable
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
            ->subject("Session " . $this->sessionName . " is ready to be filled in")
            ->view('emails.session_started');
    }
}
