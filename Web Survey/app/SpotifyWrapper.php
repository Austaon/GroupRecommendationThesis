<?php


namespace App;


use SpotifyWebAPI\SpotifyWebAPI;
use SpotifyWebAPI\Session;

/**
 * Class SpotifyWrapper
 *
 * Source: https://github.com/mikelgoig/laravel-spotify-wrapper
 *
 * @package App
 */
class SpotifyWrapper
{
    /**
     * The Spotify session.
     */
    public Session $session;

    /**
     * The Spotify API.
     */
    public SpotifyWebAPI $api;

    /**
     * The Spotify options.
     */
    private array $options = [
        'scope' => [],
        'show_dialog' => false,
    ];

    /**
     * Create a new Spotify instance.
     *
     * @param Session $session
     * @param SpotifyWebAPI $api
     * @param array $parameters
     *
     */
    public function __construct(Session $session, SpotifyWebAPI $api, array $parameters = [])
    {
        $this->session = $session;
        $this->api = $api;

        $this->options = $parameters;
    }

    /**
     * Redirect to the Spotify authorize URL.
     *
     * @return void
     */
    private function redirectToSpotifyAuthorizeUrl()
    {
        header("Location: {$this->session->getAuthorizeUrl($this->options)}");
        die();
    }

    public function getAuthorizeUrl(): string
    {

        return $this->session->getAuthorizeUrl($this->options);
    }

    /**
     * Request an access token.
     *
     * @return SpotifyWrapper | void
     */
    public function requestAccessToken()
    {
        try {
            $this->session->requestAccessToken($_GET['code']);
            return $this;
        } catch (Exception $e) {
            $this->redirectToSpotifyAuthorizeUrl();
            return;
        }
    }
}
