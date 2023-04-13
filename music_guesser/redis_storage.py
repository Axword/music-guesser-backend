import redis
from game import Player, Room

class RedisStorage:
    def __init__(self):
        self.redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

    def save_player(self, player):
        player_data = player.__dict__
        self.redis_client.hmset(f"player:{player.user_id}", player_data)

    def load_player(self, player_id):
        player_data = self.redis_client.hgetall(f"player:{player_id}")
        return Player.from_dict(player_data)

    def save_room(self, room):
        room_data = room.__dict__
        self.redis_client.hmset(f"room:{room.code}", room_data)

    def load_room(self, room_code):
        room_data = self.redis_client.hgetall(f"room:{room_code}")
        return Room.from_dict(room_data)
