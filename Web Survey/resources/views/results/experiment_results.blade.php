@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="mt-1">
            <h1>Experiment Results</h1>

            <experiment-results-component
                :sessions-initial="{{$sessions}}"
                get-track-data-route="{{route("get_track_data")}}"
                get-user-data-route="{{route("get_user_data")}}"
                spotify-id="{{$userId}}"
                :track-list="{{$trackList}}">
            </experiment-results-component>
        </div>
    </div>

@endsection
