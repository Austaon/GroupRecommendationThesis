@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="mt-1">
            <h1>Deleted user from session: {{ $sessionId }}</h1>
        </div>

        All data associated to your email address and the session has been deleted. :)

        {{--        <button href="{{ route('spotify_login') }}" type="button" class="btn btn-success">Login</button>--}}
        {{--    <a type="button" class="btn btn-success" href="{{ route('spotify_login') }}">Login</a>--}}
    </div>

@endsection
