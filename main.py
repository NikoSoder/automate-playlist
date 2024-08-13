# https://spotipy.readthedocs.io/en/2.24.0/
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from os import name, getenv
import time
import sys
from border import print_border
from playlist_selection import user_select_playlist, Song
from functions import clear_terminal, handle_api_call

load_dotenv()
CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME = 60  # 60s
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
    )
)


# list of playlist to select
PLAYLIST_ACTIVE = user_select_playlist(sp.current_user_playlists)
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


# add playlist tracks to selected playlist
playlist_tracks_info = handle_api_call(sp.playlist_tracks, PLAYLIST_ACTIVE.id)
if playlist_tracks_info:
    playlist_tracks = playlist_tracks_info["items"]
    for track in playlist_tracks:
        uri = track["track"]["uri"]
        name = track["track"]["name"]
        playlist_song = Song(uri, name)
        PLAYLIST_ACTIVE.songs.append(playlist_song)


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
    if not PLAYLIST_ACTIVE.has_song(song_uri):
        handle_api_call(sp.playlist_add_items, PLAYLIST_ACTIVE.id, [song_uri])
        print(f"Adding song: {song_name} to the playlist: {PLAYLIST_ACTIVE.name}")
        PLAYLIST_ACTIVE.songs.append(Song(song_uri, song_name))

    animated_music_icon(CHECK_CURRENTLY_PLAYING_TRACK_WAIT_TIME)
