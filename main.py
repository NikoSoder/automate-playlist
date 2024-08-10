# https://spotipy.readthedocs.io/en/2.24.0/
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import system, name, getenv
import time
import sys
from border import print_border
from requests.exceptions import ReadTimeout
from typing import Callable, List, Optional

load_dotenv()
CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME = 60  # 60s
previous_songs = []  # song uris TODO: move this to Playlist class
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
        requests_timeout=10,
        # retries=10
    )
)


def handle_api_call(func: Callable, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except ReadTimeout as e:
        print("\a")  # NOTE: remove this later(bell sound for debug)
        print(f"ReadTimeout occurred: {e}")
        return func(*args, **kwargs)
    except spotipy.SpotifyException as e:
        print(f"SpotifyException: {e}")
        sys.exit()
    except ConnectionError as e:
        print(f"ConnectionError: {e}")
        sys.exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit()


def clear_terminal():
    # for windows
    if name == "nt":
        system("cls")
        return

    # for mac, linux
    system("clear")


class Playlist:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        """
        save playlist songs here aswell?
        now playlist songs are in 'previous_songs' 
        """


def user_select_playlist() -> Optional[Playlist]:
    clear_terminal()
    user_playlists: List[Playlist] = []
    playlists = handle_api_call(sp.current_user_playlists, 20)
    if not playlists:
        sys.exit("No playlists found")

    for idx, playlist in enumerate(playlists["items"]):
        name = playlist["name"]
        id = playlist["id"]
        user_playlists.append(Playlist(id, name))
        print(f"({idx + 1}), {name}")

    print()

    try:
        user_selected_playlist_idx = int(
            input("Select a playlist to save the currently playing songs: ")
        )

        if user_selected_playlist_idx < 1 or user_selected_playlist_idx > len(
            user_playlists
        ):
            print("Not a valid index")
            return None

        selected_playlist = user_playlists[user_selected_playlist_idx - 1]
        return selected_playlist
    except ValueError as e:
        print(f"Not a valid number: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    return None


PLAYLIST_ACTIVE = user_select_playlist()
if not PLAYLIST_ACTIVE:
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


playlist_tracks_info = handle_api_call(sp.playlist_tracks, PLAYLIST_ACTIVE.id)
if playlist_tracks_info:
    playlist_tracks = playlist_tracks_info["items"]
    for track in playlist_tracks:
        uri = track["track"]["uri"]
        previous_songs.append(uri)


while True:
    clear_terminal()
    # get currently playing track
    song = handle_api_call(sp.current_user_playing_track)
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
        handle_api_call(sp.playlist_add_items, PLAYLIST_ACTIVE.id, [song_uri])
        print(f"Adding song: {song_name} to the playlist: {PLAYLIST_ACTIVE.name}")
        previous_songs.append(song_uri)

    animated_music_icon(CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME)
