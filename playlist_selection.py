import sys
from typing import Callable, List, Optional


class Playlist:
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        """
        save playlist songs here aswell?
        now playlist songs are in 'previous_songs' 
        """


def user_select_playlist(
    api_call: Callable, spotify_api_call: Callable, clear_terminal: Callable
) -> Optional[Playlist]:
    FETCH_PLAYLISTS_LIMIT = 20
    clear_terminal()
    user_playlists: List[Playlist] = []
    playlists = api_call(spotify_api_call, FETCH_PLAYLISTS_LIMIT)
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
