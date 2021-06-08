@extends('layouts.app')

@section('content')

    <div class="container">
        <div class="mt-1">
            <h1>Recommender Base</h1>
        </div>

        Create new session or join current session

        <session-join-component
            v-bind:routes="{
                sessionExistsUrl: '{{route("session_exists")}}',
                newSessionUrl: '{{route("new_session")}}'
                }"
            next-page-url="{{route("recommender_page")}}"
            access-token="{{$accessToken}}"
            refresh-token="{{$refreshToken}}">

        </session-join-component>
    </div>

@endsection
