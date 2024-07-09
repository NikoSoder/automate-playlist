import { TPLaylist } from "./types";

export function Playlists({
  accessToken,
  userPlaylists,
}: {
  accessToken: string | null;
  userPlaylists: TPLaylist[];
}) {
  return (
    <>
      {accessToken ? <p>{accessToken}</p> : <p>No accesstoken</p>}
      {userPlaylists.map((playlist) => (
        <PlaylistItem key={playlist.id} playlist={playlist} />
      ))}
    </>
  );
}

export function PlaylistItem({ playlist }: { playlist: TPLaylist }) {
  return (
    <>
      <p>{playlist.name}</p>
    </>
  );
}
