import socketio

# Create a Socket.IO server instance
sio = socketio.Server(cors_allowed_origins="*")
app = socketio.WSGIApp(sio)

# Define a connection event handler
@sio.event
def connect(sid, environ):
    print(f"Client connected: {sid}")
    sio.emit('message', {'msg': 'Welcome!'}, to=sid)

# Define a disconnection event handler
@sio.event
def disconnect(sid):
    print(f"Client disconnected: {sid}")

# Define a custom event handler
@sio.event
def my_custom_event(sid, data):
    print(f"Received data from {sid}: {data}")
    sio.emit('response', {'msg': 'Data received!'}, to=sid)

if __name__ == "__main__":
    import eventlet
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
