from django.urls import path
from guesser.views import login

urlpatterns = [
    path('login', login, name='login'),
]
