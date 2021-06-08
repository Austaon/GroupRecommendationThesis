<?php


namespace App\Http\Controllers;


use App\Session;
use App\SpotifyWrapper;
use Collective\Annotations\Routing\Annotations\Annotations\Delete;
use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;
use Illuminate\View\View;

/**
 * Class SessionController
 *
 * Handles database calls related to Sessions. For some reason that I cannot remember, I (partly) split database calls
 * and entry points for database calls, but I was not very consistent with this.
 *
 * @package App\Http\Controllers
 */
class SessionController
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
     * Returns all sessions in the database.
     * @return Builder[]|Collection
     */
    public function getAllSessions() {
        $allSessions = Session::with("users")->get();

        // The track data stored in each user is quite heavy on data, so remove the interacted and seen data.
        foreach($allSessions as $session) {
            foreach($session->users as $user) {
                unset($user->hovered_tracks);
                unset($user->seen_tracks);
            }
        }

        return $allSessions;
    }

    /**
     * Creates and returns a new session.
     * @param string $playlistName
     * @return mixed
     */
    public function createNewSession(string $playlistName = "")
    {
        $sessionId = substr(md5(mt_rand()), 0, 16);

        return Session::create(
            [
                "id" => $sessionId,
                "tracks" => [],
                "playlist_name" => $playlistName,
                "has_started" => false,
                "state" => Session::NEW_SESSION,
            ]
        );
    }

    /**
     * Creates a new user in a session, who will be seen as the "admin" of that group. This means they can start
     * the session once they deem it is ready.
     * @param Session $session
     * @param string $emailAddress
     * @param string $userId
     * @return Model
     */
    public function createNewAdmin(Session $session, string $emailAddress, string $userId): Model
    {
        return $session->users()->create(
            [
                "id" => $userId,
                "tracks" => [],
                "hovered_tracks" => [],
                "seen_tracks" => [],
                "email_address" => $emailAddress,
                "is_admin" => true,
                "has_joined" => true,
                "has_filled_in_tracks" => false,
            ]
        );
    }

    /**
     * Returns the data of a specific session.
     * This is used in the invite part of the component, once the session is no longer in the first state, it will
     * send out a route that the javascript code uses to refresh the page.
     *
     * @Get("/session_data", as="get_session_update")
     * @param Request $request
     * @return JsonResponse
     */
    public function getSession(Request $request): JsonResponse
    {
        $sessionId = $request->input("sessionId");

        $session = Session::where("id", $sessionId)->first();

        //
        if ($session->state !== Session::NEW_SESSION) {
            $newState = route("session_room", ["session" => $sessionId]);
        } else {
            $newState = false;
        }

        return response()->json(
            [
                "session" => $session,
                "users" => $session->users,
                "new_state" => $newState
            ]
        );
    }

    /**
     * Returns the state of a specific session.
     * This is used in the data collection part of the component, once the session is no longer in that state, it will
     * send out a route that the javascript code uses to refresh the page.
     * @Get("/show_playlist_status", as="get_show_playlist")
     * @param Request $request
     * @return JsonResponse
     */
    public function getShowPlaylistStatus(Request $request): JsonResponse
    {
        $sessionId = $request->input("sessionId");
        $session = Session::where("id", $sessionId)->first();

        if ($session->state === Session::SHOW_PLAYLIST) {
            $newState = route("session_room", ["session" => $sessionId]);
        } else {
            $newState = false;
        }

        return response()->json(
            [
                "new_state" => $newState
            ]
        );
    }

    /**
     * Creates a new (non-admin) user in a session and returns the session.
     * @param string $sessionId
     * @param string $emailAddress
     * @return mixed
     */
    public function createNewUser(string $sessionId, string $emailAddress)
    {
        $session = Session::where("id", $sessionId)->first();

        $session->users()->create(
            [
                "id" => "",
                "tracks" => [],
                "hovered_tracks" => [],
                "seen_tracks" => [],
                "email_address" => $emailAddress,
                "is_admin" => false,
                "has_joined" => false,
                "has_filled_in_tracks" => false,
            ]
        );

        return $session;
    }

    /**
     * Experimental code that was used to let people join without authenticating with Spotify. Unused in the end.
     * @param string $sessionId
     * @param string $emailAddress
     * @return mixed
     */
    public function confirmUserWithoutSpotify(string $sessionId, string $emailAddress) {
        $session = Session::where("id", $sessionId)->first();

        $currentUser = $session->users()->where("email_address", $emailAddress);
        $currentUser->update(
            [
                "id" => md5($emailAddress),
                "has_joined" => true,
                "has_spotify_account" => false
            ]
        );

        return $currentUser;
    }

    /**
     * Confirm a person and add their Spotify user id.
     * @param string $sessionId
     * @param string $emailAddress
     * @param string $userId
     * @return mixed
     */
    public function confirmUser(string $sessionId, string $emailAddress, string $userId)
    {
        $session = Session::where("id", $sessionId)->first();

        $currentUser = $session->users()->where("email_address", $emailAddress);
        $currentUser->update(
            [
                "id" => $userId,
                "has_joined" => true,
                "has_spotify_account" => true
            ]
        );

        return $currentUser;
    }

    /**
     * Deletes a user from a session.
     * @Delete("/delete_user_from_session", as="delete_user_from_session")
     * @param Request $request
     * @return JsonResponse
     */
    public function deleteUser(Request $request)
    {

        $sessionId = $request->input("sessionId");
        $emailAddress = $request->input("emailAddress");

        $session = Session::where("id", $sessionId)->first();

        $currentUser = $session->users()->where("email_address", $emailAddress)->first();
        $currentUser->delete();

        return response()->json(
            [
                "session" => $session,
                "users" => $session->users,
            ]
        );
    }

    /**
     * Also deletes a user but directly from the link in the sent email instead.
     * @Get("/delete_user/{session}", as="delete_user_from_session_gui")
     * @param Request $request
     * @param string $session
     * @return Application|Factory|View
     */
    public function deleteUserDisplay(Request $request, string $session)
    {

        $sessionObject = json_decode(base64_decode($session), false);
        $sessionId = $sessionObject->sessionId;
        $emailAddress = $sessionObject->emailAddress;

        $session = Session::where("id", $sessionId)->first();

        $currentUser = $session->users()->where("email_address", $emailAddress);
        $currentUser->delete();

        return view(
            "user_deleted",
            [
                "sessionId" => $sessionId,
            ]
        );
    }

    /**
     * Progresses a session to the data collection stage.
     * @param string $sessionId
     * @return mixed
     */
    public function startSession(string $sessionId)
    {
        $session = Session::where("id", $sessionId)->first();

        $session->update(
            [
                "state" => Session::ENTER_PLAYLIST,
            ]
        );

        return $session;

    }

    /**
     * Updates all track data for a user and checks if all users in a session have submitted their data.
     * @param string $sessionId
     * @param array $userObject
     * @return JsonResponse|void
     */
    public function submitUser(string $sessionId, array $userObject)
    {
        $userId = $userObject["userId"];
        $tracks = $userObject["tracks"];
        $seenTracks = $userObject["seenTracks"];
        $hoveredTracks = $userObject["hoveredTracks"];

        $session = Session::where("id", $sessionId)->first();

        $user = $session->users()->where("id", $userId);

        if (!$user->exists()) {
            return abort(404);
        } else {
            $user->first()->update(
                [
                    "tracks" => $tracks,
                    "hovered_tracks" => $hoveredTracks,
                    "seen_tracks" => $seenTracks,
                    "has_filled_in_tracks" => true
                ]
            );
        }

        $totalUsers = $session->users()->where("has_joined", true)->count();
        $totalFilledIn = $session->users()->where("has_filled_in_tracks", true)->count();

        if ($totalUsers == $totalFilledIn) {
            $users = $session->users()->where("has_filled_in_tracks", true)->get();
        } else {
            $users = [];
        }

        return response()->json(
            [
                "session" => $session,
                "user" => $user,
                "redirect_url" => route("session_room", ["session" => $sessionId]),
                "all_users_filled_in" => $totalUsers == $totalFilledIn,
                "users" => $users
            ]
        );
    }

    /**
     * Adds recommended playlists to a session.
     * @param string $sessionId
     * @param array $recommendations
     * @return JsonResponse
     */
    public function submitRecommendation(string $sessionId, array $recommendations): JsonResponse
    {
        $session = Session::where("id", $sessionId)->first();

        $session->update(
            [
                "recommendations" => $recommendations,
                "state" => Session::SHOW_PLAYLIST
            ]
        );

        return response()->json(
            [
                "session" => $session,
                "redirect_url" => route("session_room", ["session" => $sessionId])
            ]
        );
    }

    /**
     * Adds the survey to a user profile.
     * @param string $sessionId
     * @param string $userId
     * @param array $survey
     * @return JsonResponse
     */
    public function submitSurvey(string $sessionId, string $userId, array $survey)
    {
        $session = Session::where("id", $sessionId)->first();

        $user = $session->users()->where("id", $userId)->first();

        $user->update(
            [
                "survey" => $survey
            ]
        );

        return response()->json(
            [
                "session" => $session
            ]
        );
    }
}
