import { Result, Song, Image, Artist } from "./types";

export async function getCurrentlyPlayingTrack(
  accessToken: string,
): Promise<Result<Song, string>> {
  try {
    const response = await fetch(
      "https://api.spotify.com/v1/me/player/currently-playing",
      {
        headers: {
          Authorization: "Bearer " + accessToken,
        },
      },
    );

    if (!response.ok) {
      const error = await response.text();
      console.log(error);
      throw new Error("Error with currently playing track (throw)");
    }

    const data = await response.json();
    const song: Song = {
      uri: data.item.uri,
      images: data.item.album.images.map((image: Image) => ({
        url: image.url,
        height: image.height,
        width: image.width,
      })),
      trackName: data.item.name,
      artistNames: data.item.artists.map((artist: Artist) => artist.name),
    };

    return { success: true, value: song };
  } catch (e) {
    console.log(e);
    if (e instanceof Error) {
      console.log(e.message);
    }
    return {
      success: false,
      error: "Error in getCurrentlyPlayingTrack (catch)",
    };
  }
}

export async function addSongToPlaylist(
  accessToken: string,
  playlistId: string,
  songUri: string,
): Promise<Result<undefined, string>> {
  try {
    const response = await fetch(
      `https://api.spotify.com/v1/playlists/${playlistId}/tracks`,
      {
        method: "POST",
        headers: {
          Authorization: "Bearer " + accessToken,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          uris: [songUri],
        }),
      },
    );

    if (!response.ok) {
      const error = await response.text();
      console.log(error);
      throw new Error("Error with addSongToPlaylist (throw)");
    }

    const data = await response.json();
    console.log(data);

    return { success: true, value: undefined };
  } catch (e) {
    console.log(e);
    if (e instanceof Error) {
      console.log(e.message);
    }
    return {
      success: false,
      error: "Error in addSongToPlaylist (catch)",
    };
  }
}
