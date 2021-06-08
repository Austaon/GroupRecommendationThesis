@extends('layouts.app')

@section('content')

    <div class="container">
        <div class="mt-1">

            @if($session->state == App\Session::NEW_SESSION)
                <h1>Session room: {{$session->playlist_name}} / {{$session->id}}</h1>
                @if($user->is_admin)
                    <p>
                        You can invite the other group members here.
                        If you are waiting for people to accept the invite, you can safely close this tab.
                        Once everyone has joined, press the "Start Session" button below to start the session.
                    </p>
                @else
                    <p>
                        You have joined the session!
                        You can safely close this tab now, there will be a new email when the admin starts the session.
                    </p>
                @endif


                <session-invite-component
                    :original-session="{{$session}}"
                    :current-user="{{json_encode($user)}}"
                    get-session-update="{{route("get_session_update")}}"
                    add-new-user-route="{{route("add_new_user")}}"
                    delete-user-route="{{route("delete_user_from_session")}}"
                    start-session-route="{{route("lock_session")}}"
                ></session-invite-component>
            @elseif($session->state == App\Session::ENTER_PLAYLIST && !$user->has_filled_in_tracks)
                <h1> Hi {{ $spotifyUser->display_name }}</h1>

                <div class="row">
                    <div class="input-group col-sm-3 vertical-center">
                        <label id="sessionId">Session id: {{ $session->id }} </label>
                    </div>
                </div>

                <hr class="half-rule"/>

                <session-component
                    access-token="{{$accessToken}}"
                    user-id="{{$user->id}}"
                    session-id="{{$session->id}}"
                    v-bind:routes="{
                        'submitUserUrl': '{{route('submit_user_tracks')}}',
                        'putRecommendationUrl': '{{route('submit_recommendation')}}'
                        }">

                </session-component>
            @elseif($session->state == App\Session::ENTER_PLAYLIST && $user->has_filled_in_tracks)
                <div id="filledInTracks" class="row">
                    <div class="col-lg">
                        <h2>You have filled in your playlist, thank you :)</h2>
                        <p>
                            When everyone is done filling in their songs, you will get an email for the next stage.
                            For now you can safely close this page.
                        </p>
                        <hr/>
                        <display-playlist
                            :playlist-tracks="{{json_encode($user->tracks)}}"
                            header-message="Your chosen tracks"
                            session-id="{{$session->id}}"
                            show-playlist-route="{{route("get_show_playlist")}}"
                            :live-refresh="true">

                        </display-playlist>
                    </div>
                </div>
            @elseif($session->state == App\Session::SHOW_PLAYLIST)
                <display-recommendations
                    :recommendations="{{json_encode($session->recommendations)}}"
                    :user="{{$user}}"
                    session-purpose="{{$session->playlist_name}}"
                    session-id="{{$session->id}}"
                    access-token="{{$accessToken}}"
                    put-survey-route="{{route("put_survey")}}">

                </display-recommendations>
            @endif

        </div>


    </div>

@endsection
