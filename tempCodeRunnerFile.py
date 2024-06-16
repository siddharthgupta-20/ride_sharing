
# import websocket
# import json
# import threading
# import time

# # Define WebSocket URL
# websocket_url = "ws://localhost:8000/ws/rides/trip123"  # Replace with your WebSocket URL

# def on_message(ws, message):
#     print(f"Received message: {message}")

# def on_error(ws, error):
#     print(f"Error: {error}")

# def on_close(ws):
#     print("### WebSocket closed ###")

# def on_open(ws):
#     def run(*args):
#         # Send a sample message to the WebSocket server
#         data = {
#             "trip_id":'3',
#             'current_location': 'agartala'
#         }
#         ws.send(json.dumps(data))

#     threading.Thread(target=run).start()

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp(websocket_url,
#                                 on_open=on_open,
#                                 on_message=on_message,
#                                 on_error=on_error,
#                                 on_close=on_close)
#     # ws.on_open = on_open
#   