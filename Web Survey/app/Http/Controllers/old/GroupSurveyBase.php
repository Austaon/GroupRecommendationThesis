<?php


namespace App\Http\Controllers;


use Collective\Annotations\Routing\Annotations\Annotations\Get;
use Illuminate\Contracts\Foundation\Application;
use Illuminate\Contracts\View\Factory;
use Illuminate\Http\Request;
use Illuminate\View\View;

class GroupSurveyBase
{
    /**
     * @Get("/recommender_base", as="recommender_base")
     * @param Request $request
     * @return Application|Factory|View
     */
    public function main(Request $request) {
        $accessToken = $request->input("accessToken");
        $refreshToken = $request->input("refreshToken");

        return view('group_recommender_base', [
            "accessToken" => $accessToken,
            "refreshToken" => $refreshToken
        ]);
    }
}
