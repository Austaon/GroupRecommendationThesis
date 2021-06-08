<?php


namespace App\Mail;


use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Queue\SerializesModels;

/**
 * Class AdminCreateSession
 *
 * Model class for the mail that is sent to the creator of a group once they have created a group.
 *
 * @package App\Mail
 */
class AdminCreateSession extends Mailable
{
    use Queueable, SerializesModels;

    public string $sessionId;
    public string $sessionName;

    /**
     * Create a new message instance.
     *
     * @param string $sessionId
     * @param string $sessionName
     */
    public function __construct(string $sessionId, string $sessionName)
    {
        $this->sessionId = $sessionId;
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
            ->subject("Group playlist session was created!")
            ->view('emails.admin_create_session');
    }
}
