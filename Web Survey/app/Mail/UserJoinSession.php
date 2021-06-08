<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

/**
 * Class UserJoinSession
 *
 * Model class for the mail that is sent to an invited person, asking them if they want to join the session.
 *
 * @package App\Mail
 */
class UserJoinSession extends Mailable
{
    use Queueable, SerializesModels;

    public string $sessionString;
    public string $sessionName;

    /**
     * Create a new message instance.
     *
     * @param string $sessionString
     * @param string $sessionName
     */
    public function __construct(string $sessionString, string $sessionName)
    {
        $this->sessionString = $sessionString;
        $this->sessionName = $sessionName;
    }

    /**
     * Build the message.
     *
     * @return $this
     */
    public function build()
    {
        return $this
            ->subject("Invitation for participating in my group recommender research")
            ->view('emails.user_join_session');
    }
}
