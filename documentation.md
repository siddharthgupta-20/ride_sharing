## Ride Sharing platform

tech stach : Django, Python, JWT, PostgreSQL, postman
requirments at the end

database architecture:

Rides.ride : table
attributes - 
    trip_id: (string) store the unique id of each trip
    driver_name: (string) store the name of cab driver
    driver_phone_number: (string) phone number of cab driver
    current_location: (string) the actual location of the cab
    end_location: (string) the final destination of the trip
    traveler: (string) the id of the traveler that booked the ride(foreign Key)(unique)

Users.user: Table
attributes - 
    name : (string) name of the user
    email: (string) email id of the user(unique)
    password:(string) for authentication
    is_traveler: (bool) true if the user is a traveler
    is_admin: (bool) true if the user is an admin
    is_traveler_companion: (bool) true if the user is a traveler companion
    ride_id:(string) if is_traveler == true we will have a non null value of the trip_id from Rides.ride
    traveler_id: (string) if is_traveler_companion == True we will ahve a non null value of the user_id he is sharing his cab with.

Feedback.feedback: Table
attributes:
    ride:(string) used as foreignkey for the Ride.ride 
    user:(string) used as foreignkey for the User.user
    rating: (interger) 
    comment:(text) optional
    timestamp:(time) the tiem when we recieved the feedback

### Assumption: 
I assumed that this ride sharing platform is a pasrt of the app from where the traveler booked the ride. Hence the Rides.ride and Users.user for travelers will be populated automatically.

### Authentication
using JWT authentication with encoing "HS256"

design-
register: to register a new user
login: for login of existing user
logout: to deactivate an existing user

setting up a users/serializer.py to create any new entry in the database or to modify it.
we do not send the password to the server rather whenever we login we encode a payload like
payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }
and send a cookie inorder to tell the server if a user is active or not.

for user view we check if the corresponding encoded(payload) is present. If yes,  we return the details of the user.

admin: has the view to see all the database entries. Feedback entries are also visible by it.

traveler_companion - every time a traveler companion login, he gets a notification on his phone abouu the status of his ride. I planned to automate this with a refresh rate of every 2 mins so that he donot have to do it manually.

traveler - it is the one who booked the cab. the code will automatically find a companion for his ride with certain filters like same end_location. However we could also have the other  parameters to sort this like time of the day. nearest to the traveler, etc based on the location of the traveler_companion.



### messaging
We used Twilio, a library for sending and recieving msgs/whatsapp from user to server and vise-versa
pip install twilio

account_sid = 'ACb7da91fffd8d722efae6bc16656430f1' // provided by twilio
                auth_token = 'f24da2c27436de3ce3284675609cc2d0' //provided by twilio
                twilio_number = '+15417166657' // provided by twilio once you login
                target_number = user.phone_number  // the phone number to recieve msgs
                client = Client(account_sid,auth_token)
                message = client.messages.create(body = str(ride_details),
                                                from_ = twilio_number,
                                                to = target_number)


this is the basic architecture of how to send msgs to a particular mobile number.

logic- once a traveler login into the app the app will automatically search in the database  of the the traveler_companion with the same end_location with other parameters like same time, active users, etc. 
once that user is found the traveler will be notified with the traveler_companion details
and the traveler_companion will be notified with the details of the ride.(which may include a link to the live location,etc)

### real-time tracking
assuming that the data of current_location is coming from a websocket we used the websockets library to create out own server and make a client locally to share the update position of the ride.

consumers.py - using channels we create an ansync function to connect to the websocket and to raise the update function whenever the required payload is recieved.


def on_open(ws):
    def run(*args):
        data = {
            'trip_id':"3",
            'current_location': 'New York'
        }
        ws.send(json.dumps(data))
    run()

if __name__ == "__main__":
    ws_url = "ws://localhost:8000/ws/rides/3/"
    ws = websocket.WebSocketApp(ws_url,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

a sample of websocket_client.py to run the client server to send the location updates via websocket.

### defining some files for better understanding
urls.py - each app has its own urls.py which is finally shared to the urls.py in the ride_sharing module. It stores the various sub domains of a site to perform different actions.

serializer.py - to coomunicate with the database and make changes there we need a serializers in order to convert model instances into renderable json format.

models.py - shows how the database table for that app will look like. with the definition of the attibutes and their datatypes.

views.py - contains the logic. every action to be performed has to be written here. 

asgi.py - it contains the definition of the async-capable python frameworks and web servers.
in our case websockets.
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(  #authmiddlewarestack provides with read-only access to the user
        URLRouter(
            websocket_urlpatterns
        )
    ),
})


### Ideas

PRICING:
    since we plan on assigning the companion nearest to the traveler, ensures that the amount splits almost equally. 
    but since the driver has to have 2 passengers we can slightly increase the combined money payable to the driver in order to increase the company's profit.( maybe by 10%).
    then we can distribute the price rationally among the passengers based on the distance they covered.
    this ensures company's profit increase as well as passengers lower payable price.

SERVER USAGE:
    since the traveler are only concerned about companions near to him. It's better to locate more distributed servers with lesser storage that having large size piers.
    also if we can have the users device to act as a pier till the ride is complete will have cost effectiveness.


Caching: 
    we can have a functionality of storing the nearby companions until a companions gets into the cab.
    this will help if a companion plans to cancel his ride, another seach in the database would not be required.

Database:
    if a particular driver only uses the same route for lifting passangers, we do not need to delete the ride entries once completed. we can make it inactive untill the driver returns back on the same route.







### requirements
pip install channels channels_redis 
pip install psycopg2-binary
pip install djangorestframework-simplejwt
pip install twilio
pip install djangorestframework django-cors-headers












