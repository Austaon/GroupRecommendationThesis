<?php


namespace App\Http\Controllers;


use App\SpotifyWrapper;
use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Illuminate\Contracts\Container\BindingResolutionException;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Http\RedirectResponse;
use Illuminate\Routing\Redirector;
use Illuminate\Support\Facades\App;
use Illuminate\Http\Request;
use SpotifyWebAPI\SpotifyWebAPIAuthException;

/**
 * Class SpotifyLoginController
 *
 * This class handles authentication with Spotify. It is a bit of a mess since I preferred having one method being
 * called by all functions that need to log in, rather than having one method per place that needs it.
 *
 * Spotify allows a state to be send alongside the request, which is returned as-is, this is used to maintain the
 * current session and the route that should be called after authentication is successful.
 *
 * @package App\Http\Controllers
 */
class SpotifyLoginController
{

    /**
     * Creates a SpotifyWrapper object with the right values.
     * @param array $state
     * @return SpotifyWrapper
     * @throws BindingResolutionException
     */
    private function createWrapper(array $state = []): SpotifyWrapper
    {
        $scope = [
            'user-top-read',
            "playlist-modify-public",
            "user-read-private",
        ];

        return App::makeWith(
            SpotifyWrapper::class,
            [
                'callback' => 'callback/',
                'scope' => $scope,
                "state" => empty($state) ? "" : json_encode($state),
            ]
        );
    }

    /**
     * Handles refreshing a Spotify session with the refresh token.
     *
     * @Get("/refresh", as="refresh")
     * @param Request $request
     * @return RedirectResponse
     * @throws BindingResolutionException
     */
    function refresh(Request $request): RedirectResponse
    {
        $refreshToken = $request->input("refreshToken");

        // Checks if a route or session is available in the request, else set a default of an empty string.
        if ($request->input("route")) {
            $route = $request->input("route");
        } else {
            $route = "";
        }
        if ($request->input("session")) {
            $session = $request->input("session");
        } else {
            $session = "";
        }

        $spotifyWrapper = $this->createWrapper(
            [
                "route" => $route,
                "session" => $session,
            ]
        );
        $spotifyWrapper->session->refreshAccessToken($refreshToken);

        return redirect($spotifyWrapper->getAuthorizeUrl());
    }

    /**
     * Authenticates with Spotify before a session is created (for admins).
     *
     * @Get("/spotify_login", as="spotify_login")
     * @param Request $request
     * @return RedirectResponse
     * @throws BindingResolutionException
     */
    function auth(Request $request): RedirectResponse
    {
        $route = $request->input("route");

        $spotifyWrapper = $this->createWrapper(
            [
                "route" => $route,
            ]
        );

        return redirect($spotifyWrapper->getAuthorizeUrl());
    }

    /**
     * Authenticates with Spotify after a session is created.
     * @param string $returnUrl
     * @param string $session
     * @return Application|RedirectResponse|Redirector
     * @throws BindingResolutionException
     */
    function loginUser(string $returnUrl, string $session = "")
    {
        $spotifyWrapper = $this->createWrapper(
            [
                "route" => $returnUrl,
                "session" => $session,
            ]
        );

        return redirect($spotifyWrapper->getAuthorizeUrl());

    }

    /**
     * Callback function called by Spotify after the authentication process.
     * Handles retrieving the session and route from the state object.
     *
     * @Get("/callback", as="callback")
     * @param Request $request
     * @return RedirectResponse
     * @throws BindingResolutionException
     */
    function callback(Request $request)
    {
        // Return to the index if authentication failed.
        if (array_key_exists("error", $_GET) && $_GET["error"] === "access_denied") {
            return redirect()->route("index");
        }

        // Retrieve the state object.
        if ($request->input("state")) {

            $stateObject = json_decode($request->input("state"), false);
            $route = $stateObject->route;

            if (property_exists($stateObject, "session")) {
                $sessionObject = $stateObject->session;
            } else {
                $sessionObject = "";
            }

        } else {
            $route = "index";
            $sessionObject = "";
        }

        // Request a access token using the code from Spotify
        $wrapper = $this->createWrapper();
        $session = $wrapper->session;
        try {
            $wrapper->requestAccessToken();
        } catch (SpotifyWebAPIAuthException $e) {
            return $this->loginUser($route, $sessionObject);
        }

        $accessToken = $session->getAccessToken();
        $refreshToken = $session->getRefreshToken();

        // Redirects to the given route with the session and both tokens as parameters.
        return redirect()->route(
            $route,
            [
                "session" => $sessionObject,
                "accessToken" => $accessToken,
                "refreshToken" => $refreshToken,
            ]
        );
    }

}
