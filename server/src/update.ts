import { Socket } from "socket.io";
import { PlaylistSocketData } from "./types";
import { getCurrentlyPlayingTrack, addSongToPlaylist } from "./api";

export async function updatePlaylist(
  data: PlaylistSocketData,
  socket: Socket,
  prevSongs: string[],
) {
  const song = await getCurrentlyPlayingTrack(data.accessTokenLocalStorage);
  if (!song.success) {
    console.log(song.error);
    // TODO: do something here if error
    return;
  }

  if (prevSongs.includes(song.value.uri)) {
    console.log("Song is already in the playlist");
    return;
  }
  const songToPlaylist = await addSongToPlaylist(
    data.accessTokenLocalStorage,
    data.playlistId,
    song.value.uri,
  );

  if (!songToPlaylist.success) {
    console.log(songToPlaylist.error);
    // TODO: do something here if error
    return;
  }
  prevSongs.push(song.value.uri);
  console.log(`--${song.value.trackName}-- added to the playlist`);
  socket.emit("onSongPlay", song);
}
