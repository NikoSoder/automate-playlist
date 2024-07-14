const generateRandomString = (length: number) => {
  const possible =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  const values = crypto.getRandomValues(new Uint8Array(length));
  return values.reduce((acc, x) => acc + possible[x % possible.length], "");
};

export const PUBLIC_CLIENT_ID = import.meta.env.VITE_CLIENT_ID;
const SCOPE =
  "user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-read-currently-playing";
export const REDIRECT_URI = "http://localhost:5173/callback";
const state = generateRandomString(16);
export const AUTH_URL = `https://accounts.spotify.com/authorize?client_id=${PUBLIC_CLIENT_ID}&response_type=code&redirect_uri=${REDIRECT_URI}&scope=${SCOPE}&state=${state}&show_dialog=true`;
