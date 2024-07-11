import { TPLaylist } from "./types";

export function Playlists({ userPlaylists }: { userPlaylists: TPLaylist[] }) {
  const accessTokenLocalStorage = localStorage.getItem("access_token");
  return (
    <>
      {accessTokenLocalStorage ? (
        <p className="text-wrap">{accessTokenLocalStorage}</p>
      ) : (
        <p>No accesstoken</p>
      )}
      <ul className="grid sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {userPlaylists.map((playlist) => (
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
        <p className="text-white">{playlist.name}</p>
        <span className="text-stone-400">{playlist.type}</span>
        <span className="text-stone-400">&#x2B1D;</span>
        <span className="text-stone-400">{playlist.owner}</span>
      </div>
    </li>
  );
}
