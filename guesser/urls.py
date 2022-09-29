from django.urls import path
from guesser.views import login, get_rounds, get_room_data

urlpatterns = [
    path('login/', login, name='login'),
    path('rounds/', get_rounds, name='rounds'),
    path('guesser/', get_room_data, name='room'),
]
