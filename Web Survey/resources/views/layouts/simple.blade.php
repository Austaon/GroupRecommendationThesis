<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="UTF-8">
    <title>Spotify Web Survey</title>
    
    <link href="{{asset('css/app.css')}}" rel="stylesheet">
    <link href="{{asset('css/main.css')}}" rel="stylesheet">
</head>
<body>

<div id="header">

    <!-- Static navbar -->
    <nav class="navbar navbar-default">

        <div class="container-fluid">
            <a href='{{ route("index") }}'>
                <div class="navbar-header" style="vertical-align: middle">
                    <p class="navbar-brand" id="title" href="#" style="vertical-align: middle">Spotify Survey</p>
                    {{--                    <img src="{{asset("build/images/spotify.png")}}" id="icon">--}}
                    {{HTML::image('img/spotify.png', 'spotify logo', array('id' => "icon"))}}
                </div>
            </a>
        </div><!--/.container-fluid -->
    </nav>

</div>

<div id="app">
    <main class="py-4">
        @yield('content')
    </main>
</div>
<footer class="footer">
    <div class="container">
        <span class="text-muted">
            Made by <a href="{{ route("contact") }}">Aurél Bánsági</a>, adapted from a project by <a href="https://github.com/mari-linhares"> Marianne Linhares</a>.
        </span>
    </div>
</footer>

</body>
</html>
