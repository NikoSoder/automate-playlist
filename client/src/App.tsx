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
  const [userPlaylists, setUserPlaylist] = useState<TPLaylist[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let ignore = false;

    async function fetchToken() {
      const accessTokenLocalStorage = localStorage.getItem("access_token");
      if (accessTokenLocalStorage && !ignore) {
        const playlists = await getCurrentPlaylists(accessTokenLocalStorage);
        setUserPlaylist(playlists);
        setLoading(false);
        return;
      }
      const token = await getAccessToken();

      if (token && !ignore) {
        const playlists = await getCurrentPlaylists(token);
        setUserPlaylist(playlists);
        setLoading(false);
      }

      setLoading(false);
      history.pushState(null, "", "/");
    }
    fetchToken();

    return () => {
      ignore = true;
    };
  }, []);

  if (loading) {
    return <p>loading....</p>;
  }

  return (
    <>
      <Playlists userPlaylists={userPlaylists} />
    </>
  );
}

export default App;
