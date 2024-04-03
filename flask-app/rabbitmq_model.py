import pika

class RabbitMQModel:
    def __init__(self, host, port, user, password, queue_name):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.queue_name = queue_name

    def send_message(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, credentials=pika.PlainCredentials(self.user, self.password)))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        channel.basic_publish(exchange='', routing_key=self.queue_name, body=message)
        connection.close()

    def receive_messages(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port, credentials=pika.PlainCredentials(self.user, self.password)))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_name)
        method_frame, header_frame, body = channel.basic_get(self.queue_name, auto_ack=True)
        if method_frame:
            return body.decode('utf-8')
        else:
            return None