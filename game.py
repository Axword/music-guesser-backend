from spotify import Spotify
import random
import string
import json
possible_states = ('Open', 'Closed', 'In progress', 'Finished')


class JsonObject:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Player(JsonObject):

    def __init__(self, name: str, user_id) -> None:
        self.name = name
        self.points = 0
        self.user_id = user_id
        self.state = 'playing'


class Room(JsonObject):

    def __init__(self, player: Player) -> None:
        self.host = player.__dict__
        self.code = self.get_random_string()
        self.preview_url = ''
        self.state = 'Open'
        self.players = [player.__dict__]
        self.choices = []
        self.rounds = []
        self.number_of_rounds = 5
        self.playlist_url = ''
        self.round_now = 0
        self.time = 10

    @staticmethod
    def get_random_string():
        return ''.join(random.choice(string.ascii_letters) for i in range(9))

    def start_game(self):
        self.state = 'In progress'
        self.generate_rounds()
        self.reset_points()
        self.start_a_round()

    def reset_points(self):
        for player in self.players:
            player['points'] = 0

    def check_if_all_players_answered(self):
        for player in self.players:
            if player['state'] == 'playing':
                return False
        return True

    def generate_rounds(self):
        number_of_rounds = int(self.number_of_rounds)
        time = self.time
        spotify = Spotify(self.playlist_url, number_of_rounds)
        for i in range(number_of_rounds):
            songs = spotify.select_song_to_guess()
            winning_song = spotify.select_winning_tracks(songs)
            self.rounds.append(Round(time, songs, winning_song))

    def return_number_of_rounds_passed(self):
        return f"{len(self.rounds)}/{self.number_of_rounds}"

    def start_a_round(self):
        round = self.rounds[self.round_now]
        self.choices = [song['name'] for song in round.songs]
        self.preview_url = round.winning_song['preview']

    def end_round(self, answer, checking_user_id):
        round = self.rounds[self.round_now]
        won = False
        for player in self.players:
            if player['user_id'] == checking_user_id:
                if round.winning_song['name'] == answer:
                    player['points'] += 1
                    won = True
                player['state'] = 'waiting'
        self.round_now += 1
        return won

    def add_player(self, player):
        self.players.append(player.__dict__)

    def reprJSON(self):
        return dict(id=self.identity, data=self.data)


class Round(JsonObject):
    def __init__(self, time: int, songs, winning_song) -> None:
        self.songs = songs
        self.winning_song = winning_song
        self.time = time


class Page:
    rooms = {}

    def create_game(self, request):
        room = Room(request.user)
        self.rooms[room.code] = room
        return room

    def join_game(self, request):
        try:
            room = self.rooms[request.code]
        except Exception:
            return "Room not Found"
        room.players[request.user.name] = request.user
        return room


if __name__ == '__main__':
    player = Player("Michał")
    Room(player).start_game()
