@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="row">
            <div class="col consentForm">

                <div class="mt-1">
                    <h1>Joining session: {{ $session->playlist_name }}</h1>
                </div>

                Welcome to the survey! Before you can join the session, you will have to explicitly give consent that
                you want to join the experiment.
                Your participation is entirely voluntary, and you can withdraw at any time.
                If you have any questions, feel free to send an email to: A.H.J.Bansagi@student.tudelft.nl
                <br/>
                <br/>
                The experiment will consist of two stages.
                First you will be asked to fill in five songs that fit the theme of the group ({{$session->playlist_name}}).
                You can use any song that is on Spotify for this.
                When everyone has filled in their choices, you will be send another email, which has a link to the
                survey.
                In this survey you will be asked to look at and listen to three playlists and answer some questions
                about
                them.
                <br/>
                In order to join the survey, you will have to log in to Spotify, this will for example allow you to search for songs.
                No login details are stored, but your email address and Spotify user id will be stored so that you can come
                back to the session later (for example when the survey can be filled in).
                After you give consent you will prompted to log in.
                <br/>
                <br/>
                To give consent, please read the questions below thoroughly and answer them truthfully.
                If you do not want to participate, there is a withdraw button below too.
                <br/>
                <br/>
            </div>
        </div>
        <session-join-component
            email-address="{{$sessionObject->emailAddress}}"
            session-id="{{$session->id}}"
            post-consent-form-route="{{route('post_consent_form')}}"
            join-session-route="{{route('confirm_new_user', ['session' => $sessionString ])}}"
            withdraw-route="{{route('delete_user_from_session_gui', ['session' => $sessionString ])}}">
        </session-join-component>

        {{--        <a href='{{route('confirm_new_user', ["session" => $sessionString ])}}' class="btn btn-success" type="button">Login</a>--}}

        {{--        <button href="{{ route('spotify_login') }}" type="button" class="btn btn-success">Login</button>--}}
        {{--    <a type="button" class="btn btn-success" href="{{ route('spotify_login') }}">Login</a>--}}
    </div>

@endsection
