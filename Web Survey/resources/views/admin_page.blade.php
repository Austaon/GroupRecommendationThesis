@extends('layouts.app')

@section('content')
    <div class="container">
        <div class="mt-1">
            <h1>Admin page</h1>

            <admin-component
            :sessions-initial="{{$sessions}}"
            delete-session-route="{{route('delete_session')}}"
            update-session-name-route="{{route("update_session_name")}}"
            update-session-state-route="{{route("update_session_state")}}"
            template-link="{{route('new_session_admin')}}"
            spotify-id="{{$userId}}">

            </admin-component>
        </div>
    </div>

@endsection
