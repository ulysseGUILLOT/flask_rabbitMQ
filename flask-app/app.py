from flask import Flask, render_template
from flask_socketio import SocketIO
from rabbitmq_model import RabbitMQModel
from threading import Thread
import eventlet

import logging

logging.basicConfig(level=logging.INFO)

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

RABBITMQ_HOST = "rabbitmq"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "user"
RABBITMQ_PASS = "password"
QUEUE_NAME = "messages"

rabbitmq_model = RabbitMQModel(
    RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASS, QUEUE_NAME
)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def handle_connect():
    print("Client connected")


@socketio.on("disconnect")
def handle_disconnect():
    print("Client disconnected")


@socketio.on("send_message")
def handle_send_message(json):
    message = json.get("message")
    if message:
        rabbitmq_model.send_message(message)
        socketio.emit(
            "message_response",
            {"status": "success", "message": "Message sent successfully"},
        )


def listen_for_rabbitmq_messages():
    while True:
        message = eventlet.tpool.execute(rabbitmq_model.receive_messages)
        if message:
            socketio.emit("new_message", {"message": message})
        eventlet.sleep(1)


if __name__ == "__main__":
    eventlet.spawn(listen_for_rabbitmq_messages)
    socketio.run(app, debug=True, async_mode="eventlet")
