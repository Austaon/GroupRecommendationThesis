<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="UTF-8">
    <title>Spotify Web Survey</title>

    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Montserrat">
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
    <link rel='stylesheet' href='https://fonts.googleapis.com/css?family=Gloria+Hallelujah' >
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Love+Ya+Like+A+Sister" />
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Life+Savers" />
    <!-- Renders a link tag (if your module requires any CSS)
         <link rel="stylesheet" href="/build/main.css"> -->

    <script defer src="{{ asset('js/app.js') }}"></script>

    <link href="{{asset('css/result.css')}}" rel="stylesheet">
{{--    <link href="{{asset('css/main.css')}}" rel="stylesheet">--}}
</head>
<body>

<div id="header">
</div>

<div id="app">
    <main class="py-4">
        @yield('content')
        @yield('scripts')
    </main>
</div>
<footer class="footer">
    <div class="container">
        <span class="text-muted">
            Made by <a href="{{ route("contact") }}">Aurél Bánsági</a>.
        </span>
    </div>
</footer>

</body>
</html>
