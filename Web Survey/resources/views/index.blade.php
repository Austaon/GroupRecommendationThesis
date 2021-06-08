@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="mt-1">
            <h1>Group Recommender Experiment</h1>
        </div>
        This experiment aims to study different group recommender algorithms and see how effective they are.
        I'm hoping to have 3 to 8 people per group. Please let me know which people you want to invite,
        since everyone needs to give permission to store some data.
        Your participation is entirely voluntary, and you can withdraw at any time.

        If you want to create a session, please click the button below.
        <br/>
        <br/>
        <a href='{{route("new_session_admin")}}' class="btn btn-success" type="button">Create session</a>
    </div>

@endsection
