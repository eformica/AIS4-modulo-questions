from config import Settings

import pika
import json

class _BaseMensageService:
    def __init__(self, host=Settings.RABBITMQ_HOST) -> None:
        self.connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host))
        self.channel = None
        
    def set_channel(self, exchange_name: str, exchange_type="topic", durable=True):
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)
        self.exchange = exchange_name
    
    def _check_set_channel(self):
        if self.channel == None:
            raise Exception("You need to call 'set_channel' first")

    def set_consumer(self
                     , binding_keys: str|list = "#"
                     , queue_name=""
                     , exclusive=False
                     , durable=False
                     , auto_delete=True
                     , ):
        
        self._check_set_channel()

        result = self.channel.queue_declare(queue_name, exclusive=exclusive, durable=durable, auto_delete=auto_delete)
        
        if queue_name == "":
            queue_name = result.method.queue

        if type(binding_keys) == str:
            binding_keys = [binding_keys]

        for binding_key in binding_keys:
            self.channel.queue_bind(
        exchange=self.exchange, queue=queue_name, routing_key=binding_key)

    def close(self):
        self.connection.close()

class Producer(_BaseMensageService):
    def send(self, routing_key: str, message: str|dict, headers: dict = None, exchange = None, mandatory=True):

        self._check_set_channel()

        prop = pika.BasicProperties(headers=headers)

        if exchange is None:
            exchange = self.exchange

        if type(message) == dict:
            message = json.dumps(message)

        self.channel.basic_publish(
        exchange=exchange, routing_key=routing_key, body=message, properties=prop, mandatory=mandatory)

class Consumer(_BaseMensageService):

    def set_consumer(self
                    , binding_keys: str|list = "#"
                    , queue_name=""
                    , exclusive=False
                    , durable=False
                    , auto_delete=True
                    , ):
        
        self._check_set_channel()

        result = self.channel.queue_declare(queue_name, exclusive=exclusive, durable=durable, auto_delete=auto_delete)
        
        if queue_name == "":
            queue_name = result.method.queue

        if type(binding_keys) == str:
            binding_keys = [binding_keys]

        for binding_key in binding_keys:
            self.channel.queue_bind(
        exchange=self.exchange, queue=queue_name, routing_key=binding_key)
            
    # @staticmethod
    # def _basic_callback():

    # # def start_consuming(self):
    # #     self.channel.basic_consume(
    # #     queue=queue_name, on_message_callback=callback, auto_ack=True)

    # #     channel.start_consuming()