## Description

Allows you to save the currently playing songs to a selected playlist. Useful when you're listening to music with friends and want to quickly save the songs.

## Requirements

- A spotify developer account for API credentials
- Python https://www.python.org/downloads/
- pip https://pypi.org/project/pip/
- spotipy
  - https://spotipy.readthedocs.io/en/2.24.0/
  - https://pypi.org/project/spotipy/
- python-dotenv
  - https://pypi.org/project/python-dotenv/

## Usage

```
python main.py

(1), Playlist 1
(2), Playlist 2
(3), Playlist 3
(4), Playlist 4
(5), Playlist 5

Select a playlist to save the currently playing songs: 3

+---NOW LISTENING---+
|                   |
|   <Song>          |
|   <Artist>        |
|                   |
+-------------------+

Adding song: <Song> to the playlist: <Playlist 3>
```

> [!TIP]
> You can leave the program running and it will check currently playing song every minute

## Troubleshooting

- Ensure that you have the correct spotify API credentials in your .env file.
- Double-check that your redirect URI matches what you've set in the spotify developer dashboard.
- If authentication fails, clear the cache file `.cache` and try logging in again.
