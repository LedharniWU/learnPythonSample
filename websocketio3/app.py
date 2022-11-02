from threading import Lock
from unittest import result
from flask import Flask, render_template, session
from flask_socketio import SocketIO, emit
import requests
import serial

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)
# ser = serial.Serial("COM3", 921600)
# print(ser.name)

thread = None
thread_lock = Lock()

url = 'https://api.coinbase.com/v2/prices/btc-usd/spot'

def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(3)
        socketio.emit('my_response',
                      {'data': '123124'})

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected'})

if __name__ == '__main__':
    socketio.run(app)