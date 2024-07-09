import { REDIRECT_URI } from "./spotifyConfig";
import { TPLaylist } from "./types";

export async function getRefreshToken() {
  const url = "https://accounts.spotify.com/api/token";
  try {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
      throw new Error("Could not find refreshtoken in localstorage");
    }
    const payload = {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        grant_type: "refresh_token",
        refresh_token: refreshToken,
        client_id: import.meta.env.VITE_CLIENT_ID,
      }),
    };
    const body = await fetch(url, payload);
    if (!body.ok) {
      throw new Error("Error with refresh token");
    }
    const response = await body.json();

    localStorage.setItem("access_token", response.accessToken);
    localStorage.setItem("refresh_token", response.refreshToken);
  } catch (e) {
    console.log(e);
  }
}

export async function getAccessToken() {
  try {
    let code = localStorage.getItem("code");
    if (!code) {
      throw new Error("No code in localstorage");
    }

    const response = await fetch("https://accounts.spotify.com/api/token", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        Authorization:
          "Basic " +
          btoa(
            import.meta.env.VITE_CLIENT_ID +
              ":" +
              import.meta.env.VITE_SECRET_ID,
          ),
      },
      body: new URLSearchParams({
        code: code,
        redirect_uri: REDIRECT_URI,
        grant_type: "authorization_code",
      }),
    });

    if (!response.ok) {
      throw new Error("Error with accesstoken request");
    }

    const data = await response.json();
    console.log(data);
    localStorage.setItem("access_token", data.access_token);
    localStorage.setItem("refresh_token", data.refresh_token);

    return data.access_token;
  } catch (e) {
    console.log(e);
    return null;
  }
}

export async function getCurrentPlaylists(accessToken: string) {
  try {
    const response = await fetch("https://api.spotify.com/v1/me/playlists", {
      headers: {
        Authorization: "Bearer " + accessToken,
      },
    });

    if (!response.ok) {
      throw new Error("Error with get playlists request");
    }

    const data = await response.json();
    // console.log(data.items);
    const cleanData: TPLaylist[] = data.items.map((playlist) => ({
      name: playlist.name,
      id: playlist.id,
      uri: playlist.uri,
      description: playlist.description,
    }));
    console.log(cleanData);
    return cleanData;
  } catch (e) {
    console.log(e);
    return [];
  }
}
