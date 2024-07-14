type ResultSuccess<T> = { success: true; value: T };
type ResultError<E> = { success: false; error: E };
export type Result<T, E> = ResultSuccess<T> | ResultError<E>;

export interface PlaylistSocketData {
  playlistId: string;
  accessTokenLocalStorage: string;
}

export interface Song {
  uri: string;
  images: Image[];
  trackName: string;
  artistNames: string[];
}

export interface Image {
  url: string;
  height: number;
  width: number;
}

interface ExternalUrls {
  spotify: string;
}

interface Followers {
  href: string;
  total: number;
}

interface ArtistImage {
  url: string;
  height: number;
  width: number;
}

export interface Artist {
  external_urls: ExternalUrls;
  followers: Followers;
  genres: string[];
  href: string;
  id: string;
  images: ArtistImage[];
  name: string;
  popularity: number;
  type: string;
  uri: string;
}
