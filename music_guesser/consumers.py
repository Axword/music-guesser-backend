import json
from channels.generic.websocket import AsyncWebsocketConsumer
from game import Player, Room
from redis_storage import RedisStorage

redis_storage = RedisStorage()

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        user_name = self.scope['query_string'].decode().split('=')[1]

        if not self.room_code:
            # Generate a new room code and create a room
            self.user_id = self.generate_player_id()
            player = Player(user_name, self.user_id)
            room = Room(player)
            self.room_code = room.code
            redis_storage.save_room(room)
        else:
            room_data = redis_storage.load_room(self.room_code)
            room = Room.from_dict(room_data)
            self.user_id = self.generate_player_id()
            player = Player(user_name, self.user_id)
            room.add_player(player)
            redis_storage.save_room(room)

        # Add the WebSocket to the group
        await self.channel_layer.group_add(self.room_code, self.channel_name)

        await self.accept()
        await self.send(text_data=json.dumps({
            'success': True,
            'message': f"You have joined room {self.room_code}",
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_code, self.channel_name)

    def generate_player_id(self):
        # Replace this with your own player ID generation logic
        return "some_random_player_id"
