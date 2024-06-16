
import websocket
import json

def on_message(ws, message):
    print(f"Received: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

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

