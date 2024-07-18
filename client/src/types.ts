export interface TPLaylist {
  name: string;
  id: string;
  uri: string;
  description: string;
  owner: string;
  type: string;
  image: string | null;
}

type ResultSuccess<T> = { success: true; value: T };
type ResultError<E> = { success: false; error: E };
export type Result<T, E> = ResultSuccess<T> | ResultError<E>;

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
