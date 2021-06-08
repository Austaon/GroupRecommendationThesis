# Group Recommendation Experiment Processing Code

This folder shows all the code that was used to process the data obtained from either experiment.

# Configuration

The only configuration that is needed is related to connecting with Spotify. 
A tutorial of how to set this up can be found at: https://developer.spotify.com/documentation/web-api/quick-start/

The `.env.example` file shows the variables that are needed to successfully authenticate.
The database connection can also be set up in this file.

# Running

There are three "main" files in this project that can be executed freely:
* experiment1.py
* experiment2.py
* skip_dataset.py

All three files have a series of (commented) function calls. 
Each of these functions is in a separate file and has documentation. 
I have been uncommenting / commenting function calls depending on what function I needed, but feel free to modify this.

## Specific instructions
Running `database_to_json()` in `experiment1.py` requires the .zip file in the `experiment1/json_files` to be extracted in the same folder.

Running `generate_track_data()` in `skip_dataset.py` requires additional data to be downloaded.
This dataset can be found at https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge .
The `track_sum` file is also generated using the same dataset, but requires the much larger part of the data set, so it was
provided for convenience.

Running `plot_track_sum()` in `skip_dataset.py` requires the .zip file in the `skip_dataset/data` to be extracted in the same folder.


# Dependencies

The dependencies can be installed by running `pip install -r requirements.txt`.

The following dependencies are used:
* spotipy~=2.16.1
* python-dotenv~=0.17.1
* numpy~=1.19.3
* scikit-learn~=0.24.0
* mongoengine~=0.22.1
* scipy~=1.6.0
* matplotlib~=3.3.3
* pandas~=1.2.3
* textblob~=0.15.3
* tqdm~=4.55.1
* tabulate~=0.8.9
