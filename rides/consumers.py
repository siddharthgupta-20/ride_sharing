# rides/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Ride
from channels.db import database_sync_to_async
from .serializers import RideSerializer

class RideConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.trip_id = self.scope['url_route']['kwargs']['trip_id']
        self.ride_group_name = f'ride_{self.trip_id}'

        # Join ride group
        await self.channel_layer.group_add(
            self.ride_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave ride group
        await self.channel_layer.group_discard(
            self.ride_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        new_location = text_data_json['current_location']
        ride_id = text_data_json['trip_id']

        # Update the ride's current location
        try:
            ride = await self.update_ride_location(ride_id, new_location)
            response = {
                'status': 'success',
                'trip_id': ride_id,
                'current_location': ride.current_location
            }
        except Ride.DoesNotExist:
            response = {
                'status': 'error',
                'message': 'Ride does not exist'
            }

        # Send updated location to WebSocket group
        await self.channel_layer.group_send(
            self.ride_group_name,
            {
                'type': 'ride_update',
                'message': response
            }
        )

    # Receive message from ride group
    async def ride_update(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def update_ride_location(self, trip_id, new_location):
        ride = Ride.objects.get(trip_id=trip_id)
        ride.current_location = new_location
        ride.save()
        return ride
