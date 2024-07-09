import { useEffect, useState } from "react";
import { getCode } from "./getCode";
import SpotifyAuthLink from "./SpotifyLink";
import { getAccessToken, getCurrentPlaylists } from "./apiQueries";
import { TPLaylist } from "./types";
import { Playlists } from "./Playlist";

function App() {
  const code = getCode();
  return (
    <main className="container mx-auto p-2">
      {code ? <Content /> : <SpotifyAuthLink />}
    </main>
  );
}

function Content() {
  const [token, setToken] = useState<string | null>(null);
  const [userPlaylists, setUserPlaylist] = useState<TPLaylist[]>([]);

  useEffect(() => {
    // FIX: add clean up function. race conditions
    // https://react.dev/reference/react/useEffect
    async function fetchToken() {
      const accessTokenLocalStorage = localStorage.getItem("access_token");
      if (accessTokenLocalStorage) {
        setToken(accessTokenLocalStorage);
        const playlists = await getCurrentPlaylists(accessTokenLocalStorage);
        setUserPlaylist(playlists);
        return;
      }
      const token = await getAccessToken();

      if (token) {
        setToken(token);
      }
      history.pushState(null, "", "/");
    }
    fetchToken();
  }, []);
  return (
    <>
      <Playlists accessToken={token} userPlaylists={userPlaylists} />
    </>
  );
}

export default App;
