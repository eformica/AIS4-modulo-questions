import pika
import json

from typing import Callable

import pika.credentials

from utils.singletom import Singleton
    
class MessageService(Singleton):
    def __init__(self, host, username="guest", password="guest") -> None:

        if not Singleton._init:

            if host is not None:
                credentials = pika.PlainCredentials(username, password)
                parameters = pika.ConnectionParameters(host=host, port=5672, credentials=credentials) #, credentials=credentials) 
                
                self.connection = pika.BlockingConnection(parameters)

                self.channel = None
            
            print(f"RabbitMQ Host: {host}")

            Singleton._init = True
                
    def set_channel(self, exchange_name: str, exchange_type="topic", durable=True):
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable)
        self.exchange = exchange_name
    
    def _check_set_channel(self):
        if self.channel == None:
            raise Exception("You need to call 'set_channel' first")

    def close(self):
        self.connection.close()


#class Publisher(_BaseMessageService):
    def send(self, routing_key: str, content: str|dict, headers: dict = None, exchange = None, mandatory=True):

        self._check_set_channel()

        prop = pika.BasicProperties(headers=headers)

        if exchange is None:
            exchange = self.exchange

        if type(content) == dict:
            content = json.dumps(content)

        self.channel.basic_publish(
        exchange=exchange, routing_key=routing_key, body=content, properties=prop, mandatory=mandatory)


#class Consumer(_BaseMessageService):

    def set_consumer(self
                    , binding_keys: str|list = "#"
                    , queue_name=""
                    , exclusive=False
                    , durable=False
                    , auto_delete=False
                    , ):
        
        self._check_set_channel()

        result = self.channel.queue_declare(queue_name, exclusive=exclusive, durable=durable, auto_delete=auto_delete)
        
        if queue_name == "":
            self.queue_name = result.method.queue
        else:
            self.queue_name = queue_name

        if type(binding_keys) == str:
            binding_keys = [binding_keys]

        for binding_key in binding_keys:
            self.channel.queue_bind(
        exchange=self.exchange, queue=queue_name, routing_key=binding_key)
    
    def start_listener(self, callback: Callable):
        """ callback(ch, method, properties, body) """
        
        self._check_set_channel()

        self.channel.basic_consume(
            queue=self.queue_name
            , on_message_callback=callback
            , auto_ack=True)

        self.channel.start_consuming()
            
    # @staticmethod
    # def _basic_callback():

    # # def start_consuming(self):
    # #     self.channel.basic_consume(
    # #     queue=queue_name, on_message_callback=callback, auto_ack=True)

    # #     channel.start_consuming()