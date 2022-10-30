from django.urls import path, re_path

from guesser.views import login, get_rounds, get_room_data, start_game, check_answer, start_round

urlpatterns = [
    path('login/', login, name='login'),
    path('rounds/', get_rounds, name='rounds'),
    path('guesser/', get_room_data, name='room'),
    path('start-game/', start_game, name='start-game'),
    path('check-answer/', check_answer, name='check-answer'),
    path('start-new-round/', start_round, name='start-round'),
]


# websocket_urlpatterns = [
#     re_path(r'ws/guesser/$', UserNotificationConsumer.as_asgi()),
# ]
