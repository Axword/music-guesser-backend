from spotify import Spotify
import webbrowser


class Player:

    def __init__(self, name: str) -> None:
        self.name = name
        self.points = 0

    def take_a_guess(self):
        return input('')

    def check_round(self, round):
        if round.winning_song == self.guess:
            self.points = + 1


possible_states = ('Open', 'Closed', 'In progress', 'Finished')


class Room:

    def __init__(self, player: Player) -> None:
        self.host = player
        self.code = 'xyz'
        self.preview_url = ''
        self.state = 'Open'
        self.players = [player]
        self.choices = {}
        self.rounds = []
        self.settings = {}

    def change_settings(self, settings):
        self.settings = settings

    def return_players_stats(self):
        return self.players

    def start_game(self):
        self.state = 'In progress'
        self.generate_rounds()
        self.start_a_round()

    def generate_rounds(self):
        # TODO tworzyć wiele klas naraz
        number_of_rounds = self.settings.get('number_of_rounds', 15)
        time = self.settings.get('time', 15)
        spotify = Spotify()
        for i in range(number_of_rounds):
            songs = spotify.select_song_to_guess()
            winning_song = spotify.select_winning_tracks(songs)
            self.rounds.append(Round(time, songs, winning_song))

    def return_number_of_rounds_passed(self):
        return f"{len(self.rounds)}/{self.settings.get('number_of_rounds', 0)}"

    def start_a_round(self):
        for round in self.rounds:
            choices = [song['name'] for song in round.songs]
            winning_song = round.winning_song
            print(f'choices: {choices}')
            webbrowser.open(winning_song['preview'])
            guess = self.host.take_a_guess()
            print("Won") if guess.lower(
            ) == winning_song['name'].lower() else print("Lost")

    def end_round(self):
        round = self.rounds[0]
        # delete el from list
        for player in self.player.values():
            player.check_round(round)

    def add_player(self, player):
        self.players[player.name] = player

    def reprJSON(self):
        return dict(id=self.identity, data=self.data)


class Round:
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
