import pika
import logging


class RabbitMQModel:
    def __init__(self, host, port, user, password, queue_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name

    def send_message(self, message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(self.user, self.password),
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(exchange="", routing_key=self.queue_name, body=message)
        connection.close()

    def receive_messages(self):
        logging.info("Attempting to receive messages...")
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(self.user, self.password),
            )
        )
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        method_frame, header_frame, body = channel.basic_get(
            queue=self.queue_name, auto_ack=True
        )
        connection.close()
        if method_frame:
            message = body.decode("utf-8")
            logging.info(f"Received message: {message}")
            return message
        else:
            logging.info("No message received.")
            return None
