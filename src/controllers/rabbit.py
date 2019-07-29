import pika
from pyrabbit.api import Client
from controllers.log import Logger
from controllers.config import Config
from controllers.background import threaded

class Messages(object):
    def __init__(self):
        self.config = Config()
        credentials = pika.PlainCredentials(self.config["rabbitmq"]["user"],self.config["rabbitmq"]["password"])
        self.parameters = pika.ConnectionParameters(self.config["rabbitmq"]["server"],5672,'portscan',credentials)

    def _callback(self, ch, method, properties, body):
        result = body.decode("utf-8")
        Logger(result)
        ch.basic_ack(delivery_tag = method.delivery_tag)

    def send(self,topic,msg):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=topic)
        channel.basic_publish(exchange="",routing_key=topic,body=msg)
        connection.close()

    def queues(self,):
        cl = Client('%:15672' % self.config["rabbitmq"]["server"],self.config["rabbitmq"]["user"], self.config["rabbitmq"]["password"])
        queues = [q['name'] for q in cl.get_queues()]
        return queues

    @threaded
    def read(self,topic):
        connection = pika.BlockingConnection(self.parameters)
        channel = connection.channel()
        channel.queue_declare(queue=topic)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(topic,self._callback,auto_ack=False)
        channel.start_consuming()
