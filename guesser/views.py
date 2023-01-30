from rest_framework.decorators import api_view
from rest_framework.response import Response
from spotify import SpotifyException
from game import Player, Room
# TODO import redis and use it for temp Rooms
import redis
import json
from django.conf import settings


redisClient = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
rooms = {}


def update_redis(room_code, room):
    redisClient.set(str(room_code), room.toJSON())


def delete_room_from_redis(room_code):
    redisClient.delete(room_code)


def get_room_from_redis(room_code):
    return redisClient.get(room_code)


def init_dict():
    for key in redisClient.keys():
        room = get_room_from_redis(key).decode('utf-8')
        key = key.decode('utf-8')
        rooms[key] = room


init_dict()


@api_view(['POST'])
def login(request):
    data = request.data
    name = data['username']
    room = data['gamecode']
    user_id = data['user_id']
    if not name:
        return Response({'error': 'Podaj swój nick'}, status=400)
    if data['join'] and not room:
        return Response({'error': 'Podaj kod pokoju'}, status=400)
    if not room:
        player = Player(name, user_id)
        room = Room(player)
        rooms[room.code] = room
    else:
        try:
            room = rooms[room]
        except Exception:
            return Response({'error': 'Pokój z takim kodem nie został znaleziony'}, status=404)
        player = Player(name, user_id)
        room.add_player(player)
    update_redis(room.code, room)
    data = room.__dict__
    data['code'] = room.code
    return Response(data, status=200)


@api_view(['GET'])
def get_rounds(request):
    data = request.data
    room = rooms[data['room']]
    return Response(room.rounds, status=200)


@api_view(['GET'])
def get_room_data(request):
    code = request.GET.get('code')[:-1]
    room = rooms[code]
    player_data = room.host
    data = room.__dict__
    data['host'] = player_data
    players_obj_list = []
    for player in room.players:
        players_obj_list.append(player)
    data['players'] = players_obj_list
    return Response(data, status=200)


@api_view(['POST'])
def start_game(request):
    data = request.data
    try:
        room = rooms[data['code']]
    except Exception:
        return Response({'error': 'Pokój z takim kodem nie został znaleziony'}, status=404)
    playlist = data['playlist_url']
    if not playlist:
        return Response({'error': 'Playlista jest wymagana'}, status=400)
    room.playlist_url = playlist
    room.number_of_rounds = int(data.get("number_of_rounds"))
    rooms[data['code']] = room
    try:
        room.start_game()
    except SpotifyException as error:
        return Response({'error': str(error)}, status=400)
    return Response({'choices': room.choices, 'preview_url': room.preview_url}, status=200)


@api_view(['POST'])
def start_round(request):
    room = rooms[request.data['code']]
    if not room.check_if_all_players_answered():
        return Response({'error': 'Nie wszyscy gracze odpowiedzieli'}, status=400)
    if room.round_now == room.number_of_rounds:
        return Response({'error': 'Koniec gry'}, status=400)
    room.start_a_round()
    return Response({'choices': room.choices, 'preview_url': room.preview_url}, status=200)


@api_view(['POST'])
def check_answer(request):
    data = request.data
    room = rooms[data['code']]
    checking_answer_user_id = data['user_id']
    answer = data['choice']
    is_won = room.end_round(answer, checking_answer_user_id)
    return Response({"is_won": is_won, "answer": answer}, status=200)

# class UserNotificationConsumer(AsyncWebsocketConsumer):  # pragma no cover
#     async def connect(self):
#         data = request.data
#         name = data['username']
#         if not name:
#             return Response({'error': 'name is required'}, status=400)
#         host = Player(name)
#         room = Room(host)
#         rooms[room.code] = room
#         data['code'] = room.code

#         user_id = self.scope['user'].pk
#         self.notification_group_name = f'user-notifications-{user_id}'
#         await self.channel_layer.group_add(self.notification_group_name, self.channel_name)
#         await self.accept()

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.notification_group_name, self.channel_name)

#     async def send_user_notification(self, event):
#         payload = event.copy()
#         payload['type'] = event.pop('msg_type', 'info')
#         await self.send(text_data=json.dumps(payload))
