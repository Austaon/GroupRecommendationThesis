<?php


namespace App\Http\Controllers;


use App\Http\Requests\AdminRequest;
use App\Session;
use App\SessionUser;
use App\SpotifyWrapper;
use App\TrackData;
use Collective\Annotations\Routing\Annotations\Annotations\Delete;
use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Collective\Annotations\Routing\Annotations\Annotations\Post;
use Illuminate\Contracts\Container\BindingResolutionException;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Routing\Redirector;
use Illuminate\Support\Facades\App;
use Illuminate\View\View;
use SpotifyWebAPI\SpotifyWebAPIException;

/**
 * Class AdminPageController
 *
 * Controller class for some admin pages and functionality.
 * Most of these are unused/unfinished and experimental in nature.
 *
 * @package App\Http\Controllers
 */
class AdminPageController
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
     * Returns a view with all sessions, but only if the currently logged in user matches an specific spotify id.
     * @Get("/experiment_results", as="experiment_results")
     * @param Request $request
     * @return Application|Factory|View|Redirector|RedirectResponse
     * @throws BindingResolutionException
     */
    public function getExperimentResults(Request $request)
    {
        // If the request does not have an access token, attempt to log in the user.
        if (!$request->input("accessToken")) {
            $authenticationController = new SpotifyLoginController();

            return $authenticationController->loginUser(
                "experiment_results",
                ""
            );
        }

        $accessToken = $request->get("accessToken");
        $refreshToken = $request->get("refreshToken");

        // Try to authenticate the person, else refresh the token
        try {
            $user = $this->getApi($accessToken)->me();
        } catch (SpotifyWebAPIException $e) {
            return redirect()->route(
                "refresh",
                [
                    "refreshToken" => $refreshToken,
                    "route" => "experiment_results",
                    "session" => "",
                ]
            );
        }

        // Check if the user matches with an admin id.
        $userId = $user->id;
        if (strcmp(env("ADMIN_ID", ""), $userId) !== 0) {
            return redirect()->route("index");
        }

        // Get all tracks
        $trackList = TrackData::select("name", "artist", "track_id")->get();
        $sessionController = new SessionController();

        return view(
            "results.experiment_results",
            [
                "sessions" => $sessionController->getAllSessions(),
                "userId" => $user->id,
                "trackList" => $trackList
            ]
        );
    }

    /**
     * Returns a view with the admin page, but only if the currently logged in user matches an specific spotify id.
     * @Get("/admin_page", as="admin_page")
     * @param Request $request
     * @return Application|Factory|Redirector|RedirectResponse|View
     * @throws BindingResolutionException
     */
    public function getSession(Request $request)
    {
        // If the request does not have an access token, attempt to log in the user.
        if (!$request->input("accessToken")) {
            $authenticationController = new SpotifyLoginController();

            return $authenticationController->loginUser(
                "admin_page",
                ""
            );
        }

        $accessToken = $request->get("accessToken");
        $refreshToken = $request->get("refreshToken");

        // Try to authenticate the person, else refresh the token
        try {
            $user = $this->getApi($accessToken)->me();
        } catch (SpotifyWebAPIException $e) {
            return redirect()->route(
                "refresh",
                [
                    "refreshToken" => $refreshToken,
                    "route" => "boundary_page",
                    "session" => "",
                ]
            );
        }
        $userId = $user->id;

        if (strcmp(env("ADMIN_ID", ""), $userId) !== 0) {
            return redirect()->route("index");
        }

        $sessionController = new SessionController();

        return view(
            "admin_page",
            [
                "sessions" => $sessionController->getAllSessions(),
                "userId" => $user->id,
            ]
        );
    }

    /**
     * Deletes a specific session and return all sessions in the database after.
     * @Delete("/delete_session", as="delete_session")
     * @param AdminRequest $request
     * @return JsonResponse
     */
    public function deleteSession(AdminRequest $request): JsonResponse
    {
        $sessionId = $request->input("session_id");
        $session = Session::where("id", $sessionId)->first();
        $session->delete();

        $sessionController = new SessionController();

        return response()->json(
            [
                "sessions" => $sessionController->getAllSessions(),
            ]
        );
    }

    /**
     * Changes the name of a session.
     * @Post("/update_session_name", as="update_session_name")
     * @param AdminRequest $request
     * @return JsonResponse
     */
    public function changeSessionName(AdminRequest $request): JsonResponse
    {
        $sessionId = $request->input("session_id");
        $newName = $request->input("session_name");
        $session = Session::where("id", $sessionId)->first();

        $session->update(
            [
                "playlist_name" => $newName,
            ]
        );

        $sessionController = new SessionController();

        return response()->json(
            [
                "sessions" => $sessionController->getAllSessions(),
            ]
        );
    }

    /**
     * Changes the state of a session.
     * @Post("/update_session_state", as="update_session_state")
     * @param AdminRequest $request
     * @return JsonResponse
     */
    public function changeSessionState(AdminRequest $request): JsonResponse
    {
        $sessionId = $request->input("session_id");
        $newState = $request->input("session_state");
        $session = Session::where("id", $sessionId)->first();

        $session->update(
            [
                "state" => $newState,
            ]
        );

        $sessionController = new SessionController();

        return response()->json(
            [
                "sessions" => $sessionController->getAllSessions(),
            ]
        );
    }

    /**
     * Returns the track data of a number of tracks.
     * @Get("/get_track_data", as="get_track_data")
     * @param AdminRequest $request
     * @return JsonResponse
     */
    public function getTrackData(AdminRequest $request): JsonResponse
    {

        $trackIds = $request->get("track_ids");

        $tracks = TrackData::whereIn("track_id", $trackIds)->get();

        return response()->json([
            "tracks" => $tracks
        ]);
    }

    /**
     * Get the data of a specific user.
     * @Get("/get_user_data", as="get_user_data")
     * @param AdminRequest $request
     * @return JsonResponse
     */
    public function getAllUserData(AdminRequest $request): JsonResponse
    {

        $userId = $request->get("user_id");
        $user = SessionUser::where("id", $userId)->get();

        return response()->json([
            "user" => $user[0]
        ]);

    }
}
