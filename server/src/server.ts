import express from "express";
import morgan from "morgan";
import { createServer } from "node:http";
import { Server } from "socket.io";

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

  socket.on("playlist", (playlistId) => {
    console.log(playlistId);
  });
});

server.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
