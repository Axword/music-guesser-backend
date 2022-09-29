import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import random
lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'


class Spotify:
    def __init__(self):
        spotify = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials())
        results = spotify.playlist(
            '4smVZcKHknjHYbLKN4F3oL?si=4f5d35f7b1a74904')
        results = results['tracks']
        self.tracklist = []
        while results['next']:
            for track_id, track in enumerate(results['items']):
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
            results = spotify.next(results)
        print(len(self.tracklist))

    def select_song_to_guess(self):
        tracks = random.choices(self.tracklist, k=4)
        self.tracklist = [
            track for track in self.tracklist if track not in tracks]
        return tracks

    def select_winning_tracks(self, tracklist):
        # x 4 z czego pierwszy z listy usuwany i poprawny
        track = random.choice(tracklist)
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


possible_room_status = ['settings', 'starting', 'started', 'ended']


class Room:
    players = []
    status = None

    # def __init__(self) -> None:
    #     room_id = uuid3()
    #     room_qr = ''

    def connect_player(self, user):
        self.players.append(user)
        return self.players

    def start_game(self):
        self.status = 'starting'
        return self.status

    def play(self):
        """
        Zrobić tak -> user ma do wyboru n możliwości losowo wybranych i zwracanych co rundę.
        Prawidłowa opdowiedź jest wyrzucana z puli możliwych odpowiezdzi. Liczymy czas odpowiedzi i czy jest poprawna
        Sumujemy po każdej rundzie pokazując wyniki innych graczy i topliste
        """

    def function():
        items = []
        for item in items:
            print(item)
