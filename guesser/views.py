from rest_framework.decorators import api_view
from game import Player, Room

@api_view(['POST'])
def login(request):
    data = request.data
    name = data['name']
    host = Player(name)
    Room(host)