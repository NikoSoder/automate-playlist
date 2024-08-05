# https://spotipy.readthedocs.io/en/2.24.0/
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import system, name, getenv
import time
import sys
import argparse
from border import print_border

# get playlist id
parser = argparse.ArgumentParser(description="Spotify playlist id")
parser.add_argument("spotify_playlist_id", type=str, help="Playlist id")
args = parser.parse_args()
PLAYLIST_ID = args.spotify_playlist_id

load_dotenv()
CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME = 90  # 90s
previous_songs = []  # song uris
client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")
redirect_uri = getenv("REDIRECT_URI")
scope = getenv("SCOPE")

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

def animated_music_icon(duration):
    music_icon = "♫♫♫"
    width = 3
    direction = 1
    position = 0
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    start_time = time.time()

    while True:
        current_time = time.time()
        elapsed_time = current_time - start_time

        if elapsed_time >= duration:
            break

        line = [" "] * width
        line[position] = music_icon
        sys.stdout.write(HIDE_CURSOR)
        sys.stdout.write("\r" + "".join(line))
        sys.stdout.flush()

        time.sleep(1)

        position += direction
        if position == 0 or position == width - 1:
            direction *= -1

    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()


def clear_terminal():
    # for windows
    if name == "nt":
        system("cls")
        return

    # for mac, linux
    system("clear")


while True:
    clear_terminal()
    # get currently playing track
    song = sp.current_user_playing_track()
    if not song:
        sys.exit("No currently playing tracks")

    song_uri = song["item"]["uri"]
    song_name = song["item"]["name"]
    song_artists = song["item"]["artists"]
    artist_names = []
    title = "NOW LISTENING"

    for x in song_artists:
        artist_names.append(x["name"])
    merged_artists = ", ".join(artist_names)

    print_border(title, song_name, merged_artists)

    # add song to a selected playlist
    if song_uri not in previous_songs:
        print("adding song to playlist...")
        print(song_uri)
        # TODO: error handling
        snapshot_id = sp.playlist_add_items(PLAYLIST_ID, [song_uri])
        print(snapshot_id)
        previous_songs.append(song_uri)

    animated_music_icon(CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME)
