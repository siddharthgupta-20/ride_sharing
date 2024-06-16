from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from rides.views import RideView
from twilio.rest import Client
# import keys
import json

# Create your views here.
class RegisterView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
class LoginView(APIView):
    def post(self,request):
        email = request.data['email']
        password = request.data['password']
        user = User.objects.filter(email = email).first()

        if user is None:
            raise AuthenticationFailed('User not Found!')
        if not user.check_password(password):
            raise AuthenticationFailed('password Incorrect')
        
        # if the user is a traveler
        if user.is_traveler =="true":
            ride_id = user.ride_id
            ride_details = RideView.getRideInfo(ride_id)
            
            
            req_companion = User.objects.filter(ride_id = None).filter(traveler_id = None).filter(end_location = ride_details['end_location']).first()
            
            if req_companion != None:
                User.objects.filter(id=req_companion.id).update(traveler_id = str(user.id))
            else:
                print("no companions nearby!!")
            # print(type(req_companion))
            return Response(ride_details)

        if user.is_traveler_companion=="true":
            #get the traveler information and then get the ride information
            if user.traveler_id != None:
                traveler_id = user.traveler_id
                traveler = User.objects.filter(id = traveler_id).first()
                print(type(traveler))
                ride_id = traveler.ride_id
                print(ride_id)
                ride_details = RideView.getRideInfo(ride_id)
                print(ride_details)
            #     return Response({
            #     'message':'success'
            # })
                account_sid = 'twilio_sid'
                auth_token = 'twilio_token'
                twilio_number = '+15417166657'
                target_number = user.phone_number
                client = Client(account_sid,auth_token)
                message = client.messages.create(body = str(ride_details),
                                                from_ = twilio_number,
                                                to = target_number)
                print(message.body)
                return Response(ride_details)
            else:
                raise Exception("no traveler available")

        # elif user.is_admin:
        #     pass
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload,'secret', algorithm='HS256')
        decode_token = jwt.decode(token,'secret',algorithms=['HS256'])

        response = Response()
        response.set_cookie(key = 'jwt',value = token , httponly=True)
        response.data = {
            'jwt':token
        }
        
        return response
    
class UserView(APIView):
    def get(self,request):
        token = request.COOKIES.get("jwt")

        if not token:
            raise AuthenticationFailed("unauthenticated")
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("unauthenticated(ride ended)")
        
        user = User.objects.filter(id =payload['id']).first()
        serializer = UserSerializer(user)


        return Response(serializer.data)
    
class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message':'success'
        }
        return response