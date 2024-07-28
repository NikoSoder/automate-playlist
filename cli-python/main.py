# https://spotipy.readthedocs.io/en/2.24.0/
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
import sys
import argparse

# get playlist id
parser = argparse.ArgumentParser(description="Spotify playlist id")
parser.add_argument("spotify_playlist_id", type=str, help="Playlist id")
args = parser.parse_args()
PLAYLIST_ID = args.spotify_playlist_id

load_dotenv()
CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME = 90  # 90s
previous_songs = []  # song uris
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = os.getenv("REDIRECT_URI")
scope = os.getenv("SCOPE")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
    )
)

try:
    # get playlist tracks to prevent dublicates
    playlist_tracks_info = sp.playlist_tracks(PLAYLIST_ID)
    if playlist_tracks_info:
        playlist_tracks = playlist_tracks_info["items"]
        for track in playlist_tracks:
            uri = track["track"]["uri"]
            previous_songs.append(uri)

except spotipy.SpotifyException as e:
    print(f"An error occurred: {e}")
    print(f"Exception type: {e.__class__.__name__}")
    print(f"Exception args: {e.args}")
    sys.exit()
except Exception as e:
    print(f"An error occurred: {e}")
    print(f"Exception type: {e.__class__.__name__}")
    print(f"Exception args: {e.args}")
    sys.exit()


def print_now_listening(name, artists):
    name_length = len(name)
    artists_length = len(", ".join(artists))
    artists = ", ".join(artists)
    cols = max(name_length, artists_length) + 5
    # borders around song info
    print()
    print("+" + "-" * (cols) + "+")
    print(f"| {name}{' ' * (cols - name_length - 2)} |")
    print(f"| {artists}{' ' * (cols - artists_length - 2)} |")
    print("+" + "-" * (cols) + "+")
    print()


while True:
    # get currently playing track
    song = sp.current_user_playing_track()
    if not song:
        sys.exit("No currently playing tracks")

    song_uri = song["item"]["uri"]
    song_name = song["item"]["name"]
    song_artists = song["item"]["artists"]
    artist_names = []

    for x in song_artists:
        artist_names.append(x["name"])

    print_now_listening(song_name, artist_names)

    # add song to a selected playlist
    if song_uri not in previous_songs:
        print("adding song to playlist...")
        print(song_uri)
        # TODO: error handling
        snapshot_id = sp.playlist_add_items(PLAYLIST_ID, [song_uri])
        print(snapshot_id)
        previous_songs.append(song_uri)

    time.sleep(CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME)
