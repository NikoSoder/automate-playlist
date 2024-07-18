import express from "express";
import morgan from "morgan";
import { createServer } from "node:http";
import { Server } from "socket.io";
import { PlaylistSocketData } from "./types";
import { getCurrentlyPlayingTrack, addSongToPlaylist } from "./api";

const port = 6969;
const app = express();
const server = createServer(app);
const io = new Server({
  cors: {
    origin: "http://localhost:5173",
  },
});

app.use(morgan("tiny"));

app.get("/token", (req, res) => {
  res.send("token todo");
});

io.listen(4000);
io.on("connection", (socket) => {
  console.log("User connected");

  socket.on("playlist", async (data: PlaylistSocketData) => {
    // TODO: add interval to check currently playing track
    const song = await getCurrentlyPlayingTrack(data.accessTokenLocalStorage);
    if (!song.success) {
      console.log(song.error);
      // TODO: do something here if error
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
    socket.emit("onSongPlay", song);
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
