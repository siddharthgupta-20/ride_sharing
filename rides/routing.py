# rides/routing.py
from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/rides/trip123/', consumers.RideConsumer.as_asgi()),
]
