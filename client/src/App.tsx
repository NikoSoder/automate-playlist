import { useEffect, useState } from "react";
import { getCode } from "./getCode";
import SpotifyAuthLink from "./SpotifyLink";
import { REDIRECT_URI } from "./info";

function App() {
  const code = getCode();
  return (
    <main className="container mx-auto">
      {code ? <Content /> : <SpotifyAuthLink />}
    </main>
  );
}

function Content() {
  const [token, setToken] = useState("");
  useEffect(() => {
    async function fetchToken() {
      const accessTokenLocalStorage = localStorage.getItem("access_token");
      if (accessTokenLocalStorage) {
        setToken(accessTokenLocalStorage);
        return;
      }
      const token = await getToken();
      if (token !== undefined) {
        setToken(token);
      }
      window.location.href = "/";
    }
    fetchToken();
  }, []);
  return <p>{token}</p>;
}

async function getToken() {
  let code = localStorage.getItem("code");

  const response = await fetch("https://accounts.spotify.com/api/token", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization:
        "Basic " +
        btoa(
          import.meta.env.VITE_CLIENT_ID + ":" + import.meta.env.VITE_SECRET_ID,
        ),
    },
    body: new URLSearchParams({
      code: code,
      redirect_uri: REDIRECT_URI,
      grant_type: "authorization_code",
    }),
  });

  const data = await response.json();
  console.log(data);
  localStorage.setItem("access_token", data.access_token);
  localStorage.setItem("refresh_token", data.refresh_token);

  return data.access_token;
}

export default App;
