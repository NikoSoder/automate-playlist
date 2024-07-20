import express from "express";
import morgan from "morgan";
import { createServer } from "node:http";
import { Server } from "socket.io";
import { PlaylistSocketData } from "./types";
import { updatePlaylist } from "./update";

const FETCH_SONG_INTERVAL_TIME = 30000; // 30s
const previousSongs: string[] = []; // store song uris
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

  socket.on("playlist", (data: PlaylistSocketData) => {
    updatePlaylist(data, socket, previousSongs); // run this first because setInterval starts after 30s

    setInterval(
      updatePlaylist,
      FETCH_SONG_INTERVAL_TIME,
      data,
      socket,
      previousSongs,
    );
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
