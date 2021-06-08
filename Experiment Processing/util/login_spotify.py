import os

import spotipy

from dotenv import load_dotenv

from spotipy import SpotifyOAuth


def login_spotify():
    """
    Authenticates with the Spotify API through the Spotipy package.
    See https://spotipy.readthedocs.io and the .env.example file for required variables.
    :return:
    """
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyOAuth(scope=os.getenv("SCOPE")))
