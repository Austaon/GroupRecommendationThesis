import os

from dotenv import load_dotenv
from mongoengine import connect, disconnect


def connect_to_database():
    """
    Connects to the database containing data obtained from the second experiment.
    :return:
    """
    load_dotenv()
    connect('laravel', host=os.getenv("DATABASE_NAME"), port=int(os.getenv("DATABASE_PORT")))


def close_database_connection():
    """
    Close the current database connection.
    :return:
    """
    disconnect()


def connect_to_anonymous_database():
    """
    Connects to the database meant to store / use anonymised data.
    :return:
    """
    load_dotenv()
    connect('anonymous', host=os.getenv("DATABASE_NAME"), port=int(os.getenv("DATABASE_PORT")))


def connect_to_first_experiment_database():
    """
    Connects to the database containing data obtained from the first experiment.
    :return:
    """
    load_dotenv()
    connect('experiment1', host=os.getenv("DATABASE_NAME"), port=int(os.getenv("DATABASE_PORT")))


def connect_to_skip_database():
    """
    Connects to the database meant to store / use data from the Spotify Sequential Skip Prediction Challenge dataset.
    :return:
    """
    load_dotenv()
    connect('skip_dataset', host=os.getenv("DATABASE_NAME"), port=int(os.getenv("DATABASE_PORT")))
