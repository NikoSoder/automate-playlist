import sys
from typing import Callable, List, Optional
from functions import clear_terminal, handle_api_call


class Song:
    def __init__(self, uri: str, name: str):
        self.uri = uri
        self.name = name


class Playlist:
    def __init__(self, id: str, name: str, songs: List[Song]):
        self.id = id
        self.name = name
        self.songs = songs

    def has_song(self, song_uri: str) -> bool:
        return any(song.uri == song_uri for song in self.songs)


def user_select_playlist(spotify_api_call: Callable) -> Optional[Playlist]:
    FETCH_PLAYLISTS_LIMIT = 20
    clear_terminal()
    user_playlists: List[Playlist] = []
    playlists = handle_api_call(spotify_api_call, FETCH_PLAYLISTS_LIMIT)
    if not playlists:
        sys.exit("No playlists found")

    for idx, playlist in enumerate(playlists["items"]):
        name = playlist["name"]
        id = playlist["id"]
        user_playlists.append(Playlist(id, name, []))
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
