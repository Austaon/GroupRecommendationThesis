<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Http\Request;

class AdminRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     *
     * Used to make sure that some views are only viewable by specific spotify ids.
     *
     * @param Request $request
     * @return bool
     */
    public function authorize(Request $request): bool
    {
        if($request->isMethod("get")) {
            $spotifyId = $request->get("spotify_id");
        } else {
            $spotifyId = $request->input("spotify_id");

        }

        return strcmp(env("ADMIN_ID", ""), $spotifyId) === 0;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array
     */
    public function rules()
    {
        return [
            //
        ];
    }
}
