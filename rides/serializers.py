from rest_framework import serializers
from .models import Ride

class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['trip_id','cab_number','driver_name','driver_phone_number',"current_location","end_location",'traveler_id']

    def create(self,validated_data):
        
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance