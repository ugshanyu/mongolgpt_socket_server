from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit, join_room

# Initialize Flask app and SocketIO
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")  # Allow cross-origin requests

# Simple route for /hello
@app.route('/hello')
def hello_world():
    return "world"

# Event handler for client connection with room joining
@socketio.on('connect')
def handle_connect():
    print('Client connected')

# Event handler for joining a room when a page connects
@socketio.on('join_page')
def handle_join_page(data):
    page_id = data.get('page_id')
    if page_id:
        join_room(page_id)
        print(f'Client joined room for page_id: {page_id}')
        emit('server_response', {'message': f'Joined room for page_id: {page_id}', "success": True}, room=page_id)

# Event handler for client disconnection
@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Custom event handler for receiving data from clients and sending it to a room
@socketio.on('classified_event')
def handle_classified_event(data):
    print('Received classified_event:', data)
    page_id = data.get('page_id')  # Ensure `page_id` is in the event data
    if page_id:
        # Emit the event data to the room corresponding to the `page_id`
        emit('server_response', {'message': 'Received your event!', 'data': data}, room=page_id)

# Run the server
if __name__ == '__main__':
    # Use socketio.run instead of app.run to start the Socket.IO server
    socketio.run(app, host='0.0.0.0', port=3003, debug=True)
