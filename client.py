from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pickle
import socket
import signal

from network import Network

app = Flask(__name__)
sio = SocketIO(app, logger=False, cors_allowed_origins="*")

net = Network()
guessed = net.recv()

@app.route('/')
def index():
    return render_template('index.html')

@sio.on('connect')
def connect():
    print('connected client.py')
    emit('connected')

@sio.on('disconnect')
def disconnect():
    print('disconnected client.py')
    emit('disconnected')

@sio.on('letter clicked')
def letter_clicked(data):
    global guessed
    letter = data['src']
    print(f'{letter} clicked client.py')

    net.send(data=letter)
    guessed = net.recv()
    emit('update buttons', guessed)

def handle_ctr_c(sig, frame):
    net.send(data=net.disconnect_msg)
    print('pressed ctrl c')
    exit()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_ctr_c)

    sio.run(app, socket.gethostname(), 5050)