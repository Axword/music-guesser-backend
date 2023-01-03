import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'


class SpotifyException(Exception):
    pass


class Spotify:
    def __init__(self, playlist_url, number_of_rounds=10, number_of_choices=4) -> None:
        spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials())
        try:
            results = spotify.playlist(playlist_url.split('/')[-1])
        except Exception:
            raise SpotifyException("Playlista nie znaleziona")
        results = results['tracks']
        self.tracklist = []
        if results['total'] > 100:
            while results['next']:
                self.add_songs_to_tracklist(results['items'])
                results = spotify.next(results)
        else:
            self.add_songs_to_tracklist(results['items'])
        if len(self.tracklist) < number_of_rounds:
            raise SpotifyException("""Playlista jest za krótka. Sprawdź, które
             piosenki mają opcję preview, lub zmniejsz liczbę rund""")

    def add_songs_to_tracklist(self, items):
        for track_id, track in enumerate(items):
            if track['is_local']:
                continue
            track = track['track']
            url = track['preview_url']
            if not url:
                continue
            self.tracklist.append({
                'id': track_id,
                'name': track['name'],
                'preview': url,
            })

    def select_song_to_guess(self):
        tracks = random.sample(self.tracklist, k=4)
        return tracks

    def select_winning_tracks(self, tracklist):
        track = random.choice(tracklist)
        self.tracklist.remove(track)
        return track

    def game(tracklist, name):
        """
        Game for gamemode 1 - find a song by a title
        W tym wypadku całość wyświetla się jak stolik do pokera
        """

    # def get_playlist_tracks(username, playlist_id):
    #     results = sp.user_playlist_tracks(username, playlist_id)
    #     tracks = results['items']
    #     while results['next']:
    #         results = sp.next(results)
    #         tracks.extend(results['items'])
    #     return tracks

    def get_plylist_end(playlist_str):
        playlist_str.split()

    def generate_room_id():
        pass
