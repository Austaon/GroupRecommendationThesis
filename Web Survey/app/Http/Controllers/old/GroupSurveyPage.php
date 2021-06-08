<?php


namespace App\Http\Controllers;


use App\SpotifyWrapper;
use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Http\RedirectResponse;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\App;
use Illuminate\View\View;
use SpotifyWebAPI\SpotifyWebAPIException;

class GroupSurveyPage
{
    private function getApi(string $accessToken)
    {
        $wrapper = App::make(SpotifyWrapper::class);
        $wrapper->api->setAccessToken($accessToken);

        return $wrapper->api;
    }

    /**
     * @Get("/recommender_page", as="recommender_page")
     * @param Request $request
     * @return Application|Factory|RedirectResponse|View
     */
    public function main(Request $request) {
        $accessToken = $request->input("accessToken");
        $refreshToken = $request->input("refreshToken");
        $sessionId = $request->input('session_id');

        if(empty($accessToken)) {
            return view('group_recommender_page', [
                "accessToken" => $accessToken,
                "user" => false,
                "session_id" => $sessionId,
            ]);
        }

        try{
            $user = $this->getApi($accessToken)->me();
        } catch(SpotifyWebAPIException $e) {
            return redirect()->route("refresh", ["refreshToken" => $refreshToken]);
        }

        return view('group_recommender_page', [
            "accessToken" => $accessToken,
            "refreshToken" => $refreshToken,
            "user" => $user,
            "session_id" => $sessionId,
        ]);
    }
}
