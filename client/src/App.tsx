import { useEffect, useState } from "react";
import { getCode } from "./getCode";
import SpotifyAuthLink from "./SpotifyLink";
import { getAccessToken, getCurrentPlaylists } from "./apiQueries";
import { TPLaylist } from "./types";
import { Playlists } from "./Playlist";
import OnListening from "./onListening";

function App() {
  const code = getCode();

  return (
    <main className="container mx-auto p-2">
      {code ? <Content /> : <SpotifyAuthLink />}
    </main>
  );
}

function Content() {
  const [userPlaylists, setUserPlaylist] = useState<TPLaylist[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [isListening, setIsListening] = useState(false);

  useEffect(() => {
    // TODO: this is kinda messy
    let ignore = false;

    async function fetchToken() {
      const accessTokenLocalStorage = localStorage.getItem("access_token");
      if (accessTokenLocalStorage && !ignore) {
        const playlists = await getCurrentPlaylists(accessTokenLocalStorage);
        if (!playlists.success) {
          setLoading(false);
          return;
        }
        setUserPlaylist(playlists.value);
        setLoading(false);
        return;
      }
      // FIX: this is giving errors sometimes after auth
      const token = await getAccessToken();

      if (token.success && !ignore) {
        const playlists = await getCurrentPlaylists(token.value);
        if (playlists.success) {
          setUserPlaylist(playlists.value);
        }
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
      <OnListening setIsListening={setIsListening} />
      {userPlaylists && !isListening ? (
        <Playlists userPlaylists={userPlaylists} />
      ) : null}
    </>
  );
}

export default App;
