from flask import Flask, render_template, jsonify, request
from rabbitmq_model import RabbitMQModel

app = Flask(__name__)

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


@app.route("/fetch_message", methods=["GET"])
def fetch_message():
    message = rabbitmq_model.receive_messages()
    if message:
        return jsonify({"message": message})
    else:
        return jsonify({"message": "Aucun message disponible"})


@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.json
    message = data.get("message")
    if message:
        rabbitmq_model.send_message(message)
        return jsonify({"status": "success", "message": "Message envoyé avec succès"})
    else:
        return (
            jsonify({"status": "error", "message": 'Le champ "message" est requis'}),
            400,
        )


if __name__ == "__main__":
    app.run(debug=True)
