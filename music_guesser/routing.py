from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/room/', consumers.RoomConsumer.as_asgi()),
    path('ws/room/<str:room_code>/', consumers.RoomConsumer.as_asgi()),
]
