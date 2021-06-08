@extends('layouts.app')

@section('content')

    @if (!$user )

        <div class="container">
            <div class="mt-1">
                <h1>Profile</h1>
            </div>
            <p class="lead">You need to log in to see this page</p>

            <a type="button" class="btn btn-secondary" href="{{ route('spotify_login') }}">Login</a>
        </div>

    @else

        <img src="{{ asset('build/icons/chevron-right.svg') }}" alt="" width="32" height="32"
             title="Select" style="display: none" id="svgNext">

        <img src="{{ asset('build/icons/plus.svg') }}" alt="" width="32" height="32"
             title="Select" style="display: none" id="svgAdd">

        <img src="{{ asset('build/icons/x.svg') }}" alt="" width="32" height="32"
             title="Select" style="display: none" id="svgRemove">

        {{--        <script>--}}
        {{--            localStorage.setItem("is_admin", {{ 0 }});--}}
        {{--            localStorage.setItem('authentication', '{{ authentication }}');--}}
        {{--            localStorage.setItem('user_id', '{{ user.uri|json_encode }}');--}}
        {{--            localStorage.setItem('redirect_url', '{{ path("submission") }}');--}}
        {{--            localStorage.setItem('missing_image', '{{ asset("build/images/spotify.png") }}');--}}
        {{--            localStorage.setItem('session_id', '{{ session_id }}');--}}
        {{--            console.log("{{ session_id }}")--}}

        {{--            //Routes--}}
        {{--            localStorage.setItem('user_exists', '{{ path('recommender_user_exists') }}');--}}
        {{--            localStorage.setItem('create_user', '{{ path('recommender_create_user') }}');--}}
        {{--            localStorage.setItem('get_user', '{{ path('recommender_get_user') }}');--}}
        {{--            localStorage.setItem('get_other_users', '{{ path('recommender_get_other_users') }}');--}}
        {{--            localStorage.setItem('get_recommendation', '{{ path('recommender_get_recommendation') }}');--}}
        {{--            localStorage.setItem('update_recommendation', '{{ path('recommender_update_recommendation') }}');--}}
        {{--            localStorage.setItem('generate_recommendation', '{{ path('recommender_generate_recommendation') }}')--}}
        {{--        </script>--}}

        <div class="container">

            <h1> Hi {{ $user->display_name }}</h1>

            <div class="row">
                <div class="input-group col-sm-3 vertical-center">
                    <label>Session id: {{ $session_id }} </label>
                </div>
            </div>

            <hr class="half-rule"/>

            <session-component
                access-token="{{$accessToken}}"
                user-id="{{$user->id}}"
                session-id="{{$session_id}}"
                v-bind:routes="{
                    userExistsUrl: '{{ route('user_exists') }}',
                    submitUserUrl: '{{route('submit_user')}}'
                }">

            </session-component>

        </div>

    @endif


@endsection
