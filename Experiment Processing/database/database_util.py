from mongoengine import connect, disconnect


def connect_to_database():
    """
    Connects to the database containing data obtained from the second experiment.
    :return:
    """
    connect('laravel', host='localhost', port=27017)


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
    connect('anonymous', host='localhost', port=27017)


def connect_to_first_experiment_database():
    """
    Connects to the database containing data obtained from the first experiment.
    :return:
    """
    connect('experiment1', host='localhost', port=27017)


def connect_to_skip_database():
    """
    Connects to the database meant to store / use data from the Spotify Sequential Skip Prediction Challenge dataset.
    :return:
    """
    connect('skip_dataset', host='localhost', port=27017)
