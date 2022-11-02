from flask import Flask, render_template
from flask_socketio import SocketIO
import redis

app = Flask(__name__)
app.config['SECRET_KEY'] = 'froggy'
app.debug = True
socketio = SocketIO(app, message_queue='redis://')

r = redis.Redis("localhost")
r.set('button', 'not pressed')

@app.route("/")
def index():
  return render_template("index.html")

@socketio.on('button event')
def handleMessage():
    r.set('button', 'pressed')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')