import { useEffect, useState } from "react";
import { socket } from "./socket";
import { Song } from "./types";

function OnListening() {
  const [nowPlayingSong, setNowPlayingSong] = useState<Song>();
  useEffect(() => {
    socket.on("onSongPlay", (data) => {
      console.log(data.value);
      if (!data.success) {
        console.log(data);
        throw new Error("Error onSongPlay (socket.on)");
      }
      setNowPlayingSong(data.value);
      // TODO: add nowListening boolean to true
    });
  }, []);

  if (!nowPlayingSong) {
    return <p>No song playing</p>;
  }

  return (
    <div>
      <p>{nowPlayingSong.trackName}</p>
      <img src={nowPlayingSong.images[2].url} alt="Now playing song image" />
      <p>{nowPlayingSong.artistNames[0]}</p>
    </div>
  );
}
export default OnListening;
