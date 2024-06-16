from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ride
from .serializers import RideSerializer

class CreateRideView(APIView):
    def post(self,request):
        serializer = RideSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RideView(APIView):
    def getRideInfo(ride_id):
        ride = Ride.objects.filter(trip_id = ride_id).first()
        print(ride_id)
        if ride is None:
            raise Exception("ride not found!")

        payload = {
            "ride_id":ride.trip_id,
            "driver_name":ride.driver_name,
            "driver_phone_number":ride.driver_phone_number,
            "end_location":ride.end_location,
            "current_location":ride.current_location
        }
        return payload
