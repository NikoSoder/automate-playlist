from os import system, name
import sys
import spotipy
from typing import Callable
from requests.exceptions import ReadTimeout


def handle_api_call(func: Callable, *args):
    try:
        return func(*args)
    except ReadTimeout as e:
        print("\a")  # NOTE: remove this later(bell sound for debug)
        print(f"ReadTimeout occurred: {e}")
        return func(*args)
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
