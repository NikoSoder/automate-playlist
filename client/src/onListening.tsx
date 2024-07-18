import { Dispatch, SetStateAction, useEffect, useState } from "react";
import { socket } from "./socket";
import { Song } from "./types";

type OnListeningProps = {
  setIsListening: Dispatch<SetStateAction<boolean>>;
};

function OnListening({ setIsListening }: OnListeningProps) {
  const [nowPlayingSong, setNowPlayingSong] = useState<Song>();
  useEffect(() => {
    socket.on("onSongPlay", (data) => {
      console.log(data.value);
      if (!data.success) {
        console.log(data);
        throw new Error("Error onSongPlay (socket.on)");
      }
      setNowPlayingSong(data.value);
      setIsListening(true);
    });
  }, []);

  if (!nowPlayingSong) {
    return <p>No song playing</p>;
  }

  return (
    <div className="max-w-sm bg-gradient-to-l from-stone-950 to-stone-900 p-3 flex gap-4 rounded-md">
      <img
        className="rounded-md"
        src={nowPlayingSong.images[2].url}
        alt="Now playing song image"
      />
      <div className="grow flex justify-between">
        <div>
          <p className="text-white">{nowPlayingSong.trackName}</p>
          {/*TODO: loop through all artists*/}
          <p className="text-stone-400">{nowPlayingSong.artistNames[0]}</p>
        </div>
        <span className="relative flex h-3 w-3">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-600 opacity-75"></span>
          <span className="relative inline-flex rounded-full h-3 w-3 bg-green-500"></span>
        </span>
      </div>
    </div>
  );
}
export default OnListening;
