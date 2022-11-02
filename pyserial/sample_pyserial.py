from threading import Lock
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import serial

async_mode = None

app = Flask(__name__)
socketio = SocketIO(app, async_mode=async_mode)

# シリアル通信
# ser = serial.Serial("COM3",921600)
# print(ser.name)

thread = None
thread_lock = Lock()

def background_thread():
    while True:
        socketio.sleep(0.1)
        # シリアル通信
        # results = ser.readline()
        # バイト型 -> 文字列
        # results_disp = results.strip().decode('UTF-8')

        # jsonに変換
        # try:
        #     json_data = json.loads(results_disp)
        # except json.JSONDecodeError:
        #     continue
    
        # socketio.emit('my_response', {'data': results})
        # socketio.emit('my_response', {'data': results_disp})
        # socketio.emit('my_response', {'data': json_data})
        socketio.emit('my_response', {'data':'123124'})

        # シリアル通信閉じる
        # ser.close()

@app.route("/")
def index():
    return render_template("index.html", async_mode=socketio.async_mode)

@socketio.event
def connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)
    emit('my_response', {'data': 'Connected'})

if __name__=='__main__':
    socketio.run(app)

