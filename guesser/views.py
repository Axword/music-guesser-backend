from rest_framework.decorators import api_view
from rest_framework.response import Response
from game import Player, Room
# TODO import redis and use it for temp Rooms


rooms = {}


@api_view(['POST'])
def login(request):
    data = request.data
    name = data['username']
    if not name:
        return Response({'error': 'name is required'}, status=400)
    host = Player(name)
    room = Room(host)
    rooms[room.code] = room
    data['code'] = room.code
    return Response(data, status=200)


@api_view(['POST'], detailed=True)
def login_by_code(request):
    data = request.data
    name = data['username']
    room = data['room']
    if not name:
        return Response({'error': 'name is required'}, status=400)
    player = Player(name)
    try:
        room = rooms[room]
    except Exception:
        return Response({'error': 'Room does not exist'}, status=400)
    room.add_player(player)
    player_data = room.host.__dict__
    data = room.__dict__
    data['host'] = player_data
    return Response(data, status=200)


@api_view(['GET'])
def get_rounds(request):
    data = request.data
    room = rooms[data['room']]
    return Response(room.rounds, status=200)


@api_view(['GET'])
def get_room_data(request):
    data = request.data
    room = rooms[data['code']]
    player_data = room.host.__dict__
    data = room.__dict__
    data['host'] = player_data
    players_obj_list = []
    for player in room.players:
        players_obj_list.append(player.__dict__)
    data['players'] = players_obj_list
    return Response(data, status=200)
