<?php


namespace App\Http\Controllers;


use App\ConsentForm;
use App\Mail\AdminCreateSession;
use App\Mail\PlaylistReady;
use App\Mail\SessionStarted;
use App\Mail\UserJoinSession;
use App\Session;
use App\SpotifyWrapper;
use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Collective\Annotations\Routing\Annotations\Annotations\Post;
use Collective\Annotations\Routing\Annotations\Annotations\Put;
use Illuminate\Contracts\Container\BindingResolutionException;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Routing\Redirector;
use Illuminate\Support\Facades\App;
use Illuminate\Support\Facades\Mail;
use Illuminate\View\View;
use SpotifyWebAPI\SpotifyWebAPIException;

/**
 * Class SessionRoomController
 * Web call entry point for Sessions. For some reason that I cannot remember, I (partly) split database calls
 * and entry points for database calls, but I was not very consistent with this.
 *
 * @package App\Http\Controllers
 */
class SessionRoomController
{
    /**
     * Creates an instance of the Spotify API wrapper and sets the access token for authentication.
     * @param string $accessToken
     * @return mixed
     */
    private function getApi(string $accessToken)
    {
        $wrapper = App::make(SpotifyWrapper::class);
        $wrapper->api->setAccessToken($accessToken);

        return $wrapper->api;
    }

    /**
     * Main call which returns the necessary data to display the session, in whichever state it might be.
     * @Get("/session/{session}", as="session_room")
     * @param string $session
     * @param Request $request
     * @return Application|Factory|RedirectResponse|View|void
     * @throws BindingResolutionException
     */
    public function main(string $session, Request $request)
    {

        if (!Session::where("id", $session)->exists()) {
            return abort(404);
        }

        // Try to authenticate the user and send to login if both tokens are unavailable.
        $accessToken = $request->input("accessToken");
        $refreshToken = $request->input("refreshToken");

        if (!$accessToken && !$refreshToken) {
            $authController = new SpotifyLoginController();

            return $authController->loginUser("session_room", $session);
        }

        // Try to get the user's spotify profile and refresh the token if an exception is raised.
        try {
            $spotifyUser = $this->getApi($accessToken)->me();
        } catch (SpotifyWebAPIException $e) {
            return redirect()->route(
                "refresh",
                [
                    "refreshToken" => $refreshToken,
                    "route" => "session_room",
                    "session" => $session,
                ]
            ); //TODO: Fix this
        }

        // Retrieve the session and user from the database.
        $sessionObject = Session::where("id", $session)->first();
        $user = $sessionObject->users()->where("id", $spotifyUser->id)->first();

        return view(
            "session",
            [
                "session" => $sessionObject,
                "users" => $sessionObject->users,
                "isNewSession" => false,
                "accessToken" => $accessToken,
                "refreshToken" => $refreshToken,
                "user" => $user,
                "spotifyUser" => $spotifyUser,
            ]
        );
    }

    /**
     * View returned when people click on the join session link in the email.
     * Presents a consent form, asks for their permission, and explains the purpose of the experiment.
     *
     * @Get("/consent_form/{session}", as="join_new_user")
     * @param Request $request
     * @param string $sessionString
     * @return Application
     */
    public function joinSessionAsNewUser(Request $request, string $sessionString): Application
    {
        $sessionObject = json_decode(base64_decode($sessionString), false);
        $session = Session::where("id", $sessionObject->sessionId)->first();

        return view(
            'join_session',
            [
                "sessionObject" => $sessionObject,
                "sessionString" => $sessionString,
                "session" => $session,
            ]
        );
    }

    /**
     * Posts the filled in consent form.
     * @Post("/post_consent_form", as="post_consent_form")
     * @param Request $request
     * @return JsonResponse
     */
    public function postConsentForm(Request $request): JsonResponse
    {

        $consentForm = ConsentForm::create(
            [
                "email_address" => $request->input("email_address"),
                "session_id" => $request->input("session_id"),
                "consent_form" => $request->input("consent_form"),
            ]
        );

        return response()->json(
            [
                "consent_form_accepted" => $consentForm->exists,
            ]
        );

    }

    /**
     * Adds a new user to the session. Get call to allow redirection towards it from Javascript code.
     * @Get("/confirm_join_session/{session}", as="confirm_new_user")
     * @param Request $request
     * @param string $session
     * @return Application|RedirectResponse|Redirector
     * @throws BindingResolutionException
     */
    public function confirmNewUser(Request $request, string $session)
    {
        // Log in to Spotify if no access token exists.
        if (!$request->input("accessToken")) {
            $authenticationController = new SpotifyLoginController();

            return $authenticationController->loginUser(
                "confirm_new_user",
                $session
            );
        }

        $sessionObject = json_decode(base64_decode($session), false);
        $sessionId = $sessionObject->sessionId;
        $emailAddress = $sessionObject->emailAddress;

        $accessToken = $request->input("accessToken");
        $refreshToken = $request->input("refreshToken");

        $spotifyUser = $this->getApi($accessToken)->me();

        $sessionController = new SessionController();
        $newUser = $sessionController->confirmUser($sessionId, $emailAddress, $spotifyUser->id);

        return redirect()->route(
            "session_room",
            [
                "session" => $sessionId,
                "accessToken" => $accessToken,
                "refreshToken" => $refreshToken,
                "user" => $newUser,
            ]
        );
    }

    /**
     * Returns the new_session_room view.
     * @Get("/session", as="new_session_admin")
     * @param Request $request
     * @return Application|Factory|View
     */
    public function newSessionData(Request $request)
    {
        return view(
            "new_session_room",
        );
    }

    /**
     * Create a session and then returns a route to add the current user as admin to the session.
     * (The second step is done in a separate webcall due to redirects from Spotify)
     *
     * @Post("/create_session", as="create_session")
     * @param Request $request
     * @return string
     */
    public function createSession(Request $request): string
    {
        $emailAddress = $request->get("email_address");
        $sessionName = $request->input("session_name");

        $sessionController = new SessionController();
        $session = $sessionController->createNewSession($sessionName);

        $sessionObject = [
            "emailAddress" => $emailAddress,
            "sessionId" => $session->id,
        ];

        return route(
            "add_admin_to_session",
            [
                "session" => base64_encode(json_encode($sessionObject)),
            ]
        );
    }

    /**
     * Web call to add the current user as admin to the session.
     * @Get("/add_admin_to_session/{session}", as="add_admin_to_session")
     * @param Request $request
     * @param string $session
     * @return RedirectResponse
     * @throws BindingResolutionException
     */

    public function addAdmin(Request $request, string $session): RedirectResponse
    {
        // Log in to Spotify if no access token exists.
        if (!$request->input("accessToken")) {
            $authenticationController = new SpotifyLoginController();

            return $authenticationController->loginUser(
                "add_admin_to_session",
                $session
            );
        }

        $sessionObject = json_decode(base64_decode($session), false);
        $sessionId = $sessionObject->sessionId;
        $emailAddress = $sessionObject->emailAddress;

        $accessToken = $request->get("accessToken");
        $refreshToken = $request->get("refreshToken");

        $user = $this->getApi($accessToken)->me();
        $userId = $user->id;

        $sessionController = new SessionController();
        $session = Session::where("id", $sessionId)->first();

        $newUser = $sessionController->createNewAdmin($session, $emailAddress, $userId);

        // Send an email to the current person. This was added after feedback that the url of the survey was
        // difficult to find for admins.
        Mail::to($emailAddress)->send(
            new AdminCreateSession(
                $sessionId,
                $session["playlist_name"]
            )
        );

        return redirect()->route(
            "session_room",
            [
                "session" => $session->id,
                "accessToken" => $accessToken,
                "refreshToken" => $refreshToken,
                "user" => $newUser,
            ]
        );

    }

    /**
     * Web call to add a new (non-admin) user to a session. This is called after an admin invites a new person.
     * @Post("/add_new_user", as="add_new_user")
     * @param Request $request
     * @return JsonResponse
     */
    public function createUser(Request $request): JsonResponse
    {
        $sessionId = $request->input("sessionId");
        $emailAddress = $request->input("emailAddress");

        $sessionController = new SessionController();
        $session = $sessionController->createNewUser($sessionId, $emailAddress);

        $sessionObject = [
            "emailAddress" => $emailAddress,
            "sessionId" => $sessionId,
        ];

        // Send an email to the new person.
        Mail::to($emailAddress)->send(
            new UserJoinSession(
                base64_encode(json_encode($sessionObject)),
                $session["playlist_name"]
            )
        );

        // Not sure if this is necessary to do here, seems unused but unsure.
        $routeString = route(
            "join_new_user",
            [
                "session" => base64_encode(json_encode($sessionObject)),
            ]
        );

        $deleteString = route(
            "delete_user_from_session_gui",
            [
                "session" => base64_encode(json_encode($sessionObject)),
            ]
        );

        return response()->json(
            [
                "users" => $session->users,
                "session" => $session,
                "join_session_string" => $routeString,
                "delete_user_string" => $deleteString,
            ]
        );
    }

    /**
     * Starts the session, sends an email to all group members, and changes the state to data collection.
     * @Post("/lock_session", as="lock_session")
     * @param Request $request
     * @return JsonResponse
     */
    public function startSession(Request $request): JsonResponse
    {
        $sessionId = $request->input("session");
        $sessionController = new SessionController();
        $session = $sessionController->startSession($sessionId);

        //Send email to each user with link to session.
        foreach ($session->users as $user) {
            if ($user->has_joined) {
                $sessionObject = [
                    "emailAddress" => $user->email_address,
                    "sessionId" => $sessionId,
                ];
                Mail::to($user->email_address)->send(
                    new SessionStarted($sessionId, $session->playlist_name, base64_encode(json_encode($sessionObject)))
                );
            }
        }

        return response()->json(
            [
                "redirect_url" => route("session_room", ["session" => $sessionId]),
            ]
        );
    }

    /**
     * Web call to submit tracks to a user.
     * @Put("/submit_user_tracks", as="submit_user_tracks")
     * @param Request $request
     * @return JsonResponse|void
     */
    public function putUserTracks(Request $request)
    {
        $sessionId = $request->input("sessionId");
        $userData = $request->input("userData");

        $sessionController = new SessionController();

        return $sessionController->submitUser($sessionId, $userData);
    }

    /**
     * Web call to submit recommended playlists to a session.
     * @Put("/submit_recommendation", as="submit_recommendation")
     * @param Request $request
     * @return JsonResponse
     */
    public function putRecommendation(Request $request): JsonResponse
    {
        $sessionId = $request->input("sessionId");
        $session = Session::where("id", $sessionId)->first();

        $userId = $request->input("userId");

        $recommendations = $request->input("recommendations");

        $sessionController = new SessionController();
        $response = $sessionController->submitRecommendation($sessionId, $recommendations);

        // Send an email to each user to notify them.
        foreach ($session->users as $user) {
            if ($user->has_joined && $user->id != $userId) {
                $sessionObject = [
                    "emailAddress" => $user->email_address,
                    "sessionId" => $sessionId,
                ];
                Mail::to($user->email_address)->send(
                    new PlaylistReady($sessionId, $session->playlist_name, base64_encode(json_encode($sessionObject)))
                );
            }
        }

        return $response;
    }

    /**
     * Web call to submit survey data to a user.
     * @Put("/put_survey", as="put_survey")
     * @param Request $request
     * @return JsonResponse
     */
    public function putSurveyResults(Request $request): JsonResponse
    {
        $sessionId = $request->input("sessionId");
        $userId = $request->input("userId");
        $survey = $request->input("survey");

        $sessionController = new SessionController();

        return $sessionController->submitSurvey($sessionId, $userId, $survey);
    }

}
