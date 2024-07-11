import { TPLaylist } from "./types";
import { useState } from "react";

export function Playlists({ userPlaylists }: { userPlaylists: TPLaylist[] }) {
  const accessTokenLocalStorage = localStorage.getItem("access_token");
  const [query, setQuery] = useState("");

  const filteredPlaylists = userPlaylists.filter((playlist) => {
    if (query === "") {
      return playlist;
    }
    return playlist.name.toLowerCase().includes(query);
  });

  return (
    <>
      {accessTokenLocalStorage ? (
        <p className="text-wrap">{accessTokenLocalStorage}</p>
      ) : (
        <p>No accesstoken</p>
      )}
      <div className="max-w-sm">
        <input
          type="text"
          placeholder="Search"
          className="w-full bg-stone-900 rounded px-6 py-2 shadow-md placeholder:text-gray-300"
          value={query}
          onChange={(e) => setQuery(e.target.value.toLowerCase())}
        />
      </div>
      <ul className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {filteredPlaylists.map((playlist) => (
          <PlaylistItem key={playlist.id} playlist={playlist} />
        ))}
      </ul>
    </>
  );
}

export function PlaylistItem({ playlist }: { playlist: TPLaylist }) {
  return (
    <li className="flex p-3 rounded-md cursor-pointer hover:bg-stone-900">
      {playlist.image && (
        <div className="me-4">
          <img
            className="rounded-md w-full max-w-[60px] h-auto"
            src={playlist.image}
            alt="playlist image"
          />
        </div>
      )}
      <div>
        <p className="text-white font-bold">{playlist.name}</p>
        <span className="text-stone-400">{playlist.type}</span>
        <span className="text-stone-400">&#x2B1D;</span>
        <span className="text-stone-400">{playlist.owner}</span>
      </div>
    </li>
  );
}
