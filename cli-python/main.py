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
playlist_id = args.spotify_playlist_id

load_dotenv()
PLAYLIST_ID = playlist_id
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

# get playlist tracks to prevent dublicates
# FIX: errors if invalid PLAYLIST_ID
playlist_tracks_info = sp.playlist_tracks(PLAYLIST_ID)
if playlist_tracks_info:
    playlist_tracks = playlist_tracks_info["items"]
    for track in playlist_tracks:
        uri = track["track"]["uri"]
        previous_songs.append(uri)

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

    print(artist_names)
    # print(song_uri)
    # print(song_name)
    # print(song_artists)

    # add song to a selected playlist
    if song_uri not in previous_songs:
        print("adding song to playlist...")
        print(song_uri)
        # TODO: error handling
        snapshot_id = sp.playlist_add_items(PLAYLIST_ID, [song_uri])
        print(snapshot_id)
        previous_songs.append(song_uri)

    time.sleep(CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME)
