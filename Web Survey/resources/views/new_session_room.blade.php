@extends('layouts.app')

@section('content')

    <div class="container">
        <div class="mt-1">

            <div class="row">
                <div class="col consentForm">

                    <h1>Create a new session</h1>

                    <p>
                        Here you can create a new session. However, you will first have to explicitly give consent that
                        you want to join the experiment.
                        Your participation is entirely voluntary, and you can withdraw at any time.
                        If you have any questions, feel free to send an email to: A.H.J.Bansagi@student.tudelft.nl
                        <br/>
                        <br/>
                        In order to start the session, please first fill in your e-mail address to ensure we can get
                        back to you when the session is ready to proceed.
                        You also have to give the session a purpose, something for which you and the other group members
                        need a playlist for.
                        For example, if you want to do a group studying session, then you can fill in "Studying" as a name.
                        This purpose will also be used later in the closing survey to check if the playlist was
                        generated correctly.
                        <br/>
                        <br/>
                        After starting the session, you can invite people to join the session on the next page.
                        The invited people will get an email to join the experiment.
                        Once they have joined, there will be a checkmark next to their email address.
                        If you are happy with the number of people who have joined, you can start the session on the same page.
                        You can also come back to it later, in case it takes a little while for people to confirm they want to join.
                        <br/>
                        <br/>
                        The experiment will consist of two stages.
                        First you will be asked to fill in five songs that fit the theme of the group.
                        You can use any song that is on Spotify for this.
                        When everyone has filled in their choices, you will be send another email, which has a link to the
                        survey.
                        In this survey you will be asked to look at and listen to three playlists and answer some questions
                        about them.
                        <br/>
                        <br/>
                        In order to create the survey, you will have to log in to Spotify, this will for example allow you to search for songs.
                        No login details are stored, but your email address and Spotify user id will be stored so that can
                        come back to the session later (for example when the survey can be filled in).
                        After you give consent you will prompted to log in.
                        <br/>
                        <br/>
                        To give consent, please read the questions below thoroughly and answer them truthfully.
                        You can withdraw by closing this page.
                        <br/>
                        <br/>
                    </p>
                </div>
            </div>

            <create-session-component
                post-consent-form-route="{{route('post_consent_form')}}"
                join-session-route="{{route('create_session')}}">
            </create-session-component>
        </div>


    </div>

@endsection
